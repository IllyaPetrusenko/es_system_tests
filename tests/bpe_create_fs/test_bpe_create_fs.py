import copy
import json
import time
from uuid import uuid4
import requests
from pytest_testrail.plugin import pytestrail

from tests.Cassandra_session import Cassandra
from tests.essences.fs import FS

from tests.iMDM_service.get_information import MdmService
from tests.payloads.fs_payload import create_fs_payload_fs_full_data_model_treasury_money, \
    create_fs_payload_fs_full_data_model_own_money, create_fs_payload_fs_obligatory_data_model_own_money, \
    create_fs_payload_fs_obligatory_data_model_treasury_money
from useful_functions import compare_actual_result_and_expected_result, prepared_cp_id, get_human_date_in_utc_format, \
    is_it_uuid


class TestCheckOnPossibilityOfCreatingFsWithFullDataModelTreasuryMoney(object):
    @pytestrail.case("27545")
    def test_send_the_request_27545_1(self, country, language, instance, cassandra_username,
                                      cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )

    @pytestrail.case("27545")
    def test_see_the_result_in_feed_point_point_27545_2(self, country, language, instance, cassandra_username,
                                                        cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(fs.check_on_that_message_is_successfully_create_fs())
        )

    @pytestrail.case('27545')
    def test_check_on_correctness_of_publishing_fs_release_on_public_point_27545_3(self, country, language, instance,
                                                                                   cassandra_username,
                                                                                   cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        ei = fs.insert_ei_full_data_model(cp_id, ei_token)
        if "buyer" in payload.keys():
            buyer_in_payload = True
            source_entity_id = payload["buyer"]["identifier"]["scheme"] + "-" + payload["buyer"]["identifier"]["id"]
            source_entity_name = payload["buyer"]["name"]
            status = "active"
        else:
            buyer_in_payload = False
            status = "planning"
            ei_release = requests.get(
                url=ei[0] + "/" + ei[2]
            ).json()
            source_entity_id = ei_release["releases"][0]["buyer"]["id"]
            source_entity_name = ei_release["releases"][0]["buyer"]["name"]
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        mdm = MdmService(
            instance="dev",
            lang="ro",
            country=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]["id"],
            region=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"],
            locality=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["id"]
        )
        data = mdm.process_fs_data(cp_id).json()
        country_from_mdm = data["data"]["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]
        region_from_mdm = data["data"]["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]
        locality_from_mdm = data["data"]["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]
        url_create = message_from_kafka['data']['url'] + '/' + message_from_kafka['data']['outcomes']['fs'][0]['id']
        fs_release = requests.get(url=url_create).json()
        fs_release_timestamp = int(fs_release["releases"][0]["id"][46:59])
        convert_timestamp_to_date = get_human_date_in_utc_format(fs_release_timestamp)
        roles_list = list()
        for key, values in fs_release["releases"][0]["parties"][0].items():
            if key == "roles":
                role = fs_release["releases"][0]["parties"][0].get(key)
                roles_list.append(role[0])
        keys_list = list()
        for i in fs_release.keys():
            if i == "uri":
                keys_list.append(i)
            if i == "version":
                keys_list.append(i)
            if i == "extensions":
                keys_list.append(i)
            if i == "publisher":
                keys_list.append(i)
            if i == "license":
                keys_list.append(i)
            if i == "publicationPolicy":
                keys_list.append(i)
            if i == "publishedDate":
                keys_list.append(i)
            if i == "releases":
                keys_list.append(i)
        for i in fs_release["publisher"].keys():
            if i == "name":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_release["releases"][0].keys():
            if i == "ocid":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "date":
                keys_list.append(i)
            if i == "tag":
                keys_list.append(i)
            if i == "initiationType":
                keys_list.append(i)
            if i == "tender":
                keys_list.append(i)
            if i == "parties":
                keys_list.append(i)
            if i == "planning":
                keys_list.append(i)
            if i == "relatedProcesses":
                keys_list.append(i)
        for i in fs_release["releases"][0]["tender"].keys():
            if i == "id":
                keys_list.append(i)
            if i == "status":
                keys_list.append(i)
            if i == "statusDetails":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][0].keys():
            if i == "id":
                keys_list.append(i)
            if i == "name":
                keys_list.append(i)
            if i == "identifier":
                keys_list.append(i)
            if i == "address":
                keys_list.append(i)
            if i == "additionalIdentifiers":
                keys_list.append(i)
            if i == "contactPoint":
                keys_list.append(i)
            if i == "roles":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][0]["identifier"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "legalName":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][0]["address"].keys():
            if i == "streetAddress":
                keys_list.append(i)
            if i == "postalCode":
                keys_list.append(i)
            if i == "addressDetails":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][0]["address"]["addressDetails"].keys():
            if i == "country":
                keys_list.append(i)
            if i == "region":
                keys_list.append(i)
            if i == "locality":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][0]["additionalIdentifiers"][0].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "legalName":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][0]["contactPoint"].keys():
            if i == "name":
                keys_list.append(i)
            if i == "email":
                keys_list.append(i)
            if i == "telephone":
                keys_list.append(i)
            if i == "faxNumber":
                keys_list.append(i)
            if i == "url":
                keys_list.append(i)
        for i in fs_release["releases"][0]["planning"].keys():
            if i == "budget":
                keys_list.append(i)
            if i == "rationale":
                keys_list.append(i)
        for i in fs_release["releases"][0]["planning"]["budget"].keys():
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
            if i == "period":
                keys_list.append(i)
            if i == "amount":
                keys_list.append(i)
            if i == "europeanUnionFunding":
                keys_list.append(i)
            if i == "isEuropeanUnionFunded":
                keys_list.append(i)
            if i == "verified":
                keys_list.append(i)
            if i == "sourceEntity":
                keys_list.append(i)
            if i == "project":
                keys_list.append(i)
            if i == "projectID":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_release["releases"][0]["planning"]["budget"]["period"].keys():
            if i == "startDate":
                keys_list.append(i)
            if i == "endDate":
                keys_list.append(i)
        for i in fs_release["releases"][0]["planning"]["budget"]["amount"].keys():
            if i == "amount":
                keys_list.append(i)
            if i == "currency":
                keys_list.append(i)
        for i in fs_release["releases"][0]["planning"]["budget"]["europeanUnionFunding"].keys():
            if i == "projectIdentifier":
                keys_list.append(i)
            if i == "projectName":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_release["releases"][0]["planning"]["budget"]["sourceEntity"].keys():
            if i == "id":
                keys_list.append(i)
            if i == "name":
                keys_list.append(i)
        for i in fs_release["releases"][0]["relatedProcesses"][0].keys():
            if i == "id":
                keys_list.append(i)
            if i == "relationship":
                keys_list.append(i)
            if i == "scheme":
                keys_list.append(i)
            if i == "identifier":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        procuring_entity_scheme = payload["tender"]["procuringEntity"]["identifier"]["scheme"]
        procuring_entity_id = payload["tender"]["procuringEntity"]["identifier"]["id"]
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[0]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="version",
            actual_result=keys_list[1]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="extensions",
            actual_result=keys_list[2]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="publisher",
            actual_result=keys_list[3]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="license",
            actual_result=keys_list[4]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="publicationPolicy",
            actual_result=keys_list[5]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="publishedDate",
            actual_result=keys_list[6]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="releases",
            actual_result=keys_list[7]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="name",
            actual_result=keys_list[8]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[9]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="ocid",
            actual_result=keys_list[10]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[11]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="date",
            actual_result=keys_list[12]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="tag",
            actual_result=keys_list[13]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="initiationType",
            actual_result=keys_list[14]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="tender",
            actual_result=keys_list[15]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="parties",
            actual_result=keys_list[16]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="planning",
            actual_result=keys_list[17])
        assert compare_actual_result_and_expected_result(
            expected_result="relatedProcesses",
            actual_result=keys_list[18]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[19]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="status",
            actual_result=keys_list[20]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="statusDetails",
            actual_result=keys_list[21]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[22]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="name",
            actual_result=keys_list[23]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="identifier",
            actual_result=keys_list[24]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="address",
            actual_result=keys_list[25]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="additionalIdentifiers",
            actual_result=keys_list[26]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="contactPoint",
            actual_result=keys_list[27]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="roles",
            actual_result=keys_list[28]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="scheme",
            actual_result=keys_list[29]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[30]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="legalName",
            actual_result=keys_list[31]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[32]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="streetAddress",
            actual_result=keys_list[33]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="postalCode",
            actual_result=keys_list[34]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="addressDetails",
            actual_result=keys_list[35]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="country",
            actual_result=keys_list[36]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="region",
            actual_result=keys_list[37]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="locality",
            actual_result=keys_list[38]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="scheme",
            actual_result=keys_list[39]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[40]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="description",
            actual_result=keys_list[41]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[42]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="scheme",
            actual_result=keys_list[43]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[44]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="description",
            actual_result=keys_list[45]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[46]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="scheme",
            actual_result=keys_list[47]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[48]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="description",
            actual_result=keys_list[49]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[50]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="scheme",
            actual_result=keys_list[51]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[52]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="legalName",
            actual_result=keys_list[53]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[54]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="name",
            actual_result=keys_list[55]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="email",
            actual_result=keys_list[56]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="telephone",
            actual_result=keys_list[57]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="faxNumber",
            actual_result=keys_list[58]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="url",
            actual_result=keys_list[59]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="budget",
            actual_result=keys_list[60]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="rationale",
            actual_result=keys_list[61]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[62]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="description",
            actual_result=keys_list[63]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="period",
            actual_result=keys_list[64]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="amount",
            actual_result=keys_list[65]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="europeanUnionFunding",
            actual_result=keys_list[66]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="isEuropeanUnionFunded",
            actual_result=keys_list[67]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="verified",
            actual_result=keys_list[68]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="sourceEntity",
            actual_result=keys_list[69]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="project",
            actual_result=keys_list[70]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="projectID",
            actual_result=keys_list[71]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[72]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="startDate",
            actual_result=keys_list[73]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="endDate",
            actual_result=keys_list[74]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="amount",
            actual_result=keys_list[75]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="currency",
            actual_result=keys_list[76]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="projectIdentifier",
            actual_result=keys_list[77]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="projectName",
            actual_result=keys_list[78]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[79]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[80]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="name",
            actual_result=keys_list[81]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[82]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="relationship",
            actual_result=keys_list[83]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="scheme",
            actual_result=keys_list[84]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="identifier",
            actual_result=keys_list[85]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[86]
        )

        assert compare_actual_result_and_expected_result(
            expected_result=f"http://dev.public.eprocurement.systems/budgets/{message_from_kafka['data']['ocid']}/"
                            f"{message_from_kafka['data']['outcomes']['fs'][0]['id']}",
            actual_result=fs_release["uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="666",
            actual_result=fs_release["version"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="https://raw.githubusercontent.com/open-contracting/ocds_bid_extension/v1.1.1/"
                            "extension.json",
            actual_result=fs_release["extensions"][0]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="https://raw.githubusercontent.com/open-contracting/ocds_enquiry_extension/v1.1.1/"
                            "extension.js222",
            actual_result=fs_release["extensions"][1]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=instance.upper() + "-ENV",
            actual_result=fs_release["publisher"]["name"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="https://www.ustudio.com",
            actual_result=fs_release["publisher"]["uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="http://opendefinition.org/licenses/222",
            actual_result=fs_release["license"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="http://opendefinition.org/licenses/222",
            actual_result=fs_release["publicationPolicy"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=message_from_kafka["data"]["operationDate"],
            actual_result=fs_release["publishedDate"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=message_from_kafka['data']['outcomes']['fs'][0]['id'],
            actual_result=fs_release["releases"][0]["ocid"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=message_from_kafka['data']['outcomes']['fs'][0]['id'],
            actual_result=fs_release["releases"][0]["id"][0:45]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=message_from_kafka["data"]["operationDate"],
            actual_result=convert_timestamp_to_date[0]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=message_from_kafka["data"]["operationDate"],
            actual_result=fs_release["releases"][0]["date"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="planning",
            actual_result=fs_release["releases"][0]["tag"][0]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="tender",
            actual_result=fs_release["releases"][0]["initiationType"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(is_it_uuid(fs_release["releases"][0]["tender"]["id"], 4))
        )
        assert compare_actual_result_and_expected_result(
            expected_result=status,
            actual_result=fs_release["releases"][0]["tender"]["status"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="empty",
            actual_result=fs_release["releases"][0]["tender"]["statusDetails"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=procuring_entity_scheme + "-" + procuring_entity_id,
            actual_result=fs_release["releases"][0]["parties"][0]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["name"],
            actual_result=fs_release["releases"][0]["parties"][0]["name"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["identifier"]["scheme"],
            actual_result=fs_release["releases"][0]["parties"][0]["identifier"]["scheme"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["identifier"]["id"],
            actual_result=fs_release["releases"][0]["parties"][0]["identifier"]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["identifier"]["legalName"],
            actual_result=fs_release["releases"][0]["parties"][0]["identifier"]["legalName"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["identifier"]["uri"],
            actual_result=fs_release["releases"][0]["parties"][0]["identifier"]["uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["address"]["streetAddress"],
            actual_result=fs_release["releases"][0]["parties"][0]["address"]["streetAddress"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["address"]["postalCode"],
            actual_result=fs_release["releases"][0]["parties"][0]["address"]["postalCode"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=country_from_mdm["scheme"],
            actual_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["scheme"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]["id"],
            actual_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=country_from_mdm["description"],
            actual_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["description"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=country_from_mdm["uri"],
            actual_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=region_from_mdm["scheme"],
            actual_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["scheme"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"],
            actual_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=region_from_mdm["description"],
            actual_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["description"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=region_from_mdm["uri"],
            actual_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=locality_from_mdm["scheme"],
            actual_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["scheme"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["id"],
            actual_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=locality_from_mdm["description"],
            actual_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
                "description"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=locality_from_mdm["uri"],
            actual_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
                "uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["scheme"],
            actual_result=fs_release["releases"][0]["parties"][0]["additionalIdentifiers"][0]["scheme"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["id"],
            actual_result=fs_release["releases"][0]["parties"][0]["additionalIdentifiers"][0]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["legalName"],
            actual_result=fs_release["releases"][0]["parties"][0]["additionalIdentifiers"][0]["legalName"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["uri"],
            actual_result=fs_release["releases"][0]["parties"][0]["additionalIdentifiers"][0]["uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["contactPoint"]["name"],
            actual_result=fs_release["releases"][0]["parties"][0]["contactPoint"]["name"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["contactPoint"]["email"],
            actual_result=fs_release["releases"][0]["parties"][0]["contactPoint"]["email"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["contactPoint"]["telephone"],
            actual_result=fs_release["releases"][0]["parties"][0]["contactPoint"]["telephone"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["contactPoint"]["faxNumber"],
            actual_result=fs_release["releases"][0]["parties"][0]["contactPoint"]["faxNumber"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["contactPoint"]["url"],
            actual_result=fs_release["releases"][0]["parties"][0]["contactPoint"]["url"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="payer",
            actual_result=roles_list[0]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["id"],
            actual_result=fs_release["releases"][0]["planning"]["budget"]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["description"],
            actual_result=fs_release["releases"][0]["planning"]["budget"]["description"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["period"]["startDate"],
            actual_result=fs_release["releases"][0]["planning"]["budget"]["period"]["startDate"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["period"]["endDate"],
            actual_result=fs_release["releases"][0]["planning"]["budget"]["period"]["endDate"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(payload["planning"]["budget"]["amount"]["amount"]),
            actual_result=str(fs_release["releases"][0]["planning"]["budget"]["amount"]["amount"])
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["amount"]["currency"],
            actual_result=fs_release["releases"][0]["planning"]["budget"]["amount"]["currency"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["europeanUnionFunding"]["projectIdentifier"],
            actual_result=fs_release["releases"][0]["planning"]["budget"]["europeanUnionFunding"]["projectIdentifier"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["europeanUnionFunding"]["projectName"],
            actual_result=fs_release["releases"][0]["planning"]["budget"]["europeanUnionFunding"]["projectName"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["europeanUnionFunding"]["uri"],
            actual_result=fs_release["releases"][0]["planning"]["budget"]["europeanUnionFunding"]["uri"]
        )

        assert compare_actual_result_and_expected_result(
            expected_result=str(payload["planning"]["budget"]["isEuropeanUnionFunded"]),
            actual_result=str(fs_release["releases"][0]["planning"]["budget"]["isEuropeanUnionFunded"])
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(buyer_in_payload),
            actual_result=str(fs_release["releases"][0]["planning"]["budget"]["verified"])
        )
        assert compare_actual_result_and_expected_result(
            expected_result=source_entity_id,
            actual_result=fs_release["releases"][0]["planning"]["budget"]["sourceEntity"]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=source_entity_name,
            actual_result=fs_release["releases"][0]["planning"]["budget"]["sourceEntity"]["name"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["project"],
            actual_result=fs_release["releases"][0]["planning"]["budget"]["project"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["projectID"],
            actual_result=fs_release["releases"][0]["planning"]["budget"]["projectID"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["uri"],
            actual_result=fs_release["releases"][0]["planning"]["budget"]["uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["rationale"],
            actual_result=fs_release["releases"][0]["planning"]["rationale"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(is_it_uuid(fs_release["releases"][0]["relatedProcesses"][0]["id"], 1))
        )
        assert compare_actual_result_and_expected_result(
            expected_result="parent",
            actual_result=fs_release["releases"][0]["relatedProcesses"][0]["relationship"][0]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="ocid",
            actual_result=fs_release["releases"][0]["relatedProcesses"][0]["scheme"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=cp_id,
            actual_result=fs_release["releases"][0]["relatedProcesses"][0]["identifier"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{cp_id}",
            actual_result=fs_release["releases"][0]["relatedProcesses"][0]["uri"]
        )


class TestCheckOnImpossibilityOfCreatingFsFullDataModelTreasuryMoneyOfPayloadIfObligatoryAttributesAreMissed(object):
    @pytestrail.case('27547')
    def test_delete_tender_27547_1(self, country, language, instance,
                                   cassandra_username,
                                   cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["tender"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.00.00.00", "description": "Data processing exception."}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27547')
    def test_delete_tender_procuring_entity_point_27547_2(self, country, language, instance,
                                                          cassandra_username,
                                                          cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["tender"]["procuringEntity"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com."
                                                 "procurement.budget.model.dto.fs.request.TenderFsCreate] "
                                                 "value failed for JSON property procuringEntity due to "
                                                 "missing (therefore NULL) value for creator parameter "
                                                 "procuringEntity which is a non-nullable type\n at "
                                                 "[Source: UNKNOWN; line: -1, column: -1] (through "
                                                 "reference chain: com.procurement.budget.model.dto."
                                                 "fs.request.FsCreate[\"tender\"]->com.procurement.budget."
                                                 "model.dto.fs.request.TenderFsCreate[\"procuringEntity\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27547')
    def test_delete_tender_procuring_entity_name_27547_3(self, country, language, instance,
                                                         cassandra_username,
                                                         cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["tender"]["procuringEntity"]["name"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com."
                                                 "procurement.budget.model.dto.fs.OrganizationReferenceFs] "
                                                 "value failed for JSON property name due to missing (therefore "
                                                 "NULL) value for creator parameter name which is a non-"
                                                 "nullable type\n at [Source: UNKNOWN; line: -1, column: -1] "
                                                 "(through reference chain: com.procurement.budget.model.dto."
                                                 "fs.request.FsCreate[\"tender\"]->com.procurement.budget."
                                                 "model.dto.fs.request.TenderFsCreate[\"procuringEntity\"]->"
                                                 "com.procurement.budget.model.dto.fs.OrganizationReference"
                                                 "Fs[\"name\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27547')
    def test_delete_tender_procuring_entity_identifier_27547_4(self, country, language, instance,
                                                               cassandra_username,
                                                               cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["tender"]["procuringEntity"]["identifier"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00", "description": "com.fasterxml.jackson.module.kotlin.Missing"
                                                                      "KotlinParameterException: Instantiation of "
                                                                      "[simple type, class com.procurement.budget."
                                                                      "model.dto.fs.OrganizationReferenceFs] value "
                                                                      "failed for JSON property identifier due to "
                                                                      "missing (therefore NULL) value for creator "
                                                                      "parameter identifier which is a non-nullable "
                                                                      "type\n at [Source: UNKNOWN; line: -1, "
                                                                      "column: -1] (through reference chain: com."
                                                                      "procurement.budget.model.dto.fs.request."
                                                                      "FsCreate[\"tender\"]->com.procurement."
                                                                      "budget.model.dto.fs.request.TenderFsCreate"
                                                                      "[\"procuringEntity\"]->com.procurement."
                                                                      "budget.model.dto.fs.OrganizationReference"
                                                                      "Fs[\"identifier\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27547')
    def test_delete_tender_procuring_entity_identifier_scheme_27547_5(self, country, language, instance,
                                                                      cassandra_username,
                                                                      cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["tender"]["procuringEntity"]["identifier"]["scheme"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00", "description": "com.fasterxml.jackson.module.kotlin."
                                                                      "MissingKotlinParameterException: "
                                                                      "Instantiation of [simple type, class "
                                                                      "com.procurement.mdm.model.dto.data."
                                                                      "Identifier] value failed for JSON property "
                                                                      "scheme due to missing (therefore NULL) "
                                                                      "value for creator parameter scheme which "
                                                                      "is a non-nullable type\n at [Source: UNKNOWN; "
                                                                      "line: -1, column: -1] (through reference "
                                                                      "chain: com.procurement.mdm.model.dto.data."
                                                                      "FS[\"tender\"]->com.procurement.mdm.model."
                                                                      "dto.data.TenderFS[\"procuringEntity\"]->"
                                                                      "com.procurement.mdm.model.dto.data."
                                                                      "OrganizationReference[\"identifier\"]->"
                                                                      "com.procurement.mdm.model.dto.data."
                                                                      "Identifier[\"scheme\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27547')
    def test_delete_tender_procuring_entity_identifier_id_27547_6(self, country, language, instance,
                                                                  cassandra_username,
                                                                  cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["tender"]["procuringEntity"]["identifier"]["id"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00", "description": "com.fasterxml.jackson.module.kotlin.Missing"
                                                                      "KotlinParameterException: Instantiation of "
                                                                      "[simple type, class com.procurement.mdm.model."
                                                                      "dto.data.Identifier] value failed for JSON "
                                                                      "property id due to missing (therefore NULL) "
                                                                      "value for creator parameter id which is a "
                                                                      "non-nullable type\n at [Source: UNKNOWN; "
                                                                      "line: -1, column: -1] (through reference "
                                                                      "chain: com.procurement.mdm.model.dto.data."
                                                                      "FS[\"tender\"]->com.procurement.mdm.model."
                                                                      "dto.data.TenderFS[\"procuringEntity\"]->"
                                                                      "com.procurement.mdm.model.dto.data."
                                                                      "OrganizationReference[\"identifier\"]->"
                                                                      "com.procurement.mdm.model.dto.data."
                                                                      "Identifier[\"id\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27547')
    def test_delete_tender_procuring_entity_identifier_legal_name_27547_7(self, country, language, instance,
                                                                          cassandra_username,
                                                                          cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["tender"]["procuringEntity"]["identifier"]["legalName"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00", "description": "com.fasterxml.jackson.module.kotlin.Missing"
                                                                      "KotlinParameterException: Instantiation of "
                                                                      "[simple type, class com.procurement.budget."
                                                                      "model.dto.ocds.Identifier] value failed for "
                                                                      "JSON property legalName due to missing "
                                                                      "(therefore NULL) value for creator parameter "
                                                                      "legalName which is a non-nullable type\n at "
                                                                      "[Source: UNKNOWN; line: -1, column: -1] "
                                                                      "(through reference chain: com.procurement."
                                                                      "budget.model.dto.fs.request.FsCreate"
                                                                      "[\"tender\"]->com.procurement.budget.model."
                                                                      "dto.fs.request.TenderFsCreate[\"procuring"
                                                                      "Entity\"]->com.procurement.budget.model.dto."
                                                                      "fs.OrganizationReferenceFs[\"identifier\"]->"
                                                                      "com.procurement.budget.model.dto.ocds."
                                                                      "Identifier[\"legalName\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27547')
    def test_delete_tender_procuring_entity_additional_identifiers_scheme_27547_8(self, country, language, instance,
                                                                                  cassandra_username,
                                                                                  cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["scheme"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.Identifier] value failed for JSON property "
                                                 "scheme due to missing (therefore NULL) value for creator "
                                                 "parameter scheme which is a non-nullable type\n at [Source: "
                                                 "UNKNOWN; line: -1, column: -1] (through reference chain: "
                                                 "com.procurement.mdm.model.dto.data.FS[\"tender\"]->com."
                                                 "procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]->"
                                                 "com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"additionalIdentifiers\"]->java.util.ArrayList[0]->com."
                                                 "procurement.mdm.model.dto.data.Identifier[\"scheme\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27547')
    def test_delete_tender_procuring_entity_additional_identifiers_id_27547_9(self, country, language, instance,
                                                                              cassandra_username,
                                                                              cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["id"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.Identifier] value failed for JSON property id "
                                                 "due to missing (therefore NULL) value for creator parameter id "
                                                 "which is a non-nullable type\n at [Source: UNKNOWN; line: -1, "
                                                 "column: -1] (through reference chain: com.procurement.mdm.model."
                                                 "dto.data.FS[\"tender\"]->com.procurement.mdm.model.dto.data."
                                                 "TenderFS[\"procuringEntity\"]->com.procurement.mdm.model.dto."
                                                 "data.OrganizationReference[\"additionalIdentifiers\"]->java.util."
                                                 "ArrayList[0]->com.procurement.mdm.model.dto.data."
                                                 "Identifier[\"id\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27547')
    def test_delete_tender_procuring_entity_additional_identifiers_legal_name_27547_10(self, country, language,
                                                                                       instance,
                                                                                       cassandra_username,
                                                                                       cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["legalName"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "budget.model.dto.ocds.Identifier] value failed for JSON property "
                                                 "legalName due to missing (therefore NULL) value for creator "
                                                 "parameter legalName which is a non-nullable type\n at [Source: "
                                                 "UNKNOWN; line: -1, column: -1] (through reference chain: com."
                                                 "procurement.budget.model.dto.fs.request.FsCreate[\"tender\"]->"
                                                 "com.procurement.budget.model.dto.fs.request.TenderFsCreate"
                                                 "[\"procuringEntity\"]->com.procurement.budget.model.dto.fs."
                                                 "OrganizationReferenceFs[\"additionalIdentifiers\"]->java.util."
                                                 "ArrayList[0]->com.procurement.budget.model.dto.ocds."
                                                 "Identifier[\"legalName\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27547')
    def test_delete_tender_procuring_entity_address_street_address_27547_11(self, country, language,
                                                                            instance,
                                                                            cassandra_username,
                                                                            cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["tender"]["procuringEntity"]["address"]["streetAddress"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.Address] value failed for JSON property "
                                                 "streetAddress due to missing (therefore NULL) value for creator "
                                                 "parameter streetAddress which is a non-nullable type\n at "
                                                 "[Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"tender\"]->"
                                                 "com.procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]->"
                                                 "com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"address\"]->com.procurement.mdm.model.dto.data.Address"
                                                 "[\"streetAddress\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27547')
    def test_delete_tender_procuring_entity_address_address_details_27547_12(self, country, language,
                                                                             instance,
                                                                             cassandra_username,
                                                                             cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["tender"]["procuringEntity"]["address"]["addressDetails"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.Address] value failed for JSON property "
                                                 "addressDetails due to missing (therefore NULL) value for "
                                                 "creator parameter addressDetails which is a non-nullable "
                                                 "type\n at [Source: UNKNOWN; line: -1, column: -1] (through "
                                                 "reference chain: com.procurement.mdm.model.dto.data.FS"
                                                 "[\"tender\"]->com.procurement.mdm.model.dto.data.TenderFS"
                                                 "[\"procuringEntity\"]->com.procurement.mdm.model.dto.data."
                                                 "OrganizationReference[\"address\"]->com.procurement.mdm.model."
                                                 "dto.data.Address[\"addressDetails\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27547')
    def test_delete_tender_procuring_entity_address_address_details_country_27547_13(self, country, language,
                                                                                     instance,
                                                                                     cassandra_username,
                                                                                     cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com."
                                                 "procurement.mdm.model.dto.data.AddressDetails] value failed "
                                                 "for JSON property country due to missing (therefore NULL) value "
                                                 "for creator parameter country which is a non-nullable type\n "
                                                 "at [Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"tender\"]->com."
                                                 "procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]->"
                                                 "com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"address\"]->com.procurement.mdm.model.dto.data.Address"
                                                 "[\"addressDetails\"]->com.procurement.mdm.model.dto.data."
                                                 "AddressDetails[\"country\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27547')
    def test_delete_tender_procuring_entity_address_address_details_country_id_27547_14(self, country, language,
                                                                                        instance,
                                                                                        cassandra_username,
                                                                                        cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]["id"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.CountryDetails] value failed for JSON "
                                                 "property id due to missing (therefore NULL) value for creator "
                                                 "parameter id which is a non-nullable type\n at [Source: "
                                                 "UNKNOWN; line: -1, column: -1] (through reference chain: "
                                                 "com.procurement.mdm.model.dto.data.FS[\"tender\"]->com."
                                                 "procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]"
                                                 "->com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"address\"]->com.procurement.mdm.model.dto.data.Address"
                                                 "[\"addressDetails\"]->com.procurement.mdm.model.dto.data."
                                                 "AddressDetails[\"country\"]->com.procurement.mdm.model.dto."
                                                 "data.CountryDetails[\"id\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27547')
    def test_delete_tender_procuring_entity_address_address_details_region_27547_15(self, country, language,
                                                                                    instance,
                                                                                    cassandra_username,
                                                                                    cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.AddressDetails] value failed for JSON "
                                                 "property region due to missing (therefore NULL) value for "
                                                 "creator parameter region which is a non-nullable type\n at "
                                                 "[Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"tender\"]->com."
                                                 "procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]->"
                                                 "com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"address\"]->com.procurement.mdm.model.dto.data.Address"
                                                 "[\"addressDetails\"]->com.procurement.mdm.model.dto.data."
                                                 "AddressDetails[\"region\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27547')
    def test_delete_tender_procuring_entity_address_address_details_region_id_27547_16(self, country, language,
                                                                                       instance,
                                                                                       cassandra_username,
                                                                                       cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.RegionDetails] value failed for JSON property "
                                                 "id due to missing (therefore NULL) value for creator parameter "
                                                 "id which is a non-nullable type\n at [Source: UNKNOWN; line: "
                                                 "-1, column: -1] (through reference chain: com.procurement.mdm."
                                                 "model.dto.data.FS[\"tender\"]->com.procurement.mdm.model.dto."
                                                 "data.TenderFS[\"procuringEntity\"]->com.procurement.mdm.model."
                                                 "dto.data.OrganizationReference[\"address\"]->com.procurement."
                                                 "mdm.model.dto.data.Address[\"addressDetails\"]->com.procurement."
                                                 "mdm.model.dto.data.AddressDetails[\"region\"]->com.procurement."
                                                 "mdm.model.dto.data.RegionDetails[\"id\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27547')
    def test_delete_tender_procuring_entity_address_address_details_locality_27547_17(self, country, language,
                                                                                      instance,
                                                                                      cassandra_username,
                                                                                      cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.AddressDetails] value failed for JSON "
                                                 "property locality due to missing (therefore NULL) value for "
                                                 "creator parameter locality which is a non-nullable type\n at "
                                                 "[Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"tender\"]->"
                                                 "com.procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]"
                                                 "->com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"address\"]->com.procurement.mdm.model.dto.data.Address"
                                                 "[\"addressDetails\"]->com.procurement.mdm.model.dto.data."
                                                 "AddressDetails[\"locality\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27547')
    def test_delete_tender_procuring_entity_address_address_details_locality_id_27547_18(self, country, language,
                                                                                         instance,
                                                                                         cassandra_username,
                                                                                         cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["id"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.LocalityDetails] value failed for JSON "
                                                 "property id due to missing (therefore NULL) value for creator "
                                                 "parameter id which is a non-nullable type\n at [Source: "
                                                 "UNKNOWN; line: -1, column: -1] (through reference chain: "
                                                 "com.procurement.mdm.model.dto.data.FS[\"tender\"]->com."
                                                 "procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]->"
                                                 "com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"address\"]->com.procurement.mdm.model.dto.data.Address"
                                                 "[\"addressDetails\"]->com.procurement.mdm.model.dto.data."
                                                 "AddressDetails[\"locality\"]->com.procurement.mdm.model.dto."
                                                 "data.LocalityDetails[\"id\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27547')
    def test_delete_tender_procuring_entity_address_address_details_locality_scheme_27547_19(self, country, language,
                                                                                             instance,
                                                                                             cassandra_username,
                                                                                             cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["scheme"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.LocalityDetails] value failed for JSON "
                                                 "property scheme due to missing (therefore NULL) value for "
                                                 "creator parameter scheme which is a non-nullable type\n at "
                                                 "[Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"tender\"]->"
                                                 "com.procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]"
                                                 "->com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"address\"]->com.procurement.mdm.model.dto.data.Address"
                                                 "[\"addressDetails\"]->com.procurement.mdm.model.dto.data."
                                                 "AddressDetails[\"locality\"]->com.procurement.mdm.model.dto."
                                                 "data.LocalityDetails[\"scheme\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27547')
    def test_delete_tender_procuring_entity_address_address_details_locality_description_27547_20(self, country,
                                                                                                  language,
                                                                                                  instance,
                                                                                                  cassandra_username,
                                                                                                  cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["description"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.LocalityDetails] value failed for JSON "
                                                 "property description due to missing (therefore NULL) value for "
                                                 "creator parameter description which is a non-nullable type\n "
                                                 "at [Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"tender\"]->com."
                                                 "procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]->"
                                                 "com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"address\"]->com.procurement.mdm.model.dto.data.Address"
                                                 "[\"addressDetails\"]->com.procurement.mdm.model.dto.data."
                                                 "AddressDetails[\"locality\"]->com.procurement.mdm.model.dto."
                                                 "data.LocalityDetails[\"description\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27547')
    def test_delete_tender_procuring_entity_contact_point_27547_21(self, country, language,
                                                                   instance,
                                                                   cassandra_username,
                                                                   cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["tender"]["procuringEntity"]["contactPoint"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com."
                                                 "procurement.budget.model.dto.fs.OrganizationReferenceFs] "
                                                 "value failed for JSON property contactPoint due to missing "
                                                 "(therefore NULL) value for creator parameter contactPoint "
                                                 "which is a non-nullable type\n at [Source: UNKNOWN; line: "
                                                 "-1, column: -1] (through reference chain: com.procurement."
                                                 "budget.model.dto.fs.request.FsCreate[\"tender\"]->com."
                                                 "procurement.budget.model.dto.fs.request.TenderFsCreate"
                                                 "[\"procuringEntity\"]->com.procurement.budget.model.dto.fs."
                                                 "OrganizationReferenceFs[\"contactPoint\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27547')
    def test_delete_tender_procuring_entity_contact_point_name_27547_22(self, country, language,
                                                                        instance,
                                                                        cassandra_username,
                                                                        cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["tender"]["procuringEntity"]["contactPoint"]["name"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.ContactPoint] value failed for JSON property "
                                                 "name due to missing (therefore NULL) value for creator parameter "
                                                 "name which is a non-nullable type\n at [Source: UNKNOWN; line: "
                                                 "-1, column: -1] (through reference chain: com.procurement.mdm."
                                                 "model.dto.data.FS[\"tender\"]->com.procurement.mdm.model.dto."
                                                 "data.TenderFS[\"procuringEntity\"]->com.procurement.mdm.model."
                                                 "dto.data.OrganizationReference[\"contactPoint\"]->com.procurement."
                                                 "mdm.model.dto.data.ContactPoint[\"name\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27547')
    def test_delete_tender_procuring_entity_contact_point_email_27547_23(self, country, language,
                                                                         instance,
                                                                         cassandra_username,
                                                                         cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["tender"]["procuringEntity"]["contactPoint"]["email"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.ContactPoint] value failed for JSON property "
                                                 "email due to missing (therefore NULL) value for creator parameter "
                                                 "email which is a non-nullable type\n at [Source: UNKNOWN; line: "
                                                 "-1, column: -1] (through reference chain: com.procurement.mdm."
                                                 "model.dto.data.FS[\"tender\"]->com.procurement.mdm.model.dto."
                                                 "data.TenderFS[\"procuringEntity\"]->com.procurement.mdm.model."
                                                 "dto.data.OrganizationReference[\"contactPoint\"]->com."
                                                 "procurement.mdm.model.dto.data.ContactPoint[\"email\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27547')
    def test_delete_tender_procuring_entity_contact_point_telephone_27547_24(self, country, language,
                                                                             instance,
                                                                             cassandra_username,
                                                                             cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["tender"]["procuringEntity"]["contactPoint"]["telephone"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.ContactPoint] value failed for JSON property "
                                                 "telephone due to missing (therefore NULL) value for creator "
                                                 "parameter telephone which is a non-nullable type\n at [Source: "
                                                 "UNKNOWN; line: -1, column: -1] (through reference chain: com."
                                                 "procurement.mdm.model.dto.data.FS[\"tender\"]->com.procurement."
                                                 "mdm.model.dto.data.TenderFS[\"procuringEntity\"]->com.procurement."
                                                 "mdm.model.dto.data.OrganizationReference[\"contactPoint\"]->"
                                                 "com.procurement.mdm.model.dto.data.ContactPoint[\"telephone\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27547')
    def test_delete_planning_27547_25(self, country, language, instance, cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["planning"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.00.00.00", "description": "Data processing exception."}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27547')
    def test_delete_planning_budget_27547_26(self, country, language, instance, cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["planning"]["budget"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.00.00.00", "description": "Data processing exception."}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27547')
    def test_delete_planning_budget_period_27547_27(self, country, language, instance, cassandra_username,
                                                    cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["planning"]["budget"]["period"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "budget.model.dto.fs.request.BudgetFsCreate] value failed for "
                                                 "JSON property period due to missing (therefore NULL) value for "
                                                 "creator parameter period which is a non-nullable type\n at "
                                                 "[Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                 "chain: com.procurement.budget.model.dto.fs.request.FsCreate"
                                                 "[\"planning\"]->com.procurement.budget.model.dto.fs.request."
                                                 "PlanningFsCreate[\"budget\"]->com.procurement.budget.model.dto."
                                                 "fs.request.BudgetFsCreate[\"period\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27547')
    def test_delete_planning_budget_period_start_date_27547_28(self, country, language, instance, cassandra_username,
                                                               cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["planning"]["budget"]["period"]["startDate"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "budget.model.dto.ocds.Period] value failed for JSON property "
                                                 "startDate due to missing (therefore NULL) value for creator "
                                                 "parameter startDate which is a non-nullable type\n at "
                                                 "[Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                 "chain: com.procurement.budget.model.dto.fs.request.FsCreate"
                                                 "[\"planning\"]->com.procurement.budget.model.dto.fs.request."
                                                 "PlanningFsCreate[\"budget\"]->com.procurement.budget.model.dto."
                                                 "fs.request.BudgetFsCreate[\"period\"]->com.procurement.budget."
                                                 "model.dto.ocds.Period[\"startDate\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27547')
    def test_delete_planning_budget_period_end_date_27547_29(self, country, language, instance, cassandra_username,
                                                             cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["planning"]["budget"]["period"]["endDate"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com."
                                                 "procurement.budget.model.dto.ocds.Period] value failed for JSON "
                                                 "property endDate due to missing (therefore NULL) value for "
                                                 "creator parameter endDate which is a non-nullable type\n at "
                                                 "[Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                 "chain: com.procurement.budget.model.dto.fs.request.FsCreate"
                                                 "[\"planning\"]->com.procurement.budget.model.dto.fs.request."
                                                 "PlanningFsCreate[\"budget\"]->com.procurement.budget.model.dto."
                                                 "fs.request.BudgetFsCreate[\"period\"]->com.procurement.budget."
                                                 "model.dto.ocds.Period[\"endDate\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27547')
    def test_delete_planning_budget_amount_27547_30(self, country, language, instance, cassandra_username,
                                                    cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["planning"]["budget"]["amount"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.00.00.00", "description": "Data processing exception."}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27547')
    def test_delete_planning_budget_amount_amount_27547_31(self, country, language, instance, cassandra_username,
                                                           cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["planning"]["budget"]["amount"]["amount"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com."
                                                 "procurement.budget.model.dto.ocds.Value] value failed for "
                                                 "JSON property amount due to missing (therefore NULL) value "
                                                 "for creator parameter amount which is a non-nullable type\n at "
                                                 "[Source: UNKNOWN; line: -1, column: -1] (through reference chain: "
                                                 "com.procurement.budget.model.dto.fs.request.FsCreate[\"planning\"]"
                                                 "->com.procurement.budget.model.dto.fs.request.PlanningFsCreate"
                                                 "[\"budget\"]->com.procurement.budget.model.dto.fs.request."
                                                 "BudgetFsCreate[\"amount\"]->com.procurement.budget.model.dto."
                                                 "ocds.Value[\"amount\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27547')
    def test_delete_planning_budget_amount_currency_27547_32(self, country, language, instance, cassandra_username,
                                                             cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["planning"]["budget"]["amount"]["currency"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.ValueFS] value failed for JSON property "
                                                 "currency due to missing (therefore NULL) value for creator "
                                                 "parameter currency which is a non-nullable type\n at [Source: "
                                                 "UNKNOWN; line: -1, column: -1] (through reference chain: com."
                                                 "procurement.mdm.model.dto.data.FS[\"planning\"]->com.procurement."
                                                 "mdm.model.dto.data.PlanningFS[\"budget\"]->com.procurement.mdm."
                                                 "model.dto.data.BudgetFS[\"amount\"]->com.procurement.mdm.model."
                                                 "dto.data.ValueFS[\"currency\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27547')
    def test_delete_planning_budget_is_european_union_funded_27547_33(self, country, language, instance,
                                                                      cassandra_username,
                                                                      cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["planning"]["budget"]["isEuropeanUnionFunded"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com."
                                                 "procurement.budget.model.dto.fs.request.BudgetFsCreate] "
                                                 "value failed for JSON property isEuropeanUnionFunded due "
                                                 "to missing (therefore NULL) value for creator parameter "
                                                 "isEuropeanUnionFunded which is a non-nullable type\n at "
                                                 "[Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                 "chain: com.procurement.budget.model.dto.fs.request.FsCreate"
                                                 "[\"planning\"]->com.procurement.budget.model.dto.fs.request."
                                                 "PlanningFsCreate[\"budget\"]->com.procurement.budget.model."
                                                 "dto.fs.request.BudgetFsCreate[\"isEuropeanUnionFunded\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27547')
    def test_delete_planning_budget_european_union_funding_project_name_27547_34(self, country, language, instance,
                                                                                 cassandra_username,
                                                                                 cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["planning"]["budget"]["europeanUnionFunding"]["projectName"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "budget.model.dto.ocds.EuropeanUnionFunding] value failed for "
                                                 "JSON property projectName due to missing (therefore NULL) value "
                                                 "for creator parameter projectName which is a non-nullable type\n "
                                                 "at [Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                 "chain: com.procurement.budget.model.dto.fs.request.FsCreate"
                                                 "[\"planning\"]->com.procurement.budget.model.dto.fs.request."
                                                 "PlanningFsCreate[\"budget\"]->com.procurement.budget.model.dto."
                                                 "fs.request.BudgetFsCreate[\"europeanUnionFunding\"]->com."
                                                 "procurement.budget.model.dto.ocds.EuropeanUnionFunding"
                                                 "[\"projectName\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27547')
    def test_delete_planning_budget_european_union_funding_project_identifier_27547_35(self, country, language,
                                                                                       instance,
                                                                                       cassandra_username,
                                                                                       cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_treasury_money)
        del payload["planning"]["budget"]["europeanUnionFunding"]["projectIdentifier"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "budget.model.dto.ocds.EuropeanUnionFunding] value failed for "
                                                 "JSON property projectIdentifier due to missing (therefore NULL) "
                                                 "value for creator parameter projectIdentifier which is a non-"
                                                 "nullable type\n at [Source: UNKNOWN; line: -1, column: -1] "
                                                 "(through reference chain: com.procurement.budget.model.dto.fs."
                                                 "request.FsCreate[\"planning\"]->com.procurement.budget.model.dto."
                                                 "fs.request.PlanningFsCreate[\"budget\"]->com.procurement.budget."
                                                 "model.dto.fs.request.BudgetFsCreate[\"europeanUnionFunding\"]->"
                                                 "com.procurement.budget.model.dto.ocds.EuropeanUnionFunding"
                                                 "[\"projectIdentifier\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )


class TestCheckOnPossibilityOfCreatingFsWithObligatoryDataModelTreasuryMoney(object):
    @pytestrail.case("27548")
    def test_send_the_request_27548_1(self, country, language, instance, cassandra_username,
                                      cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_obligatory_data_model_treasury_money)
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )

    @pytestrail.case("27548")
    def test_see_the_result_in_feed_point_point_27548_2(self, country, language, instance, cassandra_username,
                                                        cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_obligatory_data_model_treasury_money)
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(fs.check_on_that_message_is_successfully_create_fs())
        )

    @pytestrail.case('27548')
    def test_check_on_correctness_of_publishing_fs_release_on_public_point_27548_3(self, country, language, instance,
                                                                                   cassandra_username,
                                                                                   cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_obligatory_data_model_treasury_money)
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        ei = fs.insert_ei_full_data_model(cp_id, ei_token)
        if "buyer" in payload.keys():
            buyer_in_payload = True
            source_entity_id = payload["buyer"]["identifier"]["scheme"] + "-" + payload["buyer"]["identifier"]["id"]
            source_entity_name = payload["buyer"]["name"]
            status = "active"
        else:
            buyer_in_payload = False
            status = "planning"
            ei_release = requests.get(
                url=ei[0] + "/" + ei[2]
            ).json()
            source_entity_id = ei_release["releases"][0]["buyer"]["id"]
            source_entity_name = ei_release["releases"][0]["buyer"]["name"]
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        mdm = MdmService(
            instance="dev",
            lang="ro",
            country=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]["id"],
            region=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"],
            locality=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["id"]
        )
        data = mdm.process_fs_data(cp_id).json()
        country_from_mdm = data["data"]["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]
        region_from_mdm = data["data"]["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]
        locality_from_mdm = data["data"]["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]
        url_create = message_from_kafka['data']['url'] + '/' + message_from_kafka['data']['outcomes']['fs'][0]['id']
        fs_release = requests.get(url=url_create).json()
        fs_release_timestamp = int(fs_release["releases"][0]["id"][46:59])
        convert_timestamp_to_date = get_human_date_in_utc_format(fs_release_timestamp)
        roles_list = list()
        for key, values in fs_release["releases"][0]["parties"][0].items():
            if key == "roles":
                role = fs_release["releases"][0]["parties"][0].get(key)
                roles_list.append(role[0])
        keys_list = list()
        for i in fs_release.keys():
            if i == "uri":
                keys_list.append(i)
            if i == "version":
                keys_list.append(i)
            if i == "extensions":
                keys_list.append(i)
            if i == "publisher":
                keys_list.append(i)
            if i == "license":
                keys_list.append(i)
            if i == "publicationPolicy":
                keys_list.append(i)
            if i == "publishedDate":
                keys_list.append(i)
            if i == "releases":
                keys_list.append(i)
        for i in fs_release["publisher"].keys():
            if i == "name":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_release["releases"][0].keys():
            if i == "ocid":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "date":
                keys_list.append(i)
            if i == "tag":
                keys_list.append(i)
            if i == "initiationType":
                keys_list.append(i)
            if i == "tender":
                keys_list.append(i)
            if i == "parties":
                keys_list.append(i)
            if i == "planning":
                keys_list.append(i)
            if i == "relatedProcesses":
                keys_list.append(i)
        for i in fs_release["releases"][0]["tender"].keys():
            if i == "id":
                keys_list.append(i)
            if i == "status":
                keys_list.append(i)
            if i == "statusDetails":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][0].keys():
            if i == "id":
                keys_list.append(i)
            if i == "name":
                keys_list.append(i)
            if i == "identifier":
                keys_list.append(i)
            if i == "address":
                keys_list.append(i)
            if i == "contactPoint":
                keys_list.append(i)
            if i == "roles":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][0]["identifier"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "legalName":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][0]["address"].keys():
            if i == "streetAddress":
                keys_list.append(i)
            if i == "addressDetails":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][0]["address"]["addressDetails"].keys():
            if i == "country":
                keys_list.append(i)
            if i == "region":
                keys_list.append(i)
            if i == "locality":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][0]["contactPoint"].keys():
            if i == "name":
                keys_list.append(i)
            if i == "email":
                keys_list.append(i)
            if i == "telephone":
                keys_list.append(i)
        for i in fs_release["releases"][0]["planning"].keys():
            if i == "budget":
                keys_list.append(i)
        for i in fs_release["releases"][0]["planning"]["budget"].keys():
            if i == "period":
                keys_list.append(i)
            if i == "amount":
                keys_list.append(i)
            if i == "isEuropeanUnionFunded":
                keys_list.append(i)
            if i == "verified":
                keys_list.append(i)
            if i == "sourceEntity":
                keys_list.append(i)
        for i in fs_release["releases"][0]["planning"]["budget"]["period"].keys():
            if i == "startDate":
                keys_list.append(i)
            if i == "endDate":
                keys_list.append(i)
        for i in fs_release["releases"][0]["planning"]["budget"]["amount"].keys():
            if i == "amount":
                keys_list.append(i)
            if i == "currency":
                keys_list.append(i)
        for i in fs_release["releases"][0]["planning"]["budget"]["sourceEntity"].keys():
            if i == "id":
                keys_list.append(i)
            if i == "name":
                keys_list.append(i)
        for i in fs_release["releases"][0]["relatedProcesses"][0].keys():
            if i == "id":
                keys_list.append(i)
            if i == "relationship":
                keys_list.append(i)
            if i == "scheme":
                keys_list.append(i)
            if i == "identifier":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        procuring_entity_scheme = payload["tender"]["procuringEntity"]["identifier"]["scheme"]
        procuring_entity_id = payload["tender"]["procuringEntity"]["identifier"]["id"]
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[0]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="version",
            actual_result=keys_list[1]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="extensions",
            actual_result=keys_list[2]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="publisher",
            actual_result=keys_list[3]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="license",
            actual_result=keys_list[4]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="publicationPolicy",
            actual_result=keys_list[5]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="publishedDate",
            actual_result=keys_list[6]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="releases",
            actual_result=keys_list[7]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="name",
            actual_result=keys_list[8]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[9]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="ocid",
            actual_result=keys_list[10]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[11]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="date",
            actual_result=keys_list[12]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="tag",
            actual_result=keys_list[13]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="initiationType",
            actual_result=keys_list[14]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="tender",
            actual_result=keys_list[15]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="parties",
            actual_result=keys_list[16]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="planning",
            actual_result=keys_list[17])
        assert compare_actual_result_and_expected_result(
            expected_result="relatedProcesses",
            actual_result=keys_list[18]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[19]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="status",
            actual_result=keys_list[20]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="statusDetails",
            actual_result=keys_list[21]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[22]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="name",
            actual_result=keys_list[23]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="identifier",
            actual_result=keys_list[24]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="address",
            actual_result=keys_list[25]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="contactPoint",
            actual_result=keys_list[26]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="roles",
            actual_result=keys_list[27]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="scheme",
            actual_result=keys_list[28]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[29]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="legalName",
            actual_result=keys_list[30]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="streetAddress",
            actual_result=keys_list[31]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="addressDetails",
            actual_result=keys_list[32]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="country",
            actual_result=keys_list[33]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="region",
            actual_result=keys_list[34]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="locality",
            actual_result=keys_list[35]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="scheme",
            actual_result=keys_list[36]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[37]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="description",
            actual_result=keys_list[38]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[39]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="scheme",
            actual_result=keys_list[40]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[41]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="description",
            actual_result=keys_list[42]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[43]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="scheme",
            actual_result=keys_list[44]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[45]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="description",
            actual_result=keys_list[46]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[47]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="name",
            actual_result=keys_list[48]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="email",
            actual_result=keys_list[49]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="telephone",
            actual_result=keys_list[50]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="budget",
            actual_result=keys_list[51]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="period",
            actual_result=keys_list[52]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="amount",
            actual_result=keys_list[53]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="isEuropeanUnionFunded",
            actual_result=keys_list[54]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="verified",
            actual_result=keys_list[55]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="sourceEntity",
            actual_result=keys_list[56]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="startDate",
            actual_result=keys_list[57]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="endDate",
            actual_result=keys_list[58]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="amount",
            actual_result=keys_list[59]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="currency",
            actual_result=keys_list[60]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[61]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="name",
            actual_result=keys_list[62]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[63]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="relationship",
            actual_result=keys_list[64]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="scheme",
            actual_result=keys_list[65]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="identifier",
            actual_result=keys_list[66]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[67]
        )

        assert compare_actual_result_and_expected_result(
            expected_result=f"http://dev.public.eprocurement.systems/budgets/{message_from_kafka['data']['ocid']}/"
                            f"{message_from_kafka['data']['outcomes']['fs'][0]['id']}",
            actual_result=fs_release["uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="666",
            actual_result=fs_release["version"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="https://raw.githubusercontent.com/open-contracting/ocds_bid_extension/v1.1.1/"
                            "extension.json",
            actual_result=fs_release["extensions"][0]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="https://raw.githubusercontent.com/open-contracting/ocds_enquiry_extension/v1.1.1/"
                            "extension.js222",
            actual_result=fs_release["extensions"][1]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=instance.upper() + "-ENV",
            actual_result=fs_release["publisher"]["name"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="https://www.ustudio.com",
            actual_result=fs_release["publisher"]["uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="http://opendefinition.org/licenses/222",
            actual_result=fs_release["license"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="http://opendefinition.org/licenses/222",
            actual_result=fs_release["publicationPolicy"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=message_from_kafka["data"]["operationDate"],
            actual_result=fs_release["publishedDate"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=message_from_kafka['data']['outcomes']['fs'][0]['id'],
            actual_result=fs_release["releases"][0]["ocid"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=message_from_kafka['data']['outcomes']['fs'][0]['id'],
            actual_result=fs_release["releases"][0]["id"][0:45]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=message_from_kafka["data"]["operationDate"],
            actual_result=convert_timestamp_to_date[0]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=message_from_kafka["data"]["operationDate"],
            actual_result=fs_release["releases"][0]["date"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="planning",
            actual_result=fs_release["releases"][0]["tag"][0]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="tender",
            actual_result=fs_release["releases"][0]["initiationType"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(is_it_uuid(fs_release["releases"][0]["tender"]["id"], 4))
        )
        assert compare_actual_result_and_expected_result(
            expected_result=status,
            actual_result=fs_release["releases"][0]["tender"]["status"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="empty",
            actual_result=fs_release["releases"][0]["tender"]["statusDetails"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=procuring_entity_scheme + "-" + procuring_entity_id,
            actual_result=fs_release["releases"][0]["parties"][0]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["name"],
            actual_result=fs_release["releases"][0]["parties"][0]["name"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["identifier"]["scheme"],
            actual_result=fs_release["releases"][0]["parties"][0]["identifier"]["scheme"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["identifier"]["id"],
            actual_result=fs_release["releases"][0]["parties"][0]["identifier"]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["identifier"]["legalName"],
            actual_result=fs_release["releases"][0]["parties"][0]["identifier"]["legalName"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["address"]["streetAddress"],
            actual_result=fs_release["releases"][0]["parties"][0]["address"]["streetAddress"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=country_from_mdm["scheme"],
            actual_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["scheme"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]["id"],
            actual_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=country_from_mdm["description"],
            actual_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["description"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=country_from_mdm["uri"],
            actual_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=region_from_mdm["scheme"],
            actual_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["scheme"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"],
            actual_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=region_from_mdm["description"],
            actual_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["description"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=region_from_mdm["uri"],
            actual_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=locality_from_mdm["scheme"],
            actual_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["scheme"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["id"],
            actual_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=locality_from_mdm["description"],
            actual_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
                "description"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=locality_from_mdm["uri"],
            actual_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
                "uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["contactPoint"]["name"],
            actual_result=fs_release["releases"][0]["parties"][0]["contactPoint"]["name"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["contactPoint"]["email"],
            actual_result=fs_release["releases"][0]["parties"][0]["contactPoint"]["email"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["contactPoint"]["telephone"],
            actual_result=fs_release["releases"][0]["parties"][0]["contactPoint"]["telephone"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="payer",
            actual_result=roles_list[0]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["period"]["startDate"],
            actual_result=fs_release["releases"][0]["planning"]["budget"]["period"]["startDate"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["period"]["endDate"],
            actual_result=fs_release["releases"][0]["planning"]["budget"]["period"]["endDate"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(payload["planning"]["budget"]["amount"]["amount"]),
            actual_result=str(fs_release["releases"][0]["planning"]["budget"]["amount"]["amount"])
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["amount"]["currency"],
            actual_result=fs_release["releases"][0]["planning"]["budget"]["amount"]["currency"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(payload["planning"]["budget"]["isEuropeanUnionFunded"]),
            actual_result=str(fs_release["releases"][0]["planning"]["budget"]["isEuropeanUnionFunded"])
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(buyer_in_payload),
            actual_result=str(fs_release["releases"][0]["planning"]["budget"]["verified"])
        )
        assert compare_actual_result_and_expected_result(
            expected_result=source_entity_id,
            actual_result=fs_release["releases"][0]["planning"]["budget"]["sourceEntity"]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=source_entity_name,
            actual_result=fs_release["releases"][0]["planning"]["budget"]["sourceEntity"]["name"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(is_it_uuid(fs_release["releases"][0]["relatedProcesses"][0]["id"], 1))
        )
        assert compare_actual_result_and_expected_result(
            expected_result="parent",
            actual_result=fs_release["releases"][0]["relatedProcesses"][0]["relationship"][0]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="ocid",
            actual_result=fs_release["releases"][0]["relatedProcesses"][0]["scheme"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=cp_id,
            actual_result=fs_release["releases"][0]["relatedProcesses"][0]["identifier"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{cp_id}",
            actual_result=fs_release["releases"][0]["relatedProcesses"][0]["uri"]
        )


class TestCheckOnPossibilityOfCreatingFsWithFullDataModelOwnMoney(object):
    @pytestrail.case("27549")
    def test_send_the_request_27549_1(self, country, language, instance, cassandra_username,
                                      cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )

    @pytestrail.case("27549")
    def test_see_the_result_in_feed_point_point_27549_2(self, country, language, instance, cassandra_username,
                                                        cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(fs.check_on_that_message_is_successfully_create_fs())
        )

    @pytestrail.case('27549')
    def test_check_on_correctness_of_publishing_fs_release_on_public_point_27549_3(self, country, language,
                                                                                   instance,
                                                                                   cassandra_username,
                                                                                   cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = \
            payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]["id"]
        payload["buyer"]["address"]["addressDetails"]["region"]["id"] = \
            payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"]
        payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = \
            payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["id"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        ei = fs.insert_ei_full_data_model(cp_id, ei_token)
        if "buyer" in payload.keys():
            buyer_in_payload = True
            source_entity_id = payload["buyer"]["identifier"]["scheme"] + "-" + payload["buyer"]["identifier"][
                "id"]
            source_entity_name = payload["buyer"]["name"]
            status = "active"
        else:
            buyer_in_payload = False
            status = "planning"
            ei_release = requests.get(
                url=ei[0] + "/" + ei[2]
            ).json()
            source_entity_id = ei_release["releases"][0]["buyer"]["id"]
            source_entity_name = ei_release["releases"][0]["buyer"]["name"]
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        mdm = MdmService(
            instance="dev",
            lang="ro",
            country=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]["id"],
            region=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"],
            locality=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["id"]
        )
        data = mdm.process_fs_data(cp_id).json()
        country_from_mdm = data["data"]["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]
        region_from_mdm = data["data"]["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]
        locality_from_mdm = data["data"]["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]
        url_create = message_from_kafka['data']['url'] + '/' + message_from_kafka['data']['outcomes']['fs'][0][
            'id']
        fs_release = requests.get(url=url_create).json()
        fs_release_timestamp = int(fs_release["releases"][0]["id"][46:59])
        convert_timestamp_to_date = get_human_date_in_utc_format(fs_release_timestamp)
        roles_list = list()
        for f in fs_release["releases"][0]["parties"]:
            if f["roles"] == ["payer"]:
                roles_list.append(f)
            if f["roles"] == ["funder"]:
                roles_list.append(f)
        keys_list = list()
        for i in fs_release.keys():
            if i == "uri":
                keys_list.append(i)
            if i == "version":
                keys_list.append(i)
            if i == "extensions":
                keys_list.append(i)
            if i == "publisher":
                keys_list.append(i)
            if i == "license":
                keys_list.append(i)
            if i == "publicationPolicy":
                keys_list.append(i)
            if i == "publishedDate":
                keys_list.append(i)
            if i == "releases":
                keys_list.append(i)
        for i in fs_release["publisher"].keys():
            if i == "name":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_release["releases"][0].keys():
            if i == "ocid":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "date":
                keys_list.append(i)
            if i == "tag":
                keys_list.append(i)
            if i == "initiationType":
                keys_list.append(i)
            if i == "tender":
                keys_list.append(i)
            if i == "parties":
                keys_list.append(i)
            if i == "planning":
                keys_list.append(i)
            if i == "relatedProcesses":
                keys_list.append(i)
        for i in fs_release["releases"][0]["tender"].keys():
            if i == "id":
                keys_list.append(i)
            if i == "status":
                keys_list.append(i)
            if i == "statusDetails":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][0].keys():
            if i == "id":
                keys_list.append(i)
            if i == "name":
                keys_list.append(i)
            if i == "identifier":
                keys_list.append(i)
            if i == "address":
                keys_list.append(i)
            if i == "additionalIdentifiers":
                keys_list.append(i)
            if i == "contactPoint":
                keys_list.append(i)
            if i == "roles":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][0]["identifier"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "legalName":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][0]["address"].keys():
            if i == "streetAddress":
                keys_list.append(i)
            if i == "postalCode":
                keys_list.append(i)
            if i == "addressDetails":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][0]["address"]["addressDetails"].keys():
            if i == "country":
                keys_list.append(i)
            if i == "region":
                keys_list.append(i)
            if i == "locality":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][0]["additionalIdentifiers"][0].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "legalName":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][0]["contactPoint"].keys():
            if i == "name":
                keys_list.append(i)
            if i == "email":
                keys_list.append(i)
            if i == "telephone":
                keys_list.append(i)
            if i == "faxNumber":
                keys_list.append(i)
            if i == "url":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][1].keys():
            if i == "id":
                keys_list.append(i)
            if i == "name":
                keys_list.append(i)
            if i == "identifier":
                keys_list.append(i)
            if i == "address":
                keys_list.append(i)
            if i == "additionalIdentifiers":
                keys_list.append(i)
            if i == "contactPoint":
                keys_list.append(i)
            if i == "roles":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][1]["identifier"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "legalName":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][1]["address"].keys():
            if i == "streetAddress":
                keys_list.append(i)
            if i == "postalCode":
                keys_list.append(i)
            if i == "addressDetails":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][1]["address"]["addressDetails"].keys():
            if i == "country":
                keys_list.append(i)
            if i == "region":
                keys_list.append(i)
            if i == "locality":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][1]["address"]["addressDetails"]["country"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][1]["address"]["addressDetails"]["region"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][1]["address"]["addressDetails"]["locality"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][1]["additionalIdentifiers"][0].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "legalName":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][1]["contactPoint"].keys():
            if i == "name":
                keys_list.append(i)
            if i == "email":
                keys_list.append(i)
            if i == "telephone":
                keys_list.append(i)
            if i == "faxNumber":
                keys_list.append(i)
            if i == "url":
                keys_list.append(i)
        for i in fs_release["releases"][0]["planning"].keys():
            if i == "budget":
                keys_list.append(i)
            if i == "rationale":
                keys_list.append(i)
        for i in fs_release["releases"][0]["planning"]["budget"].keys():
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
            if i == "period":
                keys_list.append(i)
            if i == "amount":
                keys_list.append(i)
            if i == "europeanUnionFunding":
                keys_list.append(i)
            if i == "isEuropeanUnionFunded":
                keys_list.append(i)
            if i == "verified":
                keys_list.append(i)
            if i == "sourceEntity":
                keys_list.append(i)
            if i == "project":
                keys_list.append(i)
            if i == "projectID":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_release["releases"][0]["planning"]["budget"]["period"].keys():
            if i == "startDate":
                keys_list.append(i)
            if i == "endDate":
                keys_list.append(i)
        for i in fs_release["releases"][0]["planning"]["budget"]["amount"].keys():
            if i == "amount":
                keys_list.append(i)
            if i == "currency":
                keys_list.append(i)
        for i in fs_release["releases"][0]["planning"]["budget"]["europeanUnionFunding"].keys():
            if i == "projectIdentifier":
                keys_list.append(i)
            if i == "projectName":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_release["releases"][0]["planning"]["budget"]["sourceEntity"].keys():
            if i == "id":
                keys_list.append(i)
            if i == "name":
                keys_list.append(i)
        for i in fs_release["releases"][0]["relatedProcesses"][0].keys():
            if i == "id":
                keys_list.append(i)
            if i == "relationship":
                keys_list.append(i)
            if i == "scheme":
                keys_list.append(i)
            if i == "identifier":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        procuring_entity_scheme = payload["tender"]["procuringEntity"]["identifier"]["scheme"]
        procuring_entity_id = payload["tender"]["procuringEntity"]["identifier"]["id"]
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[0]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="version",
            actual_result=keys_list[1]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="extensions",
            actual_result=keys_list[2]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="publisher",
            actual_result=keys_list[3]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="license",
            actual_result=keys_list[4]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="publicationPolicy",
            actual_result=keys_list[5]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="publishedDate",
            actual_result=keys_list[6]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="releases",
            actual_result=keys_list[7]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="name",
            actual_result=keys_list[8]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[9]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="ocid",
            actual_result=keys_list[10]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[11]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="date",
            actual_result=keys_list[12]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="tag",
            actual_result=keys_list[13]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="initiationType",
            actual_result=keys_list[14]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="tender",
            actual_result=keys_list[15]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="parties",
            actual_result=keys_list[16]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="planning",
            actual_result=keys_list[17])
        assert compare_actual_result_and_expected_result(
            expected_result="relatedProcesses",
            actual_result=keys_list[18]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[19]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="status",
            actual_result=keys_list[20]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="statusDetails",
            actual_result=keys_list[21]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[22]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="name",
            actual_result=keys_list[23]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="identifier",
            actual_result=keys_list[24]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="address",
            actual_result=keys_list[25]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="additionalIdentifiers",
            actual_result=keys_list[26]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="contactPoint",
            actual_result=keys_list[27]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="roles",
            actual_result=keys_list[28]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="scheme",
            actual_result=keys_list[29]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[30]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="legalName",
            actual_result=keys_list[31]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[32]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="streetAddress",
            actual_result=keys_list[33]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="postalCode",
            actual_result=keys_list[34]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="addressDetails",
            actual_result=keys_list[35]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="country",
            actual_result=keys_list[36]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="region",
            actual_result=keys_list[37]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="locality",
            actual_result=keys_list[38]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="scheme",
            actual_result=keys_list[39]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[40]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="description",
            actual_result=keys_list[41]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[42]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="scheme",
            actual_result=keys_list[43]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[44]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="description",
            actual_result=keys_list[45]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[46]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="scheme",
            actual_result=keys_list[47]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[48]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="description",
            actual_result=keys_list[49]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[50]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="scheme",
            actual_result=keys_list[51]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[52]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="legalName",
            actual_result=keys_list[53]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[54]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="name",
            actual_result=keys_list[55]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="email",
            actual_result=keys_list[56]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="telephone",
            actual_result=keys_list[57]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="faxNumber",
            actual_result=keys_list[58]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="url",
            actual_result=keys_list[59]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[60]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="name",
            actual_result=keys_list[61]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="identifier",
            actual_result=keys_list[62]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="address",
            actual_result=keys_list[63]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="additionalIdentifiers",
            actual_result=keys_list[64]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="contactPoint",
            actual_result=keys_list[65]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="roles",
            actual_result=keys_list[66]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="scheme",
            actual_result=keys_list[67]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[68]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="legalName",
            actual_result=keys_list[69]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[70]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="streetAddress",
            actual_result=keys_list[71]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="postalCode",
            actual_result=keys_list[72]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="addressDetails",
            actual_result=keys_list[73]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="country",
            actual_result=keys_list[74]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="region",
            actual_result=keys_list[75]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="locality",
            actual_result=keys_list[76]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="scheme",
            actual_result=keys_list[77]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[78]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="description",
            actual_result=keys_list[79]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[80]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="scheme",
            actual_result=keys_list[81]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[82]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="description",
            actual_result=keys_list[83]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[84]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="scheme",
            actual_result=keys_list[85]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[86]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="description",
            actual_result=keys_list[87]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[88]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="scheme",
            actual_result=keys_list[89]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[90]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="legalName",
            actual_result=keys_list[91]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[92]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="name",
            actual_result=keys_list[93]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="email",
            actual_result=keys_list[94]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="telephone",
            actual_result=keys_list[95]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="faxNumber",
            actual_result=keys_list[96]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="url",
            actual_result=keys_list[97]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="budget",
            actual_result=keys_list[98]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="rationale",
            actual_result=keys_list[99]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[100]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="description",
            actual_result=keys_list[101]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="period",
            actual_result=keys_list[102]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="amount",
            actual_result=keys_list[103]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="europeanUnionFunding",
            actual_result=keys_list[104]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="isEuropeanUnionFunded",
            actual_result=keys_list[105]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="verified",
            actual_result=keys_list[106]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="sourceEntity",
            actual_result=keys_list[107]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="project",
            actual_result=keys_list[108]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="projectID",
            actual_result=keys_list[109]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[110]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="startDate",
            actual_result=keys_list[111]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="endDate",
            actual_result=keys_list[112]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="amount",
            actual_result=keys_list[113]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="currency",
            actual_result=keys_list[114]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="projectIdentifier",
            actual_result=keys_list[115]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="projectName",
            actual_result=keys_list[116]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[117]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[118]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="name",
            actual_result=keys_list[119]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[120]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="relationship",
            actual_result=keys_list[121]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="scheme",
            actual_result=keys_list[122]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="identifier",
            actual_result=keys_list[123]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[124]
        )

        assert compare_actual_result_and_expected_result(
            expected_result=f"http://dev.public.eprocurement.systems/budgets/{message_from_kafka['data']['ocid']}/"
                            f"{message_from_kafka['data']['outcomes']['fs'][0]['id']}",
            actual_result=fs_release["uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="666",
            actual_result=fs_release["version"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="https://raw.githubusercontent.com/open-contracting/ocds_bid_extension/v1.1.1/"
                            "extension.json",
            actual_result=fs_release["extensions"][0]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="https://raw.githubusercontent.com/open-contracting/ocds_enquiry_extension/v1.1.1/"
                            "extension.js222",
            actual_result=fs_release["extensions"][1]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=instance.upper() + "-ENV",
            actual_result=fs_release["publisher"]["name"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="https://www.ustudio.com",
            actual_result=fs_release["publisher"]["uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="http://opendefinition.org/licenses/222",
            actual_result=fs_release["license"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="http://opendefinition.org/licenses/222",
            actual_result=fs_release["publicationPolicy"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=message_from_kafka["data"]["operationDate"],
            actual_result=fs_release["publishedDate"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=message_from_kafka['data']['outcomes']['fs'][0]['id'],
            actual_result=fs_release["releases"][0]["ocid"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=message_from_kafka['data']['outcomes']['fs'][0]['id'],
            actual_result=fs_release["releases"][0]["id"][0:45]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=message_from_kafka["data"]["operationDate"],
            actual_result=convert_timestamp_to_date[0]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=message_from_kafka["data"]["operationDate"],
            actual_result=fs_release["releases"][0]["date"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="planning",
            actual_result=fs_release["releases"][0]["tag"][0]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="tender",
            actual_result=fs_release["releases"][0]["initiationType"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(is_it_uuid(fs_release["releases"][0]["tender"]["id"], 4))
        )
        assert compare_actual_result_and_expected_result(
            expected_result=status,
            actual_result=fs_release["releases"][0]["tender"]["status"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="empty",
            actual_result=fs_release["releases"][0]["tender"]["statusDetails"]
        )

        assert compare_actual_result_and_expected_result(
            expected_result=procuring_entity_scheme + "-" + procuring_entity_id,
            actual_result=roles_list[1]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["name"],
            actual_result=roles_list[1]["name"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["identifier"]["scheme"],
            actual_result=roles_list[1]["identifier"]["scheme"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["identifier"]["id"],
            actual_result=roles_list[1]["identifier"]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["identifier"]["legalName"],
            actual_result=roles_list[1]["identifier"]["legalName"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["identifier"]["uri"],
            actual_result=roles_list[1]["identifier"]["uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["address"]["streetAddress"],
            actual_result=roles_list[1]["address"]["streetAddress"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["address"]["postalCode"],
            actual_result=roles_list[1]["address"]["postalCode"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=country_from_mdm["scheme"],
            actual_result=roles_list[1]["address"]["addressDetails"]["country"]["scheme"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]["id"],
            actual_result=roles_list[1]["address"]["addressDetails"]["country"]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=country_from_mdm["description"],
            actual_result=roles_list[1]["address"]["addressDetails"]["country"]["description"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=country_from_mdm["uri"],
            actual_result=roles_list[1]["address"]["addressDetails"]["country"]["uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=region_from_mdm["scheme"],
            actual_result=roles_list[1]["address"]["addressDetails"]["region"]["scheme"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"],
            actual_result=roles_list[1]["address"]["addressDetails"]["region"]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=region_from_mdm["description"],
            actual_result=roles_list[1]["address"]["addressDetails"]["region"]["description"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=region_from_mdm["uri"],
            actual_result=roles_list[1]["address"]["addressDetails"]["region"]["uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=locality_from_mdm["scheme"],
            actual_result=roles_list[1]["address"]["addressDetails"]["locality"]["scheme"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["id"],
            actual_result=roles_list[1]["address"]["addressDetails"]["locality"]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=locality_from_mdm["description"],
            actual_result=roles_list[1]["address"]["addressDetails"]["locality"]["description"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=locality_from_mdm["uri"],
            actual_result=roles_list[1]["address"]["addressDetails"]["locality"]["uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["scheme"],
            actual_result=roles_list[1]["additionalIdentifiers"][0]["scheme"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["id"],
            actual_result=roles_list[1]["additionalIdentifiers"][0]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["legalName"],
            actual_result=roles_list[1]["additionalIdentifiers"][0]["legalName"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["uri"],
            actual_result=roles_list[1]["additionalIdentifiers"][0]["uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["contactPoint"]["name"],
            actual_result=roles_list[1]["contactPoint"]["name"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["contactPoint"]["email"],
            actual_result=roles_list[1]["contactPoint"]["email"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["contactPoint"]["telephone"],
            actual_result=roles_list[1]["contactPoint"]["telephone"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["contactPoint"]["faxNumber"],
            actual_result=roles_list[1]["contactPoint"]["faxNumber"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["contactPoint"]["url"],
            actual_result=roles_list[1]["contactPoint"]["url"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="payer",
            actual_result=roles_list[1]["roles"][0]
        )

        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["identifier"]["scheme"] + "-" + payload["buyer"]["identifier"][
                "id"],
            actual_result=roles_list[0]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["name"],
            actual_result=roles_list[0]["name"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["identifier"]["scheme"],
            actual_result=roles_list[0]["identifier"]["scheme"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["identifier"]["id"],
            actual_result=roles_list[0]["identifier"]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["identifier"]["legalName"],
            actual_result=roles_list[0]["identifier"]["legalName"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["identifier"]["uri"],
            actual_result=roles_list[0]["identifier"]["uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["address"]["streetAddress"],
            actual_result=roles_list[0]["address"]["streetAddress"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["address"]["postalCode"],
            actual_result=roles_list[0]["address"]["postalCode"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=country_from_mdm["scheme"],
            actual_result=roles_list[0]["address"]["addressDetails"]["country"]["scheme"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["address"]["addressDetails"]["country"]["id"],
            actual_result=roles_list[0]["address"]["addressDetails"]["country"]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=country_from_mdm["description"],
            actual_result=roles_list[0]["address"]["addressDetails"]["country"]["description"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=country_from_mdm["uri"],
            actual_result=roles_list[0]["address"]["addressDetails"]["country"]["uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=region_from_mdm["scheme"],
            actual_result=roles_list[0]["address"]["addressDetails"]["region"]["scheme"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["address"]["addressDetails"]["region"]["id"],
            actual_result=roles_list[0]["address"]["addressDetails"]["region"]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=region_from_mdm["description"],
            actual_result=roles_list[0]["address"]["addressDetails"]["region"]["description"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=region_from_mdm["uri"],
            actual_result=roles_list[0]["address"]["addressDetails"]["region"]["uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=locality_from_mdm["scheme"],
            actual_result=roles_list[0]["address"]["addressDetails"]["locality"]["scheme"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["address"]["addressDetails"]["locality"]["id"],
            actual_result=roles_list[0]["address"]["addressDetails"]["locality"]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=locality_from_mdm["description"],
            actual_result=roles_list[0]["address"]["addressDetails"]["locality"]["description"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=locality_from_mdm["uri"],
            actual_result=roles_list[0]["address"]["addressDetails"]["locality"]["uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["additionalIdentifiers"][0]["scheme"],
            actual_result=roles_list[0]["additionalIdentifiers"][0]["scheme"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["additionalIdentifiers"][0]["id"],
            actual_result=roles_list[0]["additionalIdentifiers"][0]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["additionalIdentifiers"][0]["legalName"],
            actual_result=roles_list[0]["additionalIdentifiers"][0]["legalName"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["additionalIdentifiers"][0]["uri"],
            actual_result=roles_list[0]["additionalIdentifiers"][0]["uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["contactPoint"]["name"],
            actual_result=roles_list[0]["contactPoint"]["name"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["contactPoint"]["email"],
            actual_result=roles_list[0]["contactPoint"]["email"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["contactPoint"]["telephone"],
            actual_result=roles_list[0]["contactPoint"]["telephone"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["contactPoint"]["faxNumber"],
            actual_result=roles_list[0]["contactPoint"]["faxNumber"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["contactPoint"]["url"],
            actual_result=roles_list[0]["contactPoint"]["url"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="funder",
            actual_result=roles_list[0]["roles"][0]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["id"],
            actual_result=fs_release["releases"][0]["planning"]["budget"]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["description"],
            actual_result=fs_release["releases"][0]["planning"]["budget"]["description"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["period"]["startDate"],
            actual_result=fs_release["releases"][0]["planning"]["budget"]["period"]["startDate"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["period"]["endDate"],
            actual_result=fs_release["releases"][0]["planning"]["budget"]["period"]["endDate"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(payload["planning"]["budget"]["amount"]["amount"]),
            actual_result=str(fs_release["releases"][0]["planning"]["budget"]["amount"]["amount"])
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["amount"]["currency"],
            actual_result=fs_release["releases"][0]["planning"]["budget"]["amount"]["currency"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["europeanUnionFunding"]["projectIdentifier"],
            actual_result=fs_release["releases"][0]["planning"]["budget"]["europeanUnionFunding"][
                "projectIdentifier"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["europeanUnionFunding"]["projectName"],
            actual_result=fs_release["releases"][0]["planning"]["budget"]["europeanUnionFunding"]["projectName"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["europeanUnionFunding"]["uri"],
            actual_result=fs_release["releases"][0]["planning"]["budget"]["europeanUnionFunding"]["uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(payload["planning"]["budget"]["isEuropeanUnionFunded"]),
            actual_result=str(fs_release["releases"][0]["planning"]["budget"]["isEuropeanUnionFunded"])
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(buyer_in_payload),
            actual_result=str(fs_release["releases"][0]["planning"]["budget"]["verified"])
        )
        assert compare_actual_result_and_expected_result(
            expected_result=source_entity_id,
            actual_result=fs_release["releases"][0]["planning"]["budget"]["sourceEntity"]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=source_entity_name,
            actual_result=fs_release["releases"][0]["planning"]["budget"]["sourceEntity"]["name"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["project"],
            actual_result=fs_release["releases"][0]["planning"]["budget"]["project"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["projectID"],
            actual_result=fs_release["releases"][0]["planning"]["budget"]["projectID"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["uri"],
            actual_result=fs_release["releases"][0]["planning"]["budget"]["uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["rationale"],
            actual_result=fs_release["releases"][0]["planning"]["rationale"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(is_it_uuid(fs_release["releases"][0]["relatedProcesses"][0]["id"], 1))
        )
        assert compare_actual_result_and_expected_result(
            expected_result="parent",
            actual_result=fs_release["releases"][0]["relatedProcesses"][0]["relationship"][0]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="ocid",
            actual_result=fs_release["releases"][0]["relatedProcesses"][0]["scheme"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=cp_id,
            actual_result=fs_release["releases"][0]["relatedProcesses"][0]["identifier"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{cp_id}",
            actual_result=fs_release["releases"][0]["relatedProcesses"][0]["uri"]
        )


class TestCheckOnImpossibilityOfCreatingFsWithFullDataModelOwnMoneyOfPayloadIfObligatoryAttributesAreMissed(object):
    @pytestrail.case('27550')
    def test_delete_tender_27550_1(self, country, language, instance,
                                   cassandra_username,
                                   cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["tender"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.00.00.00", "description": "Data processing exception."}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_tender_procuring_entity_point_27550_2(self, country, language, instance,
                                                          cassandra_username,
                                                          cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["tender"]["procuringEntity"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com."
                                                 "procurement.budget.model.dto.fs.request.TenderFsCreate] "
                                                 "value failed for JSON property procuringEntity due to "
                                                 "missing (therefore NULL) value for creator parameter "
                                                 "procuringEntity which is a non-nullable type\n at "
                                                 "[Source: UNKNOWN; line: -1, column: -1] (through "
                                                 "reference chain: com.procurement.budget.model.dto."
                                                 "fs.request.FsCreate[\"tender\"]->com.procurement.budget."
                                                 "model.dto.fs.request.TenderFsCreate[\"procuringEntity\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_tender_procuring_entity_name_27550_3(self, country, language, instance,
                                                         cassandra_username,
                                                         cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["tender"]["procuringEntity"]["name"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com."
                                                 "procurement.budget.model.dto.fs.OrganizationReferenceFs] "
                                                 "value failed for JSON property name due to missing (therefore "
                                                 "NULL) value for creator parameter name which is a non-"
                                                 "nullable type\n at [Source: UNKNOWN; line: -1, column: -1] "
                                                 "(through reference chain: com.procurement.budget.model.dto."
                                                 "fs.request.FsCreate[\"tender\"]->com.procurement.budget."
                                                 "model.dto.fs.request.TenderFsCreate[\"procuringEntity\"]->"
                                                 "com.procurement.budget.model.dto.fs.OrganizationReference"
                                                 "Fs[\"name\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_tender_procuring_entity_identifier_27550_4(self, country, language, instance,
                                                               cassandra_username,
                                                               cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["tender"]["procuringEntity"]["identifier"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str(
                [{"code": "400.10.00", "description": "com.fasterxml.jackson.module.kotlin.Missing"
                                                      "KotlinParameterException: Instantiation of "
                                                      "[simple type, class com.procurement.budget."
                                                      "model.dto.fs.OrganizationReferenceFs] value "
                                                      "failed for JSON property identifier due to "
                                                      "missing (therefore NULL) value for creator "
                                                      "parameter identifier which is a non-nullable "
                                                      "type\n at [Source: UNKNOWN; line: -1, "
                                                      "column: -1] (through reference chain: com."
                                                      "procurement.budget.model.dto.fs.request."
                                                      "FsCreate[\"tender\"]->com.procurement."
                                                      "budget.model.dto.fs.request.TenderFsCreate"
                                                      "[\"procuringEntity\"]->com.procurement."
                                                      "budget.model.dto.fs.OrganizationReference"
                                                      "Fs[\"identifier\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_tender_procuring_entity_identifier_scheme_27550_5(self, country, language, instance,
                                                                      cassandra_username,
                                                                      cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["tender"]["procuringEntity"]["identifier"]["scheme"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00", "description": "com.fasterxml.jackson.module.kotlin."
                                                                      "MissingKotlinParameterException: "
                                                                      "Instantiation of [simple type, class "
                                                                      "com.procurement.mdm.model.dto.data."
                                                                      "Identifier] value failed for JSON property "
                                                                      "scheme due to missing (therefore NULL) "
                                                                      "value for creator parameter scheme which "
                                                                      "is a non-nullable type\n at [Source: UNKNOWN; "
                                                                      "line: -1, column: -1] (through reference "
                                                                      "chain: com.procurement.mdm.model.dto.data."
                                                                      "FS[\"tender\"]->com.procurement.mdm.model."
                                                                      "dto.data.TenderFS[\"procuringEntity\"]->"
                                                                      "com.procurement.mdm.model.dto.data."
                                                                      "OrganizationReference[\"identifier\"]->"
                                                                      "com.procurement.mdm.model.dto.data."
                                                                      "Identifier[\"scheme\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_tender_procuring_entity_identifier_id_27550_6(self, country, language, instance,
                                                                  cassandra_username,
                                                                  cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["tender"]["procuringEntity"]["identifier"]["id"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str(
                [{"code": "400.20.00", "description": "com.fasterxml.jackson.module.kotlin.Missing"
                                                      "KotlinParameterException: Instantiation of "
                                                      "[simple type, class com.procurement.mdm.model."
                                                      "dto.data.Identifier] value failed for JSON "
                                                      "property id due to missing (therefore NULL) "
                                                      "value for creator parameter id which is a "
                                                      "non-nullable type\n at [Source: UNKNOWN; "
                                                      "line: -1, column: -1] (through reference "
                                                      "chain: com.procurement.mdm.model.dto.data."
                                                      "FS[\"tender\"]->com.procurement.mdm.model."
                                                      "dto.data.TenderFS[\"procuringEntity\"]->"
                                                      "com.procurement.mdm.model.dto.data."
                                                      "OrganizationReference[\"identifier\"]->"
                                                      "com.procurement.mdm.model.dto.data."
                                                      "Identifier[\"id\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_tender_procuring_entity_identifier_legal_name_27550_7(self, country, language, instance,
                                                                          cassandra_username,
                                                                          cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["tender"]["procuringEntity"]["identifier"]["legalName"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str(
                [{"code": "400.10.00", "description": "com.fasterxml.jackson.module.kotlin.Missing"
                                                      "KotlinParameterException: Instantiation of "
                                                      "[simple type, class com.procurement.budget."
                                                      "model.dto.ocds.Identifier] value failed for "
                                                      "JSON property legalName due to missing "
                                                      "(therefore NULL) value for creator parameter "
                                                      "legalName which is a non-nullable type\n at "
                                                      "[Source: UNKNOWN; line: -1, column: -1] "
                                                      "(through reference chain: com.procurement."
                                                      "budget.model.dto.fs.request.FsCreate"
                                                      "[\"tender\"]->com.procurement.budget.model."
                                                      "dto.fs.request.TenderFsCreate[\"procuring"
                                                      "Entity\"]->com.procurement.budget.model.dto."
                                                      "fs.OrganizationReferenceFs[\"identifier\"]->"
                                                      "com.procurement.budget.model.dto.ocds."
                                                      "Identifier[\"legalName\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_tender_procuring_entity_additional_identifiers_scheme_27550_8(self, country, language,
                                                                                  instance,
                                                                                  cassandra_username,
                                                                                  cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["scheme"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.Identifier] value failed for JSON property "
                                                 "scheme due to missing (therefore NULL) value for creator "
                                                 "parameter scheme which is a non-nullable type\n at [Source: "
                                                 "UNKNOWN; line: -1, column: -1] (through reference chain: "
                                                 "com.procurement.mdm.model.dto.data.FS[\"tender\"]->com."
                                                 "procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]->"
                                                 "com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"additionalIdentifiers\"]->java.util.ArrayList[0]->com."
                                                 "procurement.mdm.model.dto.data.Identifier[\"scheme\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_tender_procuring_entity_additional_identifiers_id_27550_9(self, country, language, instance,
                                                                              cassandra_username,
                                                                              cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["id"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.Identifier] value failed for JSON property id "
                                                 "due to missing (therefore NULL) value for creator parameter id "
                                                 "which is a non-nullable type\n at [Source: UNKNOWN; line: -1, "
                                                 "column: -1] (through reference chain: com.procurement.mdm.model."
                                                 "dto.data.FS[\"tender\"]->com.procurement.mdm.model.dto.data."
                                                 "TenderFS[\"procuringEntity\"]->com.procurement.mdm.model.dto."
                                                 "data.OrganizationReference[\"additionalIdentifiers\"]->java.util."
                                                 "ArrayList[0]->com.procurement.mdm.model.dto.data."
                                                 "Identifier[\"id\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_tender_procuring_entity_additional_identifiers_legal_name_27550_10(self, country, language,
                                                                                       instance,
                                                                                       cassandra_username,
                                                                                       cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["legalName"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "budget.model.dto.ocds.Identifier] value failed for JSON property "
                                                 "legalName due to missing (therefore NULL) value for creator "
                                                 "parameter legalName which is a non-nullable type\n at [Source: "
                                                 "UNKNOWN; line: -1, column: -1] (through reference chain: com."
                                                 "procurement.budget.model.dto.fs.request.FsCreate[\"tender\"]->"
                                                 "com.procurement.budget.model.dto.fs.request.TenderFsCreate"
                                                 "[\"procuringEntity\"]->com.procurement.budget.model.dto.fs."
                                                 "OrganizationReferenceFs[\"additionalIdentifiers\"]->java.util."
                                                 "ArrayList[0]->com.procurement.budget.model.dto.ocds."
                                                 "Identifier[\"legalName\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_tender_procuring_entity_address_street_address_27550_11(self, country, language,
                                                                            instance,
                                                                            cassandra_username,
                                                                            cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["tender"]["procuringEntity"]["address"]["streetAddress"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.Address] value failed for JSON property "
                                                 "streetAddress due to missing (therefore NULL) value for creator "
                                                 "parameter streetAddress which is a non-nullable type\n at "
                                                 "[Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"tender\"]->"
                                                 "com.procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]->"
                                                 "com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"address\"]->com.procurement.mdm.model.dto.data.Address"
                                                 "[\"streetAddress\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_tender_procuring_entity_address_address_details_27550_12(self, country, language,
                                                                             instance,
                                                                             cassandra_username,
                                                                             cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["tender"]["procuringEntity"]["address"]["addressDetails"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.Address] value failed for JSON property "
                                                 "addressDetails due to missing (therefore NULL) value for "
                                                 "creator parameter addressDetails which is a non-nullable "
                                                 "type\n at [Source: UNKNOWN; line: -1, column: -1] (through "
                                                 "reference chain: com.procurement.mdm.model.dto.data.FS"
                                                 "[\"tender\"]->com.procurement.mdm.model.dto.data.TenderFS"
                                                 "[\"procuringEntity\"]->com.procurement.mdm.model.dto.data."
                                                 "OrganizationReference[\"address\"]->com.procurement.mdm.model."
                                                 "dto.data.Address[\"addressDetails\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_tender_procuring_entity_address_address_details_country_27550_13(self, country, language,
                                                                                     instance,
                                                                                     cassandra_username,
                                                                                     cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com."
                                                 "procurement.mdm.model.dto.data.AddressDetails] value failed "
                                                 "for JSON property country due to missing (therefore NULL) value "
                                                 "for creator parameter country which is a non-nullable type\n "
                                                 "at [Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"tender\"]->com."
                                                 "procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]->"
                                                 "com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"address\"]->com.procurement.mdm.model.dto.data.Address"
                                                 "[\"addressDetails\"]->com.procurement.mdm.model.dto.data."
                                                 "AddressDetails[\"country\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_tender_procuring_entity_address_address_details_country_id_27550_14(self, country, language,
                                                                                        instance,
                                                                                        cassandra_username,
                                                                                        cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]["id"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.CountryDetails] value failed for JSON "
                                                 "property id due to missing (therefore NULL) value for creator "
                                                 "parameter id which is a non-nullable type\n at [Source: "
                                                 "UNKNOWN; line: -1, column: -1] (through reference chain: "
                                                 "com.procurement.mdm.model.dto.data.FS[\"tender\"]->com."
                                                 "procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]"
                                                 "->com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"address\"]->com.procurement.mdm.model.dto.data.Address"
                                                 "[\"addressDetails\"]->com.procurement.mdm.model.dto.data."
                                                 "AddressDetails[\"country\"]->com.procurement.mdm.model.dto."
                                                 "data.CountryDetails[\"id\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_tender_procuring_entity_address_address_details_region_27550_15(self, country, language,
                                                                                    instance,
                                                                                    cassandra_username,
                                                                                    cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.AddressDetails] value failed for JSON "
                                                 "property region due to missing (therefore NULL) value for "
                                                 "creator parameter region which is a non-nullable type\n at "
                                                 "[Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"tender\"]->com."
                                                 "procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]->"
                                                 "com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"address\"]->com.procurement.mdm.model.dto.data.Address"
                                                 "[\"addressDetails\"]->com.procurement.mdm.model.dto.data."
                                                 "AddressDetails[\"region\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_tender_procuring_entity_address_address_details_region_id_27550_16(self, country, language,
                                                                                       instance,
                                                                                       cassandra_username,
                                                                                       cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.RegionDetails] value failed for JSON property "
                                                 "id due to missing (therefore NULL) value for creator parameter "
                                                 "id which is a non-nullable type\n at [Source: UNKNOWN; line: "
                                                 "-1, column: -1] (through reference chain: com.procurement.mdm."
                                                 "model.dto.data.FS[\"tender\"]->com.procurement.mdm.model.dto."
                                                 "data.TenderFS[\"procuringEntity\"]->com.procurement.mdm.model."
                                                 "dto.data.OrganizationReference[\"address\"]->com.procurement."
                                                 "mdm.model.dto.data.Address[\"addressDetails\"]->com.procurement."
                                                 "mdm.model.dto.data.AddressDetails[\"region\"]->com.procurement."
                                                 "mdm.model.dto.data.RegionDetails[\"id\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_tender_procuring_entity_address_address_details_locality_27550_17(self, country, language,
                                                                                      instance,
                                                                                      cassandra_username,
                                                                                      cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.AddressDetails] value failed for JSON "
                                                 "property locality due to missing (therefore NULL) value for "
                                                 "creator parameter locality which is a non-nullable type\n at "
                                                 "[Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"tender\"]->"
                                                 "com.procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]"
                                                 "->com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"address\"]->com.procurement.mdm.model.dto.data.Address"
                                                 "[\"addressDetails\"]->com.procurement.mdm.model.dto.data."
                                                 "AddressDetails[\"locality\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_tender_procuring_entity_address_address_details_locality_id_27550_18(self, country,
                                                                                         language,
                                                                                         instance,
                                                                                         cassandra_username,
                                                                                         cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["id"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.LocalityDetails] value failed for JSON "
                                                 "property id due to missing (therefore NULL) value for creator "
                                                 "parameter id which is a non-nullable type\n at [Source: "
                                                 "UNKNOWN; line: -1, column: -1] (through reference chain: "
                                                 "com.procurement.mdm.model.dto.data.FS[\"tender\"]->com."
                                                 "procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]->"
                                                 "com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"address\"]->com.procurement.mdm.model.dto.data.Address"
                                                 "[\"addressDetails\"]->com.procurement.mdm.model.dto.data."
                                                 "AddressDetails[\"locality\"]->com.procurement.mdm.model.dto."
                                                 "data.LocalityDetails[\"id\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_tender_procuring_entity_address_address_details_locality_scheme_27550_19(self, country,
                                                                                             language,
                                                                                             instance,
                                                                                             cassandra_username,
                                                                                             cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["scheme"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.LocalityDetails] value failed for JSON "
                                                 "property scheme due to missing (therefore NULL) value for "
                                                 "creator parameter scheme which is a non-nullable type\n at "
                                                 "[Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"tender\"]->"
                                                 "com.procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]"
                                                 "->com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"address\"]->com.procurement.mdm.model.dto.data.Address"
                                                 "[\"addressDetails\"]->com.procurement.mdm.model.dto.data."
                                                 "AddressDetails[\"locality\"]->com.procurement.mdm.model.dto."
                                                 "data.LocalityDetails[\"scheme\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_tender_procuring_entity_address_address_details_locality_description_27550_20(self, country,
                                                                                                  language,
                                                                                                  instance,
                                                                                                  cassandra_username,
                                                                                                  cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["description"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.LocalityDetails] value failed for JSON "
                                                 "property description due to missing (therefore NULL) value for "
                                                 "creator parameter description which is a non-nullable type\n "
                                                 "at [Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"tender\"]->com."
                                                 "procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]->"
                                                 "com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"address\"]->com.procurement.mdm.model.dto.data.Address"
                                                 "[\"addressDetails\"]->com.procurement.mdm.model.dto.data."
                                                 "AddressDetails[\"locality\"]->com.procurement.mdm.model.dto."
                                                 "data.LocalityDetails[\"description\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_tender_procuring_entity_contact_point_27550_21(self, country, language,
                                                                   instance,
                                                                   cassandra_username,
                                                                   cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["tender"]["procuringEntity"]["contactPoint"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com."
                                                 "procurement.budget.model.dto.fs.OrganizationReferenceFs] "
                                                 "value failed for JSON property contactPoint due to missing "
                                                 "(therefore NULL) value for creator parameter contactPoint "
                                                 "which is a non-nullable type\n at [Source: UNKNOWN; line: "
                                                 "-1, column: -1] (through reference chain: com.procurement."
                                                 "budget.model.dto.fs.request.FsCreate[\"tender\"]->com."
                                                 "procurement.budget.model.dto.fs.request.TenderFsCreate"
                                                 "[\"procuringEntity\"]->com.procurement.budget.model.dto.fs."
                                                 "OrganizationReferenceFs[\"contactPoint\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_tender_procuring_entity_contact_point_name_27550_22(self, country, language,
                                                                        instance,
                                                                        cassandra_username,
                                                                        cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["tender"]["procuringEntity"]["contactPoint"]["name"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.ContactPoint] value failed for JSON property "
                                                 "name due to missing (therefore NULL) value for creator parameter "
                                                 "name which is a non-nullable type\n at [Source: UNKNOWN; line: "
                                                 "-1, column: -1] (through reference chain: com.procurement.mdm."
                                                 "model.dto.data.FS[\"tender\"]->com.procurement.mdm.model.dto."
                                                 "data.TenderFS[\"procuringEntity\"]->com.procurement.mdm.model."
                                                 "dto.data.OrganizationReference[\"contactPoint\"]->com.procurement."
                                                 "mdm.model.dto.data.ContactPoint[\"name\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_tender_procuring_entity_contact_point_email_27550_23(self, country, language,
                                                                         instance,
                                                                         cassandra_username,
                                                                         cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["tender"]["procuringEntity"]["contactPoint"]["email"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.ContactPoint] value failed for JSON property "
                                                 "email due to missing (therefore NULL) value for creator parameter "
                                                 "email which is a non-nullable type\n at [Source: UNKNOWN; line: "
                                                 "-1, column: -1] (through reference chain: com.procurement.mdm."
                                                 "model.dto.data.FS[\"tender\"]->com.procurement.mdm.model.dto."
                                                 "data.TenderFS[\"procuringEntity\"]->com.procurement.mdm.model."
                                                 "dto.data.OrganizationReference[\"contactPoint\"]->com."
                                                 "procurement.mdm.model.dto.data.ContactPoint[\"email\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_tender_procuring_entity_contact_point_telephone_27550_24(self, country, language,
                                                                             instance,
                                                                             cassandra_username,
                                                                             cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["tender"]["procuringEntity"]["contactPoint"]["telephone"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.ContactPoint] value failed for JSON property "
                                                 "telephone due to missing (therefore NULL) value for creator "
                                                 "parameter telephone which is a non-nullable type\n at [Source: "
                                                 "UNKNOWN; line: -1, column: -1] (through reference chain: com."
                                                 "procurement.mdm.model.dto.data.FS[\"tender\"]->com.procurement."
                                                 "mdm.model.dto.data.TenderFS[\"procuringEntity\"]->com.procurement."
                                                 "mdm.model.dto.data.OrganizationReference[\"contactPoint\"]->"
                                                 "com.procurement.mdm.model.dto.data.ContactPoint[\"telephone\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_planning_27550_25(self, country, language, instance, cassandra_username,
                                      cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["planning"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.00.00.00", "description": "Data processing exception."}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_planning_budget_27550_26(self, country, language, instance, cassandra_username,
                                             cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["planning"]["budget"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.00.00.00", "description": "Data processing exception."}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_planning_budget_period_27550_27(self, country, language, instance, cassandra_username,
                                                    cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["planning"]["budget"]["period"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "budget.model.dto.fs.request.BudgetFsCreate] value failed for "
                                                 "JSON property period due to missing (therefore NULL) value for "
                                                 "creator parameter period which is a non-nullable type\n at "
                                                 "[Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                 "chain: com.procurement.budget.model.dto.fs.request.FsCreate"
                                                 "[\"planning\"]->com.procurement.budget.model.dto.fs.request."
                                                 "PlanningFsCreate[\"budget\"]->com.procurement.budget.model.dto."
                                                 "fs.request.BudgetFsCreate[\"period\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_planning_budget_period_start_date_27550_28(self, country, language, instance,
                                                               cassandra_username,
                                                               cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["planning"]["budget"]["period"]["startDate"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "budget.model.dto.ocds.Period] value failed for JSON property "
                                                 "startDate due to missing (therefore NULL) value for creator "
                                                 "parameter startDate which is a non-nullable type\n at "
                                                 "[Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                 "chain: com.procurement.budget.model.dto.fs.request.FsCreate"
                                                 "[\"planning\"]->com.procurement.budget.model.dto.fs.request."
                                                 "PlanningFsCreate[\"budget\"]->com.procurement.budget.model.dto."
                                                 "fs.request.BudgetFsCreate[\"period\"]->com.procurement.budget."
                                                 "model.dto.ocds.Period[\"startDate\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_planning_budget_period_end_date_27550_29(self, country, language, instance,
                                                             cassandra_username,
                                                             cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["planning"]["budget"]["period"]["endDate"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com."
                                                 "procurement.budget.model.dto.ocds.Period] value failed for JSON "
                                                 "property endDate due to missing (therefore NULL) value for "
                                                 "creator parameter endDate which is a non-nullable type\n at "
                                                 "[Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                 "chain: com.procurement.budget.model.dto.fs.request.FsCreate"
                                                 "[\"planning\"]->com.procurement.budget.model.dto.fs.request."
                                                 "PlanningFsCreate[\"budget\"]->com.procurement.budget.model.dto."
                                                 "fs.request.BudgetFsCreate[\"period\"]->com.procurement.budget."
                                                 "model.dto.ocds.Period[\"endDate\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_planning_budget_amount_27550_30(self, country, language, instance, cassandra_username,
                                                    cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["planning"]["budget"]["amount"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.00.00.00", "description": "Data processing exception."}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_planning_budget_amount_amount_27550_31(self, country, language, instance,
                                                           cassandra_username,
                                                           cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["planning"]["budget"]["amount"]["amount"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com."
                                                 "procurement.budget.model.dto.ocds.Value] value failed for "
                                                 "JSON property amount due to missing (therefore NULL) value "
                                                 "for creator parameter amount which is a non-nullable type\n at "
                                                 "[Source: UNKNOWN; line: -1, column: -1] (through reference chain: "
                                                 "com.procurement.budget.model.dto.fs.request.FsCreate[\"planning\"]"
                                                 "->com.procurement.budget.model.dto.fs.request.PlanningFsCreate"
                                                 "[\"budget\"]->com.procurement.budget.model.dto.fs.request."
                                                 "BudgetFsCreate[\"amount\"]->com.procurement.budget.model.dto."
                                                 "ocds.Value[\"amount\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_planning_budget_amount_currency_27550_32(self, country, language, instance,
                                                             cassandra_username,
                                                             cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["planning"]["budget"]["amount"]["currency"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.ValueFS] value failed for JSON property "
                                                 "currency due to missing (therefore NULL) value for creator "
                                                 "parameter currency which is a non-nullable type\n at [Source: "
                                                 "UNKNOWN; line: -1, column: -1] (through reference chain: com."
                                                 "procurement.mdm.model.dto.data.FS[\"planning\"]->com.procurement."
                                                 "mdm.model.dto.data.PlanningFS[\"budget\"]->com.procurement.mdm."
                                                 "model.dto.data.BudgetFS[\"amount\"]->com.procurement.mdm.model."
                                                 "dto.data.ValueFS[\"currency\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_planning_budget_is_european_union_funded_27550_33(self, country, language, instance,
                                                                      cassandra_username,
                                                                      cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["planning"]["budget"]["isEuropeanUnionFunded"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com."
                                                 "procurement.budget.model.dto.fs.request.BudgetFsCreate] "
                                                 "value failed for JSON property isEuropeanUnionFunded due "
                                                 "to missing (therefore NULL) value for creator parameter "
                                                 "isEuropeanUnionFunded which is a non-nullable type\n at "
                                                 "[Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                 "chain: com.procurement.budget.model.dto.fs.request.FsCreate"
                                                 "[\"planning\"]->com.procurement.budget.model.dto.fs.request."
                                                 "PlanningFsCreate[\"budget\"]->com.procurement.budget.model."
                                                 "dto.fs.request.BudgetFsCreate[\"isEuropeanUnionFunded\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_planning_budget_european_union_funding_project_name_27550_34(self, country, language,
                                                                                 instance,
                                                                                 cassandra_username,
                                                                                 cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["planning"]["budget"]["europeanUnionFunding"]["projectName"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "budget.model.dto.ocds.EuropeanUnionFunding] value failed for "
                                                 "JSON property projectName due to missing (therefore NULL) value "
                                                 "for creator parameter projectName which is a non-nullable type\n "
                                                 "at [Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                 "chain: com.procurement.budget.model.dto.fs.request.FsCreate"
                                                 "[\"planning\"]->com.procurement.budget.model.dto.fs.request."
                                                 "PlanningFsCreate[\"budget\"]->com.procurement.budget.model.dto."
                                                 "fs.request.BudgetFsCreate[\"europeanUnionFunding\"]->com."
                                                 "procurement.budget.model.dto.ocds.EuropeanUnionFunding"
                                                 "[\"projectName\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_planning_budget_european_union_funding_project_identifier_27550_35(self, country, language,
                                                                                       instance,
                                                                                       cassandra_username,
                                                                                       cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["planning"]["budget"]["europeanUnionFunding"]["projectIdentifier"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "budget.model.dto.ocds.EuropeanUnionFunding] value failed for "
                                                 "JSON property projectIdentifier due to missing (therefore NULL) "
                                                 "value for creator parameter projectIdentifier which is a non-"
                                                 "nullable type\n at [Source: UNKNOWN; line: -1, column: -1] "
                                                 "(through reference chain: com.procurement.budget.model.dto.fs."
                                                 "request.FsCreate[\"planning\"]->com.procurement.budget.model.dto."
                                                 "fs.request.PlanningFsCreate[\"budget\"]->com.procurement.budget."
                                                 "model.dto.fs.request.BudgetFsCreate[\"europeanUnionFunding\"]->"
                                                 "com.procurement.budget.model.dto.ocds.EuropeanUnionFunding"
                                                 "[\"projectIdentifier\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_buyer_name_27550_36(self, country, language, instance, cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["buyer"]["name"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "budget.model.dto.fs.OrganizationReferenceFs] value failed for "
                                                 "JSON property name due to missing (therefore NULL) value for "
                                                 "creator parameter name which is a non-nullable type\n at "
                                                 "[Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                 "chain: com.procurement.budget.model.dto.fs.request.FsCreate"
                                                 "[\"buyer\"]->com.procurement.budget.model.dto.fs.Organization"
                                                 "ReferenceFs[\"name\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_buyer_identifier_27550_37(self, country, language, instance, cassandra_username,
                                              cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["buyer"]["identifier"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "budget.model.dto.fs.OrganizationReferenceFs] value failed for "
                                                 "JSON property identifier due to missing (therefore NULL) value "
                                                 "for creator parameter identifier which is a non-nullable type\n "
                                                 "at [Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                 "chain: com.procurement.budget.model.dto.fs.request.FsCreate"
                                                 "[\"buyer\"]->com.procurement.budget.model.dto.fs.Organization"
                                                 "ReferenceFs[\"identifier\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_buyer_identifier_id_27550_38(self, country, language, instance, cassandra_username,
                                                 cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["buyer"]["identifier"]["id"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.Identifier] value failed for JSON property id "
                                                 "due to missing (therefore NULL) value for creator parameter id "
                                                 "which is a non-nullable type\n at [Source: UNKNOWN; line: -1, "
                                                 "column: -1] (through reference chain: com.procurement.mdm.model."
                                                 "dto.data.FS[\"buyer\"]->com.procurement.mdm.model.dto.data."
                                                 "OrganizationReference[\"identifier\"]->com.procurement.mdm."
                                                 "model.dto.data.Identifier[\"id\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_buyer_identifier_scheme_27550_39(self, country, language, instance, cassandra_username,
                                                     cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["buyer"]["identifier"]["scheme"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.Identifier] value failed for JSON property "
                                                 "scheme due to missing (therefore NULL) value for creator "
                                                 "parameter scheme which is a non-nullable type\n at [Source: "
                                                 "UNKNOWN; line: -1, column: -1] (through reference chain: com."
                                                 "procurement.mdm.model.dto.data.FS[\"buyer\"]->com.procurement."
                                                 "mdm.model.dto.data.OrganizationReference[\"identifier\"]->com."
                                                 "procurement.mdm.model.dto.data.Identifier[\"scheme\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_buyer_identifier_legal_name_27550_40(self, country, language, instance, cassandra_username,
                                                         cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["buyer"]["identifier"]["legalName"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "budget.model.dto.ocds.Identifier] value failed for JSON property "
                                                 "legalName due to missing (therefore NULL) value for creator "
                                                 "parameter legalName which is a non-nullable type\n at [Source: "
                                                 "UNKNOWN; line: -1, column: -1] (through reference chain: com."
                                                 "procurement.budget.model.dto.fs.request.FsCreate[\"buyer\"]->"
                                                 "com.procurement.budget.model.dto.fs.OrganizationReferenceFs"
                                                 "[\"identifier\"]->com.procurement.budget.model.dto.ocds."
                                                 "Identifier[\"legalName\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_buyer_address_27550_41(self, country, language, instance, cassandra_username,
                                           cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["buyer"]["address"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "budget.model.dto.fs.OrganizationReferenceFs] value failed for "
                                                 "JSON property address due to missing (therefore NULL) value "
                                                 "for creator parameter address which is a non-nullable type\n "
                                                 "at [Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                 "chain: com.procurement.budget.model.dto.fs.request.FsCreate"
                                                 "[\"buyer\"]->com.procurement.budget.model.dto.fs.Organization"
                                                 "ReferenceFs[\"address\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_buyer_address_street_address_27550_42(self, country, language, instance, cassandra_username,
                                                          cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["buyer"]["address"]["streetAddress"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.Address] value failed for JSON property "
                                                 "streetAddress due to missing (therefore NULL) value for creator "
                                                 "parameter streetAddress which is a non-nullable type\n at "
                                                 "[Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"buyer\"]->com."
                                                 "procurement.mdm.model.dto.data.OrganizationReference[\"address\"]"
                                                 "->com.procurement.mdm.model.dto.data.Address[\"streetAddress\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_buyer_address_address_details_27550_43(self, country, language, instance, cassandra_username,
                                                           cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["buyer"]["address"]["addressDetails"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.Address] value failed for JSON property address"
                                                 "Details due to missing (therefore NULL) value for creator "
                                                 "parameter addressDetails which is a non-nullable type\n at "
                                                 "[Source: UNKNOWN; line: -1, column: -1] (through reference chain: "
                                                 "com.procurement.mdm.model.dto.data.FS[\"buyer\"]->com.procurement."
                                                 "mdm.model.dto.data.OrganizationReference[\"address\"]->com."
                                                 "procurement.mdm.model.dto.data.Address[\"addressDetails\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_buyer_address_address_details_country_27550_44(self, country, language, instance,
                                                                   cassandra_username,
                                                                   cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["buyer"]["address"]["addressDetails"]["country"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.AddressDetails] value failed for JSON property "
                                                 "country due to missing (therefore NULL) value for creator "
                                                 "parameter country which is a non-nullable type\n at [Source: "
                                                 "UNKNOWN; line: -1, column: -1] (through reference chain: com."
                                                 "procurement.mdm.model.dto.data.FS[\"buyer\"]->com.procurement."
                                                 "mdm.model.dto.data.OrganizationReference[\"address\"]->com."
                                                 "procurement.mdm.model.dto.data.Address[\"addressDetails\"]->"
                                                 "com.procurement.mdm.model.dto.data.AddressDetails[\"country\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_buyer_address_address_details_country_id_27550_45(self, country, language, instance,
                                                                      cassandra_username,
                                                                      cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["buyer"]["address"]["addressDetails"]["country"]["id"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.CountryDetails] value failed for JSON property "
                                                 "id due to missing (therefore NULL) value for creator parameter id "
                                                 "which is a non-nullable type\n at [Source: UNKNOWN; line: -1, "
                                                 "column: -1] (through reference chain: com.procurement.mdm.model."
                                                 "dto.data.FS[\"buyer\"]->com.procurement.mdm.model.dto.data."
                                                 "OrganizationReference[\"address\"]->com.procurement.mdm.model."
                                                 "dto.data.Address[\"addressDetails\"]->com.procurement.mdm.model."
                                                 "dto.data.AddressDetails[\"country\"]->com.procurement.mdm.model."
                                                 "dto.data.CountryDetails[\"id\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_buyer_address_address_details_region_27550_46(self, country, language, instance,
                                                                  cassandra_username,
                                                                  cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["buyer"]["address"]["addressDetails"]["region"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.AddressDetails] value failed for JSON property "
                                                 "region due to missing (therefore NULL) value for creator parameter "
                                                 "region which is a non-nullable type\n at [Source: UNKNOWN; line: "
                                                 "-1, column: -1] (through reference chain: com.procurement.mdm."
                                                 "model.dto.data.FS[\"buyer\"]->com.procurement.mdm.model.dto.data."
                                                 "OrganizationReference[\"address\"]->com.procurement.mdm.model."
                                                 "dto.data.Address[\"addressDetails\"]->com.procurement.mdm.model."
                                                 "dto.data.AddressDetails[\"region\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_buyer_address_address_details_region_id_27550_47(self, country, language, instance,
                                                                     cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["buyer"]["address"]["addressDetails"]["region"]["id"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.RegionDetails] value failed for JSON property "
                                                 "id due to missing (therefore NULL) value for creator parameter id "
                                                 "which is a non-nullable type\n at [Source: UNKNOWN; line: -1, "
                                                 "column: -1] (through reference chain: com.procurement.mdm.model."
                                                 "dto.data.FS[\"buyer\"]->com.procurement.mdm.model.dto.data."
                                                 "OrganizationReference[\"address\"]->com.procurement.mdm.model."
                                                 "dto.data.Address[\"addressDetails\"]->com.procurement.mdm.model."
                                                 "dto.data.AddressDetails[\"region\"]->com.procurement.mdm.model."
                                                 "dto.data.RegionDetails[\"id\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_buyer_address_address_details_locality_27550_48(self, country, language, instance,
                                                                    cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["buyer"]["address"]["addressDetails"]["locality"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.AddressDetails] value failed for JSON property "
                                                 "locality due to missing (therefore NULL) value for creator "
                                                 "parameter locality which is a non-nullable type\n at [Source: "
                                                 "UNKNOWN; line: -1, column: -1] (through reference chain: com."
                                                 "procurement.mdm.model.dto.data.FS[\"buyer\"]->com.procurement."
                                                 "mdm.model.dto.data.OrganizationReference[\"address\"]->com."
                                                 "procurement.mdm.model.dto.data.Address[\"addressDetails\"]->com."
                                                 "procurement.mdm.model.dto.data.AddressDetails[\"locality\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_buyer_address_address_details_locality_scheme_27550_49(self, country, language, instance,
                                                                           cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.LocalityDetails] value failed for JSON "
                                                 "property scheme due to missing (therefore NULL) value for "
                                                 "creator parameter scheme which is a non-nullable type\n at "
                                                 "[Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"buyer\"]->com."
                                                 "procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"address\"]->com.procurement.mdm.model.dto.data.Address"
                                                 "[\"addressDetails\"]->com.procurement.mdm.model.dto.data."
                                                 "AddressDetails[\"locality\"]->com.procurement.mdm.model.dto."
                                                 "data.LocalityDetails[\"scheme\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_buyer_address_address_details_locality_id_27550_50(self, country, language, instance,
                                                                       cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["buyer"]["address"]["addressDetails"]["locality"]["id"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.LocalityDetails] value failed for JSON "
                                                 "property id due to missing (therefore NULL) value for creator "
                                                 "parameter id which is a non-nullable type\n at [Source: UNKNOWN; "
                                                 "line: -1, column: -1] (through reference chain: com.procurement."
                                                 "mdm.model.dto.data.FS[\"buyer\"]->com.procurement.mdm.model.dto."
                                                 "data.OrganizationReference[\"address\"]->com.procurement.mdm."
                                                 "model.dto.data.Address[\"addressDetails\"]->com.procurement.mdm."
                                                 "model.dto.data.AddressDetails[\"locality\"]->com.procurement.mdm."
                                                 "model.dto.data.LocalityDetails[\"id\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_buyer_address_address_details_locality_description_27550_51(self, country, language, instance,
                                                                                cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["buyer"]["address"]["addressDetails"]["locality"]["description"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.LocalityDetails] value failed for JSON "
                                                 "property description due to missing (therefore NULL) value for "
                                                 "creator parameter description which is a non-nullable type\n at "
                                                 "[Source: UNKNOWN; line: -1, column: -1] (through reference chain: "
                                                 "com.procurement.mdm.model.dto.data.FS[\"buyer\"]->com.procurement."
                                                 "mdm.model.dto.data.OrganizationReference[\"address\"]->com."
                                                 "procurement.mdm.model.dto.data.Address[\"addressDetails\"]->"
                                                 "com.procurement.mdm.model.dto.data.AddressDetails[\"locality\"]->"
                                                 "com.procurement.mdm.model.dto.data.LocalityDetails"
                                                 "[\"description\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_buyer_additional_identifiers_id_27550_52(self, country, language, instance,
                                                             cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["buyer"]["additionalIdentifiers"][0]["id"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.Identifier] value failed for JSON property "
                                                 "id due to missing (therefore NULL) value for creator parameter "
                                                 "id which is a non-nullable type\n at [Source: UNKNOWN; line: -1, "
                                                 "column: -1] (through reference chain: com.procurement.mdm.model."
                                                 "dto.data.FS[\"buyer\"]->com.procurement.mdm.model.dto.data."
                                                 "OrganizationReference[\"additionalIdentifiers\"]->java.util."
                                                 "ArrayList[0]->com.procurement.mdm.model.dto.data.Identifier"
                                                 "[\"id\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_buyer_additional_identifiers_scheme_27550_53(self, country, language, instance,
                                                                 cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["buyer"]["additionalIdentifiers"][0]["scheme"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.Identifier] value failed for JSON property "
                                                 "scheme due to missing (therefore NULL) value for creator parameter "
                                                 "scheme which is a non-nullable type\n at [Source: UNKNOWN; line: "
                                                 "-1, column: -1] (through reference chain: com.procurement.mdm."
                                                 "model.dto.data.FS[\"buyer\"]->com.procurement.mdm.model.dto.data."
                                                 "OrganizationReference[\"additionalIdentifiers\"]->java.util."
                                                 "ArrayList[0]->com.procurement.mdm.model.dto.data.Identifier"
                                                 "[\"scheme\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_buyer_additional_identifiers_legal_name_27550_54(self, country, language, instance,
                                                                     cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["buyer"]["additionalIdentifiers"][0]["legalName"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "budget.model.dto.ocds.Identifier] value failed for JSON property "
                                                 "legalName due to missing (therefore NULL) value for creator "
                                                 "parameter legalName which is a non-nullable type\n at [Source: "
                                                 "UNKNOWN; line: -1, column: -1] (through reference chain: com."
                                                 "procurement.budget.model.dto.fs.request.FsCreate[\"buyer\"]->"
                                                 "com.procurement.budget.model.dto.fs.OrganizationReferenceFs"
                                                 "[\"additionalIdentifiers\"]->java.util.ArrayList[0]->com."
                                                 "procurement.budget.model.dto.ocds.Identifier[\"legalName\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_buyer_contact_point_27550_55(self, country, language, instance, cassandra_username,
                                                 cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["buyer"]["contactPoint"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "budget.model.dto.fs.OrganizationReferenceFs] value failed for "
                                                 "JSON property contactPoint due to missing (therefore NULL) value "
                                                 "for creator parameter contactPoint which is a non-nullable type\n "
                                                 "at [Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                 "chain: com.procurement.budget.model.dto.fs.request.FsCreate"
                                                 "[\"buyer\"]->com.procurement.budget.model.dto.fs.Organization"
                                                 "ReferenceFs[\"contactPoint\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_buyer_contact_point_name_27550_56(self, country, language, instance, cassandra_username,
                                                      cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["buyer"]["contactPoint"]["name"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.ContactPoint] value failed for JSON property "
                                                 "name due to missing (therefore NULL) value for creator parameter "
                                                 "name which is a non-nullable type\n at [Source: UNKNOWN; line: -1, "
                                                 "column: -1] (through reference chain: com.procurement.mdm.model."
                                                 "dto.data.FS[\"buyer\"]->com.procurement.mdm.model.dto.data."
                                                 "OrganizationReference[\"contactPoint\"]->com.procurement.mdm."
                                                 "model.dto.data.ContactPoint[\"name\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_buyer_contact_point_email_27550_57(self, country, language, instance, cassandra_username,
                                                       cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["buyer"]["contactPoint"]["email"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.ContactPoint] value failed for JSON property "
                                                 "email due to missing (therefore NULL) value for creator parameter "
                                                 "email which is a non-nullable type\n at [Source: UNKNOWN; line: "
                                                 "-1, column: -1] (through reference chain: com.procurement.mdm."
                                                 "model.dto.data.FS[\"buyer\"]->com.procurement.mdm.model.dto.data."
                                                 "OrganizationReference[\"contactPoint\"]->com.procurement.mdm.model."
                                                 "dto.data.ContactPoint[\"email\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27550')
    def test_delete_buyer_contact_point_telephone_27550_58(self, country, language, instance, cassandra_username,
                                                           cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        del payload["buyer"]["contactPoint"]["telephone"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.ContactPoint] value failed for JSON property "
                                                 "telephone due to missing (therefore NULL) value for creator "
                                                 "parameter telephone which is a non-nullable type\n at [Source: "
                                                 "UNKNOWN; line: -1, column: -1] (through reference chain: com."
                                                 "procurement.mdm.model.dto.data.FS[\"buyer\"]->com.procurement."
                                                 "mdm.model.dto.data.OrganizationReference[\"contactPoint\"]->com."
                                                 "procurement.mdm.model.dto.data.ContactPoint[\"telephone\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )


class TestCheckOnPossibilityOfCreatingFsWithObligatoryDataModelOwnMoney(object):
    @pytestrail.case("27551")
    def test_send_the_request_27551_1(self, country, language, instance, cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_obligatory_data_model_own_money)
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )

    @pytestrail.case("27551")
    def test_see_the_result_in_feed_point_point_27551_2(self, country, language, instance, cassandra_username,
                                                        cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_obligatory_data_model_own_money)
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(fs.check_on_that_message_is_successfully_create_fs())
        )

    @pytestrail.case('27551')
    def test_check_on_correctness_of_publishing_fs_release_on_public_point_27551_3(self, country, language,
                                                                                   instance, cassandra_username,
                                                                                   cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_obligatory_data_model_own_money)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = \
            payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]["id"]
        payload["buyer"]["address"]["addressDetails"]["region"]["id"] = \
            payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"]
        payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = \
            payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["id"]
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        ei = fs.insert_ei_full_data_model(cp_id, ei_token)
        if "buyer" in payload.keys():
            buyer_in_payload = True
            source_entity_id = payload["buyer"]["identifier"]["scheme"] + "-" + payload["buyer"]["identifier"][
                "id"]
            source_entity_name = payload["buyer"]["name"]
            status = "active"
        else:
            buyer_in_payload = False
            status = "planning"
            ei_release = requests.get(
                url=ei[0] + "/" + ei[2]
            ).json()
            source_entity_id = ei_release["releases"][0]["buyer"]["id"]
            source_entity_name = ei_release["releases"][0]["buyer"]["name"]
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        mdm = MdmService(
            instance="dev",
            lang="ro",
            country=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]["id"],
            region=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"],
            locality=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["id"]
        )
        data = mdm.process_fs_data(cp_id).json()
        country_from_mdm = data["data"]["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]
        region_from_mdm = data["data"]["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]
        locality_from_mdm = data["data"]["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]
        url_create = message_from_kafka['data']['url'] + '/' + message_from_kafka['data']['outcomes']['fs'][0][
            'id']
        fs_release = requests.get(url=url_create).json()
        fs_release_timestamp = int(fs_release["releases"][0]["id"][46:59])
        convert_timestamp_to_date = get_human_date_in_utc_format(fs_release_timestamp)
        roles_list = list()
        for f in fs_release["releases"][0]["parties"]:
            if f["roles"] == ["payer"]:
                roles_list.append(f)
            if f["roles"] == ["funder"]:
                roles_list.append(f)
        keys_list = list()
        for i in fs_release.keys():
            if i == "uri":
                keys_list.append(i)
            if i == "version":
                keys_list.append(i)
            if i == "extensions":
                keys_list.append(i)
            if i == "publisher":
                keys_list.append(i)
            if i == "license":
                keys_list.append(i)
            if i == "publicationPolicy":
                keys_list.append(i)
            if i == "publishedDate":
                keys_list.append(i)
            if i == "releases":
                keys_list.append(i)
        for i in fs_release["publisher"].keys():
            if i == "name":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_release["releases"][0].keys():
            if i == "ocid":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "date":
                keys_list.append(i)
            if i == "tag":
                keys_list.append(i)
            if i == "initiationType":
                keys_list.append(i)
            if i == "tender":
                keys_list.append(i)
            if i == "parties":
                keys_list.append(i)
            if i == "planning":
                keys_list.append(i)
            if i == "relatedProcesses":
                keys_list.append(i)
        for i in fs_release["releases"][0]["tender"].keys():
            if i == "id":
                keys_list.append(i)
            if i == "status":
                keys_list.append(i)
            if i == "statusDetails":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][0].keys():
            if i == "id":
                keys_list.append(i)
            if i == "name":
                keys_list.append(i)
            if i == "identifier":
                keys_list.append(i)
            if i == "address":
                keys_list.append(i)
            if i == "contactPoint":
                keys_list.append(i)
            if i == "roles":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][0]["identifier"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "legalName":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][0]["address"].keys():
            if i == "streetAddress":
                keys_list.append(i)
            if i == "addressDetails":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][0]["address"]["addressDetails"].keys():
            if i == "country":
                keys_list.append(i)
            if i == "region":
                keys_list.append(i)
            if i == "locality":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][0]["contactPoint"].keys():
            if i == "name":
                keys_list.append(i)
            if i == "email":
                keys_list.append(i)
            if i == "telephone":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][1].keys():
            if i == "id":
                keys_list.append(i)
            if i == "name":
                keys_list.append(i)
            if i == "identifier":
                keys_list.append(i)
            if i == "address":
                keys_list.append(i)
            if i == "contactPoint":
                keys_list.append(i)
            if i == "roles":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][1]["identifier"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "legalName":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][1]["address"].keys():
            if i == "streetAddress":
                keys_list.append(i)
            if i == "addressDetails":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][1]["address"]["addressDetails"].keys():
            if i == "country":
                keys_list.append(i)
            if i == "region":
                keys_list.append(i)
            if i == "locality":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][1]["address"]["addressDetails"]["country"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][1]["address"]["addressDetails"]["region"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][1]["address"]["addressDetails"]["locality"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_release["releases"][0]["parties"][1]["contactPoint"].keys():
            if i == "name":
                keys_list.append(i)
            if i == "email":
                keys_list.append(i)
            if i == "telephone":
                keys_list.append(i)
        for i in fs_release["releases"][0]["planning"].keys():
            if i == "budget":
                keys_list.append(i)
        for i in fs_release["releases"][0]["planning"]["budget"].keys():
            if i == "period":
                keys_list.append(i)
            if i == "amount":
                keys_list.append(i)
            if i == "isEuropeanUnionFunded":
                keys_list.append(i)
            if i == "verified":
                keys_list.append(i)
            if i == "sourceEntity":
                keys_list.append(i)
        for i in fs_release["releases"][0]["planning"]["budget"]["period"].keys():
            if i == "startDate":
                keys_list.append(i)
            if i == "endDate":
                keys_list.append(i)
        for i in fs_release["releases"][0]["planning"]["budget"]["amount"].keys():
            if i == "amount":
                keys_list.append(i)
            if i == "currency":
                keys_list.append(i)
        for i in fs_release["releases"][0]["planning"]["budget"]["sourceEntity"].keys():
            if i == "id":
                keys_list.append(i)
            if i == "name":
                keys_list.append(i)
        for i in fs_release["releases"][0]["relatedProcesses"][0].keys():
            if i == "id":
                keys_list.append(i)
            if i == "relationship":
                keys_list.append(i)
            if i == "scheme":
                keys_list.append(i)
            if i == "identifier":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        procuring_entity_scheme = payload["tender"]["procuringEntity"]["identifier"]["scheme"]
        procuring_entity_id = payload["tender"]["procuringEntity"]["identifier"]["id"]
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[0]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="version",
            actual_result=keys_list[1]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="extensions",
            actual_result=keys_list[2]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="publisher",
            actual_result=keys_list[3]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="license",
            actual_result=keys_list[4]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="publicationPolicy",
            actual_result=keys_list[5]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="publishedDate",
            actual_result=keys_list[6]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="releases",
            actual_result=keys_list[7]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="name",
            actual_result=keys_list[8]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[9]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="ocid",
            actual_result=keys_list[10]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[11]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="date",
            actual_result=keys_list[12]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="tag",
            actual_result=keys_list[13]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="initiationType",
            actual_result=keys_list[14]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="tender",
            actual_result=keys_list[15]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="parties",
            actual_result=keys_list[16]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="planning",
            actual_result=keys_list[17])
        assert compare_actual_result_and_expected_result(
            expected_result="relatedProcesses",
            actual_result=keys_list[18]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[19]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="status",
            actual_result=keys_list[20]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="statusDetails",
            actual_result=keys_list[21]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[22]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="name",
            actual_result=keys_list[23]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="identifier",
            actual_result=keys_list[24]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="address",
            actual_result=keys_list[25]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="contactPoint",
            actual_result=keys_list[26]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="roles",
            actual_result=keys_list[27]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="scheme",
            actual_result=keys_list[28]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[29]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="legalName",
            actual_result=keys_list[30]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="streetAddress",
            actual_result=keys_list[31]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="addressDetails",
            actual_result=keys_list[32]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="country",
            actual_result=keys_list[33]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="region",
            actual_result=keys_list[34]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="locality",
            actual_result=keys_list[35]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="scheme",
            actual_result=keys_list[36]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[37]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="description",
            actual_result=keys_list[38]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[39]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="scheme",
            actual_result=keys_list[40]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[41]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="description",
            actual_result=keys_list[42]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[43]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="scheme",
            actual_result=keys_list[44]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[45]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="description",
            actual_result=keys_list[46]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[47]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="name",
            actual_result=keys_list[48]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="email",
            actual_result=keys_list[49]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="telephone",
            actual_result=keys_list[50]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[51]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="name",
            actual_result=keys_list[52]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="identifier",
            actual_result=keys_list[53]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="address",
            actual_result=keys_list[54]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="contactPoint",
            actual_result=keys_list[55]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="roles",
            actual_result=keys_list[56]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="scheme",
            actual_result=keys_list[57]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[58]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="legalName",
            actual_result=keys_list[59]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="streetAddress",
            actual_result=keys_list[60]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="addressDetails",
            actual_result=keys_list[61]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="country",
            actual_result=keys_list[62]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="region",
            actual_result=keys_list[63]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="locality",
            actual_result=keys_list[64]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="scheme",
            actual_result=keys_list[65]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[66]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="description",
            actual_result=keys_list[67]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[68]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="scheme",
            actual_result=keys_list[69]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[70]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="description",
            actual_result=keys_list[71]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[72]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="scheme",
            actual_result=keys_list[73]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[74]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="description",
            actual_result=keys_list[75]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[76]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="name",
            actual_result=keys_list[77]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="email",
            actual_result=keys_list[78]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="telephone",
            actual_result=keys_list[79]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="budget",
            actual_result=keys_list[80]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="period",
            actual_result=keys_list[81]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="amount",
            actual_result=keys_list[82]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="isEuropeanUnionFunded",
            actual_result=keys_list[83]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="verified",
            actual_result=keys_list[84]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="sourceEntity",
            actual_result=keys_list[85]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="startDate",
            actual_result=keys_list[86]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="endDate",
            actual_result=keys_list[87]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="amount",
            actual_result=keys_list[88]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="currency",
            actual_result=keys_list[89]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[90]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="name",
            actual_result=keys_list[91]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="id",
            actual_result=keys_list[92]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="relationship",
            actual_result=keys_list[93]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="scheme",
            actual_result=keys_list[94]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="identifier",
            actual_result=keys_list[95]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[96]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=f"http://dev.public.eprocurement.systems/budgets/{message_from_kafka['data']['ocid']}/"
                            f"{message_from_kafka['data']['outcomes']['fs'][0]['id']}",
            actual_result=fs_release["uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="666",
            actual_result=fs_release["version"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="https://raw.githubusercontent.com/open-contracting/ocds_bid_extension/v1.1.1/"
                            "extension.json",
            actual_result=fs_release["extensions"][0]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="https://raw.githubusercontent.com/open-contracting/ocds_enquiry_extension/v1.1.1/"
                            "extension.js222",
            actual_result=fs_release["extensions"][1]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=instance.upper() + "-ENV",
            actual_result=fs_release["publisher"]["name"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="https://www.ustudio.com",
            actual_result=fs_release["publisher"]["uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="http://opendefinition.org/licenses/222",
            actual_result=fs_release["license"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="http://opendefinition.org/licenses/222",
            actual_result=fs_release["publicationPolicy"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=message_from_kafka["data"]["operationDate"],
            actual_result=fs_release["publishedDate"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=message_from_kafka['data']['outcomes']['fs'][0]['id'],
            actual_result=fs_release["releases"][0]["ocid"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=message_from_kafka['data']['outcomes']['fs'][0]['id'],
            actual_result=fs_release["releases"][0]["id"][0:45]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=message_from_kafka["data"]["operationDate"],
            actual_result=convert_timestamp_to_date[0]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=message_from_kafka["data"]["operationDate"],
            actual_result=fs_release["releases"][0]["date"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="planning",
            actual_result=fs_release["releases"][0]["tag"][0]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="tender",
            actual_result=fs_release["releases"][0]["initiationType"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(is_it_uuid(fs_release["releases"][0]["tender"]["id"], 4))
        )
        assert compare_actual_result_and_expected_result(
            expected_result=status,
            actual_result=fs_release["releases"][0]["tender"]["status"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="empty",
            actual_result=fs_release["releases"][0]["tender"]["statusDetails"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=procuring_entity_scheme + "-" + procuring_entity_id,
            actual_result=roles_list[1]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["name"],
            actual_result=roles_list[1]["name"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["identifier"]["scheme"],
            actual_result=roles_list[1]["identifier"]["scheme"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["identifier"]["id"],
            actual_result=roles_list[1]["identifier"]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["identifier"]["legalName"],
            actual_result=roles_list[1]["identifier"]["legalName"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["address"]["streetAddress"],
            actual_result=roles_list[1]["address"]["streetAddress"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=country_from_mdm["scheme"],
            actual_result=roles_list[1]["address"]["addressDetails"]["country"]["scheme"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]["id"],
            actual_result=roles_list[1]["address"]["addressDetails"]["country"]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=country_from_mdm["description"],
            actual_result=roles_list[1]["address"]["addressDetails"]["country"]["description"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=country_from_mdm["uri"],
            actual_result=roles_list[1]["address"]["addressDetails"]["country"]["uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=region_from_mdm["scheme"],
            actual_result=roles_list[1]["address"]["addressDetails"]["region"]["scheme"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"],
            actual_result=roles_list[1]["address"]["addressDetails"]["region"]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=region_from_mdm["description"],
            actual_result=roles_list[1]["address"]["addressDetails"]["region"]["description"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=region_from_mdm["uri"],
            actual_result=roles_list[1]["address"]["addressDetails"]["region"]["uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=locality_from_mdm["scheme"],
            actual_result=roles_list[1]["address"]["addressDetails"]["locality"]["scheme"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["id"],
            actual_result=roles_list[1]["address"]["addressDetails"]["locality"]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=locality_from_mdm["description"],
            actual_result=roles_list[1]["address"]["addressDetails"]["locality"]["description"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=locality_from_mdm["uri"],
            actual_result=roles_list[1]["address"]["addressDetails"]["locality"]["uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["contactPoint"]["name"],
            actual_result=roles_list[1]["contactPoint"]["name"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["contactPoint"]["email"],
            actual_result=roles_list[1]["contactPoint"]["email"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["contactPoint"]["telephone"],
            actual_result=roles_list[1]["contactPoint"]["telephone"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="payer",
            actual_result=roles_list[1]["roles"][0]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["identifier"]["scheme"] + "-" + payload["buyer"]["identifier"][
                "id"],
            actual_result=roles_list[0]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["name"],
            actual_result=roles_list[0]["name"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["identifier"]["scheme"],
            actual_result=roles_list[0]["identifier"]["scheme"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["identifier"]["id"],
            actual_result=roles_list[0]["identifier"]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["identifier"]["legalName"],
            actual_result=roles_list[0]["identifier"]["legalName"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["address"]["streetAddress"],
            actual_result=roles_list[0]["address"]["streetAddress"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=country_from_mdm["scheme"],
            actual_result=roles_list[0]["address"]["addressDetails"]["country"]["scheme"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["address"]["addressDetails"]["country"]["id"],
            actual_result=roles_list[0]["address"]["addressDetails"]["country"]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=country_from_mdm["description"],
            actual_result=roles_list[0]["address"]["addressDetails"]["country"]["description"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=country_from_mdm["uri"],
            actual_result=roles_list[0]["address"]["addressDetails"]["country"]["uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=region_from_mdm["scheme"],
            actual_result=roles_list[0]["address"]["addressDetails"]["region"]["scheme"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["address"]["addressDetails"]["region"]["id"],
            actual_result=roles_list[0]["address"]["addressDetails"]["region"]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=region_from_mdm["description"],
            actual_result=roles_list[0]["address"]["addressDetails"]["region"]["description"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=region_from_mdm["uri"],
            actual_result=roles_list[0]["address"]["addressDetails"]["region"]["uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=locality_from_mdm["scheme"],
            actual_result=roles_list[0]["address"]["addressDetails"]["locality"]["scheme"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["address"]["addressDetails"]["locality"]["id"],
            actual_result=roles_list[0]["address"]["addressDetails"]["locality"]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=locality_from_mdm["description"],
            actual_result=roles_list[0]["address"]["addressDetails"]["locality"]["description"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=locality_from_mdm["uri"],
            actual_result=roles_list[0]["address"]["addressDetails"]["locality"]["uri"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["contactPoint"]["name"],
            actual_result=roles_list[0]["contactPoint"]["name"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["contactPoint"]["email"],
            actual_result=roles_list[0]["contactPoint"]["email"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["contactPoint"]["telephone"],
            actual_result=roles_list[0]["contactPoint"]["telephone"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="funder",
            actual_result=roles_list[0]["roles"][0]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["period"]["startDate"],
            actual_result=fs_release["releases"][0]["planning"]["budget"]["period"]["startDate"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["period"]["endDate"],
            actual_result=fs_release["releases"][0]["planning"]["budget"]["period"]["endDate"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(payload["planning"]["budget"]["amount"]["amount"]),
            actual_result=str(fs_release["releases"][0]["planning"]["budget"]["amount"]["amount"])
        )
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["amount"]["currency"],
            actual_result=fs_release["releases"][0]["planning"]["budget"]["amount"]["currency"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(payload["planning"]["budget"]["isEuropeanUnionFunded"]),
            actual_result=str(fs_release["releases"][0]["planning"]["budget"]["isEuropeanUnionFunded"])
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(buyer_in_payload),
            actual_result=str(fs_release["releases"][0]["planning"]["budget"]["verified"])
        )
        assert compare_actual_result_and_expected_result(
            expected_result=source_entity_id,
            actual_result=fs_release["releases"][0]["planning"]["budget"]["sourceEntity"]["id"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=source_entity_name,
            actual_result=fs_release["releases"][0]["planning"]["budget"]["sourceEntity"]["name"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(is_it_uuid(fs_release["releases"][0]["relatedProcesses"][0]["id"], 1))
        )
        assert compare_actual_result_and_expected_result(
            expected_result="parent",
            actual_result=fs_release["releases"][0]["relatedProcesses"][0]["relationship"][0]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="ocid",
            actual_result=fs_release["releases"][0]["relatedProcesses"][0]["scheme"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=cp_id,
            actual_result=fs_release["releases"][0]["relatedProcesses"][0]["identifier"]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{cp_id}",
            actual_result=fs_release["releases"][0]["relatedProcesses"][0]["uri"]
        )


class TestCheckTheCorrectSettingOfTheReleaseDateValueInTheFsRelease(object):
    @pytestrail.case("27552")
    def test_send_the_request_27552_1(self, country, language, instance, cassandra_username,
                                      cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )

    @pytestrail.case("27552")
    def test_see_the_result_in_feed_point_point_27552_2(self, country, language, instance, cassandra_username,
                                                        cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(fs.check_on_that_message_is_successfully_create_fs())
        )

    @pytestrail.case('27552')
    def test_navigate_to_the_database_27552_3(self, country, language, instance, cassandra_username,
                                              cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        database = Cassandra(
            cp_id=cp_id,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        start_date = database.execute_cql_from_orchestrator_operation_step_by_oper_id(
            operation_id=message_from_kafka["X-OPERATION-ID"],
            task_id="NoticeCreateReleaseTask",
        )[3]["startDate"]

    @pytestrail.case('27552')
    def test_compare_context_start_date_from_database_and_release_date_from_fs_release_27552_4(self, country,
                                                                                               language,
                                                                                               instance,
                                                                                               cassandra_username,
                                                                                               cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        url_create = message_from_kafka['data']['url'] + '/' + message_from_kafka['data']['outcomes']['fs'][0][
            'id']
        fs_release = requests.get(url=url_create).json()
        database = Cassandra(
            cp_id=cp_id,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        start_date = database.execute_cql_from_orchestrator_operation_step_by_oper_id(
            operation_id=message_from_kafka["X-OPERATION-ID"],
            task_id="NoticeCreateReleaseTask",
        )[3]["startDate"]
        assert compare_actual_result_and_expected_result(
            expected_result=start_date,
            actual_result=fs_release["releases"][0]["date"]
        )


class TestCheckOnImpossibilityOfCreatingFsIfBearerTokenIsFake(object):
    @pytestrail.case("27553")
    def test_send_the_request_27553_1(self, country, language, instance, cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            platform="zzz"
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)

        assert compare_actual_result_and_expected_result(
            expected_result=str(
                [{'code': '401.81.03.04',
                  'description': 'The error of verification of the authentication token.'}]),
            actual_result=str(json.loads(create_fs_response.text)['errors'])
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(401),
            actual_result=str(create_fs_response.status_code)
        )


class TestCheckOnImpossibilityOfCreatingFsIfValueOfAuthorizationIsFake(object):
    @pytestrail.case("27554")
    def test_send_the_request_27554_1(self, country, language, instance, cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            platform="zzz"
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs_with_fake_authorization_token(cp_id=cp_id)
        assert compare_actual_result_and_expected_result(
            expected_result=str(
                [{"code": "401.81.02.02",
                  "description": "Invalid type of the authentication token. Expected type is 'Bearer'."
                  }]),
            actual_result=str(json.loads(create_fs_response.text)['errors'])
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(401),
            actual_result=str(create_fs_response.status_code)
        )


class TestCheckOnImpossibilityOfCreatingFsIfRequestOwnerEqualOwnerFromDB(object):
    @pytestrail.case("27555")
    def test_send_the_request_27555_1(self, country, language, instance, cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            platform="platform_two"
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id=cp_id)
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )

    @pytestrail.case("27555")
    def test_send_the_request_27555_2(self, country, language, instance, cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            platform="platform_two"
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id=cp_id)
        database = Cassandra(
            cp_id=cp_id,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs_budget_create_fs_task = database.execute_cql_from_orchestrator_operation_step(
            task_id='BudgetCreateFsTask'
        )
        fs_notice_create_release_task = database.execute_cql_from_orchestrator_operation_step(
            task_id='NoticeCreateReleaseTask'
        )
        fs_save_context_task = database.execute_cql_from_orchestrator_operation_step(
            task_id='SaveContextTask'
        )
        fs_send_message_to_platform_task = database.execute_cql_from_orchestrator_operation_step(
            task_id='SendMessageToPlatformTask'
        )

        assert compare_actual_result_and_expected_result(
            expected_result=str(cp_id + "-FS-"),
            actual_result=str(fs_budget_create_fs_task["fs"]["ocid"][0:32])
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(cp_id + "-FS-"),
            actual_result=str(fs_notice_create_release_task["ocid"][0:32])
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(cp_id + "-FS-"),
            actual_result=str(fs_save_context_task["ocid"][0:32])
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(cp_id + "-FS-"),
            actual_result=str(fs_send_message_to_platform_task["ocid"][0:32])
        )


class TestCheckThatEmptyObjectsAndArraysAreNotPublishedOrThereIsAnErrorMessage(object):
    @pytestrail.case('27556')
    def test_send_request_where_tender_is_empty_object_27556_1(self, country, language, instance,
                                                               cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"] = {}
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "budget.model.dto.fs.request.TenderFsCreate] value failed for JSON "
                                                 "property procuringEntity due to missing (therefore NULL) value for "
                                                 "creator parameter procuringEntity which is a non-nullable type\n "
                                                 "at [Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                 "chain: com.procurement.budget.model.dto.fs.request.FsCreate"
                                                 "[\"tender\"]->com.procurement.budget.model.dto.fs.request.Tender"
                                                 "FsCreate[\"procuringEntity\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27556')
    def test_send_request_where_tender_procuring_entity_is_empty_object_27556_2(self, country, language, instance,
                                                                                cassandra_username,
                                                                                cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"] = {}
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "budget.model.dto.fs.OrganizationReferenceFs] value failed for "
                                                 "JSON property name due to missing (therefore NULL) value for "
                                                 "creator parameter name which is a non-nullable type\n at "
                                                 "[Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                 "chain: com.procurement.budget.model.dto.fs.request.FsCreate"
                                                 "[\"tender\"]->com.procurement.budget.model.dto.fs.request."
                                                 "TenderFsCreate[\"procuringEntity\"]->com.procurement.budget."
                                                 "model.dto.fs.OrganizationReferenceFs[\"name\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27556')
    def test_send_request_where_tender_procuring_entity_identifier_is_empty_object_27556_3(self, country, language,
                                                                                           instance,
                                                                                           cassandra_username,
                                                                                           cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["identifier"] = {}
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.Identifier] value failed for JSON property id "
                                                 "due to missing (therefore NULL) value for creator parameter id "
                                                 "which is a non-nullable type\n at [Source: UNKNOWN; line: -1, "
                                                 "column: -1] (through reference chain: com.procurement.mdm.model."
                                                 "dto.data.FS[\"tender\"]->com.procurement.mdm.model.dto.data."
                                                 "TenderFS[\"procuringEntity\"]->com.procurement.mdm.model.dto.data."
                                                 "OrganizationReference[\"identifier\"]->com.procurement.mdm.model."
                                                 "dto.data.Identifier[\"id\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27556')
    def test_send_request_where_tender_procuring_entity_address_is_empty_object_27556_4(self, country, language,
                                                                                        instance,
                                                                                        cassandra_username,
                                                                                        cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["address"] = {}
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str(
                [{"code": "400.20.00", "description": "com.fasterxml.jackson.module.kotlin.MissingKotlin"
                                                      "ParameterException: Instantiation of [simple "
                                                      "type, class com.procurement.mdm.model.dto.data."
                                                      "Address] value failed for JSON property street"
                                                      "Address due to missing (therefore NULL) value "
                                                      "for creator parameter streetAddress which is a "
                                                      "non-nullable type\n at [Source: UNKNOWN; line: "
                                                      "-1, column: -1] (through reference chain: com."
                                                      "procurement.mdm.model.dto.data.FS[\"tender\"]->"
                                                      "com.procurement.mdm.model.dto.data.TenderFS"
                                                      "[\"procuringEntity\"]->com.procurement.mdm.model."
                                                      "dto.data.OrganizationReference[\"address\"]->"
                                                      "com.procurement.mdm.model.dto.data.Address"
                                                      "[\"streetAddress\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27556')
    def test_tender_procuring_entity_address_address_details_is_empty_object_27556_5(self, country,
                                                                                     language, instance,
                                                                                     cassandra_username,
                                                                                     cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["address"]["addressDetails"] = {}
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.AddressDetails] value failed for JSON property "
                                                 "country due to missing (therefore NULL) value for creator "
                                                 "parameter country which is a non-nullable type\n at [Source: "
                                                 "UNKNOWN; line: -1, column: -1] (through reference chain: com."
                                                 "procurement.mdm.model.dto.data.FS[\"tender\"]->com.procurement."
                                                 "mdm.model.dto.data.TenderFS[\"procuringEntity\"]->com.procurement."
                                                 "mdm.model.dto.data.OrganizationReference[\"address\"]->com."
                                                 "procurement.mdm.model.dto.data.Address[\"addressDetails\"]->com."
                                                 "procurement.mdm.model.dto.data.AddressDetails[\"country\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27556')
    def test_tender_procuring_entity_address_address_details_country_is_empty_object_27556_6(self, country,
                                                                                             language, instance,
                                                                                             cassandra_username,
                                                                                             cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"] = {}
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.CountryDetails] value failed for JSON property "
                                                 "id due to missing (therefore NULL) value for creator parameter "
                                                 "id which is a non-nullable type\n at [Source: UNKNOWN; line: -1, "
                                                 "column: -1] (through reference chain: com.procurement.mdm.model."
                                                 "dto.data.FS[\"tender\"]->com.procurement.mdm.model.dto.data."
                                                 "TenderFS[\"procuringEntity\"]->com.procurement.mdm.model.dto."
                                                 "data.OrganizationReference[\"address\"]->com.procurement.mdm."
                                                 "model.dto.data.Address[\"addressDetails\"]->com.procurement.mdm."
                                                 "model.dto.data.AddressDetails[\"country\"]->com.procurement.mdm."
                                                 "model.dto.data.CountryDetails[\"id\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27556')
    def test_tender_procuring_entity_address_address_details_region_is_empty_object_27556_7(self, country,
                                                                                            language, instance,
                                                                                            cassandra_username,
                                                                                            cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"] = {}
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.RegionDetails] value failed for JSON property "
                                                 "id due to missing (therefore NULL) value for creator parameter "
                                                 "id which is a non-nullable type\n at [Source: UNKNOWN; line: -1, "
                                                 "column: -1] (through reference chain: com.procurement.mdm.model."
                                                 "dto.data.FS[\"tender\"]->com.procurement.mdm.model.dto.data.Tender"
                                                 "FS[\"procuringEntity\"]->com.procurement.mdm.model.dto.data."
                                                 "OrganizationReference[\"address\"]->com.procurement.mdm.model."
                                                 "dto.data.Address[\"addressDetails\"]->com.procurement.mdm.model."
                                                 "dto.data.AddressDetails[\"region\"]->com.procurement.mdm.model."
                                                 "dto.data.RegionDetails[\"id\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27556')
    def test_tender_procuring_entity_address_address_details_locality_is_empty_object_27556_8(self, country,
                                                                                              language, instance,
                                                                                              cassandra_username,
                                                                                              cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"] = {}
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.LocalityDetails] value failed for JSON property "
                                                 "scheme due to missing (therefore NULL) value for creator parameter "
                                                 "scheme which is a non-nullable type\n at [Source: UNKNOWN; line: "
                                                 "-1, column: -1] (through reference chain: com.procurement.mdm."
                                                 "model.dto.data.FS[\"tender\"]->com.procurement.mdm.model.dto.data."
                                                 "TenderFS[\"procuringEntity\"]->com.procurement.mdm.model.dto.data."
                                                 "OrganizationReference[\"address\"]->com.procurement.mdm.model.dto."
                                                 "data.Address[\"addressDetails\"]->com.procurement.mdm.model.dto."
                                                 "data.AddressDetails[\"locality\"]->com.procurement.mdm.model.dto."
                                                 "data.LocalityDetails[\"scheme\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27556')
    def test_tender_procuring_entity_additional_identifiers_is_empty_array_27556_9(self, country,
                                                                                   language, instance,
                                                                                   cassandra_username,
                                                                                   cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["additionalIdentifiers"] = []
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        url_create = message_from_kafka['data']['url'] + '/' + message_from_kafka['data']['outcomes']['fs'][0][
            'id']
        fs_release = requests.get(url=url_create).json()
        procuring_entity_obj = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                procuring_entity_obj.append(p)
        check_procuring_entity_additional_identifiers = "additionalIdentifiers" in procuring_entity_obj[0]
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(fs.check_on_that_message_is_successfully_create_fs())
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(False),
            actual_result=str(check_procuring_entity_additional_identifiers)
        )

    @pytestrail.case('27556')
    def test_tender_procuring_entity_additional_identifiers_is_empty_object_27556_10(self, country,
                                                                                     language, instance,
                                                                                     cassandra_username,
                                                                                     cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["additionalIdentifiers"] = [] = {}
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.exc.MismatchedInput"
                                                 "Exception: Cannot deserialize instance of `java.util."
                                                 "ArrayList` out of START_OBJECT token\n at [Source: "
                                                 "UNKNOWN; line: -1, column: -1] (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS"
                                                 "[\"tender\"]->com.procurement.mdm.model.dto.data."
                                                 "TenderFS[\"procuringEntity\"]->com.procurement.mdm."
                                                 "model.dto.data.OrganizationReference[\"additional"
                                                 "Identifiers\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27556')
    def test_tender_procuring_entity_contact_point_is_empty_object_27556_11(self, country,
                                                                            language, instance,
                                                                            cassandra_username,
                                                                            cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["contactPoint"] = {}
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.ContactPoint] value failed for JSON property "
                                                 "name due to missing (therefore NULL) value for creator parameter "
                                                 "name which is a non-nullable type\n at [Source: UNKNOWN; line: -1, "
                                                 "column: -1] (through reference chain: com.procurement.mdm.model."
                                                 "dto.data.FS[\"tender\"]->com.procurement.mdm.model.dto.data."
                                                 "TenderFS[\"procuringEntity\"]->com.procurement.mdm.model.dto."
                                                 "data.OrganizationReference[\"contactPoint\"]->com.procurement.mdm."
                                                 "model.dto.data.ContactPoint[\"name\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27556')
    def test_buyer_is_empty_object_27556_12(self, country, language, instance, cassandra_username,
                                            cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"] = {}
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlin"
                                                 "ParameterException: Instantiation of [simple type, class com."
                                                 "procurement.budget.model.dto.fs.OrganizationReferenceFs] value "
                                                 "failed for JSON property name due to missing (therefore NULL) "
                                                 "value for creator parameter name which is a non-nullable type\n "
                                                 "at [Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                 "chain: com.procurement.budget.model.dto.fs.request.FsCreate"
                                                 "[\"buyer\"]->com.procurement.budget.model.dto.fs.Organization"
                                                 "ReferenceFs[\"name\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27556')
    def test_buyer_identifier_is_empty_object_27556_13(self, country, language, instance, cassandra_username,
                                                       cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["identifier"] = {}
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.Identifier] value failed for JSON property id "
                                                 "due to missing (therefore NULL) value for creator parameter id "
                                                 "which is a non-nullable type\n at [Source: UNKNOWN; line: -1, "
                                                 "column: -1] (through reference chain: com.procurement.mdm.model."
                                                 "dto.data.FS[\"buyer\"]->com.procurement.mdm.model.dto.data."
                                                 "OrganizationReference[\"identifier\"]->com.procurement.mdm.model."
                                                 "dto.data.Identifier[\"id\"])"}]),
            actual_result=str(message_from_kafka["errors"])

        )

    @pytestrail.case('27556')
    def test_buyer_address_is_empty_object_27556_14(self, country, language, instance, cassandra_username,
                                                    cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["address"] = {}
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.Address] value failed for JSON property street"
                                                 "Address due to missing (therefore NULL) value for creator "
                                                 "parameter streetAddress which is a non-nullable type\n at "
                                                 "[Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"buyer\"]->com."
                                                 "procurement.mdm.model.dto.data.OrganizationReference[\"address\"]"
                                                 "->com.procurement.mdm.model.dto.data.Address[\"streetAddress\"])"}]),
            actual_result=str(message_from_kafka["errors"])

        )

    @pytestrail.case('27556')
    def test_buyer_address_address_details_is_empty_object_27556_15(self, country, language, instance,
                                                                    cassandra_username,
                                                                    cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["address"]["addressDetails"] = {}
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.AddressDetails] value failed for JSON "
                                                 "property country due to missing (therefore NULL) value for "
                                                 "creator parameter country which is a non-nullable type\n at "
                                                 "[Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"buyer\"]->com."
                                                 "procurement.mdm.model.dto.data.OrganizationReference[\"address\"]"
                                                 "->com.procurement.mdm.model.dto.data.Address[\"addressDetails\"]->"
                                                 "com.procurement.mdm.model.dto.data.AddressDetails[\"country\"])"}]),
            actual_result=str(message_from_kafka["errors"])

        )

    @pytestrail.case('27556')
    def test_buyer_address_address_details_country_is_empty_object_27556_16(self, country, language, instance,
                                                                            cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["address"]["addressDetails"]["country"] = {}
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.CountryDetails] value failed for JSON "
                                                 "property id due to missing (therefore NULL) value for creator "
                                                 "parameter id which is a non-nullable type\n at [Source: UNKNOWN; "
                                                 "line: -1, column: -1] (through reference chain: com."
                                                 "procurement.mdm.model.dto.data.FS[\"buyer\"]->com.procurement."
                                                 "mdm.model.dto.data.OrganizationReference[\"address\"]->com."
                                                 "procurement.mdm.model.dto.data.Address[\"addressDetails\"]->com."
                                                 "procurement.mdm.model.dto.data.AddressDetails[\"country\"]->com."
                                                 "procurement.mdm.model.dto.data.CountryDetails[\"id\"])"}]),
            actual_result=str(message_from_kafka["errors"])

        )

    @pytestrail.case('27556')
    def test_buyer_address_address_details_country_is_empty_object_27556_16(self, country, language, instance,
                                                                            cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["address"]["addressDetails"]["country"] = {}
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.CountryDetails] value failed for JSON "
                                                 "property id due to missing (therefore NULL) value for creator "
                                                 "parameter id which is a non-nullable type\n at [Source: UNKNOWN; "
                                                 "line: -1, column: -1] (through reference chain: com."
                                                 "procurement.mdm.model.dto.data.FS[\"buyer\"]->com.procurement."
                                                 "mdm.model.dto.data.OrganizationReference[\"address\"]->com."
                                                 "procurement.mdm.model.dto.data.Address[\"addressDetails\"]->com."
                                                 "procurement.mdm.model.dto.data.AddressDetails[\"country\"]->com."
                                                 "procurement.mdm.model.dto.data.CountryDetails[\"id\"])"}]),
            actual_result=str(message_from_kafka["errors"])

        )

    @pytestrail.case('27556')
    def test_buyer_address_address_details_region_is_empty_object_27556_17(self, country, language, instance,
                                                                           cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["address"]["addressDetails"]["region"] = {}
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.RegionDetails] value failed for JSON property "
                                                 "id due to missing (therefore NULL) value for creator parameter "
                                                 "id which is a non-nullable type\n at [Source: UNKNOWN; line: -1, "
                                                 "column: -1] (through reference chain: com.procurement.mdm.model."
                                                 "dto.data.FS[\"buyer\"]->com.procurement.mdm.model.dto.data."
                                                 "OrganizationReference[\"address\"]->com.procurement.mdm.model.dto."
                                                 "data.Address[\"addressDetails\"]->com.procurement.mdm.model.dto."
                                                 "data.AddressDetails[\"region\"]->com.procurement.mdm.model.dto."
                                                 "data.RegionDetails[\"id\"])"}]),
            actual_result=str(message_from_kafka["errors"])

        )

    @pytestrail.case('27556')
    def test_buyer_address_address_details_locality_is_empty_object_27556_18(self, country, language, instance,
                                                                             cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["address"]["addressDetails"]["locality"] = {}
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.LocalityDetails] value failed for JSON property "
                                                 "scheme due to missing (therefore NULL) value for creator "
                                                 "parameter scheme which is a non-nullable type\n at [Source: "
                                                 "UNKNOWN; line: -1, column: -1] (through reference chain: "
                                                 "com.procurement.mdm.model.dto.data.FS[\"buyer\"]->com.procurement."
                                                 "mdm.model.dto.data.OrganizationReference[\"address\"]->com."
                                                 "procurement.mdm.model.dto.data.Address[\"addressDetails\"]->"
                                                 "com.procurement.mdm.model.dto.data.AddressDetails[\"locality\"]"
                                                 "->com.procurement.mdm.model.dto.data.LocalityDetails[\"scheme\"])"}]),
            actual_result=str(message_from_kafka["errors"])

        )

    @pytestrail.case('27556')
    def test_buyer_additional_identifiers_is_empty_array_27556_19(self, country, language, instance,
                                                                  cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["additionalIdentifiers"] = []
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        url_create = message_from_kafka['data']['url'] + '/' + message_from_kafka['data']['outcomes']['fs'][0][
            'id']
        fs_release = requests.get(url=url_create).json()
        buyer_obj = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                buyer_obj.append(p)
        check_buyer_additional_identifiers = "additionalIdentifiers" in buyer_obj[0]
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(fs.check_on_that_message_is_successfully_create_fs())
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(False),
            actual_result=str(check_buyer_additional_identifiers)
        )

    @pytestrail.case('27556')
    def test_buyer_additional_identifiers_is_empty_object_27556_20(self, country, language, instance,
                                                                   cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["additionalIdentifiers"][0] = {}
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.Identifier] value failed for JSON property "
                                                 "id due to missing (therefore NULL) value for creator parameter "
                                                 "id which is a non-nullable type\n at [Source: UNKNOWN; line: -1, "
                                                 "column: -1] (through reference chain: com.procurement.mdm.model."
                                                 "dto.data.FS[\"buyer\"]->com.procurement.mdm.model.dto.data."
                                                 "OrganizationReference[\"additionalIdentifiers\"]->java.util."
                                                 "ArrayList[0]->com.procurement.mdm.model.dto.data.Identifier"
                                                 "[\"id\"])"}]),
            actual_result=str(message_from_kafka["errors"])

        )

    @pytestrail.case('27556')
    def test_buyer_contact_point_is_empty_object_27556_21(self, country, language, instance,
                                                          cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["contactPoint"] = {}
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.ContactPoint] value failed for JSON property "
                                                 "name due to missing (therefore NULL) value for creator parameter "
                                                 "name which is a non-nullable type\n at [Source: UNKNOWN; line: "
                                                 "-1, column: -1] (through reference chain: com.procurement.mdm."
                                                 "model.dto.data.FS[\"buyer\"]->com.procurement.mdm.model.dto.data."
                                                 "OrganizationReference[\"contactPoint\"]->com.procurement.mdm."
                                                 "model.dto.data.ContactPoint[\"name\"])"}]),
            actual_result=str(message_from_kafka["errors"])

        )

    @pytestrail.case('27556')
    def test_planning_is_empty_object_27556_22(self, country, language, instance,
                                               cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["planning"] = {}
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.00.00.00", "description": "Data processing exception."}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27556')
    def test_planning_budget_is_empty_object_27556_23(self, country, language, instance, cassandra_username,
                                                      cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["planning"]["budget"] = {}
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.00.00.00", "description": "Data processing exception."}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27556')
    def test_planning_budget_period_is_empty_object_27556_24(self, country, language, instance, cassandra_username,
                                                             cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["planning"]["budget"]["period"] = {}
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "budget.model.dto.ocds.Period] value failed for JSON property "
                                                 "startDate due to missing (therefore NULL) value for creator "
                                                 "parameter startDate which is a non-nullable type\n at [Source: "
                                                 "UNKNOWN; line: -1, column: -1] (through reference chain: com."
                                                 "procurement.budget.model.dto.fs.request.FsCreate[\"planning\"]->"
                                                 "com.procurement.budget.model.dto.fs.request.PlanningFsCreate"
                                                 "[\"budget\"]->com.procurement.budget.model.dto.fs.request.Budget"
                                                 "FsCreate[\"period\"]->com.procurement.budget.model.dto.ocds."
                                                 "Period[\"startDate\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27556')
    def test_planning_budget_amount_is_empty_object_27556_25(self, country, language, instance, cassandra_username,
                                                             cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["planning"]["budget"]["amount"] = {}
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "mdm.model.dto.data.ValueFS] value failed for JSON property "
                                                 "currency due to missing (therefore NULL) value for creator "
                                                 "parameter currency which is a non-nullable type\n at [Source: "
                                                 "UNKNOWN; line: -1, column: -1] (through reference chain: com."
                                                 "procurement.mdm.model.dto.data.FS[\"planning\"]->com.procurement."
                                                 "mdm.model.dto.data.PlanningFS[\"budget\"]->com.procurement.mdm."
                                                 "model.dto.data.BudgetFS[\"amount\"]->com.procurement.mdm.model.dto."
                                                 "data.ValueFS[\"currency\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27556')
    def test_planning_budget_european_union_funding_is_empty_object_27556_26(self, country, language, instance,
                                                                             cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["planning"]["budget"]["europeanUnionFunding"] = {}
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                 "Exception: Instantiation of [simple type, class com.procurement."
                                                 "budget.model.dto.ocds.EuropeanUnionFunding] value failed for JSON "
                                                 "property projectName due to missing (therefore NULL) value for "
                                                 "creator parameter projectName which is a non-nullable type\n at "
                                                 "[Source: UNKNOWN; line: -1, column: -1] (through reference chain: "
                                                 "com.procurement.budget.model.dto.fs.request.FsCreate[\"planning\"]"
                                                 "->com.procurement.budget.model.dto.fs.request.PlanningFsCreate"
                                                 "[\"budget\"]->com.procurement.budget.model.dto.fs.request.Budget"
                                                 "FsCreate[\"europeanUnionFunding\"]->com.procurement.budget.model."
                                                 "dto.ocds.EuropeanUnionFunding[\"projectName\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27556')
    def test_payload_is_empty_object_27556_27(self, country, language, instance,
                                              cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = {}
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str(
                [{
                    "code": "400.00.00.00",
                    "description": "Data is empty!"
                }]
            ),
            actual_result=str(json.loads(create_fs_response.text)['errors'])
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(400),
            actual_result=str(create_fs_response.status_code)
        )


class TestCheckOnImpossibilityOfCreatingFsWithEmptyOrBlankStrings(object):
    @pytestrail.case('27557')
    def test_tender_is_empty_string_27557_1(self, country, language, instance,
                                            cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.00.00.00",
                                  "description": "com.fasterxml.jackson.databind.node.TextNode cannot be cast to "
                                                 "com.fasterxml.jackson.databind.node.ObjectNode"}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_tender_procuring_entity_is_empty_str_27557_2(self, country, language, instance,
                                                          cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.exc.MismatchedInputException: "
                                                 "Cannot construct instance of `com.procurement.mdm.model.dto.data."
                                                 "OrganizationReference` (although at least one Creator exists): no "
                                                 "String-argument constructor/factory method to deserialize from "
                                                 "String value ('')\n at [Source: UNKNOWN; line: -1, column: -1] "
                                                 "(through reference chain: com.procurement.mdm.model.dto.data.FS"
                                                 "[\"tender\"]->com.procurement.mdm.model.dto.data.TenderFS"
                                                 "[\"procuringEntity\"])"}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_tender_procuring_entity_name_is_empty_str_27557_3(self, country, language, instance,
                                                               cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["name"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'tender."
                                                 "procuringEntity.name' is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_tender_procuring_entity_identifier_id_is_empty_str_27557_4(self, country, language, instance,
                                                                        cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["identifier"]["id"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'tender.procuringEntity."
                                                 "identifier.id' is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_tender_procuring_entity_identifier_scheme_is_empty_str_27557_5(self, country, language, instance,
                                                                            cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["identifier"]["scheme"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00.12", "description": "Registration scheme not found. "}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_tender_procuring_entity_identifier_legal_name_is_empty_str_27557_6(self, country, language, instance,
                                                                                cassandra_username,
                                                                                cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["identifier"]["legalName"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'tender.procuring"
                                                 "Entity.identifier.legalName' is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_tender_procuring_entity_identifier_uri_is_empty_str_27557_7(self, country, language, instance,
                                                                         cassandra_username,
                                                                         cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["identifier"]["uri"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'tender.procuring"
                                                 "Entity.identifier.uri' is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_tender_procuring_entity_address_street_address_is_empty_str_27557_8(self, country, language, instance,
                                                                                 cassandra_username,
                                                                                 cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["address"]["streetAddress"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11", "description": "Incorrect an attribute value.The attribute "
                                                                         "'tender.procuringEntity.address.street"
                                                                         "Address' is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_tender_procuring_entity_address_postal_code_is_empty_str_27557_9(self, country, language, instance,
                                                                              cassandra_username,
                                                                              cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["address"]["postalCode"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'tender.procuring"
                                                 "Entity.address.postalCode' is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_tender_procuring_entity_address_address_details_country_id_is_empty_str_27557_10(self, country,
                                                                                              language, instance,
                                                                                              cassandra_username,
                                                                                              cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]["id"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00.11", "description": "Country not found. "}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_tender_procuring_entity_address_address_details_region_id_is_empty_str_27557_11(self, country,
                                                                                             language, instance,
                                                                                             cassandra_username,
                                                                                             cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00.13", "description": "Region not found. "}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_tender_procuring_entity_address_address_details_locality_id_is_empty_str_27557_12(self, country,
                                                                                               language, instance,
                                                                                               cassandra_username,
                                                                                               cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["id"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00.14", "description": "Locality not found. "}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_tender_procuring_entity_address_address_details_locality_scheme_is_empty_str_27557_13(self, country,
                                                                                                   language,
                                                                                                   instance,
                                                                                                   cassandra_username,
                                                                                                   cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["scheme"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'tender.procuring"
                                                 "Entity.address.addressDetails.locality.scheme' is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_tender_procuring_entity_address_details_locality_description_is_empty_str_27557_14(self, country,
                                                                                                language, instance,
                                                                                                cassandra_username,
                                                                                                cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["description"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        url_create = message_from_kafka['data']['url'] + '/' + message_from_kafka['data']['outcomes']['fs'][0]['id']
        fs_release = requests.get(url=url_create).json()
        procuring_entity_obj = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                procuring_entity_obj.append(p)
        mdm = MdmService(
            instance="dev",
            lang="ro",
            country=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]["id"],
            region=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"],
            locality=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["id"]
        )
        data = mdm.process_fs_data(cp_id).json()
        locality_from_mdm = data["data"]["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(locality_from_mdm["description"]),
            actual_result=str(procuring_entity_obj[0]["address"]["addressDetails"]["locality"]["description"])
        )

    @pytestrail.case('27557')
    def test_tender_procur_entity_address_address_details_locality_descr_is_empty_str_27557_14(self, country,
                                                                                               language, instance,
                                                                                               cassandra_username,
                                                                                               cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["description"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        url_create = message_from_kafka['data']['url'] + '/' + message_from_kafka['data']['outcomes']['fs'][0]['id']
        fs_release = requests.get(url=url_create).json()
        procuring_entity_obj = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                procuring_entity_obj.append(p)
        mdm = MdmService(
            instance="dev",
            lang="ro",
            country=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]["id"],
            region=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"],
            locality=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["id"]
        )
        data = mdm.process_fs_data(cp_id).json()
        locality_from_mdm = data["data"]["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(fs.check_on_that_message_is_successfully_create_fs())
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(locality_from_mdm["description"]),
            actual_result=str(procuring_entity_obj[0]["address"]["addressDetails"]["locality"]["description"])
        )

    @pytestrail.case('27557')
    def test_tender_procuring_entity_additional_identifiers_id_is_empty_str_27557_15(self, country,
                                                                                     language, instance,
                                                                                     cassandra_username,
                                                                                     cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["id"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'tender.procuring"
                                                 "Entity.additionalIdentifiers.[0]id' is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_tender_procuring_entity_additional_identifiers_scheme_is_empty_str_27557_16(self, country,
                                                                                         language, instance,
                                                                                         cassandra_username,
                                                                                         cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["scheme"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'tender.procuring"
                                                 "Entity.additionalIdentifiers.[0]scheme' is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_tender_procuring_entity_additional_identifiers_legal_name_is_empty_str_27557_17(self, country,
                                                                                             language, instance,
                                                                                             cassandra_username,
                                                                                             cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["legalName"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'tender.procuring"
                                                 "Entity.additionalIdentifiers.[0]legalName' is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_tender_procuring_entity_additional_identifiers_uri_is_empty_str_27557_18(self, country,
                                                                                      language, instance,
                                                                                      cassandra_username,
                                                                                      cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["uri"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'tender.procuring"
                                                 "Entity.additionalIdentifiers.[0]uri' is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_tender_procuring_entity_contact_point_name_is_empty_str_27557_19(self, country,
                                                                              language, instance,
                                                                              cassandra_username,
                                                                              cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["contactPoint"]["name"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'tender.procuring"
                                                 "Entity.contactPoint.name' is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_tender_procuring_entity_contact_point_email_is_empty_str_27557_20(self, country,
                                                                               language, instance,
                                                                               cassandra_username,
                                                                               cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["contactPoint"]["email"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'tender.procuring"
                                                 "Entity.contactPoint.email' is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_tender_procuring_entity_contact_point_telephone_is_empty_str_27557_21(self, country,
                                                                                   language, instance,
                                                                                   cassandra_username,
                                                                                   cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["contactPoint"]["telephone"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'tender."
                                                 "procuringEntity.contactPoint.telephone' is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_tender_procuring_entity_contact_point_fax_is_empty_str_27557_22(self, country,
                                                                             language, instance,
                                                                             cassandra_username,
                                                                             cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["contactPoint"]["faxNumber"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'tender.procuring"
                                                 "Entity.contactPoint.faxNumber' is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_tender_procuring_entity_contact_point_url_is_empty_str_27557_23(self, country,
                                                                             language, instance,
                                                                             cassandra_username,
                                                                             cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["contactPoint"]["url"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'tender.procuring"
                                                 "Entity.contactPoint.url' is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_buyer_name_is_empty_str_27557_24(self, country, language, instance, cassandra_username,
                                              cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["name"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'buyer.name' is "
                                                 "empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])

        )

    @pytestrail.case('27557')
    def test_buyer_identifier_id_is_empty_str_27557_25(self, country, language, instance, cassandra_username,
                                                       cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["identifier"]["id"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'buyer.identifier.id' "
                                                 "is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])

        )

    @pytestrail.case('27557')
    def test_buyer_identifier_scheme_is_empty_str_27557_26(self, country, language, instance, cassandra_username,
                                                           cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["identifier"]["scheme"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00.12", "description": "Registration scheme not found. "}]),
            actual_result=str(message_from_kafka['errors'])

        )

    @pytestrail.case('27557')
    def test_buyer_identifier_legal_name_is_empty_str_27557_27(self, country, language, instance, cassandra_username,
                                                               cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["identifier"]["legalName"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11", "description": "Incorrect an attribute value.The attribute "
                                                                         "'buyer.identifier.legalName' is empty or "
                                                                         "blank."}]),
            actual_result=str(message_from_kafka['errors'])

        )

    @pytestrail.case('27557')
    def test_buyer_identifier_uri_is_empty_str_27557_28(self, country, language, instance, cassandra_username,
                                                        cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["identifier"]["uri"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'buyer.identifier.uri' "
                                                 "is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])

        )

    @pytestrail.case('27557')
    def test_buyer_address_street_address_is_empty_str_27557_29(self, country, language, instance, cassandra_username,
                                                                cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["address"]["streetAddress"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'buyer.address."
                                                 "streetAddress' is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])

        )

    @pytestrail.case('27557')
    def test_buyer_address_postal_code_is_empty_str_27557_30(self, country, language, instance, cassandra_username,
                                                             cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["address"]["postalCode"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11", "description": "Incorrect an attribute value.The attribute "
                                                                         "'buyer.address.postalCode' is empty or "
                                                                         "blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_buyer_address_address_details_country_id_is_empty_str_27557_31(self, country, language, instance,
                                                                            cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00.11", "description": "Country not found. "}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_buyer_address_address_details_region_id_is_empty_str_27557_32(self, country, language, instance,
                                                                           cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["address"]["addressDetails"]["region"]["id"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00.13", "description": "Region not found. "}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_buyer_address_address_details_locality_id_is_empty_str_27557_33(self, country, language, instance,
                                                                             cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00.14", "description": "Locality not found. "}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_buyer_address_address_details_locality_id_is_empty_str_27557_34(self, country, language, instance,
                                                                             cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'buyer.address.address"
                                                 "Details.locality.scheme' is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_buyer_address_address_details_locality_id_is_empty_str_27557_35(self, country, language, instance,
                                                                             cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["address"]["addressDetails"]["region"]["id"] = \
            payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"]
        payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = \
            payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["id"]
        payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = \
            payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["scheme"]
        payload["buyer"]["address"]["addressDetails"]["locality"]["description"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        url_create = message_from_kafka['data']['url'] + '/' + message_from_kafka['data']['outcomes']['fs'][0]['id']
        fs_release = requests.get(url=url_create).json()
        buyer_obj = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                buyer_obj.append(p)
        mdm = MdmService(
            instance="dev",
            lang="ro",
            country=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]["id"],
            region=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"],
            locality=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["id"]
        )
        data = mdm.process_fs_data(cp_id).json()
        locality_from_mdm = data["data"]["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(locality_from_mdm["description"]),
            actual_result=str(buyer_obj[0]["address"]["addressDetails"]["locality"]["description"])
        )

    @pytestrail.case('27557')
    def test_buyer_additional_identifiers_id_is_empty_str_27557_36(self, country, language, instance,
                                                                   cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["additionalIdentifiers"][0]["id"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'buyer.additional"
                                                 "Identifiers.[0]id' is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_buyer_additional_identifiers_scheme_is_empty_str_27557_37(self, country, language, instance,
                                                                       cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["additionalIdentifiers"][0]["scheme"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'buyer.additional"
                                                 "Identifiers.[0]scheme' is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_buyer_additional_identifiers_legal_name_is_empty_str_27557_38(self, country, language, instance,
                                                                           cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["additionalIdentifiers"][0]["legalName"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'buyer.additional"
                                                 "Identifiers.[0]legalName' is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_buyer_additional_identifiers_uri_is_empty_str_27557_39(self, country, language, instance,
                                                                    cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["additionalIdentifiers"][0]["uri"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'buyer.additional"
                                                 "Identifiers.[0]uri' is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_buyer_contact_point_name_is_empty_str_27557_40(self, country, language, instance,
                                                            cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["contactPoint"]["name"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'buyer.contactPoint."
                                                 "name' is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_buyer_contact_point_email_is_empty_str_27557_41(self, country, language, instance,
                                                             cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["contactPoint"]["email"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'buyer.contactPoint."
                                                 "email' is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_buyer_contact_point_telephone_is_empty_str_27557_42(self, country, language, instance,
                                                                 cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["contactPoint"]["telephone"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'buyer.contactPoint."
                                                 "telephone' is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_buyer_contact_point_fax_is_empty_str_27557_43(self, country, language, instance,
                                                           cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["contactPoint"]["faxNumber"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'buyer.contactPoint."
                                                 "faxNumber' is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_buyer_contact_point_url_is_empty_str_27557_44(self, country, language, instance,
                                                           cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["contactPoint"]["url"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'buyer.contactPoint."
                                                 "url' is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_planning_rationale_is_empty_str_27557_45(self, country, language, instance,
                                                      cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["planning"]["rationale"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'planning.rationale' "
                                                 "is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_planning_budget_id_is_empty_str_27557_46(self, country, language, instance,
                                                      cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["planning"]["budget"]["id"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'planning.budget.id' "
                                                 "is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_planning_budget_description_is_empty_str_27557_47(self, country, language, instance,
                                                               cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["planning"]["budget"]["description"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'planning.budget."
                                                 "description' is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_planning_budget_period_start_date_is_empty_str_27557_48(self, country, language, instance,
                                                                     cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["planning"]["budget"]["period"]["startDate"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: Text '' "
                                                 "could not be parsed at index 0 (through reference chain: com."
                                                 "procurement.budget.model.dto.fs.request.FsCreate[\"planning\"]->"
                                                 "com.procurement.budget.model.dto.fs.request.PlanningFsCreate"
                                                 "[\"budget\"]->com.procurement.budget.model.dto.fs.request.Budget"
                                                 "FsCreate[\"period\"]->com.procurement.budget.model.dto.ocds."
                                                 "Period[\"startDate\"])"}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_planning_budget_period_end_date_is_empty_str_27557_49(self, country, language, instance,
                                                                   cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["planning"]["budget"]["period"]["endDate"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: Text '' "
                                                 "could not be parsed at index 0 (through reference chain: com."
                                                 "procurement.budget.model.dto.fs.request.FsCreate[\"planning\"]->"
                                                 "com.procurement.budget.model.dto.fs.request.PlanningFsCreate"
                                                 "[\"budget\"]->com.procurement.budget.model.dto.fs.request."
                                                 "BudgetFsCreate[\"period\"]->com.procurement.budget.model.dto.ocds."
                                                 "Period[\"endDate\"])"}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_planning_budget_amount_amount_is_empty_str_27557_50(self, country, language, instance,
                                                                 cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["planning"]["budget"]["amount"]["amount"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: amount "
                                                 "(through reference chain: com.procurement.budget.model.dto.fs."
                                                 "request.FsCreate[\"planning\"]->com.procurement.budget.model.dto."
                                                 "fs.request.PlanningFsCreate[\"budget\"]->com.procurement.budget."
                                                 "model.dto.fs.request.BudgetFsCreate[\"amount\"]->com.procurement."
                                                 "budget.model.dto.ocds.Value[\"amount\"])"}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_planning_budget_amount_currency_is_empty_str_27557_51(self, country, language, instance,
                                                                   cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["planning"]["budget"]["amount"]["currency"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00.10", "description": "Currency not found. "}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_planning_budget_is_european_union_funded_is_empty_str_27557_52(self, country, language, instance,
                                                                            cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["planning"]["budget"]["isEuropeanUnionFunded"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: "
                                                 "isEuropeanUnionFunded (through reference chain: com.procurement."
                                                 "budget.model.dto.fs.request.FsCreate[\"planning\"]->com."
                                                 "procurement.budget.model.dto.fs.request.PlanningFsCreate"
                                                 "[\"budget\"]->com.procurement.budget.model.dto.fs.request."
                                                 "BudgetFsCreate[\"isEuropeanUnionFunded\"])"}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_planning_budget_european_union_funding_project_name_is_empty_str_27557_53(self, country, language,
                                                                                       instance,
                                                                                       cassandra_username,
                                                                                       cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["planning"]["budget"]["europeanUnionFunding"]["projectName"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'planning.budget."
                                                 "europeanUnionFunding.projectName' is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_planning_budget_european_union_funding_project_identifier_is_empty_str_27557_54(self, country, language,
                                                                                             instance,
                                                                                             cassandra_username,
                                                                                             cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["planning"]["budget"]["europeanUnionFunding"]["projectIdentifier"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'planning.budget."
                                                 "europeanUnionFunding.projectIdentifier' is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_planning_budget_european_union_funding_uri_is_empty_str_27557_55(self, country, language,
                                                                              instance, cassandra_username,
                                                                              cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["planning"]["budget"]["europeanUnionFunding"]["uri"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'planning.budget."
                                                 "europeanUnionFunding.uri' is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_planning_budget_project_is_empty_str_27557_56(self, country, language, instance, cassandra_username,
                                                           cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["planning"]["budget"]["project"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'planning.budget."
                                                 "project' is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_planning_budget_project_id_is_empty_str_27557_57(self, country, language, instance, cassandra_username,
                                                              cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["planning"]["budget"]["projectID"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'planning.budget."
                                                 "projectID' is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )

    @pytestrail.case('27557')
    def test_planning_budget_uri_is_empty_str_27557_58(self, country, language, instance, cassandra_username,
                                                       cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["planning"]["budget"]["uri"] = ""
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        create_fs_response = fs.create_fs(cp_id)
        time.sleep(2)
        message_from_kafka = fs.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_fs_response.status_code)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.20.11",
                                  "description": "Incorrect an attribute value.The attribute 'planning.budget.uri' "
                                                 "is empty or blank."}]),
            actual_result=str(message_from_kafka['errors'])
        )


class TestCheckOnImpossibilityOfCreatingFsWithInvalidDataTypes(object):
    @pytestrail.case('27558')
    def test_tender_procuring_entity_name_address_as_bool_27558_1(self, country, language, instance, cassandra_username,
                                                                  cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["name"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was "
                                                 "com.procurement.mdm.exception.InErrorException) (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"tender\"]->com."
                                                 "procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]->"
                                                 "com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"name\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_tender_procuring_entity_identifier_id_address_as_bool_27558_2(self, country, language, instance,
                                                                           cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["identifier"]["id"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: "
                                                 "(was com.procurement.mdm.exception.InErrorException) (through "
                                                 "reference chain: com.procurement.mdm.model.dto.data.FS[\"tender\"]"
                                                 "->com.procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]"
                                                 "->com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"identifier\"]->com.procurement.mdm.model.dto.data.Identifier"
                                                 "[\"id\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_tender_procuring_entity_identifier_scheme_address_as_bool_27558_3(self, country, language, instance,
                                                                               cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["identifier"]["scheme"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was "
                                                 "com.procurement.mdm.exception.InErrorException) (through "
                                                 "reference chain: com.procurement.mdm.model.dto.data.FS"
                                                 "[\"tender\"]->com.procurement.mdm.model.dto.data.TenderFS"
                                                 "[\"procuringEntity\"]->com.procurement.mdm.model.dto.data."
                                                 "OrganizationReference[\"identifier\"]->com.procurement.mdm.model."
                                                 "dto.data.Identifier[\"scheme\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_tender_procuring_entity_identifier_legal_name_address_as_bool_27558_4(self, country, language, instance,
                                                                                   cassandra_username,
                                                                                   cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["identifier"]["legalName"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was com."
                                                 "procurement.mdm.exception.InErrorException) (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"tender\"]->com."
                                                 "procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]->com."
                                                 "procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"identifier\"]->com.procurement.mdm.model.dto.data.Identifier"
                                                 "[\"legalName\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_tender_procuring_entity_identifier_uri_address_as_bool_27558_5(self, country, language, instance,
                                                                            cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["identifier"]["uri"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was com."
                                                 "procurement.mdm.exception.InErrorException) (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"tender\"]->com."
                                                 "procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]->"
                                                 "com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"identifier\"]->com.procurement.mdm.model.dto.data.Identifier"
                                                 "[\"uri\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_tender_procuring_entity_address_street_address_as_bool_27558_6(self, country, language, instance,
                                                                            cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["address"]["streetAddress"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was com."
                                                 "procurement.mdm.exception.InErrorException) (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"tender\"]->com."
                                                 "procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]->com."
                                                 "procurement.mdm.model.dto.data.OrganizationReference[\"address\"]->"
                                                 "com.procurement.mdm.model.dto.data.Address[\"streetAddress\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_tender_procuring_entity_address_postal_code_as_bool_27558_7(self, country, language, instance,
                                                                         cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["address"]["postalCode"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: "
                                                 "(was com.procurement.mdm.exception.InErrorException) "
                                                 "(through reference chain: com.procurement.mdm.model.dto.data."
                                                 "FS[\"tender\"]->com.procurement.mdm.model.dto.data.TenderFS"
                                                 "[\"procuringEntity\"]->com.procurement.mdm.model.dto.data."
                                                 "OrganizationReference[\"address\"]->com.procurement.mdm.model."
                                                 "dto.data.Address[\"postalCode\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_tender_procuring_entity_address_address_detail_country_id_as_bool_27558_8(self, country, language,
                                                                                       instance,
                                                                                       cassandra_username,
                                                                                       cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]["id"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was com."
                                                 "procurement.mdm.exception.InErrorException) (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"tender\"]->com."
                                                 "procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]->"
                                                 "com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"address\"]->com.procurement.mdm.model.dto.data.Address"
                                                 "[\"addressDetails\"]->com.procurement.mdm.model.dto.data."
                                                 "AddressDetails[\"country\"]->com.procurement.mdm.model.dto."
                                                 "data.CountryDetails[\"id\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_tender_procuring_entity_address_address_detail_region_id_as_bool_27558_9(self, country, language, instance,
                                                                                      cassandra_username,
                                                                                      cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was com."
                                                 "procurement.mdm.exception.InErrorException) (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"tender\"]->com."
                                                 "procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]->com."
                                                 "procurement.mdm.model.dto.data.OrganizationReference[\"address\"]->"
                                                 "com.procurement.mdm.model.dto.data.Address[\"addressDetails\"]->"
                                                 "com.procurement.mdm.model.dto.data.AddressDetails[\"region\"]->"
                                                 "com.procurement.mdm.model.dto.data.RegionDetails[\"id\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_tender_procuring_entity_address_address_detail_locality_id_as_bool_27558_10(self, country, language,
                                                                                         instance,
                                                                                         cassandra_username,
                                                                                         cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["id"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was com."
                                                 "procurement.mdm.exception.InErrorException) (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"tender\"]->com."
                                                 "procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]->"
                                                 "com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"address\"]->com.procurement.mdm.model.dto.data.Address"
                                                 "[\"addressDetails\"]->com.procurement.mdm.model.dto.data.Address"
                                                 "Details[\"locality\"]->com.procurement.mdm.model.dto.data.Locality"
                                                 "Details[\"id\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_tender_procuring_entity_address_address_detail_locality_scheme_as_bool_27558_11(self, country, language,
                                                                                             instance,
                                                                                             cassandra_username,
                                                                                             cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["scheme"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was com."
                                                 "procurement.mdm.exception.InErrorException) (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"tender\"]->com."
                                                 "procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]->com."
                                                 "procurement.mdm.model.dto.data.OrganizationReference[\"address\"]"
                                                 "->com.procurement.mdm.model.dto.data.Address[\"addressDetails\"]"
                                                 "->com.procurement.mdm.model.dto.data.AddressDetails[\"locality\"]"
                                                 "->com.procurement.mdm.model.dto.data.LocalityDetails[\"scheme\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_tender_procuring_entity_address_address_detail_locality_description_as_bool_27558_12(self, country,
                                                                                                  language,
                                                                                                  instance,
                                                                                                  cassandra_username,
                                                                                                  cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["description"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was com."
                                                 "procurement.mdm.exception.InErrorException) (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"tender\"]->com."
                                                 "procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]->"
                                                 "com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"address\"]->com.procurement.mdm.model.dto.data.Address"
                                                 "[\"addressDetails\"]->com.procurement.mdm.model.dto.data."
                                                 "AddressDetails[\"locality\"]->com.procurement.mdm.model.dto."
                                                 "data.LocalityDetails[\"description\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_tender_procuring_entity_additional_identifiers_id_as_bool27558_13(self, country, language,
                                                                               instance, cassandra_username,
                                                                               cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["id"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was com."
                                                 "procurement.mdm.exception.InErrorException) (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"tender\"]->com."
                                                 "procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]->"
                                                 "com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"additionalIdentifiers\"]->java.util.ArrayList[0]->com."
                                                 "procurement.mdm.model.dto.data.Identifier[\"id\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_tender_procuring_entity_additional_identifiers_scheme_as_bool_27558_14(self, country, language,
                                                                                    instance, cassandra_username,
                                                                                    cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["scheme"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was com."
                                                 "procurement.mdm.exception.InErrorException) (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"tender\"]->com."
                                                 "procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]->"
                                                 "com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"additionalIdentifiers\"]->java.util.ArrayList[0]->com."
                                                 "procurement.mdm.model.dto.data.Identifier[\"scheme\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_tender_procuring_entity_additional_identifiers_legal_name_as_bool_27558_15(self, country, language,
                                                                                        instance, cassandra_username,
                                                                                        cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["legalName"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was com."
                                                 "procurement.mdm.exception.InErrorException) (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"tender\"]->com."
                                                 "procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]->com."
                                                 "procurement.mdm.model.dto.data.OrganizationReference[\"additional"
                                                 "Identifiers\"]->java.util.ArrayList[0]->com.procurement.mdm.model."
                                                 "dto.data.Identifier[\"legalName\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_tender_procuring_entity_additional_identifiers_uri_as_bool_27558_16(self, country, language,
                                                                                 instance, cassandra_username,
                                                                                 cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["uri"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was com."
                                                 "procurement.mdm.exception.InErrorException) (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"tender\"]->com."
                                                 "procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]->"
                                                 "com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"additionalIdentifiers\"]->java.util.ArrayList[0]->com."
                                                 "procurement.mdm.model.dto.data.Identifier[\"uri\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_tender_procuring_entity_contact_point_name_as_bool_27558_17(self, country, language,
                                                                         instance, cassandra_username,
                                                                         cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["contactPoint"]["name"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was com."
                                                 "procurement.mdm.exception.InErrorException) (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"tender\"]->com."
                                                 "procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]->"
                                                 "com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"contactPoint\"]->com.procurement.mdm.model.dto.data."
                                                 "ContactPoint[\"name\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_tender_procuring_entity_contact_point_email_as_bool_27558_18(self, country, language,
                                                                          instance, cassandra_username,
                                                                          cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["contactPoint"]["email"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was com."
                                                 "procurement.mdm.exception.InErrorException) (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"tender\"]->com."
                                                 "procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]->"
                                                 "com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"contactPoint\"]->com.procurement.mdm.model.dto.data."
                                                 "ContactPoint[\"email\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_tender_procuring_entity_contact_point_telephone_as_bool_27558_19(self, country, language,
                                                                              instance, cassandra_username,
                                                                              cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["contactPoint"]["telephone"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was com."
                                                 "procurement.mdm.exception.InErrorException) (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"tender\"]->com."
                                                 "procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]->com."
                                                 "procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"contactPoint\"]->com.procurement.mdm.model.dto.data."
                                                 "ContactPoint[\"telephone\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_tender_procuring_entity_contact_point_fax_number_as_bool_27558_20(self, country, language,
                                                                               instance, cassandra_username,
                                                                               cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["contactPoint"]["faxNumber"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was com."
                                                 "procurement.mdm.exception.InErrorException) (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"tender\"]->com."
                                                 "procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]->"
                                                 "com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"contactPoint\"]->com.procurement.mdm.model.dto.data."
                                                 "ContactPoint[\"faxNumber\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_tender_procuring_entity_contact_point_url_as_bool_27558_21(self, country, language,
                                                                        instance, cassandra_username,
                                                                        cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["tender"]["procuringEntity"]["contactPoint"]["url"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was com."
                                                 "procurement.mdm.exception.InErrorException) (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"tender\"]->com."
                                                 "procurement.mdm.model.dto.data.TenderFS[\"procuringEntity\"]->com."
                                                 "procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"contactPoint\"]->com.procurement.mdm.model.dto.data.Contact"
                                                 "Point[\"url\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_buyer_name_as_bool_27558_22(self, country, language,
                                         instance, cassandra_username,
                                         cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["name"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was com."
                                                 "procurement.mdm.exception.InErrorException) (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"buyer\"]->com."
                                                 "procurement.mdm.model.dto.data.OrganizationReference[\"name\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_buyer_identifier_id_as_bool_27558_23(self, country, language,
                                                  instance, cassandra_username,
                                                  cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["identifier"]["id"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was "
                                                 "com.procurement.mdm.exception.InErrorException) (through "
                                                 "reference chain: com.procurement.mdm.model.dto.data.FS"
                                                 "[\"buyer\"]->com.procurement.mdm.model.dto.data.Organization"
                                                 "Reference[\"identifier\"]->com.procurement.mdm.model.dto.data."
                                                 "Identifier[\"id\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_buyer_identifier_scheme_as_bool_27558_24(self, country, language,
                                                      instance, cassandra_username,
                                                      cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["identifier"]["scheme"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was com."
                                                 "procurement.mdm.exception.InErrorException) (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"buyer\"]->com."
                                                 "procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"identifier\"]->com.procurement.mdm.model.dto.data."
                                                 "Identifier[\"scheme\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_buyer_identifier_legal_name_as_bool_27558_25(self, country, language,
                                                          instance, cassandra_username,
                                                          cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["identifier"]["legalName"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was "
                                                 "com.procurement.mdm.exception.InErrorException) (through "
                                                 "reference chain: com.procurement.mdm.model.dto.data.FS[\"buyer\"]"
                                                 "->com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"identifier\"]->com.procurement.mdm.model.dto.data."
                                                 "Identifier[\"legalName\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_buyer_identifier_uri_as_bool_27558_26(self, country, language,
                                                   instance, cassandra_username,
                                                   cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["identifier"]["uri"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was "
                                                 "com.procurement.mdm.exception.InErrorException) (through "
                                                 "reference chain: com.procurement.mdm.model.dto.data.FS"
                                                 "[\"buyer\"]->com.procurement.mdm.model.dto.data.Organization"
                                                 "Reference[\"identifier\"]->com.procurement.mdm.model.dto.data."
                                                 "Identifier[\"uri\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_buyer_address_street_address_as_bool_27558_27(self, country, language,
                                                           instance, cassandra_username,
                                                           cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["address"]["streetAddress"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was com."
                                                 "procurement.mdm.exception.InErrorException) (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"buyer\"]->com."
                                                 "procurement.mdm.model.dto.data.OrganizationReference[\"address\"]"
                                                 "->com.procurement.mdm.model.dto.data.Address[\"streetAddress\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_buyer_address_postal_code_as_bool_27558_28(self, country, language,
                                                        instance, cassandra_username,
                                                        cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["address"]["postalCode"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was com."
                                                 "procurement.mdm.exception.InErrorException) (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"buyer\"]->com."
                                                 "procurement.mdm.model.dto.data.OrganizationReference[\"address\"]"
                                                 "->com.procurement.mdm.model.dto.data.Address[\"postalCode\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_buyer_address_address_details_country_id_as_bool_27558_29(self, country, language,
                                                                       instance, cassandra_username,
                                                                       cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{'code': '400.20.00',
                                  'description': 'com.fasterxml.jackson.databind.JsonMappingException: (was com.'
                                                 'procurement.mdm.exception.InErrorException) (through reference '
                                                 'chain: com.procurement.mdm.model.dto.data.FS["buyer"]->com.'
                                                 'procurement.mdm.model.dto.data.OrganizationReference["address"]->'
                                                 'com.procurement.mdm.model.dto.data.Address["addressDetails"]->com.'
                                                 'procurement.mdm.model.dto.data.AddressDetails["country"]->com.'
                                                 'procurement.mdm.model.dto.data.CountryDetails["id"])'}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_buyer_address_address_details_region_id_as_bool_27558_30(self, country, language,
                                                                      instance, cassandra_username,
                                                                      cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["address"]["addressDetails"]["region"]["id"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was "
                                                 "com.procurement.mdm.exception.InErrorException) (through "
                                                 "reference chain: com.procurement.mdm.model.dto.data.FS"
                                                 "[\"buyer\"]->com.procurement.mdm.model.dto.data.Organization"
                                                 "Reference[\"address\"]->com.procurement.mdm.model.dto.data."
                                                 "Address[\"addressDetails\"]->com.procurement.mdm.model.dto."
                                                 "data.AddressDetails[\"region\"]->com.procurement.mdm.model."
                                                 "dto.data.RegionDetails[\"id\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_buyer_address_address_details_locality_id_as_bool_27558_31(self, country, language,
                                                                        instance, cassandra_username,
                                                                        cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was com."
                                                 "procurement.mdm.exception.InErrorException) (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"buyer\"]->com."
                                                 "procurement.mdm.model.dto.data.OrganizationReference[\"address\"]"
                                                 "->com.procurement.mdm.model.dto.data.Address[\"addressDetails\"]"
                                                 "->com.procurement.mdm.model.dto.data.AddressDetails[\"locality\"]"
                                                 "->com.procurement.mdm.model.dto.data.LocalityDetails[\"id\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_buyer_address_address_details_locality_scheme_as_bool_27558_32(self, country, language,
                                                                            instance, cassandra_username,
                                                                            cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was "
                                                 "com.procurement.mdm.exception.InErrorException) (through "
                                                 "reference chain: com.procurement.mdm.model.dto.data.FS[\"buyer\"]"
                                                 "->com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"address\"]->com.procurement.mdm.model.dto.data.Address"
                                                 "[\"addressDetails\"]->com.procurement.mdm.model.dto.data."
                                                 "AddressDetails[\"locality\"]->com.procurement.mdm.model.dto."
                                                 "data.LocalityDetails[\"scheme\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_buyer_address_address_details_locality_description_as_bool_27558_33(self, country, language,
                                                                                 instance, cassandra_username,
                                                                                 cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["address"]["addressDetails"]["locality"]["description"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was "
                                                 "com.procurement.mdm.exception.InErrorException) (through "
                                                 "reference chain: com.procurement.mdm.model.dto.data.FS[\"buyer\"]"
                                                 "->com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"address\"]->com.procurement.mdm.model.dto.data.Address"
                                                 "[\"addressDetails\"]->com.procurement.mdm.model.dto.data."
                                                 "AddressDetails[\"locality\"]->com.procurement.mdm.model.dto."
                                                 "data.LocalityDetails[\"description\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_buyer_additional_identifiers_id_as_bool_27558_34(self, country, language, instance, cassandra_username,
                                                              cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["additionalIdentifiers"][0]["id"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: "
                                                 "(was com.procurement.mdm.exception.InErrorException) (through "
                                                 "reference chain: com.procurement.mdm.model.dto.data.FS[\"buyer\"]"
                                                 "->com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"additionalIdentifiers\"]->java.util.ArrayList[0]->com."
                                                 "procurement.mdm.model.dto.data.Identifier[\"id\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_buyer_additional_identifiers_scheme_as_bool_27558_35(self, country, language, instance, cassandra_username,
                                                                  cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["additionalIdentifiers"][0]["scheme"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was "
                                                 "com.procurement.mdm.exception.InErrorException) (through "
                                                 "reference chain: com.procurement.mdm.model.dto.data.FS[\"buyer\"]"
                                                 "->com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"additionalIdentifiers\"]->java.util.ArrayList[0]->com."
                                                 "procurement.mdm.model.dto.data.Identifier[\"scheme\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_buyer_additional_identifiers_legal_name_as_bool_27558_36(self, country, language, instance,
                                                                      cassandra_username,
                                                                      cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["additionalIdentifiers"][0]["legalName"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was "
                                                 "com.procurement.mdm.exception.InErrorException) (through "
                                                 "reference chain: com.procurement.mdm.model.dto.data.FS[\"buyer\"]"
                                                 "->com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"additionalIdentifiers\"]->java.util.ArrayList[0]->com."
                                                 "procurement.mdm.model.dto.data.Identifier[\"legalName\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_buyer_additional_identifiers_uri_as_bool_27558_37(self, country, language, instance,
                                                               cassandra_username,
                                                               cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["additionalIdentifiers"][0]["uri"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was com."
                                                 "procurement.mdm.exception.InErrorException) (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"buyer\"]->com."
                                                 "procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"additionalIdentifiers\"]->java.util.ArrayList[0]->com."
                                                 "procurement.mdm.model.dto.data.Identifier[\"uri\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_buyer_contact_point_name_as_bool_27558_38(self, country, language, instance,
                                                       cassandra_username,
                                                       cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["contactPoint"]["name"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was "
                                                 "com.procurement.mdm.exception.InErrorException) (through "
                                                 "reference chain: com.procurement.mdm.model.dto.data.FS[\"buyer\"]"
                                                 "->com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"contactPoint\"]->com.procurement.mdm.model.dto.data."
                                                 "ContactPoint[\"name\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_buyer_contact_point_email_as_bool_27558_39(self, country, language, instance,
                                                        cassandra_username,
                                                        cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["contactPoint"]["email"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was com."
                                                 "procurement.mdm.exception.InErrorException) (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"buyer\"]->com."
                                                 "procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"contactPoint\"]->com.procurement.mdm.model.dto.data."
                                                 "ContactPoint[\"email\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_buyer_contact_point_telephone_as_bool_27558_40(self, country, language, instance,
                                                            cassandra_username,
                                                            cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["contactPoint"]["telephone"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: "
                                                 "(was com.procurement.mdm.exception.InErrorException) "
                                                 "(through reference chain: com.procurement.mdm.model.dto.data."
                                                 "FS[\"buyer\"]->com.procurement.mdm.model.dto.data.Organization"
                                                 "Reference[\"contactPoint\"]->com.procurement.mdm.model.dto.data."
                                                 "ContactPoint[\"telephone\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_buyer_contact_point_fax_number_as_bool_27558_41(self, country, language, instance,
                                                             cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["contactPoint"]["faxNumber"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: "
                                                 "(was com.procurement.mdm.exception.InErrorException) (through "
                                                 "reference chain: com.procurement.mdm.model.dto.data.FS[\"buyer\"]"
                                                 "->com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"contactPoint\"]->com.procurement.mdm.model.dto.data.Contact"
                                                 "Point[\"faxNumber\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_buyer_contact_point_url_as_bool_27558_42(self, country, language, instance,
                                                      cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["buyer"]["contactPoint"]["url"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was "
                                                 "com.procurement.mdm.exception.InErrorException) (through "
                                                 "reference chain: com.procurement.mdm.model.dto.data.FS[\"buyer\"]"
                                                 "->com.procurement.mdm.model.dto.data.OrganizationReference"
                                                 "[\"contactPoint\"]->com.procurement.mdm.model.dto.data.Contact"
                                                 "Point[\"url\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_planning_rationale_as_bool_27558_43(self, country, language, instance,
                                                 cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["planning"]["rationale"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: rationale "
                                                 "(through reference chain: com.procurement.budget.model.dto.fs."
                                                 "request.FsCreate[\"planning\"]->com.procurement.budget.model."
                                                 "dto.fs.request.PlanningFsCreate[\"rationale\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_planning_budget_id_as_bool_27558_44(self, country, language, instance,
                                                 cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["planning"]["budget"]["id"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: id "
                                                 "(through reference chain: com.procurement.budget.model.dto.fs."
                                                 "request.FsCreate[\"planning\"]->com.procurement.budget.model."
                                                 "dto.fs.request.PlanningFsCreate[\"budget\"]->com.procurement."
                                                 "budget.model.dto.fs.request.BudgetFsCreate[\"id\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_planning_budget_description_as_bool_27558_45(self, country, language, instance,
                                                          cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["planning"]["budget"]["description"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: description "
                                                 "(through reference chain: com.procurement.budget.model.dto.fs."
                                                 "request.FsCreate[\"planning\"]->com.procurement.budget.model."
                                                 "dto.fs.request.PlanningFsCreate[\"budget\"]->com.procurement."
                                                 "budget.model.dto.fs.request.BudgetFsCreate[\"description\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_planning_budget_period_start_date_as_bool_27558_46(self, country, language, instance,
                                                                cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["planning"]["budget"]["period"]["startDate"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: Text 'true' "
                                                 "could not be parsed at index 0 (through reference chain: com."
                                                 "procurement.budget.model.dto.fs.request.FsCreate[\"planning\"]->"
                                                 "com.procurement.budget.model.dto.fs.request.PlanningFsCreate"
                                                 "[\"budget\"]->com.procurement.budget.model.dto.fs.request."
                                                 "BudgetFsCreate[\"period\"]->com.procurement.budget.model.dto."
                                                 "ocds.Period[\"startDate\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_planning_budget_period_end_date_as_bool_27558_47(self, country, language, instance,
                                                              cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["planning"]["budget"]["period"]["endDate"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: Text 'true' "
                                                 "could not be parsed at index 0 (through reference chain: com."
                                                 "procurement.budget.model.dto.fs.request.FsCreate[\"planning\"]->"
                                                 "com.procurement.budget.model.dto.fs.request.PlanningFsCreate"
                                                 "[\"budget\"]->com.procurement.budget.model.dto.fs.request.Budget"
                                                 "FsCreate[\"period\"]->com.procurement.budget.model.dto.ocds."
                                                 "Period[\"endDate\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_planning_budget_amount_amount_as_bool_27558_48(self, country, language, instance,
                                                            cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["planning"]["budget"]["amount"]["amount"] = "2000.0"
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: amount "
                                                 "(through reference chain: com.procurement.budget.model.dto.fs."
                                                 "request.FsCreate[\"planning\"]->com.procurement.budget.model."
                                                 "dto.fs.request.PlanningFsCreate[\"budget\"]->com.procurement."
                                                 "budget.model.dto.fs.request.BudgetFsCreate[\"amount\"]->com."
                                                 "procurement.budget.model.dto.ocds.Value[\"amount\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_planning_budget_amount_currency_as_bool_27558_49(self, country, language, instance,
                                                              cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["planning"]["budget"]["amount"]["currency"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.20.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: (was com."
                                                 "procurement.mdm.exception.InErrorException) (through reference "
                                                 "chain: com.procurement.mdm.model.dto.data.FS[\"planning\"]->com."
                                                 "procurement.mdm.model.dto.data.PlanningFS[\"budget\"]->com."
                                                 "procurement.mdm.model.dto.data.BudgetFS[\"amount\"]->com."
                                                 "procurement.mdm.model.dto.data.ValueFS[\"currency\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_planning_budget_is_european_union_funded_as_bool_27558_50(self, country, language, instance,
                                                                       cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["planning"]["budget"]["isEuropeanUnionFunded"] = str(True)
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: "
                                                 "isEuropeanUnionFunded (through reference chain: com.procurement."
                                                 "budget.model.dto.fs.request.FsCreate[\"planning\"]->com."
                                                 "procurement.budget.model.dto.fs.request.PlanningFsCreate"
                                                 "[\"budget\"]->com.procurement.budget.model.dto.fs.request.Budget"
                                                 "FsCreate[\"isEuropeanUnionFunded\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_planning_budget_european_union_funding_project_name_as_bool_27558_51(self, country, language, instance,
                                                                                  cassandra_username,
                                                                                  cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["planning"]["budget"]["europeanUnionFunding"]["projectName"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: projectName "
                                                 "(through reference chain: com.procurement.budget.model.dto.fs."
                                                 "request.FsCreate[\"planning\"]->com.procurement.budget.model."
                                                 "dto.fs.request.PlanningFsCreate[\"budget\"]->com.procurement."
                                                 "budget.model.dto.fs.request.BudgetFsCreate[\"europeanUnion"
                                                 "Funding\"]->com.procurement.budget.model.dto.ocds.EuropeanUnion"
                                                 "Funding[\"projectName\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_planning_budget_european_union_funding_project_name_as_bool_27558_52(self, country, language, instance,
                                                                                  cassandra_username,
                                                                                  cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["planning"]["budget"]["europeanUnionFunding"]["projectIdentifier"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: "
                                                 "projectIdentifier (through reference chain: com.procurement."
                                                 "budget.model.dto.fs.request.FsCreate[\"planning\"]->com."
                                                 "procurement.budget.model.dto.fs.request.PlanningFsCreate"
                                                 "[\"budget\"]->com.procurement.budget.model.dto.fs.request."
                                                 "BudgetFsCreate[\"europeanUnionFunding\"]->com.procurement."
                                                 "budget.model.dto.ocds.EuropeanUnionFunding"
                                                 "[\"projectIdentifier\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_planning_budget_european_union_funding_uri_as_bool_27558_53(self, country, language, instance,
                                                                         cassandra_username,
                                                                         cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["planning"]["budget"]["europeanUnionFunding"]["uri"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: uri "
                                                 "(through reference chain: com.procurement.budget.model.dto.fs."
                                                 "request.FsCreate[\"planning\"]->com.procurement.budget.model."
                                                 "dto.fs.request.PlanningFsCreate[\"budget\"]->com.procurement."
                                                 "budget.model.dto.fs.request.BudgetFsCreate[\"europeanUnion"
                                                 "Funding\"]->com.procurement.budget.model.dto.ocds.European"
                                                 "UnionFunding[\"uri\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_planning_budget_project_as_bool_27558_54(self, country, language, instance,
                                                      cassandra_username,
                                                      cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["planning"]["budget"]["project"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: project "
                                                 "(through reference chain: com.procurement.budget.model.dto.fs."
                                                 "request.FsCreate[\"planning\"]->com.procurement.budget.model.dto."
                                                 "fs.request.PlanningFsCreate[\"budget\"]->com.procurement.budget."
                                                 "model.dto.fs.request.BudgetFsCreate[\"project\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_planning_budget_project_id_as_bool_27558_55(self, country, language, instance,
                                                         cassandra_username,
                                                         cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["planning"]["budget"]["projectID"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: projectID "
                                                 "(through reference chain: com.procurement.budget.model.dto.fs."
                                                 "request.FsCreate[\"planning\"]->com.procurement.budget.model."
                                                 "dto.fs.request.PlanningFsCreate[\"budget\"]->com.procurement."
                                                 "budget.model.dto.fs.request.BudgetFsCreate[\"projectID\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    @pytestrail.case('27558')
    def test_planning_budget_uri_as_bool_27558_56(self, country, language, instance,
                                                  cassandra_username,
                                                  cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_fs_payload_fs_full_data_model_own_money)
        payload["planning"]["budget"]["uri"] = True
        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        fs.insert_ei_full_data_model(cp_id, ei_token)
        fs.create_fs(cp_id)
        message_from_kafka = fs.get_message_from_kafka()
        time.sleep(2)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{"code": "400.10.00",
                                  "description": "com.fasterxml.jackson.databind.JsonMappingException: uri "
                                                 "(through reference chain: com.procurement.budget.model.dto.fs."
                                                 "request.FsCreate[\"planning\"]->com.procurement.budget.model.dto."
                                                 "fs.request.PlanningFsCreate[\"budget\"]->com.procurement.budget."
                                                 "model.dto.fs.request.BudgetFsCreate[\"uri\"])"}]),
            actual_result=str(message_from_kafka["errors"])
        )

    # =========================
    # class TestCreateTreasuryMoneyFsOnFullDataModel(object):
    #     @pytestrail.case("24601")
    #     def test_send_the_request_24601_1(self, country, language, instance, cassandra_username,
    #                                       cassandra_password):
    #         cp_id = prepared_cp_id()
    #         ei_token = str(uuid4())
    #         payload = copy.deepcopy(payload_fs_full_data_model_treasury_money)
    #         fs = FS(
    #             payload=payload,
    #             lang=language,
    #             country=country,
    #             instance=instance,
    #             cassandra_username=cassandra_username,
    #             cassandra_password=cassandra_password
    #         )
    #         fs.insert_ei_full_data_model(cp_id, ei_token)
    #         create_fs_response = fs.create_fs(cp_id)
    #         assert compare_actual_result_and_expected_result(
    #             expected_result=str(202),
    #             actual_result=str(create_fs_response.status_code)
    #         )
    #
    #     @pytestrail.case("24601")
    #     def test_see_the_result_in_feed_point_point_24601_2(self, country, language, instance, cassandra_username,
    #                                                         cassandra_password):
    #         cp_id = prepared_cp_id()
    #         ei_token = str(uuid4())
    #         payload = copy.deepcopy(payload_fs_full_data_model_treasury_money)
    #         fs = FS(
    #             payload=payload,
    #             lang=language,
    #             country=country,
    #             instance=instance,
    #             cassandra_username=cassandra_username,
    #             cassandra_password=cassandra_password
    #         )
    #         fs.insert_ei_full_data_model(cp_id, ei_token)
    #         fs.create_fs(cp_id)
    #         fs.get_message_from_kafka()
    #         assert compare_actual_result_and_expected_result(
    #             expected_result=str(True),
    #             actual_result=str(fs.check_on_that_message_is_successfully_create_fs())
    #         )
    #
    #     @pytestrail.case("24601")
    #     def test_check_all_sent_information_is_published_24601_3(self, country, language, instance, cassandra_user
    #     name,
    #                                                              cassandra_password):
    #         cp_id = prepared_cp_id()
    #         ei_token = str(uuid4())
    #         payload = copy.deepcopy(payload_fs_full_data_model_treasury_money)
    #         fs = FS(
    #             payload=payload,
    #             lang=language,
    #             country=country,
    #             instance=instance,
    #             cassandra_username=cassandra_username,
    #             cassandra_password=cassandra_password
    #         )
    #         fs.insert_ei_full_data_model(cp_id, ei_token)
    #         fs.create_fs(cp_id)
    #         message_from_kafka = fs.get_message_from_kafka()
    #         time.sleep(2)
    #         url_create = message_from_kafka['data']['url'] + '/' + message_from_kafka['data']['outcomes']['fs'][0]
    #         ['id']

    # publicPoint_create = requests.get(url=url_create).json()
    # assert publicPoint_create['releases'][0]['planning']['budget']['id'] == \
    #        payload['planning']['budget']['id']
    # assert publicPoint_create['releases'][0]['planning']['budget']['description'] == \
    #        payload['planning']['budget']['description']
    # assert publicPoint_create['releases'][0]['planning']['budget']['period']['startDate'] == \
    #        payload['planning']['budget']['period']['startDate']
    # assert publicPoint_create['releases'][0]['planning']['budget']['period']['endDate'] == \
    #        payload['planning']['budget']['period']['endDate']
    # assert publicPoint_create['releases'][0]['planning']['budget']['amount']['amount'] == \
    #        payload['planning']['budget']['amount']['amount']
    # assert publicPoint_create['releases'][0]['planning']['budget']['amount']['currency'] == \
    #        payload['planning']['budget']['amount']['currency']
    # assert publicPoint_create['releases'][0]['planning']['budget']['europeanUnionFunding']['projectIdentifier'] == \
    #        payload['planning']['budget']['europeanUnionFunding']['projectIdentifier']
    # assert publicPoint_create['releases'][0]['planning']['budget']['europeanUnionFunding']['projectName'] == \
    #        payload['planning']['budget']['europeanUnionFunding']['projectName']
    # assert publicPoint_create['releases'][0]['planning']['budget']['europeanUnionFunding']['uri'] == \
    #        payload['planning']['budget']['europeanUnionFunding']['uri']
    # assert publicPoint_create['releases'][0]['planning']['budget']['isEuropeanUnionFunded'] == \
    #        payload['planning']['budget']['isEuropeanUnionFunded']
    # assert publicPoint_create['releases'][0]['planning']['budget']['project'] == \
    #        payload['planning']['budget']['project']
    # assert publicPoint_create['releases'][0]['planning']['budget']['projectID'] == \
    #        payload['planning']['budget']['projectID']
    # assert publicPoint_create['releases'][0]['planning']['budget']['uri'] == \
    #        payload['planning']['budget']['uri']
    # assert publicPoint_create['releases'][0]['planning']['rationale'] == \
    #        payload['planning']['rationale']
    # assert publicPoint_create['releases'][0]['parties'][0]['id'] == \
    #        payload['tender']['procuringEntity']['identifier']['scheme'] + '-' + \
    #        payload['tender']['procuringEntity']['identifier']['id']
    # assert publicPoint_create['releases'][0]['parties'][0]['name'] == \
    #        payload['tender']['procuringEntity']['name']
    # assert publicPoint_create['releases'][0]['parties'][0]['identifier']['scheme'] == \
    #        payload['tender']['procuringEntity']['identifier']['scheme']
    # assert publicPoint_create['releases'][0]['parties'][0]['identifier']['id'] == \
    #        payload['tender']['procuringEntity']['identifier']['id']
    # assert publicPoint_create['releases'][0]['parties'][0]['identifier']['legalName'] == \
    #        payload['tender']['procuringEntity']['identifier']['legalName']
    # assert publicPoint_create['releases'][0]['parties'][0]['identifier']['uri'] == \
    #        payload['tender']['procuringEntity']['identifier']['uri']
    # assert publicPoint_create['releases'][0]['parties'][0]['address']['streetAddress'] == \
    #        payload['tender']['procuringEntity']['address']['streetAddress']
    # assert publicPoint_create['releases'][0]['parties'][0]['address']['postalCode'] == \
    #        payload['tender']['procuringEntity']['address']['postalCode']
    # assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country']['id'] == \
    #        payload['tender']['procuringEntity']['address']['addressDetails']['country']['id']
    # assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['region']['id'] == \
    #        payload['tender']['procuringEntity']['address']['addressDetails']['region']['id']
    # assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality']['scheme'] == \
    #        payload['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme']
    # assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality']['id'] == \
    #        payload['tender']['procuringEntity']['address']['addressDetails']['locality']['id']
    # assert publicPoint_create['releases'][0]['parties'][0]['additionalIdentifiers'][0]['scheme'] == \
    #        payload['tender']['procuringEntity']['additionalIdentifiers'][0]['scheme']
    # assert publicPoint_create['releases'][0]['parties'][0]['additionalIdentifiers'][0]['id'] == \
    #        payload['tender']['procuringEntity']['additionalIdentifiers'][0]['id']
    # assert publicPoint_create['releases'][0]['parties'][0]['additionalIdentifiers'][0]['legalName'] == \
    #        payload['tender']['procuringEntity']['additionalIdentifiers'][0]['legalName']
    # assert publicPoint_create['releases'][0]['parties'][0]['additionalIdentifiers'][0]['uri'] == \
    #        payload['tender']['procuringEntity']['additionalIdentifiers'][0]['uri']
    # assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['name'] == \
    #        payload['tender']['procuringEntity']['contactPoint']['name']
    # assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['email'] == \
    #        payload['tender']['procuringEntity']['contactPoint']['email']
    # assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['telephone'] == \
    #        payload['tender']['procuringEntity']['contactPoint']['telephone']
    # assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['faxNumber'] == \
    #        payload['tender']['procuringEntity']['contactPoint']['faxNumber']
    # assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['url'] == \
    #        payload['tender']['procuringEntity']['contactPoint']['url']

# class TestCreateOwnMoneyFsWithObligatoryFieldsOnly(object):
#     @pytestrail.case("24604")
#     def test_send_the_request_24604_1(self, country, language, instance, cassandra_username, cassandra_password):
#         cp_id = prepared_cp_id()
#         ei_token = str(uuid4())
#         buyer_identifier_id = "987654321"
#         buyer_identifier_scheme = "MD-IDNO"
#         buyer_name = "LLC Petrusenko"
#         payload = copy.deepcopy(payload_fs_obligatory_data_model_treasury_money)
#         fs = FS(payload=payload, lang=language, country=country, instance=instance,
#                 cassandra_username=cassandra_username, cassandra_password=cassandra_password,
#                 buyer_identifier_id=buyer_identifier_id, buyer_identifier_scheme=buyer_identifier_scheme,
#                 buyer_name=buyer_name)
#         fs.insert_ei_obligatory_data_model(cp_id, ei_token)
#         create_fs_response = fs.create_fs(cp_id)
#         expected_result = str(202)
#         actual_result = str(create_fs_response.status_code)
#         assert compare_actual_result_and_expected_result(expected_result=expected_result,
#                                                          actual_result=actual_result)
#
#     @pytestrail.case("24604")
#     def test_see_the_result_in_feed_point_point_24604_2(self, country, language, instance, cassandra_username,
#                                                         cassandra_password):
#         cp_id = prepared_cp_id()
#         ei_token = str(uuid4())
#         buyer_identifier_id = "987654321"
#         buyer_identifier_scheme = "MD-IDNO"
#         buyer_name = "LLC Petrusenko"
#         payload = copy.deepcopy(payload_fs_obligatory_data_model_treasury_money)
#         fs = FS(payload=payload, lang=language, country=country, instance=instance,
#                 cassandra_username=cassandra_username, cassandra_password=cassandra_password,
#                 buyer_identifier_id=buyer_identifier_id, buyer_identifier_scheme=buyer_identifier_scheme,
#                 buyer_name=buyer_name)
#         fs.insert_ei_full_data_model(cp_id, ei_token)
#         fs.create_fs(cp_id)
#         fs.get_message_from_kafka()
#         actual_result = str(fs.check_on_that_message_is_successfully_create_fs())
#         expected_result = str(True)
#         assert compare_actual_result_and_expected_result(expected_result=expected_result,
#                                                          actual_result=actual_result)
#
#     @pytestrail.case('24604')
#     def test_check_all_sent_information_is_published_24604_3(self, country, language, instance, cassandra_username,
#                                                              cassandra_password):
#         cp_id = prepared_cp_id()
#         ei_token = str(uuid4())
#         buyer_identifier_id = "987654321"
#         buyer_identifier_scheme = "MD-IDNO"
#         buyer_name = "LLC Petrusenko"
#         payload = copy.deepcopy(payload_fs_obligatory_data_model_treasury_money)
#         fs = FS(payload=payload, lang=language, country=country, instance=instance,
#                 cassandra_username=cassandra_username, cassandra_password=cassandra_password,
#                 buyer_identifier_id=buyer_identifier_id, buyer_identifier_scheme=buyer_identifier_scheme,
#                 buyer_name=buyer_name)
#         fs.insert_ei_full_data_model(cp_id, ei_token)
#         fs.create_fs(cp_id)
#         message_from_kafka = fs.get_message_from_kafka()
#         time.sleep(2)
#         url_create = message_from_kafka['data']['url'] + '/' + message_from_kafka['data']['outcomes']['fs'][0]['id']
#         publicPoint_create = requests.get(url=url_create).json()
#         assert publicPoint_create['releases'][0]['planning']['budget']['period']['startDate'] == \
#                payload['planning']['budget']['period']['startDate']
#         assert publicPoint_create['releases'][0]['planning']['budget']['period']['endDate'] == \
#                payload['planning']['budget']['period']['endDate']
#         assert publicPoint_create['releases'][0]['planning']['budget']['amount']['amount'] == \
#                payload['planning']['budget']['amount']['amount']
#         assert publicPoint_create['releases'][0]['planning']['budget']['amount']['currency'] == \
#                payload['planning']['budget']['amount']['currency']
#         assert publicPoint_create['releases'][0]['planning']['budget']['isEuropeanUnionFunded'] == \
#                payload['planning']['budget']['isEuropeanUnionFunded']
#         assert publicPoint_create['releases'][0]['planning']['budget']['sourceEntity']['id'] == \
#                buyer_identifier_scheme + '-' + buyer_identifier_id
#         assert publicPoint_create['releases'][0]['planning']['budget']['sourceEntity']['name'] == buyer_name
#         assert publicPoint_create['releases'][0]['parties'][0]['id'] == \
#                payload['tender']['procuringEntity']['identifier']['scheme'] + '-' + \
#                payload['tender']['procuringEntity']['identifier']['id']
#         assert publicPoint_create['releases'][0]['parties'][0]['name'] == \
#                payload['tender']['procuringEntity']['name']
#         assert publicPoint_create['releases'][0]['parties'][0]['identifier']['scheme'] == \
#                payload['tender']['procuringEntity']['identifier']['scheme']
#         assert publicPoint_create['releases'][0]['parties'][0]['identifier']['id'] == \
#                payload['tender']['procuringEntity']['identifier']['id']
#         assert publicPoint_create['releases'][0]['parties'][0]['identifier']['legalName'] == \
#                payload['tender']['procuringEntity']['identifier']['legalName']
#         assert publicPoint_create['releases'][0]['parties'][0]['address']['streetAddress'] == \
#                payload['tender']['procuringEntity']['address']['streetAddress']
#         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country']['id'] == \
#                payload['tender']['procuringEntity']['address']['addressDetails']['country']['id']
#         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['region']['id'] == \
#                payload['tender']['procuringEntity']['address']['addressDetails']['region']['id']
#         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality']['scheme'] == \
#                payload['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme']
#         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality']['id'] == \
#                payload['tender']['procuringEntity']['address']['addressDetails']['locality']['id']
#         assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['name'] == \
#                payload['tender']['procuringEntity']['contactPoint']['name']
#         assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['email'] == \
#                payload['tender']['procuringEntity']['contactPoint']['email']
#         assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['telephone'] == \
#                payload['tender']['procuringEntity']['contactPoint']['telephone']
#         assert publicPoint_create['releases'][0]['parties'][0]['id'] == \
#                payload['tender']['procuringEntity']['identifier']['scheme'] + '-' + \
#                payload['tender']['procuringEntity']['identifier']['id']
#         assert publicPoint_create['releases'][0]['parties'][0]['name'] == payload['tender']['procuringEntity']['name']
#         assert publicPoint_create['releases'][0]['parties'][0]['identifier']['scheme'] == \
#                payload['tender']['procuringEntity']['identifier']['scheme']
#         assert publicPoint_create['releases'][0]['parties'][0]['identifier']['id'] == \
#                payload['tender']['procuringEntity']['identifier']['id']
#         assert publicPoint_create['releases'][0]['parties'][0]['identifier']['legalName'] == \
#                payload['tender']['procuringEntity']['identifier']['legalName']
#         assert publicPoint_create['releases'][0]['parties'][0]['address']['streetAddress'] == \
#                payload['tender']['procuringEntity']['address']['streetAddress']
#         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country']['id'] == \
#                payload['tender']['procuringEntity']['address']['addressDetails']['country']['id']
#         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['region']['id'] == \
#                payload['tender']['procuringEntity']['address']['addressDetails']['region']['id']
#         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality']['scheme'] == \
#                payload['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme']
#         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality']['id'] == \
#                payload['tender']['procuringEntity']['address']['addressDetails']['locality']['id']
#         assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['name'] == \
#                payload['tender']['procuringEntity']['contactPoint']['name']
#         assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['email'] == \
#                payload['tender']['procuringEntity']['contactPoint']['email']
#         assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['telephone'] == \
#                payload['tender']['procuringEntity']['contactPoint']['telephone']


# #
# #     @pytestrail.case('24605')
# #     def test_24605_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['tender']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.00.00.00'
# #         assert create_fs_response[1]['errors'][0]['description'] == 'Data processing exception.'
# #
# #     @pytestrail.case('24605')
# #     def test_24605_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['tender']['procuringEntity']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
# #         assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
# #                                                                     'KotlinParameterException: Instantiation of ' \
# #                                                                     '[simple type, class com.procurement.budget.' \
# #                                                                     'model.dto.fs.request.TenderFsCreate] value ' \
# #                                                                     'failed for JSON property procuringEntity
# due ' \
# #                                                                     'to missing (therefore NULL) value for
# creator ' \
# #                                                                     'parameter procuringEntity which is a non-' \
# #                                                                     'nullable type\n at [Source: UNKNOWN; line: ' \
# #                                                                     '-1, column: -1] (through reference
# chain: com.' \
# #                                                                     'procurement.budget.model.dto.fs.request.Fs' \
# #                                                                     'Create[\"tender\"]->com.procurement.budget.' \
# #                                                                     'model.dto.fs.request.TenderFsCreate' \
# #                                                                     '[\"procuringEntity\"])'
# #
# #     @pytestrail.case('24605')
# #     def test_24605_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['tender']['procuringEntity']['name']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
# #         assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
# #                                                                     'KotlinParameterException: Instantiation of ' \
# #                                                                     '[simple type, class com.procurement.budget.' \
# #                                                                     'model.dto.fs.OrganizationReferenceFs] value ' \
# #                                                                     'failed for JSON property name due to
# missing ' \
# #                                                                     '(therefore NULL) value for creator
# parameter ' \
# #                                                                     'name which is a non-nullable type\n
# at [Source:' \
# #                                                                     ' UNKNOWN; line: -1, column: -1] (through ' \
# #                                                                     'reference chain: com.procurement.budget.' \
# #                                                                     'model.dto.fs.request.FsCreate[\"tender\"]->' \
# #                                                                     'com.procurement.budget.model.dto.fs.request.' \
# #                                                                     'TenderFsCreate[\"procuringEntity\"]->com.' \
# #                                                                     'procurement.budget.model.dto.fs.Organization' \
# #                                                                     'ReferenceFs[\"name\"])'
# #
# #     @pytestrail.case('24605')
# #     def test_24605_4(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['tender']['procuringEntity']['identifier']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
# #         assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
# #                                                                     'KotlinParameterException: Instantiation of ' \
# #                                                                     '[simple type, class com.procurement.budget.' \
# #                                                                     'model.dto.fs.OrganizationReferenceFs] value ' \
# #                                                                     'failed for JSON property identifier due to ' \
# #                                                                     'missing (therefore NULL) value for creator ' \
# #                                                                     'parameter identifier which is a non-
# nullable ' \
# #                                                                     'type\n at [Source: UNKNOWN; line: -1,
# column:' \
# #                                                                     ' -1] (through reference chain: com.
# procurement.' \
# #                                                                     'budget.model.dto.fs.request.FsCreate' \
# #                                                                     '[\"tender\"]->com.procurement.budget.model.' \
# #                                                                     'dto.fs.request.TenderFsCreate[\"procuring' \
# #                                                                     'Entity\"]->com.procurement.budget.model.
# dto.fs.' \
# #                                                                     'OrganizationReferenceFs[\"identifier\"])'
# #
# #     @pytestrail.case('24605')
# #     def test_24605_5(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['tender']['procuringEntity']['identifier']['id']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
# #                                                                     'KotlinParameterException: Instantiation of [' \
# #                                                                     'simple type, class com.procurement.mdm.
# model.' \
# #                                                                     'dto.data.Identifier] value failed for JSON ' \
# #                                                                     'property id due to missing (therefore NULL) ' \
# #                                                                     'value for creator parameter id which is
# a non-' \
# #                                                                     'nullable type\n at [Source: UNKNOWN;
# line: -1, ' \
# #                                                                     'column: -1] (through reference chain: com.' \
# #                                                                     'procurement.mdm.model.dto.data.FS[\"
# tender\"]->' \
# #                                                                     'com.procurement.mdm.model.dto.data.TenderFS' \
# #                                                                     '[\"procuringEntity\"]->com.procurement.mdm.' \
# #                                                                     'model.dto.data.OrganizationReference' \
# #                                                                     '[\"identifier\"]->com.procurement.mdm.model.' \
# #                                                                     'dto.data.Identifier[\"id\"])'
# #
# #     @pytestrail.case('24605')
# #     def test_24605_6(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['tender']['procuringEntity']['identifier']['scheme']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
# #                                                                     'KotlinParameterException: Instantiation of ' \
# #                                                                     '[simple type, class com.procurement.mdm
# .model.' \
# #                                                                     'dto.data.Identifier] value failed for JSON ' \
# #                                                                     'property scheme due to missing (therefore
# NULL) ' \
# #                                                                     'value for creator parameter scheme which
# is a ' \
# #                                                                     'non-nullable type\n at [Source: UNKNOWN;
# line: ' \
# #                                                                     '-1, column: -1] (through reference chain:
# com.' \
# #                                                                     'procurement.mdm.model.dto.data.FS[\
# "tender\"]' \
# #                                                                     '->com.procurement.mdm.model.dto.data.
# TenderFS' \
# #                                                                     '[\"procuringEntity\"]->com.procurement.mdm.' \
# #                                                                     'model.dto.data.OrganizationReference' \
# #                                                                     '[\"identifier\"]->com.procurement.mdm.
# model.dto.' \
# #                                                                     'data.Identifier[\"scheme\"])'
# #
# #     @pytestrail.case('24605')
# #     def test_24605_7(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['tender']['procuringEntity']['identifier']['legalName']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
# #         assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
# #                                                                     'KotlinParameterException: Instantiation of ' \
# #                                                                     '[simple type, class com.procurement.budget.' \
# #                                                                     'model.dto.ocds.Identifier] value failed for ' \
# #                                                                     'JSON property legalName due to missing ' \
# #                                                                     '(therefore NULL) value for creator
# parameter ' \
# #                                                                     'legalName which is a non-nullable type\n at ' \
# #                                                                     '[Source: UNKNOWN; line: -1, column: -1] ' \
# #                                                                     '(through reference chain: com.procurement.' \
# #                                                                     'budget.model.dto.fs.request.FsCreate' \
# #                                                                     '[\"tender\"]->com.procurement.budget.
# model.dto.' \
# #                                                                     'fs.request.TenderFsCreate[\"procuring' \
# #                                                                     'Entity\"]->com.procurement.budget.model.dto.' \
# #                                                                     'fs.OrganizationReferenceFs[\"identifier\"]->' \
# #                                                                     'com.procurement.budget.model.dto.ocds.' \
# #                                                                     'Identifier[\"legalName\"])'
# #
# #     @pytestrail.case('24605')
# #     def test_24605_8(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['tender']['procuringEntity']['address']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
# #         assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
# #                                                                     'KotlinParameterException: Instantiation of ' \
# #                                                                     '[simple type, class com.procurement.budget.' \
# #                                                                     'model.dto.fs.OrganizationReferenceFs] value ' \
# #                                                                     'failed for JSON property address due
# to missing' \
# #                                                                     ' (therefore NULL) value for creator
# parameter ' \
# #                                                                     'address which is a non-nullable type\n at ' \
# #                                                                     '[Source: UNKNOWN; line: -1, column: -1] ' \
# #                                                                     '(through reference chain: com.procurement.' \
# #                                                                     'budget.model.dto.fs.request.FsCreate' \
# #                                                                     '[\"tender\"]->com.procurement.budget
# .model.dto.' \
# #                                                                     'fs.request.TenderFsCreate[\"procuring' \
# #                                                                     'Entity\"]->com.procurement.budget.model.dto.' \
# #                                                                     'fs.OrganizationReferenceFs[\"address\"])'
# #
# #     @pytestrail.case('24605')
# #     def test_24605_9(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['tender']['procuringEntity']['address']['streetAddress']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
# #                                                                     'KotlinParameterException: Instantiation of ' \
# #                                                                     '[simple type, class com.procurement.mdm.
# model.' \
# #                                                                     'dto.data.Address] value failed for JSON ' \
# #                                                                     'property streetAddress due to missing ' \
# #                                                                     '(therefore NULL) value for creator
# parameter ' \
# #                                                                     'streetAddress which is a non-nullable
# type\n ' \
# #                                                                     'at [Source: UNKNOWN; line: -1, column: -1] ' \
# #                                                                     '(through reference chain: com.procurement
# .mdm.' \
# #                                                                     'model.dto.data.FS[\"tender\"]->com.
# procurement.' \
# #                                                                     'mdm.model.dto.data.TenderFS[\"procuring' \
# #                                                                     'Entity\"]->com.procurement.mdm.model.
# dto.data.' \
# #                                                                     'OrganizationReference[\"address\"]->com.' \
# #                                                                     'procurement.mdm.model.dto.data.Address' \
# #                                                                     '[\"streetAddress\"])'
# #
# #     @pytestrail.case('24605')
# #     def test_24605_10(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['tender']['procuringEntity']['address']['addressDetails']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] ==
# #
# #     @pytestrail.case('24605')
# #     def test_24605_11(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['tender']['procuringEntity']['address']['addressDetails']['country']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] ==
# #
# #     @pytestrail.case('24605')
# #     def test_24605_12(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['tender']['procuringEntity']['address']['addressDetails']['country']['id']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
# #                                                                     'KotlinParameterException: Instantiation of ' \
# #                                                                     '[simple type, class com.procurement.mdm.
# model.' \
# #                                                                     'dto.data.CountryDetails] value failed for ' \
# #                                                                     'JSON property id due to missing (therefore ' \
# #                                                                     'NULL) value for creator parameter id which
# is ' \
# #                                                                     'a non-nullable type\n at [Source: UNKNOWN; ' \
# #                                                                     'line: -1, column: -1] (through reference
# chain: ' \
# #                                                                     'com.procurement.mdm.model.dto.data.FS' \
# #                                                                     '[\"tender\"]->com.procurement.mdm.model.dto.' \
# #                                                                     'data.TenderFS[\"procuringEntity\"]->com.' \
# #                                                                     'procurement.mdm.model.dto.data.Organization' \
# #                                                                     'Reference[\"address\"]->com.procurement.mdm.' \
# #                                                                     'model.dto.data.Address[\"addressDetails\"]->' \
# #                                                                     'com.procurement.mdm.model.dto.data.Address' \
# #                                                                     'Details[\"country\"]->com.procurement.mdm.' \
# #                                                                     'model.dto.data.CountryDetails[\"id\"])'
# #
# #     @pytestrail.case('24605')
# #     def test_24605_13(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['tender']['procuringEntity']['address']['addressDetails']['region']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
# #                                                                     'KotlinParameterException: Instantiation of ' \
# #                                                                     '[simple type, class com.procurement.mdm.
# model.' \
# #                                                                     'dto.data.AddressDetails] value failed
# for JSON ' \
# #                                                                     'property region due to missing (therefore
# NULL) ' \
# #                                                                     'value for creator parameter region which
# is a non' \
# #                                                                     '-nullable type\n at [Source: UNKNOWN;
# line: -1, ' \
# #                                                                     'column: -1] (through reference chain: com.' \
# #                                                                     'procurement.mdm.model.dto.data.FS[
# \"tender\"]->' \
# #                                                                     'com.procurement.mdm.model.dto.data.TenderFS' \
# #                                                                     '[\"procuringEntity\"]->com.procurement.mdm.' \
# #                                                                     'model.dto.data.OrganizationReference' \
# #                                                                     '[\"address\"]->com.procurement.mdm.
# model.dto.' \
# #                                                                     'data.Address[\"addressDetails\"]->com.' \
# #                                                                     'procurement.mdm.model.dto.data.Address' \
# #                                                                     'Details[\"region\"])'
# #
# #     @pytestrail.case('24605')
# #     def test_24605_14(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
# #                                                                     'KotlinParameterException: Instantiation of ' \
# #                                                                     '[simple type, class com.procurement.
# mdm.model.' \
# #                                                                     'dto.data.RegionDetails] value failed
# for JSON ' \
# #                                                                     'property id due to missing (therefore NULL) ' \
# #                                                                     'value for creator parameter id which
# is a non-' \
# #                                                                     'nullable type\n at [Source: UNKNOWN;
# line: -1, ' \
# #                                                                     'column: -1] (through reference chain: com.' \
# #                                                                     'procurement.mdm.model.dto.data.FS
# [\"tender\"]->' \
# #                                                                     'com.procurement.mdm.model.dto.data.TenderFS' \
# #                                                                     '[\"procuringEntity\"]->com.procurement.mdm.' \
# #                                                                     'model.dto.data.OrganizationReference' \
# #                                                                     '[\"address\"]->com.procurement.mdm.
# model.dto.' \
# #                                                                     'data.Address[\"addressDetails\"]->com.' \
# #                                                                     'procurement.mdm.model.dto.data.
# AddressDetails' \
# #                                                                     '[\"region\"]->com.procurement.mdm.model.dto.' \
# #                                                                     'data.RegionDetails[\"id\"])'
# #
# #     @pytestrail.case('24605')
# #     def test_24605_15(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
# #                                                                     'KotlinParameterException: Instantiation of ' \
# #                                                                     '[simple type, class com.procurement.
# mdm.model.' \
# #                                                                     'dto.data.AddressDetails] value failed
# for JSON ' \
# #                                                                     'property locality due to missing (therefore ' \
# #                                                                     'NULL) value for creator parameter locality ' \
# #                                                                     'which is a non-nullable type\n at [Source: ' \
# #                                                                     'UNKNOWN; line: -1, column: -1] (through ' \
# #                                                                     'reference chain: com.procurement.mdm.
# model.dto.' \
# #                                                                     'data.FS[\"tender\"]->com.procurement.
# mdm.model.' \
# #                                                                     'dto.data.TenderFS[\"procuringEntity\"]->com.' \
# #                                                                     'procurement.mdm.model.dto.data.Organization' \
# #                                                                     'Reference[\"address\"]->com.procurement.mdm.' \
# #                                                                     'model.dto.data.Address[\"addressDetails\"]->' \
# #                                                                     'com.procurement.mdm.model.dto.data.Address' \
# #                                                                     'Details[\"locality\"])'
# #
# #     @pytestrail.case('24605')
# #     def test_24605_16(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
# #                                                                     'KotlinParameterException: Instantiation of ' \
# #                                                                     '[simple type, class com.procurement.
# mdm.model.' \
# #                                                                     'dto.data.LocalityDetails] value failed
# for JSON ' \
# #                                                                     'property id due to missing (therefore NULL) ' \
# #                                                                     'value for creator parameter id which
# is a non-' \
# #                                                                     'nullable type\n at [Source: UNKNOWN;
# line: -1, ' \
# #                                                                     'column: -1] (through reference chain: com.' \
# #                                                                     'procurement.mdm.model.dto.data.FS[\
# "tender\"]->' \
# #                                                                     'com.procurement.mdm.model.dto.data.TenderFS' \
# #                                                                     '[\"procuringEntity\"]->com.procurement.mdm.' \
# #                                                                     'model.dto.data.OrganizationReference' \
# #                                                                     '[\"address\"]->com.procurement.mdm.
# model.dto.' \
# #                                                                     'data.Address[\"addressDetails\"]->com.' \
# #                                                                     'procurement.mdm.model.dto.data.
# AddressDetails' \
# #                                                                     '[\"locality\"]->com.procurement.mdm.
# model.dto.' \
# #                                                                     'data.LocalityDetails[\"id\"])'
# #
# #     @pytestrail.case('24605')
# #     def test_24605_17(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
# #                                                                     'KotlinParameterException: Instantiation of ' \
# #                                                                     '[simple type, class com.procurement.mdm.
# model.' \
# #                                                                     'dto.data.LocalityDetails] value failed for ' \
# #                                                                     'JSON property scheme due to missing
# (therefore ' \
# #                                                                     'NULL) value for creator parameter
# scheme which ' \
# #                                                                     'is a non-nullable type\n at [Source:
# UNKNOWN; ' \
# #                                                                     'line: -1, column: -1] (through
# reference chain: ' \
# #                                                                     'com.procurement.mdm.model.dto.data.FS' \
# #                                                                     '[\"tender\"]->com.procurement.mdm.model.dto.' \
# #                                                                     'data.TenderFS[\"procuringEntity\"]->com.' \
# #                                                                     'procurement.mdm.model.dto.data.Organization' \
# #                                                                     'Reference[\"address\"]->com.procurement.mdm.' \
# #                                                                     'model.dto.data.Address[\"addressDetails\"]->' \
# #                                                                     'com.procurement.mdm.model.dto.data.Address' \
# #                                                                     'Details[\"locality\"]->com.procurement.mdm.' \
# #                                                                     'model.dto.data.LocalityDetails[\"scheme\"])'
# #
# #     @pytestrail.case('24605')
# #     def test_24605_18(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['description']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
# #                                                                     'KotlinParameterException: Instantiation of ' \
# #                                                                     '[simple type, class com.procurement.
# mdm.model.' \
# #                                                                     'dto.data.LocalityDetails] value failed for ' \
# #                                                                     'JSON property description due to missing ' \
# #                                                                     '(therefore NULL) value for creator
# parameter ' \
# #                                                                     'description which is a non-nullable
# type\n at ' \
# #                                                                     '[Source: UNKNOWN; line: -1, column: -1]
# (through' \
# #                                                                     ' reference chain: com.procurement.mdm.model.' \
# #                                                                     'dto.data.FS[\"tender\"]->com.procurement.
# mdm.' \
# #                                                                     'model.dto.data.TenderFS[\"procuring
# Entity\"]->' \
# #                                                                     'com.procurement.mdm.model.dto.data.
# Organization' \
# #                                                                     'Reference[\"address\"]->com.procurement.mdm.' \
# #                                                                     'model.dto.data.Address[\"addressDetails\"]->' \
# #                                                                     'com.procurement.mdm.model.dto.data.Address' \
# #                                                                     'Details[\"locality\"]->com.procurement.mdm.' \
# #                                                                     'model.dto.data.LocalityDetails[\"
# description\"])'
# #
# #     @pytestrail.case('24605')
# #     def test_24605_19(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['tender']['procuringEntity']['contactPoint']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
# #         assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
# #                                                                     'KotlinParameterException: Instantiation of ' \
# #                                                                     '[simple type, class com.procurement.budget.' \
# #                                                                     'model.dto.fs.OrganizationReferenceFs] value ' \
# #                                                                     'failed for JSON property contactPoint
# due to ' \
# #                                                                     'missing (therefore NULL) value for creator ' \
# #                                                                     'parameter contactPoint which is a
# non-nullable ' \
# #                                                                     'type\n at [Source: UNKNOWN; line: -1,
# column: ' \
# #                                                                     '-1] (through reference chain: com.
# procurement.' \
# #                                                                     'budget.model.dto.fs.request.FsCreate' \
# #                                                                     '[\"tender\"]->com.procurement.budget.model.' \
# #                                                                     'dto.fs.request.TenderFsCreate' \
# #                                                                     '[\"procuringEntity\"]->com.procurement.
# budget.' \
# #                                                                     'model.dto.fs.OrganizationReferenceFs' \
# #                                                                     '[\"contactPoint\"])'
# #
# #     @pytestrail.case('24605')
# #     def test_24605_20(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['tender']['procuringEntity']['contactPoint']['name']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] == ''
# #
# #     @pytestrail.case('24605')
# #     def test_24605_21(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['tender']['procuringEntity']['contactPoint']['email']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] == ''
# #
# #     @pytestrail.case('24605')
# #     def test_24605_22(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['tender']['procuringEntity']['contactPoint']['telephone']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] == ''
# #
# #     @pytestrail.case('24605')
# #     def test_24605_23(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['buyer']['name']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
# #         assert create_fs_response[1]['errors'][0]['description'] == ''
# #
# #     @pytestrail.case('24605')
# #     def test_24605_24(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['buyer']['identifier']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
# #         assert create_fs_response[1]['errors'][0]['description'] == ''
# #
# #     @pytestrail.case('24605')
# #     def test_24605_25(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['buyer']['identifier']['id']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] == ''
# #
# #     @pytestrail.case('24605')
# #     def test_24605_26(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['buyer']['identifier']['scheme']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] == ''
# #
# #     @pytestrail.case('24605')
# #     def test_24605_27(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['buyer']['identifier']['legalName']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
# #         assert create_fs_response[1]['errors'][0]['description'] == ''
# #
# #     @pytestrail.case('24605')
# #     def test_24605_28(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['buyer']['address']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
# #         assert create_fs_response[1]['errors'][0]['description'] == ''
# #
# #     @pytestrail.case('24605')
# #     def test_24605_29(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['buyer']['address']['streetAddress']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] == ''
# #
# #     @pytestrail.case('24605')
# #     def test_24605_30(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['buyer']['address']['streetAddress']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] == ''
# #
# #     @pytestrail.case('24605')
# #     def test_24605_31(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['buyer']['address']['addressDetails']['country']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] ==
# #     @pytestrail.case('24605')
# #     def test_24605_32(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['buyer']['address']['addressDetails']['country']['id']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] ==
# #
# #     @pytestrail.case('24605')
# #     def test_24605_33(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['buyer']['address']['addressDetails']['region']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] ==
# #
# #     @pytestrail.case('24605')
# #     def test_24605_34(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['buyer']['address']['addressDetails']['region']['id']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] ==
# #
# #     @pytestrail.case('24605')
# #     def test_24605_35(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['buyer']['address']['addressDetails']['locality']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] ==
# #
# #     @pytestrail.case('24605')
# #     def test_24605_36(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['buyer']['address']['addressDetails']['locality']['scheme']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] ==
# #
# #     @pytestrail.case('24605')
# #     def test_24605_37(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['buyer']['address']['addressDetails']['locality']['id']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] ==
# #
# #     @pytestrail.case('24605')
# #     def test_24605_38(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['buyer']['address']['addressDetails']['locality']['description']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] ==
# #     @pytestrail.case('24605')
# #     def test_24605_39(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['buyer']['contactPoint']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
# #         assert create_fs_response[1]['errors'][0]['description'] ==
# #
# #     @pytestrail.case('24605')
# #     def test_24605_40(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['buyer']['contactPoint']['name']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] ==
# #     @pytestrail.case('24605')
# #     def test_24605_41(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['buyer']['contactPoint']['email']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] ==
# #
# #     @pytestrail.case('24605')
# #     def test_24605_42(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['buyer']['contactPoint']['telephone']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] ==
# #
# #     @pytestrail.case('24605')
# #     def test_24605_43(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['planning']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.00.00.00'
# #         assert create_fs_response[1]['errors'][0]['description'] == 'Data processing exception.'
# #
# #     @pytestrail.case('24605')
# #     def test_24605_44(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['planning']['budget']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.00.00.00'
# #         assert create_fs_response[1]['errors'][0]['description'] == 'Data processing exception.'
# #
# #     @pytestrail.case('24605')
# #     def test_24605_45(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['planning']['budget']['period']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
# #         assert create_fs_response[1]['errors'][0]['description'] ==
# #     @pytestrail.case('24605')
# #     def test_24605_46(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['planning']['budget']['period']['startDate']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
# #         assert create_fs_response[1]['errors'][0]['description'] ==
# #
# #     @pytestrail.case('24605')
# #     def test_24605_47(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['planning']['budget']['period']['endDate']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
# #         assert create_fs_response[1]['errors'][0]['description'] ==
# #
# #     @pytestrail.case('24605')
# #     def test_24605_48(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['planning']['budget']['amount']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.00.00.00'
# #         assert create_fs_response[1]['errors'][0]['description'] == 'Data processing exception.'
# #
# #     @pytestrail.case('24605')
# #     def test_24605_49(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['planning']['budget']['amount']['amount']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
# #         assert create_fs_response[1]['errors'][0]['description'] ==
# #
# #     @pytestrail.case('24605')
# #     def test_24605_50(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['planning']['budget']['amount']['currency']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] ==
# #
# #     @pytestrail.case('24605')
# #     def test_24605_51(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         del fs_create['planning']['budget']['isEuropeanUnionFunded']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
# #         assert create_fs_response[1]['errors'][0]['description'] ==
# #
# #     @pytestrail.case('24605')
# #     def test_24605_52(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['planning']['budget']['isEuropeanUnionFunded'] = True
# #         del fs_create['planning']['budget']['europeanUnionFunding']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.10.01.04'
# #         assert create_fs_response[1]['errors'][0]['description'] == 'EuropeanUnionFunding must not be empty.'
# #
# #     @pytestrail.case('24605')
# #     def test_24605_53(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['planning']['budget']['isEuropeanUnionFunded'] = True
# #         del fs_create['planning']['budget']['europeanUnionFunding']['projectName']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
# #         assert create_fs_response[1]['errors'][0]['description'] ==
# #
# #     @pytestrail.case('24605')
# #     def test_24605_54(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['planning']['budget']['isEuropeanUnionFunded'] = True
# #         del fs_create['planning']['budget']['europeanUnionFunding']['projectIdentifier']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
# #         assert create_fs_response[1]['errors'][0]['description'] ==
# #
# #     @pytestrail.case('24605')
# #     def test_24605_55(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         del fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['id']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] ==
# #
# #     @pytestrail.case('24605')
# #     def test_24605_56(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         del fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['scheme']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] ==
# #
# #     @pytestrail.case('24605')
# #     def test_24605_57(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         del fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['legalName']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
# #         assert create_fs_response[1]['errors'][0]['description'] ==
# #
# #     @pytestrail.case('24605')
# #     def test_24605_58(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         del fs_create['buyer']['additionalIdentifiers'][0]['id']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] ==
# #     @pytestrail.case('24605')
# #     def test_24605_59(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         del fs_create['buyer']['additionalIdentifiers'][0]['scheme']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] ==
# #
# #     @pytestrail.case('24605')
# #     def test_24605_60(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         del fs_create['buyer']['additionalIdentifiers'][0]['legalName']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
# #         assert create_fs_response[1]['errors'][0]['description'] ==
# #
# #     @pytestrail.case('24606')
# #     def test_24606_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['tender']['procuringEntity']['name'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['
# fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][1]['name'] == fs_create['tender']['
# procuringEntity']['name']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['tender']['procuringEntity']['identifier']['uri'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][1]['identifier']['uri'] == \
# #                fs_create['tender']['procuringEntity']['identifier']['uri']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['tender']['procuringEntity']['identifier']['id'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][1]['identifier']['id'] == \
# #                fs_create['tender']['procuringEntity']['identifier']['id']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_4(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['tender']['procuringEntity']['identifier']['legalName'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][1]['identifier']['legalName'] == \
# #                fs_create['tender']['procuringEntity']['identifier']['legalName']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_5(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['tender']['procuringEntity']['address']['streetAddress'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][1]['address']['streetAddress'] == \
# #                fs_create['tender']['procuringEntity']['address']['streetAddress']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_6(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['tender']['procuringEntity']['address']['postalCode'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][1]['address']['postalCode'] == \
# #                fs_create['tender']['procuringEntity']['address']['postalCode']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_7(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] = 'other'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][1]['address']['addressDetails']['locality']['id'] == \
# #                fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_8(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][1]['address']['addressDetails']['
# locality']['scheme'] == \
# #                fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_9(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] = 'other'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['description'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][1]['address']['addressDetails']['locality'][
# #                    'description'] == fs_create['tender']['procuringEntity']['address']['
# addressDetails']['locality'][
# #                    'description']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_10(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['tender']['procuringEntity']['contactPoint']['name'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data'][
# 'outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][1]['contactPoint']['name'] == \
# #                fs_create['tender']['procuringEntity']['contactPoint']['name']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_11(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['tender']['procuringEntity']['contactPoint']['email'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][1]['contactPoint']['email'] == \
# #                fs_create['tender']['procuringEntity']['contactPoint']['email']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_12(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['tender']['procuringEntity']['contactPoint']['telephone'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][1]['contactPoint']['telephone'] == \
# #                fs_create['tender']['procuringEntity']['contactPoint']['telephone']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_13(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['tender']['procuringEntity']['contactPoint']['faxNumber'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][1]['contactPoint']['faxNumber'] == \
# #                fs_create['tender']['procuringEntity']['contactPoint']['faxNumber']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_14(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['tender']['procuringEntity']['contactPoint']['url'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][1]['contactPoint']['url'] == \
# #                fs_create['tender']['procuringEntity']['contactPoint']['url']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_15(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['id'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][1]['additionalIdentifiers'][0]['id'] == \
# #                fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['id']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_16(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['scheme'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][1]['additionalIdentifiers'][0]['scheme'] == \
# #                fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['scheme']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_17(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['legalName'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][1]['additionalIdentifiers'][0]['legalName'] == \
# #                fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['legalName']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_18(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #
# #         fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['uri'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][1]['additionalIdentifiers'][0]['uri'] == \
# #                fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['uri']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_19(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['buyer']['name'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][0]['name'] == fs_create['buyer']['name']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_20(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['buyer']['identifier']['id'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][0]['identifier']['id'] == fs_create['
# buyer']['identifier'][
# #             'id']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_21(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['buyer']['identifier']['legalName'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][0]['identifier']['legalName'] == \
# #                fs_create['buyer']['identifier']['legalName']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_22(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['buyer']['identifier']['uri'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][0]['identifier']['uri'] == \
# #                fs_create['buyer']['identifier']['uri']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_23(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['buyer']['address']['streetAddress'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][0]['address']['streetAddress'] == \
# #                fs_create['buyer']['address']['streetAddress']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_24(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['buyer']['address']['postalCode'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][0]['address']['postalCode'] == \
# #                fs_create['buyer']['address']['postalCode']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_25(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['buyer']['address']['addressDetails']['locality']['scheme'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality']['
# scheme'] == \
# #                fs_create['buyer']['address']['addressDetails']['locality']['scheme']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_26(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['buyer']['address']['addressDetails']['locality']['scheme'] = 'other'
# #         fs_create['buyer']['address']['addressDetails']['locality']['id'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality']['id'] == \
# #                fs_create['buyer']['address']['addressDetails']['locality']['id']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_27(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['buyer']['address']['addressDetails']['locality']['scheme'] = 'other'
# #         fs_create['buyer']['address']['addressDetails']['locality']['description'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality'][
# #                    'description'] == \
# #                fs_create['buyer']['address']['addressDetails']['locality']['description']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_28(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['buyer']['contactPoint']['url'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['url'] == \
# #                fs_create['buyer']['contactPoint']['url']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_29(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['buyer']['contactPoint']['name'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['name'] == \
# #                fs_create['buyer']['contactPoint']['name']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_30(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['buyer']['contactPoint']['email'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['email'] == \
# #                fs_create['buyer']['contactPoint']['email']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_31(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['buyer']['contactPoint']['telephone'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['telephone'] == \
# #                fs_create['buyer']['contactPoint']['telephone']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_32(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['buyer']['contactPoint']['faxNumber'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['faxNumber'] == \
# #                fs_create['buyer']['contactPoint']['faxNumber']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_33(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['buyer']['additionalIdentifiers'][0]['id'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][0]['additionalIdentifiers'][0]['id'] == \
# #                fs_create['buyer']['additionalIdentifiers'][0]['id']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_34(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['buyer']['additionalIdentifiers'][0]['scheme'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][0]['additionalIdentifiers'][0]['scheme'] == \
# #                fs_create['buyer']['additionalIdentifiers'][0]['scheme']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_35(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['buyer']['additionalIdentifiers'][0]['legalName'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][0]['additionalIdentifiers'][0]['legalName'] == \
# #                fs_create['buyer']['additionalIdentifiers'][0]['legalName']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_36(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['buyer']['additionalIdentifiers'][0]['uri'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][0]['additionalIdentifiers'][0]['uri'] == \
# #                fs_create['buyer']['additionalIdentifiers'][0]['uri']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_37(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['planning']['rationale'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['planning']['rationale'] == \
# #                fs_create['planning']['rationale']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_38(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['planning']['budget']['id'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['planning']['budget']['id'] == \
# #                fs_create['planning']['budget']['id']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_39(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['planning']['budget']['description'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['planning']['budget']['description'] == \
# #                fs_create['planning']['budget']['description']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_40(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['planning']['budget']['isEuropeanUnionFunded'] = True
# #         fs_create['planning']['budget']['europeanUnionFunding']['projectName'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['planning']['budget']['europeanUnionFunding']['
# projectName'] == \
# #                fs_create['planning']['budget']['europeanUnionFunding']['projectName']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_41(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['planning']['budget']['isEuropeanUnionFunded'] = True
# #         fs_create['planning']['budget']['europeanUnionFunding']['projectIdentifier'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['planning']['budget']['europeanUnionFunding']['
# projectIdentifier'] == \
# #                fs_create['planning']['budget']['europeanUnionFunding']['projectIdentifier']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_42(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['planning']['budget']['project'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['planning']['budget']['project'] == fs_create['
# planning']['budget'][
# #             'project']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_43(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['planning']['budget']['projectID'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['planning']['budget']['projectID'] == fs_create['
# planning']['budget'][
# #             'projectID']
# #
# #     @pytestrail.case('24606')
# #     def test_24606_44(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['planning']['budget']['uri'] = ''
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['planning']['budget']['uri'] == fs_create['
# planning']['budget'][
# #             'uri']
# #
# #     @pytestrail.case('24607')
# #     def test_24607_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_treasury_money)
# #         create_fs_response_1 = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #         host = set_instance_for_request()
# #
# #         access_token = get_access_token_for_platform_one()
# #         x_operation_id = get_x_operation_id(access_token)
# #
# #         requests.post(
# #             url=host + create_fs + create_fs_response_1[3],
# #             headers={
# #                 'Authorization': 'Bearer ' + access_token,
# #                 'X-OPERATION-ID': x_operation_id,
# #                 'Content-Type': 'application/json'},
# #             json=fs_create)
# #         time.sleep(2)
# #
# #         get_message_from_kafka(x_operation_id)
# #
# #         assert create_fs_response_1[0].text == 'ok'
# #         assert create_fs_response_1[0].status_code == 202
# #         assert create_fs_response_1[1]['X-OPERATION-ID'] == create_fs_response_1[2]
# #
# #     @pytestrail.case('24607')
# #     def test_24607_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_treasury_money)
# #         create_fs_response_1 = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #         host = set_instance_for_request()
# #
# #         access_token = get_access_token_for_platform_one()
# #         x_operation_id = get_x_operation_id(access_token)
# #
# #         requests.post(
# #             url=host + create_fs + create_fs_response_1[3],
# #             headers={
# #                 'Authorization': 'Bearer ' + access_token,
# #                 'X-OPERATION-ID': x_operation_id,
# #                 'Content-Type': 'application/json'},
# #             json=fs_create)
# #         time.sleep(2)
# #
# #         get_message_from_kafka(x_operation_id)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response_1[1]['data']['ocid'], '*')
# #         assert ocid == True
# #         assert create_fs_response_1[1]['X-OPERATION-ID'] == create_fs_response_1[2]
# #
# #     @pytestrail.case('24607')
# #     def test_24607_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_treasury_money)
# #         create_fs_response_1 = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #         host = set_instance_for_request()
# #         access_token = get_access_token_for_platform_one()
# #         x_operation_id = get_x_operation_id(access_token)
# #
# #         create_fs_response_2 = requests.post(
# #             url=host + create_fs + create_fs_response_1[3],
# #             headers={
# #                 'Authorization': 'Bearer ' + access_token,
# #                 'X-OPERATION-ID': x_operation_id,
# #                 'Content-Type': 'application/json'},
# #             json=fs_create)
# #         time.sleep(2)
# #
# #         message_from_kafka = get_message_from_kafka(x_operation_id)
# #
# #         assert create_fs_response_2.text == 'ok'
# #         assert create_fs_response_2.status_code == 202
# #         assert message_from_kafka['X-OPERATION-ID'] == x_operation_id
# #
# #     @pytestrail.case('24607')
# #     def test_24607_4(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_treasury_money)
# #         create_fs_response_1 = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #         host = set_instance_for_request()
# #         access_token = get_access_token_for_platform_one()
# #         x_operation_id = get_x_operation_id(access_token)
# #
# #         requests.post(
# #             url=host + create_fs + create_fs_response_1[3],
# #             headers={
# #                 'Authorization': 'Bearer ' + access_token,
# #                 'X-OPERATION-ID': x_operation_id,
# #                 'Content-Type': 'application/json'},
# #             json=fs_create)
# #         time.sleep(2)
# #
# #         message_from_kafka = get_message_from_kafka(x_operation_id)
# #
# #         ocid = fnmatch.fnmatch(message_from_kafka['data']['ocid'], '*')
# #         assert ocid == True
# #         assert message_from_kafka['X-OPERATION-ID'] == x_operation_id
# #
# #     @pytestrail.case('24608')
# #     def test_24608_1(self):
# #         fs_create = copy.deepcopy(fs_create_obligatory_treasury_money)
# #
# #         time.sleep(2)
# #         host = set_instance_for_request()
# #         access_token = get_access_token_for_platform_one()
# #         x_operation_id = get_x_operation_id(access_token)
# #         fake_cpid = prepared_cpid()
# #         create_fs_response = requests.post(
# #             url=host + create_fs + fake_cpid,
# #             headers={
# #                 'Authorization': 'Bearer ' + access_token,
# #                 'X-OPERATION-ID': x_operation_id,
# #                 'Content-Type': 'application/json'},
# #             json=fs_create)
# #         time.sleep(1)
# #
# #         assert create_fs_response.status_code == 400
# #         assert create_fs_response.json()['errors'][0]['code'] == '400.00.00.00'
# #         assert create_fs_response.json()['errors'][0]['description'] == 'Context not found.'
# #
# #     @pytestrail.case('24609')
# #     def test_24609_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24609')
# #     def test_24609_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #
# #     @pytestrail.case('24610')
# #     def test_24610_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24610')
# #     def test_24610_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
# #         token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         assert token == True
# #
# #     @pytestrail.case('24610')
# #     def test_24610_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         timestamp = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'][32:45], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['data']['outcomes']['fs'][0]['id'][0:28] == create_fs_response[3]
# #         assert create_fs_response[1]['data']['outcomes']['fs'][0]['id'][28:32] == '-FS-'
# #         assert timestamp == True
# #
# #     @pytestrail.case('24611')
# #     def test_24611_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24611')
# #     def test_24611_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
# #         token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         assert token == True
# #
# #     @pytestrail.case('24611')
# #     def test_24611_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         url_create_fs = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #
# #         publicPoint_update = requests.get(url=url_create_fs).json()
# #
# #         check_tender_id = is_valid_uuid(publicPoint_update['releases'][0]['tender']['id'])
# #         assert check_tender_id == True
# #
# #     @pytestrail.case('24612')
# #     def test_24612_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create_1 = copy.deepcopy(fs_create_obligatory_treasury_money)
# #         fs_create_1['planning']['budget']['amount']['amount'] = 133.26
# #         fs_create_1['planning']['budget']['amount']['currency'] = 'EUR'
# #         create_fs_response_1 = bpe_create_fs(ei_create, fs_create_1)
# #         time.sleep(2)
# #
# #         fs_create_2 = copy.deepcopy(fs_create_obligatory_treasury_money)
# #         fs_create_1['planning']['budget']['amount']['amount'] = 50.34
# #         fs_create_1['planning']['budget']['amount']['currency'] = 'EUR'
# #
# #         access_token = get_access_token_for_platform_one()
# #         x_operation_id = get_x_operation_id(access_token)
# #         host = set_instance_for_request()
# #         requests.post(
# #             url=host + create_fs + create_fs_response_1[3],
# #             headers={
# #                 'Authorization': 'Bearer ' + access_token,
# #                 'X-OPERATION-ID': x_operation_id,
# #                 'Content-Type': 'application/json'},
# #             json=fs_create_2)
# #         time.sleep(2)
# #
# #         get_message_from_kafka(x_operation_id)
# #
# #         assert create_fs_response_1[0].text == 'ok'
# #         assert create_fs_response_1[0].status_code == 202
# #         assert create_fs_response_1[1]['X-OPERATION-ID'] == create_fs_response_1[2]
# #
# #     @pytestrail.case('24612')
# #     def test_24612_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create_1 = copy.deepcopy(fs_create_obligatory_treasury_money)
# #         fs_create_1['planning']['budget']['amount']['amount'] = 133.26
# #         fs_create_1['planning']['budget']['amount']['currency'] = 'EUR'
# #         create_fs_response_1 = bpe_create_fs(ei_create, fs_create_1)
# #         time.sleep(2)
# #
# #         fs_create_2 = copy.deepcopy(fs_create_obligatory_treasury_money)
# #         fs_create_1['planning']['budget']['amount']['amount'] = 50.34
# #         fs_create_1['planning']['budget']['amount']['currency'] = 'EUR'
# #
# #         access_token = get_access_token_for_platform_one()
# #         x_operation_id = get_x_operation_id(access_token)
# #         host = set_instance_for_request()
# #         requests.post(
# #             url=host + create_fs + create_fs_response_1[3],
# #             headers={
# #                 'Authorization': 'Bearer ' + access_token,
# #                 'X-OPERATION-ID': x_operation_id,
# #                 'Content-Type': 'application/json'},
# #             json=fs_create_2)
# #         time.sleep(2)
# #
# #         get_message_from_kafka(x_operation_id)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response_1[1]['data']['ocid'], '*')
# #         assert ocid == True
# #         assert create_fs_response_1[1]['X-OPERATION-ID'] == create_fs_response_1[2]
# #
# #     @pytestrail.case('24612')
# #     def test_24612_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create_1 = copy.deepcopy(fs_create_obligatory_treasury_money)
# #         fs_create_1['planning']['budget']['amount']['amount'] = 133.26
# #         fs_create_1['planning']['budget']['amount']['currency'] = 'EUR'
# #         create_fs_response_1 = bpe_create_fs(ei_create, fs_create_1)
# #         time.sleep(2)
# #
# #         fs_create_2 = copy.deepcopy(fs_create_obligatory_treasury_money)
# #         fs_create_2['planning']['budget']['amount']['amount'] = 50.34
# #         fs_create_2['planning']['budget']['amount']['currency'] = 'EUR'
# #
# #         access_token = get_access_token_for_platform_one()
# #         x_operation_id = get_x_operation_id(access_token)
# #         host = set_instance_for_request()
# #         requests.post(
# #             url=host + create_fs + create_fs_response_1[3],
# #             headers={
# #                 'Authorization': 'Bearer ' + access_token,
# #                 'X-OPERATION-ID': x_operation_id,
# #                 'Content-Type': 'application/json'},
# #             json=fs_create_2)
# #         time.sleep(2)
# #
# #         message_from_kafka = get_message_from_kafka(x_operation_id)
# #         url_create_ei = message_from_kafka['data']['url'] + '/' + message_from_kafka['data']['outcomes']['
# fs'][0]['id'][
# #                                                                   0:28]
# #
# #         publicPoint_create_ei = requests.get(url=url_create_ei).json()
# #         sum_of_fs = fs_create_1['planning']['budget']['amount']['amount'] + fs_create_2['planning']['
# budget']['amount'][
# #             'amount']
# #
# #         assert publicPoint_create_ei['releases'][0]['planning']['budget']['amount']['amount'] == sum_of_fs
# #
# #     @pytestrail.case('24613')
# #     def test_24613_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24613')
# #     def test_24613_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
# #         token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         assert token == True
# #
# #     @pytestrail.case('24613')
# #     def test_24613_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         url_create_fs = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_update = requests.get(url=url_create_fs).json()
# #
# #         assert publicPoint_update['releases'][0]['planning']['budget']['verified'] == True
# #
# #     @pytestrail.case('24614')
# #     def test_24614_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24614')
# #     def test_24614_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
# #         token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         assert token == True
# #
# #     @pytestrail.case('24614')
# #     def test_24614_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         url_create_fs = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data'][
# 'outcomes']['fs'][0][
# #             'id']
# #         publicPoint_update = requests.get(url=url_create_fs).json()
# #
# #         assert publicPoint_update['releases'][0]['planning']['budget']['verified'] == False
# #
# #     @pytestrail.case('24615')
# #     def test_24615_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_treasury_money)
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24615')
# #     def test_24615_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_treasury_money)
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #
# #     @pytestrail.case('24615')
# #     def test_24615_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_treasury_money)
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data'][
# 'outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['tender']['statusDetails'] == 'empty'
# #
# #     @pytestrail.case('24616')
# #     def test_24616_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24616')
# #     def test_24616_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #
# #     @pytestrail.case('24616')
# #     def test_24616_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data'][
# 'outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['tender']['status'] == 'active'
# #
# #     @pytestrail.case('24617')
# #     def test_24617_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24617')
# #     def test_24617_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #
# #     @pytestrail.case('24617')
# #     def test_24617_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['tender']['status'] == 'planning'
# #
# #     @pytestrail.case('24618')
# #     def test_24618_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24618')
# #     def test_24618_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #
# #     @pytestrail.case('24618')
# #     def test_24618_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][0]['roles'][0] != 'funder'
# #
# #     @pytestrail.case('24619')
# #     def test_24619_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24619')
# #     def test_24619_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #
# #     @pytestrail.case('24619')
# #     def test_24619_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_update).json()
# #         print(url_update)
# #         assert publicPoint_create['releases'][0]['parties'][0]['roles'][0] == 'funder'
# #         assert publicPoint_create['releases'][0]['parties'][1]['roles'][0] != 'funder'
# #
# #     @pytestrail.case('24620')
# #     def test_24620_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['tender']['procuringEntity']['name'] = 'Znatok'
# #         fs_create['tender']['procuringEntity']['identifier']['id'] = '777'
# #         fs_create['tender']['procuringEntity']['identifier']['scheme'] = 'MD-IDNO'
# #         fs_create['tender']['procuringEntity']['identifier']['legalName'] = 'Kunitskiy Peto Oleksiyovich company'
# #         fs_create['tender']['procuringEntity']['identifier']['url'] = 'www.dobro.ua'
# #         fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['id'] = 'Dodatovo id'
# #         fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['scheme'] = 'PROSTO'
# #         fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['legalName'] = 'Ne_yiridi4na_osoba'
# #         fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['uri'] = 'www.zeebra.ua'
# #         fs_create['tender']['procuringEntity']['address']['streetAddress'] = 'Voloshkova'
# #         fs_create['tender']['procuringEntity']['address']['postalCode'] = '77777'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['country']['id'] = 'MD'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '1700000'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] = 'CUATM'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id'] = '1701000'
# #         fs_create['tender']['procuringEntity']['contactPoint']['name'] = 'Petro Oleksiyovich'
# #         fs_create['tender']['procuringEntity']['contactPoint']['email'] = 'petro@sobakin.md'
# #         fs_create['tender']['procuringEntity']['contactPoint']['telephone'] = '044-555-88-96'
# #         fs_create['tender']['procuringEntity']['contactPoint']['faxNumber'] = '044-555-88-97'
# #         fs_create['tender']['procuringEntity']['contactPoint']['url'] = 'www.webPetrovicha'
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24620')
# #     def test_24620_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['tender']['procuringEntity']['name'] = 'Znatok'
# #         fs_create['tender']['procuringEntity']['identifier']['id'] = '777'
# #         fs_create['tender']['procuringEntity']['identifier']['scheme'] = 'MD-IDNO'
# #         fs_create['tender']['procuringEntity']['identifier']['legalName'] = 'Kunitskiy Peto Oleksiyovich company'
# #         fs_create['tender']['procuringEntity']['identifier']['url'] = 'www.dobro.ua'
# #         fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['id'] = 'Dodatovo id'
# #         fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['scheme'] = 'PROSTO'
# #         fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['legalName'] = 'Ne_yiridi4na_osoba'
# #         fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['uri'] = 'www.zeebra.ua'
# #         fs_create['tender']['procuringEntity']['address']['streetAddress'] = 'Voloshkova'
# #         fs_create['tender']['procuringEntity']['address']['postalCode'] = '77777'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['country']['id'] = 'MD'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '1700000'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] = 'CUATM'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id'] = '1701000'
# #         fs_create['tender']['procuringEntity']['contactPoint']['name'] = 'Petro Oleksiyovich'
# #         fs_create['tender']['procuringEntity']['contactPoint']['email'] = 'petro@sobakin.md'
# #         fs_create['tender']['procuringEntity']['contactPoint']['telephone'] = '044-555-88-96'
# #         fs_create['tender']['procuringEntity']['contactPoint']['faxNumber'] = '044-555-88-97'
# #         fs_create['tender']['procuringEntity']['contactPoint']['url'] = 'www.webPetrovicha'
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
# #         token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         assert token == True
# #
# #     @pytestrail.case('24620')
# #     def test_24620_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['tender']['procuringEntity']['name'] = 'Znatok'
# #         fs_create['tender']['procuringEntity']['identifier']['id'] = '777'
# #         fs_create['tender']['procuringEntity']['identifier']['scheme'] = 'MD-IDNO'
# #         fs_create['tender']['procuringEntity']['identifier']['legalName'] = 'Kunitskiy Peto Oleksiyovich company'
# #         fs_create['tender']['procuringEntity']['identifier']['url'] = 'www.dobro.ua'
# #         fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['id'] = 'Dodatovo id'
# #         fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['scheme'] = 'PROSTO'
# #         fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['legalName'] = 'Ne_yiridi4na_osoba'
# #         fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['uri'] = 'www.zeebra.ua'
# #         fs_create['tender']['procuringEntity']['address']['streetAddress'] = 'Voloshkova'
# #         fs_create['tender']['procuringEntity']['address']['postalCode'] = '77777'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['country']['id'] = 'MD'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '1700000'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] = 'CUATM'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id'] = '1701000'
# #         fs_create['tender']['procuringEntity']['contactPoint']['name'] = 'Petro Oleksiyovich'
# #         fs_create['tender']['procuringEntity']['contactPoint']['email'] = 'petro@sobakin.md'
# #         fs_create['tender']['procuringEntity']['contactPoint']['telephone'] = '044-555-88-96'
# #         fs_create['tender']['procuringEntity']['contactPoint']['faxNumber'] = '044-555-88-97'
# #         fs_create['tender']['procuringEntity']['contactPoint']['url'] = 'www.webPetrovicha'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_create).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][1]['roles'][0] == 'payer'
# #         assert publicPoint_create['releases'][0]['parties'][1]['id'] == \
# #                fs_create['tender']['procuringEntity']['identifier']['scheme'] + '-' + \
# #                fs_create['tender']['procuringEntity']['identifier']['id']
# #         assert publicPoint_create['releases'][0]['parties'][1]['name'] == fs_create['tender']['
# procuringEntity']['name']
# #         assert publicPoint_create['releases'][0]['parties'][1]['identifier']['scheme'] == \
# #                fs_create['tender']['procuringEntity']['identifier']['scheme']
# #         assert publicPoint_create['releases'][0]['parties'][1]['identifier']['id'] == \
# #                fs_create['tender']['procuringEntity']['identifier']['id']
# #         assert publicPoint_create['releases'][0]['parties'][1]['identifier']['legalName'] == \
# #                fs_create['tender']['procuringEntity']['identifier']['legalName']
# #         assert publicPoint_create['releases'][0]['parties'][1]['identifier']['uri'] == \
# #                fs_create['tender']['procuringEntity']['identifier']['uri']
# #         assert publicPoint_create['releases'][0]['parties'][1]['address']['streetAddress'] == \
# #                fs_create['tender']['procuringEntity']['address']['streetAddress']
# #         assert publicPoint_create['releases'][0]['parties'][1]['address']['postalCode'] == \
# #                fs_create['tender']['procuringEntity']['address']['postalCode']
# #         assert publicPoint_create['releases'][0]['parties'][1]['address']['addressDetails']['country']['id'] == \
# #                fs_create['tender']['procuringEntity']['address']['addressDetails']['country']['id']
# #         assert publicPoint_create['releases'][0]['parties'][1]['address']['addressDetails']['region']['id'] == \
# #                fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id']
# #         assert publicPoint_create['releases'][0]['parties'][1]['address']['addressDetails']['locality']['
# scheme'] == \
# #                fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme']
# #         assert publicPoint_create['releases'][0]['parties'][1]['address']['addressDetails']['locality']['id'] == \
# #                fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id']
# #         assert publicPoint_create['releases'][0]['parties'][1]['additionalIdentifiers'][0]['scheme'] == \
# #                fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['scheme']
# #         assert publicPoint_create['releases'][0]['parties'][1]['additionalIdentifiers'][0]['id'] == \
# #                fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['id']
# #         assert publicPoint_create['releases'][0]['parties'][1]['additionalIdentifiers'][0]['legalName'] == \
# #                fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['legalName']
# #         assert publicPoint_create['releases'][0]['parties'][1]['additionalIdentifiers'][0]['uri'] == \
# #                fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['uri']
# #         assert publicPoint_create['releases'][0]['parties'][1]['contactPoint']['name'] == \
# #                fs_create['tender']['procuringEntity']['contactPoint']['name']
# #         assert publicPoint_create['releases'][0]['parties'][1]['contactPoint']['email'] == \
# #                fs_create['tender']['procuringEntity']['contactPoint']['email']
# #         assert publicPoint_create['releases'][0]['parties'][1]['contactPoint']['telephone'] == \
# #                fs_create['tender']['procuringEntity']['contactPoint']['telephone']
# #         assert publicPoint_create['releases'][0]['parties'][1]['contactPoint']['faxNumber'] == \
# #                fs_create['tender']['procuringEntity']['contactPoint']['faxNumber']
# #         assert publicPoint_create['releases'][0]['parties'][1]['contactPoint']['url'] == \
# #                fs_create['tender']['procuringEntity']['contactPoint']['url']
# #
# #     @pytestrail.case('24621')
# #     def test_24621_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['buyer']['identifier']['id'] = 'fs_01010101-test'
# #         fs_create['buyer']['identifier']['scheme'] = 'MD-IDNO'
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24621')
# #     def test_24621_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['buyer']['identifier']['id'] = 'fs_01010101-test'
# #         fs_create['buyer']['identifier']['scheme'] = 'MD-IDNO'
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
# #         token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         assert token == True
# #
# #     @pytestrail.case('24621')
# #     def test_24621_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['buyer']['identifier']['id'] = 'fs_01010101-test'
# #         fs_create['buyer']['identifier']['scheme'] = 'MD-IDNO'
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_create).json()
# #
# #         assert publicPoint_create['releases'][0]['planning']['budget']['sourceEntity']['id'] == \
# #                fs_create['buyer']['identifier']['scheme'] + '-' + fs_create['buyer']['identifier']['id']
# #
# #     @pytestrail.case('24622')
# #     def test_24622_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         ei_create['buyer']['identifier']['id'] = 'ei_01010101-test'
# #         ei_create['buyer']['identifier']['scheme'] = 'MD-IDNO'
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24622')
# #     def test_24622_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         ei_create['buyer']['identifier']['id'] = 'ei_01010101-test'
# #         ei_create['buyer']['identifier']['scheme'] = 'MD-IDNO'
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
# #         token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         assert token == True
# #
# #     @pytestrail.case('24622')
# #     def test_24622_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         ei_create['buyer']['identifier']['id'] = 'ei_01010101-test'
# #         ei_create['buyer']['identifier']['scheme'] = 'MD-IDNO'
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_create).json()
# #
# #         assert publicPoint_create['releases'][0]['planning']['budget']['sourceEntity']['id'] == \
# #                ei_create['buyer']['identifier']['scheme'] + '-' + ei_create['buyer']['identifier']['id']
# #
# #     @pytestrail.case('24623')
# #     def test_24623_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['buyer']['name'] = 'name from fs buyer'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24623')
# #     def test_24623_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['buyer']['name'] = 'name from fs buyer'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
# #         token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         assert token == True
# #
# #     @pytestrail.case('24623')
# #     def test_24623_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['buyer']['name'] = 'name from fs buyer'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_create).json()
# #
# #         assert publicPoint_create['releases'][0]['planning']['budget']['sourceEntity']['name'] == \
# #                fs_create['buyer']['name']
# #
# #     @pytestrail.case('24624')
# #     def test_24624_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         ei_create['buyer']['name'] = 'name from ei buyer'
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24624')
# #     def test_24624_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         ei_create['buyer']['name'] = 'name from ei buyer'
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
# #         token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         assert token == True
# #
# #     @pytestrail.case('24624')
# #     def test_24624_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         ei_create['buyer']['name'] = 'name from ei buyer'
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_create).json()
# #
# #         assert publicPoint_create['releases'][0]['planning']['budget']['sourceEntity']['name'] == \
# #                ei_create['buyer']['name']
# #
# #     @pytestrail.case('24625')
# #     def test_24625_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['tender']['procuringEntity']['identifier']['id'] = '777'
# #         fs_create['tender']['procuringEntity']['identifier']['scheme'] = 'MD-IDNO'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24625')
# #     def test_24625_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['tender']['procuringEntity']['identifier']['id'] = '777'
# #         fs_create['tender']['procuringEntity']['identifier']['scheme'] = 'MD-IDNO'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
# #         token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         assert token == True
# #
# #     @pytestrail.case('24625')
# #     def test_24625_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['tender']['procuringEntity']['identifier']['id'] = '777'
# #         fs_create['tender']['procuringEntity']['identifier']['scheme'] = 'MD-IDNO'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_create).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][1]['roles'][0] == 'payer'
# #         assert publicPoint_create['releases'][0]['parties'][1]['id'] == \
# #                fs_create['tender']['procuringEntity']['identifier']['scheme'] + '-' + \
# #                fs_create['tender']['procuringEntity']['identifier']['id']
# #
# #     @pytestrail.case('24626')
# #     def test_24626_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['buyer']['identifier']['id'] = '222'
# #         fs_create['buyer']['identifier']['scheme'] = 'MD-IDNO'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24626')
# #     def test_24626_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['buyer']['identifier']['id'] = '222'
# #         fs_create['buyer']['identifier']['scheme'] = 'MD-IDNO'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
# #         token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         assert token == True
# #
# #     @pytestrail.case('24626')
# #     def test_24626_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['buyer']['identifier']['id'] = '222'
# #         fs_create['buyer']['identifier']['scheme'] = 'MD-IDNO'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_create).json()
# #         print(url_create)
# #         assert publicPoint_create['releases'][0]['parties'][0]['roles'][0] == 'funder'
# #         assert publicPoint_create['releases'][0]['parties'][0]['id'] == \
# #                fs_create['buyer']['identifier']['scheme'] + '-' + fs_create['buyer']['identifier']['id']
# #
# #     @pytestrail.case('24627')
# #     def test_24627_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['planning']['budget']['amount']['currency'] = 'USD'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24627')
# #     def test_24627_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['planning']['budget']['amount']['currency'] = 'USD'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
# #         token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         assert token == True
# #
# #     @pytestrail.case('24628')
# #     def test_24628(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         fs_create['planning']['budget']['amount']['currency'] = 'UAH'
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00.10'
# #         assert create_fs_response[1]['errors'][0]['description'] == 'Currency not found. '
# #
# #     @pytestrail.case('24629')
# #     def test_24629(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         fs_create['tender']['procuringEntity']['identifier']['scheme'] = 'ADCDEF'
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00.12'
# #         assert create_fs_response[1]['errors'][0]['description'] == 'Registration scheme not found. '
# #
# #     @pytestrail.case('24630')
# #     def test_24630(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         fs_create['buyer']['identifier']['scheme'] = 'ADCDEF'
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00.12'
# #         assert create_fs_response[1]['errors'][0]['description'] == 'Registration scheme not found. '
# #
# #     @pytestrail.case('24631')
# #     def test_24631_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['tender']['procuringEntity']['identifier']['scheme'] = 'MD-IDNO'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24631')
# #     def test_24631_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['tender']['procuringEntity']['identifier']['scheme'] = 'MD-IDNO'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
# #         token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         assert token == True
# #
# #     @pytestrail.case('24632')
# #     def test_24632_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['buyer']['identifier']['scheme'] = 'MD-IDNO'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24632')
# #     def test_24632_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['buyer']['identifier']['scheme'] = 'MD-IDNO'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
# #         token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         assert token == True
# #
# #     @pytestrail.case('24633')
# #     def test_24633(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         fs_create['planning']['budget']['amount']['currency'] = True
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] == '
# #
# #     @pytestrail.case('24634')
# #     def test_24634_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['planning']['budget']['amount']['amount'] = 0.01
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24634')
# #     def test_24634_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['planning']['budget']['amount']['amount'] = 0.01
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
# #         token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         assert token == True
# #
# #     @pytestrail.case('24635')
# #     def test_24635(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         fs_create['planning']['budget']['amount']['amount'] = 0
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.10.00.07'
# #         assert create_fs_response[1]['errors'][0]['description'] == 'Invalid amount.'
# #
# #     @pytestrail.case('24636')
# #     def test_24636(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         fs_create['planning']['budget']['amount']['amount'] = -25.3
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.10.00.07'
# #         assert create_fs_response[1]['errors'][0]['description'] == 'Invalid amount.'
# #
# #     @pytestrail.case('24637')
# #     def test_24637(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_own_money)
# #         fs_create['planning']['budget']['amount']['amount'] = False
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
# #         assert create_fs_response[1]['errors'][0]['description'] ==
# #
# #     @pytestrail.case('24638')
# #     def test_24638_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         ei_create['planning']['budget']['period']['startDate'] = '2020-01-01T00:00:00Z'
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['planning']['budget']['period']['startDate'] = '2020-01-01T00:00:00Z'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24638')
# #     def test_24638_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         ei_create['planning']['budget']['period']['startDate'] = '2020-01-01T00:00:00Z'
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['planning']['budget']['period']['startDate'] = '2020-01-01T00:00:00Z'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
# #         token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         assert token == True
# #
# #     @pytestrail.case('24639')
# #     def test_24639_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         ei_create['planning']['budget']['period']['endDate'] = '2020-12-31T00:00:00Z'
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['planning']['budget']['period']['endDate'] = '2020-12-31T00:00:00Z'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24639')
# #     def test_24639_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         ei_create['planning']['budget']['period']['endDate'] = '2020-12-31T00:00:00Z'
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['planning']['budget']['period']['endDate'] = '2020-12-31T00:00:00Z'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
# #         token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         assert token == True
# #
# #     @pytestrail.case('24640')
# #     def test_24640(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         ei_create['planning']['budget']['period']['startDate'] = '2020-01-05T00:00:00Z'
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['planning']['budget']['period']['startDate'] = '2020-01-01T00:00:00Z'
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.10.01.01'
# #         assert create_fs_response[1]['errors'][0]['description'] == 'Invalid period.'
# #
# #     @pytestrail.case('24641')
# #     def test_24641(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         ei_create['planning']['budget']['period']['endDate'] = '2020-12-31T00:00:00Z'
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['planning']['budget']['period']['endDate'] = '2021-01-01T00:00:00Z'
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.10.01.01'
# #         assert create_fs_response[1]['errors'][0]['description'] == 'Invalid period.'
# #
# #     @pytestrail.case('24642')
# #     def test_24642(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['planning']['budget']['period']['startDate'] = '2021-01-05T00:00:00Z'
# #         fs_create['planning']['budget']['period']['endDate'] = '2021-01-01T00:00:00Z'
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.10.01.01'
# #         assert create_fs_response[1]['errors'][0]['description'] == 'Invalid period.'
# #
# #     @pytestrail.case('24643')
# #     def test_24643(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         ei_create['planning']['budget']['period']['startDate'] = '2020-01-01T00:00:00Z'
# #         ei_create['planning']['budget']['period']['endDate'] = '2020-12-20T00:00:00Z'
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['planning']['budget']['period']['startDate'] = '2020-01-01T00:00:00Z'
# #         fs_create['planning']['budget']['period']['endDate'] = '2020-12-20T00:00:00Z'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
# #         token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         assert token == True
# #
# #     @pytestrail.case('24644')
# #     def test_24644(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         ei_create['planning']['budget']['period']['startDate'] = '2020-01-01T00:00:00Z'
# #         ei_create['planning']['budget']['period']['endDate'] = '2020-12-20T00:00:00Z'
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['planning']['budget']['period']['startDate'] = '2020-01-01T00:00:00Z'
# #         today = datetime.datetime.now()
# #
# #         tomorrow = today.day + 1
# #
# #         fs_create['planning']['budget']['period']['endDate'] = f'2020-12-{tomorrow}T16:16:29Z'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
# #         token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         assert token == True
# #
# #     @pytestrail.case('24645')
# #     def test_24645(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         ei_create['planning']['budget']['period']['startDate'] = '2020-01-01T00:00:00Z'
# #         ei_create['planning']['budget']['period']['endDate'] = '2020-12-09T00:00:00Z'
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['planning']['budget']['period']['startDate'] = '2020-01-01T00:00:00Z'
# #         fs_create['planning']['budget']['period']['endDate'] = '2020-12-09T00:00:00Z'
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.10.01.01'
# #         assert create_fs_response[1]['errors'][0]['description'] == 'Invalid period.'
# #
# #     @pytestrail.case('24646')
# #     def test_24646(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['planning']['budget']['isEuropeanUnionFunded'] = True
# #         del fs_create['planning']['budget']['europeanUnionFunding']['projectName']
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
# #         assert create_fs_response[1]['errors'][0]['description'] ==
# #
# #     @pytestrail.case('24647')
# #     def test_24647(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['planning']['budget']['isEuropeanUnionFunded'] = True
# #         del fs_create['planning']['budget']['europeanUnionFunding']['projectIdentifier']
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
# #         assert create_fs_response[1]['errors'][0]['description'] ==
# #     @pytestrail.case('24648')
# #     def test_24648_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create_1 = copy.deepcopy(fs_create_obligatory_treasury_money)
# #         fs_create_1['planning']['budget']['amount']['currency'] = 'MDL'
# #         create_fs_response_1 = bpe_create_fs(ei_create, fs_create_1)
# #         time.sleep(2)
# #         fs_create_2 = copy.deepcopy(fs_create_obligatory_treasury_money)
# #         fs_create_2['planning']['budget']['amount']['currency'] = 'EUR'
# #         access_token = get_access_token_for_platform_one()
# #         x_operation_id = get_x_operation_id(access_token)
# #         host = set_instance_for_request()
# #         requests.post(
# #             url=host + create_fs + create_fs_response_1[3],
# #             headers={
# #                 'Authorization': 'Bearer ' + access_token,
# #                 'X-OPERATION-ID': x_operation_id,
# #                 'Content-Type': 'application/json'},
# #             json=fs_create_2)
# #         time.sleep(2)
# #
# #         get_message_from_kafka(x_operation_id)
# #
# #         assert create_fs_response_1[0].text == 'ok'
# #         assert create_fs_response_1[0].status_code == 202
# #         assert create_fs_response_1[1]['X-OPERATION-ID'] == create_fs_response_1[2]
# #
# #     @pytestrail.case('24648')
# #     def test_24648_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create_1 = copy.deepcopy(fs_create_obligatory_treasury_money)
# #         fs_create_1['planning']['budget']['amount']['currency'] = 'MDL'
# #         create_fs_response_1 = bpe_create_fs(ei_create, fs_create_1)
# #         time.sleep(2)
# #         fs_create_2 = copy.deepcopy(fs_create_obligatory_treasury_money)
# #         fs_create_2['planning']['budget']['amount']['currency'] = 'EUR'
# #         access_token = get_access_token_for_platform_one()
# #         x_operation_id = get_x_operation_id(access_token)
# #         host = set_instance_for_request()
# #         requests.post(
# #             url=host + create_fs + create_fs_response_1[3],
# #             headers={
# #                 'Authorization': 'Bearer ' + access_token,
# #                 'X-OPERATION-ID': x_operation_id,
# #                 'Content-Type': 'application/json'},
# #             json=fs_create_2)
# #         time.sleep(2)
# #
# #         messages = get_message_from_kafka(x_operation_id)
# #
# #         assert messages['X-OPERATION-ID'] == x_operation_id
# #         assert messages['errors'][0]['code'] == '400.10.00.06'
# #         assert messages['errors'][0]['description'] == 'Invalid currency.'
# #
# #     @pytestrail.case('24649')
# #     def test_24649(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['planning']['budget']['period']['startDate'] = '2020/08/10T11:00:00Z'
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
# #         assert create_fs_response[1]['errors'][0]['description'] == \
# #                f"com.fasterxml.jackson.databind.JsonMappingException: Text " \
# #                f"'{fs_create['planning']['budget']['period']['startDate']}' " \
# #                f"could not be parsed at index 4 (through reference chain: com.procurement.budget.model.dto.fs." \
# #                f"request.FsCreate[\"planning\"]->com.procurement.budget.model.dto.fs.request.PlanningFsCreate" \
# #                f"[\"budget\"]->com.procurement.budget.model.dto.fs.request.BudgetFsCreate[\"period\"]->com." \
# #                f"procurement.budget.model.dto.ocds.Period[\"startDate\"])"
# #
# #     @pytestrail.case('24650')
# #     def test_24650_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24650')
# #     def test_24650_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
# #         token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         assert token == True
# #
# #     @pytestrail.case('24650')
# #     def test_24650_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_create).json()
# #
# #         assert publicPoint_create['releases'][0]['tag'][0] == 'planning'
# #
# #     @pytestrail.case('24651')
# #     def test_24651_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24651')
# #     def test_24651_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
# #         token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         assert token == True
# #
# #     @pytestrail.case('24651')
# #     def test_24651_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data'][
# 'outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_create).json()
# #
# #         date_from_database = get_date_execute_cql_from_orchestrator_operation_step_by_oper_id(create_fs_response[2],
# #                                                                                               'NoticeCreateRel
# easeTask')
# #         date_in_format = date_from_database.strftime('%Y-%m-%dT%H:%M:%SZ')
# #
# #         assert publicPoint_create['releases'][0]['date'] == date_in_format
# #
# #     @pytestrail.case('24652')
# #     def test_24652_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
# #         token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         assert token == True
# #
# #     @pytestrail.case('24652')
# #     def test_24652_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #
# #         time.sleep(2)
# #         url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_create).json()
# #
# #         timestamp = fnmatch.fnmatch(publicPoint_create['releases'][0]['id'][46:58], '*')
# #
# #         assert publicPoint_create['releases'][0]['id'][0:28] == create_fs_response[1]['data']['outcomes']['fs'][0][
# #                                                                     'id'][0:28]
# #         assert publicPoint_create['releases'][0]['id'][28:32] == create_fs_response[1]['data']['outcomes']['fs'][0][
# #                                                                      'id'][28:32]
# #         assert publicPoint_create['releases'][0]['id'][32:45] == create_fs_response[1]['data']['outcomes']['fs'][0][
# #                                                                      'id'][32:45]
# #         assert publicPoint_create['releases'][0]['id'][45:46] == '-'
# #         assert timestamp == True
# #
# #     @pytestrail.case('24653')
# #     def test_24653_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create_1 = copy.deepcopy(fs_create_obligatory_treasury_money)
# #         fs_create_1['planning']['budget']['amount']['amount'] = 133.26
# #         fs_create_1['planning']['budget']['amount']['currency'] = 'EUR'
# #         create_fs_response_1 = bpe_create_fs(ei_create, fs_create_1)
# #         time.sleep(2)
# #
# #         fs_create_2 = copy.deepcopy(fs_create_full_own_money)
# #         fs_create_1['planning']['budget']['amount']['amount'] = 50.34
# #         fs_create_1['planning']['budget']['amount']['currency'] = 'EUR'
# #
# #         access_token = get_access_token_for_platform_one()
# #         x_operation_id = get_x_operation_id(access_token)
# #         host = set_instance_for_request()
# #         requests.post(
# #             url=host + create_fs + create_fs_response_1[3],
# #             headers={
# #                 'Authorization': 'Bearer ' + access_token,
# #                 'X-OPERATION-ID': x_operation_id,
# #                 'Content-Type': 'application/json'},
# #             json=fs_create_2)
# #         time.sleep(2)
# #
# #         get_message_from_kafka(x_operation_id)
# #
# #         assert create_fs_response_1[0].text == 'ok'
# #         assert create_fs_response_1[0].status_code == 202
# #         assert create_fs_response_1[1]['X-OPERATION-ID'] == create_fs_response_1[2]
# #
# #     @pytestrail.case('24653')
# #     def test_24653_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create_1 = copy.deepcopy(fs_create_obligatory_treasury_money)
# #         fs_create_1['planning']['budget']['amount']['amount'] = 133.26
# #         fs_create_1['planning']['budget']['amount']['currency'] = 'EUR'
# #         create_fs_response_1 = bpe_create_fs(ei_create, fs_create_1)
# #         time.sleep(2)
# #
# #         fs_create_2 = copy.deepcopy(fs_create_full_own_money)
# #         fs_create_1['planning']['budget']['amount']['amount'] = 50.34
# #         fs_create_1['planning']['budget']['amount']['currency'] = 'EUR'
# #
# #         access_token = get_access_token_for_platform_one()
# #         x_operation_id = get_x_operation_id(access_token)
# #         host = set_instance_for_request()
# #         requests.post(
# #             url=host + create_fs + create_fs_response_1[3],
# #             headers={
# #                 'Authorization': 'Bearer ' + access_token,
# #                 'X-OPERATION-ID': x_operation_id,
# #                 'Content-Type': 'application/json'},
# #             json=fs_create_2)
# #         time.sleep(2)
# #
# #         get_message_from_kafka(x_operation_id)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response_1[1]['data']['ocid'], '*')
# #         assert ocid == True
# #         assert create_fs_response_1[1]['X-OPERATION-ID'] == create_fs_response_1[2]
# #
# #     @pytestrail.case('24653')
# #     def test_24653_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create_1 = copy.deepcopy(fs_create_obligatory_treasury_money)
# #         fs_create_1['planning']['budget']['amount']['amount'] = 133.26
# #         fs_create_1['planning']['budget']['amount']['currency'] = 'EUR'
# #         create_fs_response_1 = bpe_create_fs(ei_create, fs_create_1)
# #         time.sleep(2)
# #
# #         fs_create_2 = copy.deepcopy(fs_create_full_own_money)
# #         fs_create_2['planning']['budget']['amount']['amount'] = 50.34
# #         fs_create_2['planning']['budget']['amount']['currency'] = 'EUR'
# #
# #         access_token = get_access_token_for_platform_one()
# #         x_operation_id = get_x_operation_id(access_token)
# #         host = set_instance_for_request()
# #         requests.post(
# #             url=host + create_fs + create_fs_response_1[3],
# #             headers={
# #                 'Authorization': 'Bearer ' + access_token,
# #                 'X-OPERATION-ID': x_operation_id,
# #                 'Content-Type': 'application/json'},
# #             json=fs_create_2)
# #         time.sleep(2)
# #
# #         message_from_kafka = get_message_from_kafka(x_operation_id)
# #         url_create_ei = message_from_kafka['data']['url'] + '/' + message_from_kafka['data']['outcomes'][
# 'fs'][0]['id'][
# #                                                                   0:28]
# #
# #         publicPoint_create_ei = requests.get(url=url_create_ei).json()
# #         sum_of_fs = fs_create_1['planning']['budget']['amount']['amount'] + fs_create_2['planning']['
# budget']['amount'][
# #             'amount']
# #
# #         assert publicPoint_create_ei['releases'][0]['planning']['budget']['amount']['amount'] == sum_of_fs
# #
# #     @pytestrail.case('24655')
# #     def test_24655_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create_1 = copy.deepcopy(fs_create_obligatory_treasury_money)
# #         fs_create_1['planning']['budget']['amount']['currency'] = 'MDL'
# #         create_fs_response_1 = bpe_create_fs(ei_create, fs_create_1)
# #
# #         assert create_fs_response_1[0].text == 'ok'
# #         assert create_fs_response_1[0].status_code == 202
# #         assert create_fs_response_1[1]['X-OPERATION-ID'] == create_fs_response_1[2]
# #
# #     @pytestrail.case('24655')
# #     def test_24655_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create_1 = copy.deepcopy(fs_create_obligatory_treasury_money)
# #         fs_create_1['planning']['budget']['amount']['currency'] = 'MDL'
# #         create_fs_response_1 = bpe_create_fs(ei_create, fs_create_1)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response_1[1]['data']['ocid'], '*')
# #         assert ocid == True
# #         assert create_fs_response_1[1]['X-OPERATION-ID'] == create_fs_response_1[2]
# #
# #     @pytestrail.case('24655')
# #     def test_24655_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create_1 = copy.deepcopy(fs_create_obligatory_treasury_money)
# #         fs_create_1['planning']['budget']['amount']['currency'] = 'MDL'
# #         create_fs_response_1 = bpe_create_fs(ei_create, fs_create_1)
# #
# #         url_create_ei = create_fs_response_1[1]['data']['url'] + '/' + create_fs_response_1[3]
# #
# #         publicPoint_create_ei = requests.get(url=url_create_ei).json()
# #         print(url_create_ei)
# #         assert publicPoint_create_ei['releases'][0]['planning']['budget']['amount']['currency'] == \
# #                fs_create_1['planning']['budget']['amount']['currency']
# #
# #     @pytestrail.case('24656')
# #     def test_24656(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create_1 = copy.deepcopy(fs_create_obligatory_treasury_money)
# #         fs_create_1['planning']['budget']['amount']['currency'] = 'EUR'
# #         create_fs_response_1 = bpe_create_fs(ei_create, fs_create_1)
# #         time.sleep(2)
# #
# #         fs_create_2 = copy.deepcopy(fs_create_full_own_money)
# #         fs_create_2['planning']['budget']['amount']['currency'] = 'USD'
# #
# #         access_token = get_access_token_for_platform_one()
# #         x_operation_id = get_x_operation_id(access_token)
# #         host = set_instance_for_request()
# #         requests.post(
# #             url=host + create_fs + create_fs_response_1[3],
# #             headers={
# #                 'Authorization': 'Bearer ' + access_token,
# #                 'X-OPERATION-ID': x_operation_id,
# #                 'Content-Type': 'application/json'},
# #             json=fs_create_2)
# #         time.sleep(2)
# #
# #         message_from_kafka = get_message_from_kafka(x_operation_id)
# #
# #         assert message_from_kafka['errors'][0]['code'] == '400.10.00.06'
# #         assert message_from_kafka['errors'][0]['description'] == 'Invalid currency.'
# #
# #     @pytestrail.case('24657')
# #     def test_24657_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['country']['id'] = 'MD'
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24657')
# #     def test_24657_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['country']['id'] = 'MD'
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
# #         token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         assert token == True
# #
# #     @pytestrail.case('24657')
# #     def test_24657_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['country']['id'] = 'MD'
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_create).json()
# #         country_scheme = fnmatch.fnmatch(publicPoint_create['releases'][0]['parties'][0]
# #                                          ['address']['addressDetails']['country']['scheme'], '*')
# #         country_id = fnmatch.fnmatch(
# #             publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country']['id'], '*')
# #         country_description = fnmatch.fnmatch(
# #             publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country']['
# description'], '*')
# #         country_uri = fnmatch.fnmatch(
# #             publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country']['uri'], '*')
# #
# #         assert country_scheme == True
# #         assert country_id == True
# #         assert country_description == True
# #         assert country_uri == True
# #         assert publicPoint_create['releases'][0]['parties'][0]['roles'][0] == 'payer'
# #
# #     @pytestrail.case('24657')
# #     def test_24657_4(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_obligatory_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['country']['id'] = 'MD'
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_create).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country']['id'] == \
# #                fs_create['tender']['procuringEntity']['address']['addressDetails']['country']['id']
# #         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country'][
# #                    'description'] == 'Moldova, Republica'
# #         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country'][
# #                    'scheme'] == 'iso-alpha2'
# #         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country'][
# #                    'uri'] == 'https://www.iso.org'
# #
# #     @pytestrail.case('24658')
# #     def test_24658_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['buyer']['address']['addressDetails']['country']['id'] = 'MD'
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24658')
# #     def test_24658_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['buyer']['address']['addressDetails']['country']['id'] = 'MD'
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
# #         token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         assert token == True
# #
# #     @pytestrail.case('24658')
# #     def test_24658_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['buyer']['address']['addressDetails']['country']['id'] = 'MD'
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_create).json()
# #         country_scheme = fnmatch.fnmatch(publicPoint_create['releases'][0]['parties'][0]
# #                                          ['address']['addressDetails']['country']['scheme'], '*')
# #         country_id = fnmatch.fnmatch(
# #             publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country']['id'], '*')
# #         country_description = fnmatch.fnmatch(
# #             publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country'][
# 'description'], '*')
# #         country_uri = fnmatch.fnmatch(
# #             publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country']['uri'], '*')
# #
# #         assert country_scheme == True
# #         assert country_id == True
# #         assert country_description == True
# #         assert country_uri == True
# #         assert publicPoint_create['releases'][0]['parties'][0]['roles'][0] == 'funder'
# #         assert publicPoint_create['releases'][0]['parties'][1]['roles'][0] == 'payer'
# #
# #     @pytestrail.case('24658')
# #     def test_24658_4(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_own_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['country']['id'] = 'MD'
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_create).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country']['id'] == \
# #                fs_create['buyer']['address']['addressDetails']['country']['id']
# #         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country'][
# #                    'description'] == 'Moldova, Republica'
# #         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country'][
# #                    'scheme'] == 'iso-alpha2'
# #         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country'][
# #                    'uri'] == 'https://www.iso.org'
# #
# #     @pytestrail.case('24659')
# #     def test_24659_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails'] = {
# #             "country": {
# #                 "id": "MD",
# #                 "scheme": "prosto_scheme"
# #             },
# #             "region": {
# #                 "id": "3400000"
# #             },
# #             "locality": {
# #                 "scheme": "CUATM",
# #                 "id": "3401000",
# #                 "description": ""
# #             }
# #         }
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24659')
# #     def test_24659_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails'] = {
# #             "country": {
# #                 "id": "MD",
# #                 "scheme": "prosto_scheme"
# #             },
# #             "region": {
# #                 "id": "3400000"
# #             },
# #             "locality": {
# #                 "scheme": "CUATM",
# #                 "id": "3401000",
# #                 "description": ""
# #             }
# #         }
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
# #         token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         assert token == True
# #
# #     @pytestrail.case('24659')
# #     def test_24659_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails'] = {
# #             "country": {
# #                 "id": "MD",
# #                 "scheme": "prosto_scheme"
# #             },
# #             "region": {
# #                 "id": "3400000"
# #             },
# #             "locality": {
# #                 "scheme": "CUATM",
# #                 "id": "3401000",
# #                 "description": ""
# #             }
# #         }
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_create).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country'][
# #                    'scheme'] == 'iso-alpha2'
# #
# #     @pytestrail.case('24660')
# #     def test_24660_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails'] = {
# #             "country": {
# #                 "id": "MD",
# #                 "uri": "www.lol.md"
# #             },
# #             "region": {
# #                 "id": "3400000"
# #             },
# #             "locality": {
# #                 "scheme": "CUATM",
# #                 "id": "3401000",
# #                 "description": ""
# #             }
# #         }
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24660')
# #     def test_24660_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails'] = {
# #             "country": {
# #                 "id": "MD",
# #                 "uri": "www.lol.md"
# #             },
# #             "region": {
# #                 "id": "3400000"
# #             },
# #             "locality": {
# #                 "scheme": "CUATM",
# #                 "id": "3401000",
# #                 "description": ""
# #             }
# #         }
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
# #         token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         assert token == True
# #
# #     @pytestrail.case('24660')
# #     def test_24660_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails'] = {
# #             "country": {
# #                 "id": "MD",
# #                 "uri": "www.lol.md"
# #             },
# #             "region": {
# #                 "id": "3400000"
# #             },
# #             "locality": {
# #                 "scheme": "CUATM",
# #                 "id": "3401000",
# #                 "description": ""
# #             }
# #         }
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_create).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country'][
# #                    'uri'] == 'https://www.iso.org'
# #
# #     @pytestrail.case('24661')
# #     def test_24661_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails'] = {
# #             "country": {
# #                 "id": "MD",
# #                 "description": " opis_polya_1"
# #             },
# #             "region": {
# #                 "id": "3400000"
# #             },
# #             "locality": {
# #                 "scheme": "CUATM",
# #                 "id": "3401000",
# #                 "description": ""
# #             }
# #         }
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24661')
# #     def test_24661_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails'] = {
# #             "country": {
# #                 "id": "MD",
# #                 "description": " opis_polya_1"
# #             },
# #             "region": {
# #                 "id": "3400000"
# #             },
# #             "locality": {
# #                 "scheme": "CUATM",
# #                 "id": "3401000",
# #                 "description": ""
# #             }
# #         }
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
# #         token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         assert token == True
# #
# #     @pytestrail.case('24661')
# #     def test_24661_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails'] = {
# #             "country": {
# #                 "id": "MD",
# #                 "description": " opis_polya_1"
# #             },
# #             "region": {
# #                 "id": "3400000"
# #             },
# #             "locality": {
# #                 "scheme": "CUATM",
# #                 "id": "3401000",
# #                 "description": ""
# #             }
# #         }
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_create).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country'][
# #                    'description'] == 'Moldova, Republica'
# #
# #     @pytestrail.case('24662')
# #     def test_24662_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['country']['id'] = 'DE'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24662')
# #     def test_24662_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['country']['id'] = 'DE'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.01.10'
# #         assert create_fs_response[1]['errors'][0]['description'] == 'Invalid country. '
# #
# #     @pytestrail.case('24663')
# #     def test_24663_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24663')
# #     def test_24663_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
# #         token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         assert token == True
# #
# #     @pytestrail.case('24663')
# #     def test_24663_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_create).json()
# #
# #         check_region_scheme = fnmatch.fnmatch(
# #             publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['region']['scheme'], '*')
# #         check_region_id = fnmatch.fnmatch(
# #             publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['region']['id'], '*')
# #         check_region_description = fnmatch.fnmatch(
# #             publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['region'][
# 'description'], '*')
# #         check_region_uri = fnmatch.fnmatch(
# #             publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['region']['uri'], '*')
# #
# #         assert check_region_scheme == True
# #         assert check_region_id == True
# #         assert check_region_description == True
# #         assert check_region_uri == True
# #
# #     @pytestrail.case('24663')
# #     def test_24663_4(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_create).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['region'][
# #                    'scheme'] == 'CUATM'
# #         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['region']['id'] == \
# #                fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id']
# #         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['region'][
# #                    'description'] == 'Donduşeni'
# #         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['region'][
# #                    'uri'] == 'http://statistica.md'
# #
# #     @pytestrail.case('24664')
# #     def test_24664_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['scheme'] = 'prosto_scheme'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24664')
# #     def test_24664_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['scheme'] = 'prosto_scheme'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
# #         token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         assert token == True
# #
# #     @pytestrail.case('24664')
# #     def test_24664_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['scheme'] = 'prosto_scheme'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_create).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['region'][
# #                    'scheme'] == 'CUATM'
# #
# #     @pytestrail.case('24665')
# #     def test_24665_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['uri'] = 'prosto_uri'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24665')
# #     def test_24665_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['uri'] = 'prosto_uri'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
# #         token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         assert token == True
# #
# #     @pytestrail.case('24665')
# #     def test_24665_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['uri'] = 'prosto_uri'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_create).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['region'][
# #                    'uri'] == 'http://statistica.md'
# #
# #     @pytestrail.case('24666')
# #     def test_24666_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['description'] = '
# prosto_descri'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24666')
# #     def test_24666_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['description'] = '
# prosto_descri'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
# #         token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         assert token == True
# #
# #     @pytestrail.case('24666')
# #     def test_24666_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['description'] = '
# prosto_descri'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_create).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['region'][
# #                    'description'] == 'Donduşeni'
# #
# #     @pytestrail.case('24667')
# #     def test_24667_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '4to_popalo'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24667')
# #     def test_24667_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '4to_popalo'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00.13'
# #         assert create_fs_response[1]['errors'][0]['description'] == 'Region not found. '
# #
# #     @pytestrail.case('24668')
# #     def test_24668_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['locality'] = {
# #             "scheme": "CUATM",
# #             "id": "4to_popalo",
# #             "description": "google"
# #         }
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24668')
# #     def test_24668_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['locality'] = {
# #             "scheme": "CUATM",
# #             "id": "4to_popalo",
# #             "description": "google"
# #         }
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00.14'
# #         assert create_fs_response[1]['errors'][0]['description'] == 'Locality not found. '
# #
# #     @pytestrail.case('24669')
# #     def test_24669_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id'] = '3401000'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] = 'CUATM'
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24669')
# #     def test_24669_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id'] = '3401000'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] = 'CUATM'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
# #         token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         assert token == True
# #
# #     @pytestrail.case('24669')
# #     def test_24669_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id'] = '3401000'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] = 'CUATM'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_create).json()
# #
# #         check_locality_scheme = fnmatch.fnmatch(
# #             publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality']['scheme'], '*')
# #         check_locality_id = fnmatch.fnmatch(
# #             publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality']['id'], '*')
# #         check_locality_description = fnmatch.fnmatch(
# #             publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality']['description'],
# #             '*')
# #         check_locality_uri = fnmatch.fnmatch(
# #             publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality']['uri'], '*')
# #
# #         assert check_locality_scheme == True
# #         assert check_locality_id == True
# #         assert check_locality_description == True
# #         assert check_locality_uri == True
# #
# #     @pytestrail.case('24669')
# #     def test_24669_4(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id'] = '3401000'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] = 'CUATM'
# #
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_create).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality'][
# #                    'scheme'] == 'CUATM'
# #         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality']['id'] == \
# #                fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id']
# #         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality'][
# #                    'description'] == 'or.Donduşeni (r-l Donduşeni)'
# #         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality'][
# #                    'uri'] == 'http://statistica.md'
# #
# #     @pytestrail.case('24670')
# #     def test_24670_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id'] = '3401000'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] = 'other'
# #         del fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['description']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24670')
# #     def test_24670_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id'] = '3401000'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] = 'other'
# #         del fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['description']
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
# #         assert create_fs_response[1]['errors'][0]['description'] ==
# #
# #     @pytestrail.case('24671')
# #     def test_24671_1(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id'] = '777K'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] = 'other'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['description'] = 'rusanovka'
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         assert create_fs_response[0].text == 'ok'
# #         assert create_fs_response[0].status_code == 202
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #
# #     @pytestrail.case('24671')
# #     def test_24671_2(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id'] = '777K'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] = 'other'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['description'] = 'rusanovka'
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
# #         token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')
# #
# #         assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
# #         assert ocid == True
# #         assert token == True
# #
# #     @pytestrail.case('24671')
# #     def test_24671_3(self):
# #         ei_create = copy.deepcopy(ei_full)
# #         fs_create = copy.deepcopy(fs_create_full_treasury_money)
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id'] = '777K'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] = 'other'
# #         fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['description'] = 'rusanovka'
# #         create_fs_response = bpe_create_fs(ei_create, fs_create)
# #         time.sleep(2)
# #
# #         url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['
# outcomes']['fs'][0][
# #             'id']
# #         publicPoint_create = requests.get(url=url_create).json()
# #
# #         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality'][
# #                    'scheme'] == fs_create['tender']['procuringEntity']['address']['addressDetails']['locality'][
# #                    'scheme']
# #         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality']['id'] == \
# #                fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id']
# #         assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality'][
# #                    'description'] == fs_create['tender']['procuringEntity']['address']['
# addressDetails']['locality'][
# #                    'description']
#
#
# # Actual version for Allure
# import copy
# import json
#
# from pytest_testrail.plugin import pytestrail
#
# from tests.essences.fs import FS
# from tests.payloads.fs_payload import payload_fs_full_data_model_own_money
# from useful_functions import compare_actual_result_and_expected_result
#
#
# class TestCheckOnImpossibilityOfCreatingFsObligatoryDataIfTheObligatoryAttributesAreMissedOfThePayload(object):
#     @pytestrail.case("24605")
#     def test_delete_tender_attribute_from_the_payload_24605_1(self, country, language):
#         payload = copy.deepcopy(payload_fs_full_data_model_own_money)
#         del payload["tender"]
#         fs = FS(payload=payload, lang=language, country=country)
#         fs.insert_ei_full_data_model()
#         fs.create_fs()
#         message_from_kafka = fs.get_message_from_kafka()
#         actual_result = str(message_from_kafka["errors"])
#         expected_result = str([{"code": "400.00.00.00", "description": "Data processing exception."}])
#         assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)
