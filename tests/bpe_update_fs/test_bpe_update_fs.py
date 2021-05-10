import copy
from uuid import uuid4
import requests
from pytest_testrail.plugin import pytestrail
from tests.essences.fs import FS
from tests.payloads.fs_payload import payload_fs_obligatory_data_model_treasury_money
from useful_functions import prepared_cp_id, compare_actual_result_and_expected_result, get_new_period, \
    get_human_date_in_utc_format


class TestCheckOnCorrectnessOfUpdatingFsTreasuryObligatoryDataModelToTreasuryObligatoryDataModel(object):
    @pytestrail.case("27559")
    def test_check_on_correctness_of_publishing_fs_27559_3(self, country, language, instance, cassandra_username,
                                                           cassandra_password):
        date = get_new_period()
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_fs_obligatory_data_model_treasury_money)
        payload["planning"]["budget"]["amount"]["amount"] = 9959.99
        payload["planning"]["budget"]["period"]["startDate"] = date[0]
        payload["planning"]["budget"]["period"]["endDate"] = date[1]
        payload["planning"]["budget"]["isEuropeanUnionFunded"] = True
        payload["planning"]["budget"]["europeanUnionFunding"] = {
            "projectName": "update name of this project",
            "projectIdentifier": "update projectIdentifier",
            "uri": " update http://uriuri.th"
        }

        fs = FS(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        create_fs_response = fs.insert_fs_treasury_obligatory(
            cp_id=cp_id,
            ei_token=ei_token
        )
        url_create = create_fs_response[0] + "/" + create_fs_response[1]
        fs_create = requests.get(url=url_create).json()
        fs.update_fs(
            cp_id=cp_id,
            fs_id=create_fs_response[1],
            fs_token=str(create_fs_response[2])
        )
        message_from_kafka = fs.get_message_from_kafka()
        url_update = message_from_kafka['data']['url']
        fs_update = requests.get(url=url_update).json()
        release_list = list()
        for key, values in fs_update["releases"][0]["parties"][0].items():
            if key == "roles":
                role = fs_update["releases"][0]["parties"][0].get(key)
                release_list.append(role[0])
        keys_list = list()
        for i in fs_update.keys():
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
        for i in fs_update["publisher"].keys():
            if i == "name":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_update["releases"][0].keys():
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
        for i in fs_update["releases"][0]["tender"].keys():
            if i == "id":
                keys_list.append(i)
            if i == "status":
                keys_list.append(i)
            if i == "statusDetails":
                keys_list.append(i)
        for i in fs_update["releases"][0]["parties"][0].keys():
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
        for i in fs_update["releases"][0]["parties"][0]["identifier"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "legalName":
                keys_list.append(i)
        for i in fs_update["releases"][0]["parties"][0]["address"].keys():
            if i == "streetAddress":
                keys_list.append(i)
            if i == "addressDetails":
                keys_list.append(i)
        for i in fs_update["releases"][0]["parties"][0]["address"]["addressDetails"].keys():
            if i == "country":
                keys_list.append(i)
            if i == "region":
                keys_list.append(i)
            if i == "locality":
                keys_list.append(i)
        for i in fs_update["releases"][0]["parties"][0]["address"]["addressDetails"]["country"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_update["releases"][0]["parties"][0]["address"]["addressDetails"]["region"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_update["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in fs_update["releases"][0]["parties"][0]["contactPoint"].keys():
            if i == "name":
                keys_list.append(i)
            if i == "email":
                keys_list.append(i)
            if i == "telephone":
                keys_list.append(i)
        for i in fs_update["releases"][0]["planning"].keys():
            if i == "budget":
                keys_list.append(i)
        for i in fs_update["releases"][0]["planning"]["budget"].keys():
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
        for i in fs_update["releases"][0]["planning"]["budget"]["period"].keys():
            if i == "startDate":
                keys_list.append(i)
            if i == "endDate":
                keys_list.append(i)
        for i in fs_update["releases"][0]["planning"]["budget"]["amount"].keys():
            if i == "amount":
                keys_list.append(i)
            if i == "currency":
                keys_list.append(i)
        for i in fs_update["releases"][0]["planning"]["budget"]["sourceEntity"].keys():
            if i == "id":
                keys_list.append(i)
            if i == "name":
                keys_list.append(i)
        for i in fs_update["releases"][0]["relatedProcesses"][0].keys():
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
        for i in fs_update["releases"][0]["planning"]["budget"]["europeanUnionFunding"].keys():
            if i == "projectIdentifier":
                keys_list.append(i)
            if i == "projectName":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)

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
            expected_result="projectIdentifier",
            actual_result=keys_list[68]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="projectName",
            actual_result=keys_list[69]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="uri",
            actual_result=keys_list[70]
        )

        assert compare_actual_result_and_expected_result(expected_result=fs_create["uri"],
                                                         actual_result=fs_update["uri"])
        assert compare_actual_result_and_expected_result(expected_result=fs_create["version"],
                                                         actual_result=fs_update["version"])
        assert compare_actual_result_and_expected_result(expected_result=fs_create["extensions"],
                                                         actual_result=fs_update["extensions"])
        assert compare_actual_result_and_expected_result(expected_result=fs_create["publisher"]["name"],
                                                         actual_result=fs_update["publisher"]["name"])
        assert compare_actual_result_and_expected_result(expected_result=fs_create["publisher"]["uri"],
                                                         actual_result=fs_update["publisher"]["uri"])
        assert compare_actual_result_and_expected_result(expected_result=fs_create["license"],
                                                         actual_result=fs_update["license"])
        assert compare_actual_result_and_expected_result(expected_result=fs_create["publicationPolicy"],
                                                         actual_result=fs_update["publicationPolicy"])
        assert compare_actual_result_and_expected_result(expected_result=fs_create["publishedDate"],
                                                         actual_result=fs_update["publishedDate"])
        assert compare_actual_result_and_expected_result(expected_result=fs_create["releases"][0]["ocid"],
                                                         actual_result=fs_update["releases"][0]["ocid"])
        assert compare_actual_result_and_expected_result(expected_result=fs_create["releases"][0]["id"][0:46],
                                                         actual_result=fs_update["releases"][0]["id"][0:46])
        assert compare_actual_result_and_expected_result(
            expected_result=get_human_date_in_utc_format(int(fs_update["releases"][0]["id"][46:59]))[0],
            actual_result=fs_update["releases"][0]["date"])
        assert compare_actual_result_and_expected_result(expected_result=message_from_kafka["data"]["operationDate"],
                                                         actual_result=fs_update["releases"][0]["date"])
        assert compare_actual_result_and_expected_result(expected_result=fs_create["releases"][0]["tag"][0],
                                                         actual_result=fs_update["releases"][0]["tag"][0])
        assert compare_actual_result_and_expected_result(expected_result=fs_create["releases"][0]["initiationType"],
                                                         actual_result=fs_update["releases"][0]["initiationType"])
        assert compare_actual_result_and_expected_result(expected_result=fs_create["releases"][0]["tender"]["id"],
                                                         actual_result=fs_update["releases"][0]["tender"]["id"])
        assert compare_actual_result_and_expected_result(expected_result=fs_create["releases"][0]["tender"]["status"],
                                                         actual_result=fs_update["releases"][0]["tender"]["status"])
        assert compare_actual_result_and_expected_result(
            expected_result=fs_create["releases"][0]["tender"]["statusDetails"],
            actual_result=fs_update["releases"][0]["tender"]["statusDetails"])
        assert compare_actual_result_and_expected_result(expected_result=fs_create["releases"][0]["parties"][0]["id"],
                                                         actual_result=fs_update["releases"][0]["parties"][0]["id"])
        assert compare_actual_result_and_expected_result(expected_result=fs_create["releases"][0]["parties"][0]["name"],
                                                         actual_result=fs_update["releases"][0]["parties"][0]["name"])
        assert compare_actual_result_and_expected_result(
            expected_result=fs_create["releases"][0]["parties"][0]["identifier"]["scheme"],
            actual_result=fs_update["releases"][0]["parties"][0]["identifier"]["scheme"])
        assert compare_actual_result_and_expected_result(
            expected_result=fs_create["releases"][0]["parties"][0]["identifier"]["id"],
            actual_result=fs_update["releases"][0]["parties"][0]["identifier"]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result=fs_create["releases"][0]["parties"][0]["identifier"]["legalName"],
            actual_result=fs_update["releases"][0]["parties"][0]["identifier"]["legalName"])
        assert compare_actual_result_and_expected_result(
            expected_result=fs_create["releases"][0]["parties"][0]["address"]["streetAddress"],
            actual_result=fs_update["releases"][0]["parties"][0]["address"]["streetAddress"])
        assert compare_actual_result_and_expected_result(
            expected_result=fs_create["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["scheme"],
            actual_result=fs_update["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["scheme"])
        assert compare_actual_result_and_expected_result(
            expected_result=fs_create["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["id"],
            actual_result=fs_update["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result=fs_create["releases"][0]["parties"][0]["address"]["addressDetails"]["country"][
                "description"],
            actual_result=fs_update["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["description"])
        assert compare_actual_result_and_expected_result(
            expected_result=fs_create["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["uri"],
            actual_result=fs_update["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["uri"])
        assert compare_actual_result_and_expected_result(
            expected_result=fs_create["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["scheme"],
            actual_result=fs_update["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["scheme"])
        assert compare_actual_result_and_expected_result(
            expected_result=fs_create["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["id"],
            actual_result=fs_update["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result=fs_create["releases"][0]["parties"][0]["address"]["addressDetails"]["region"][
                "description"],
            actual_result=fs_update["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["description"])
        assert compare_actual_result_and_expected_result(
            expected_result=fs_create["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["uri"],
            actual_result=fs_update["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["uri"])
        assert compare_actual_result_and_expected_result(
            expected_result=fs_create["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["scheme"],
            actual_result=fs_update["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["scheme"])
        assert compare_actual_result_and_expected_result(
            expected_result=fs_create["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["id"],
            actual_result=fs_update["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result=fs_create["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
                "description"],
            actual_result=fs_update["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
                "description"])
        assert compare_actual_result_and_expected_result(
            expected_result=fs_create["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["uri"],
            actual_result=fs_update["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["uri"])
        assert compare_actual_result_and_expected_result(
            expected_result=fs_create["releases"][0]["parties"][0]["contactPoint"]["name"],
            actual_result=fs_update["releases"][0]["parties"][0]["contactPoint"]["name"])
        assert compare_actual_result_and_expected_result(
            expected_result=fs_create["releases"][0]["parties"][0]["contactPoint"]["email"],
            actual_result=fs_update["releases"][0]["parties"][0]["contactPoint"]["email"])
        assert compare_actual_result_and_expected_result(
            expected_result=fs_create["releases"][0]["parties"][0]["contactPoint"]["telephone"],
            actual_result=fs_update["releases"][0]["parties"][0]["contactPoint"]["telephone"])
        assert compare_actual_result_and_expected_result(
            expected_result=fs_create["releases"][0]["parties"][0]["roles"][0],
            actual_result=fs_update["releases"][0]["parties"][0]["roles"][0])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["period"]["startDate"],
            actual_result=fs_update["releases"][0]["planning"]["budget"]["period"]["startDate"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["period"]["endDate"],
            actual_result=fs_update["releases"][0]["planning"]["budget"]["period"]["endDate"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["amount"]["amount"],
            actual_result=fs_update["releases"][0]["planning"]["budget"]["amount"]["amount"])
        assert compare_actual_result_and_expected_result(
            expected_result=fs_create["releases"][0]["planning"]["budget"]["amount"]["currency"],
            actual_result=fs_update["releases"][0]["planning"]["budget"]["amount"]["currency"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["isEuropeanUnionFunded"],
            actual_result=fs_update["releases"][0]["planning"]["budget"]["isEuropeanUnionFunded"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["europeanUnionFunding"]["projectName"],
            actual_result=fs_update["releases"][0]["planning"]["budget"]["europeanUnionFunding"]["projectName"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["europeanUnionFunding"]["projectIdentifier"],
            actual_result=fs_update["releases"][0]["planning"]["budget"]["europeanUnionFunding"]["projectIdentifier"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["europeanUnionFunding"]["uri"],
            actual_result=fs_update["releases"][0]["planning"]["budget"]["europeanUnionFunding"]["uri"])
        assert compare_actual_result_and_expected_result(
            expected_result=fs_create["releases"][0]["planning"]["budget"]["verified"],
            actual_result=fs_update["releases"][0]["planning"]["budget"]["verified"])
        assert compare_actual_result_and_expected_result(
            expected_result=fs_create["releases"][0]["planning"]["budget"]["sourceEntity"]["id"],
            actual_result=fs_update["releases"][0]["planning"]["budget"]["sourceEntity"]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result=fs_create["releases"][0]["planning"]["budget"]["sourceEntity"]["name"],
            actual_result=fs_update["releases"][0]["planning"]["budget"]["sourceEntity"]["name"])
        assert compare_actual_result_and_expected_result(
            expected_result=fs_create["releases"][0]["relatedProcesses"][0]["id"],
            actual_result=fs_update["releases"][0]["relatedProcesses"][0]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result=fs_create["releases"][0]["relatedProcesses"][0]["relationship"][0],
            actual_result=fs_update["releases"][0]["relatedProcesses"][0]["relationship"][0])
        assert compare_actual_result_and_expected_result(
            expected_result=fs_create["releases"][0]["relatedProcesses"][0]["scheme"],
            actual_result=fs_update["releases"][0]["relatedProcesses"][0]["scheme"])
        assert compare_actual_result_and_expected_result(
            expected_result=fs_create["releases"][0]["relatedProcesses"][0]["identifier"],
            actual_result=fs_update["releases"][0]["relatedProcesses"][0]["identifier"])
        assert compare_actual_result_and_expected_result(
            expected_result=fs_create["releases"][0]["relatedProcesses"][0]["uri"],
            actual_result=fs_update["releases"][0]["relatedProcesses"][0]["uri"])

# ==============================================================
# class TestBpeCreateEI(object):
#     @pytestrail.case("25537")
#     def test_25537_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         create_fs_currency = \
#             requests.get(url=create_fs_response[0]).json()["releases"][0]["planning"]["budget"]["amount"]["currency"]
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["amount"]["currency"] = "USD"
#         check_currency = fnmatch.fnmatch(create_fs_currency, payload["planning"]["budget"]["amount"]["currency"])
#         if check_currency == False:
#             update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#             assert update_fs_response[0].text == "ok"
#             assert update_fs_response[0].status_code == 202
#             assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         else:
#             print("You use the same currency -> all be fine")
#
#     @pytestrail.case("25537")
#     def test_25537_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         create_fs_currency = \
#             requests.get(url=create_fs_response[0]).json()["releases"][0]["planning"]["budget"]["amount"]["currency"]
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["amount"]["currency"] = "USD"
#         check_currency = fnmatch.fnmatch(create_fs_currency, payload["planning"]["budget"]["amount"]["currency"])
#         if check_currency == False:
#             update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#             assert update_fs_response[0].text == "ok"
#             assert update_fs_response[0].status_code == 202
#             assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#             assert update_fs_response[1]["errors"][0]["code"] == "400.10.00.06"
#             assert update_fs_response[1]["errors"][0]["description"] == "Invalid currency."
#         else:
#             print("You use the same currency -> all be fine")
#
#     @pytestrail.case("25530")
#     def test_25530_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_obligatory_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25530")
#     def test_25530_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_obligatory_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25530")
#     def test_25530_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         publicPoint_create = requests.get(url=create_fs_response[0]).json()
#         payload = copy.deepcopy(fs_update_obligatory_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         time.sleep(2)
#         url_update = update_fs_response[1]["data"]["url"]
#         publicPoint_update = requests.get(url=url_update).json()
#         assert publicPoint_create["releases"][0]["tender"]["id"] == publicPoint_update["releases"][0]["tender"]["id"]
#
#     @pytestrail.case("25531")
#     def test_25531_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_obligatory_own_money)
#         payload["buyer"]["identifier"]["id"] = "update buyer"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25531")
#     def test_25531_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_obligatory_own_money)
#         payload["buyer"]["identifier"]["id"] = "update buyer"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25531")
#     def test_25531_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         publicPoint_create = requests.get(url=create_fs_response[0]).json()
#         payload = copy.deepcopy(fs_update_obligatory_own_money)
#         payload["buyer"]["identifier"]["id"] = "update buyer"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         time.sleep(2)
#         url_update = update_fs_response[1]["data"]["url"]
#         publicPoint_update = requests.get(url=url_update).json()
#         assert publicPoint_create["releases"][0]["planning"]["budget"]["sourceEntity"]["id"] == \
#                publicPoint_update["releases"][0]["planning"]["budget"]["sourceEntity"]["id"]
#
#     @pytestrail.case("25532")
#     def test_25532_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_obligatory_own_money)
#         payload["buyer"]["name"] = "update name of buyer"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25532")
#     def test_25532_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_obligatory_own_money)
#         payload["buyer"]["name"] = "update name of buyer"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25532")
#     def test_25532_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         publicPoint_create = requests.get(url=create_fs_response[0]).json()
#         payload = copy.deepcopy(fs_update_obligatory_own_money)
#         payload["buyer"]["name"] = "update name of buyer"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         time.sleep(2)
#         url_update = update_fs_response[1]["data"]["url"]
#         publicPoint_update = requests.get(url=url_update).json()
#         assert publicPoint_create["releases"][0]["planning"]["budget"]["sourceEntity"]["name"] == \
#                publicPoint_update["releases"][0]["planning"]["budget"]["sourceEntity"]["name"]
#
#     @pytestrail.case("25533")
#     def test_25533_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["tender"]["procuringEntity"]["name"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["identifier"]["id"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["identifier"]["scheme"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["identifier"]["legalName"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["identifier"]["uri"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["id"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["scheme"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["legalName"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["uri"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["address"]["streetAddress"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["address"]["postalCode"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]["id"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["id"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"][
#             "scheme"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"][
#             "description"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["contactPoint"]["name"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["contactPoint"]["email"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["contactPoint"]["telephone"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["contactPoint"]["faxNumber"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["contactPoint"]["url"] = "update value of payer"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25533")
#     def test_25533_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["tender"]["procuringEntity"]["name"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["identifier"]["id"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["identifier"]["scheme"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["identifier"]["legalName"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["identifier"]["uri"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["id"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["scheme"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["legalName"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["uri"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["address"]["streetAddress"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["address"]["postalCode"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]["id"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["id"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"][
#             "scheme"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"][
#             "description"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["contactPoint"]["name"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["contactPoint"]["email"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["contactPoint"]["telephone"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["contactPoint"]["faxNumber"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["contactPoint"]["url"] = "update value of payer"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25533")
#     def test_25533_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         publicPoint_create = requests.get(url=create_fs_response[0]).json()
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["tender"]["procuringEntity"]["name"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["identifier"]["id"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["identifier"]["scheme"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["identifier"]["legalName"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["identifier"]["uri"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["id"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["scheme"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["legalName"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["uri"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["address"]["streetAddress"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["address"]["postalCode"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]["id"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["id"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"][
#             "scheme"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"][
#             "description"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["contactPoint"]["name"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["contactPoint"]["email"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["contactPoint"]["telephone"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["contactPoint"]["faxNumber"] = "update value of payer"
#         payload["tender"]["procuringEntity"]["contactPoint"]["url"] = "update value of payer"
#
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         time.sleep(2)
#         url_update = update_fs_response[1]["data"]["url"]
#         publicPoint_update = requests.get(url=url_update).json()
#         if publicPoint_update["releases"][0]["parties"][0]["roles"][0] == "payer":
#             assert publicPoint_create["releases"][0]["parties"][0]["name"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["name"]
#             assert publicPoint_create["releases"][0]["parties"][0]["identifier"]["scheme"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["identifier"]["scheme"]
#             assert publicPoint_create["releases"][0]["parties"][0]["identifier"]["id"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["identifier"]["id"]
#             assert publicPoint_create["releases"][0]["parties"][0]["identifier"]["legalName"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["identifier"]["legalName"]
#             assert publicPoint_create["releases"][0]["parties"][0]["identifier"]["uri"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["identifier"]["uri"]
#             assert publicPoint_create["releases"][0]["parties"][0]["address"]["streetAddress"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["address"]["streetAddress"]
#             assert publicPoint_create["releases"][0]["parties"][0]["address"]["postalCode"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["address"]["postalCode"]
#             assert publicPoint_create["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["id"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["id"]
#             assert publicPoint_create["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["scheme"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["scheme"]
#             assert publicPoint_create["releases"][0]["parties"][0]["address"]["addressDetails"]["country"][
#                        "description"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["country"][
#                        "description"]
#             assert publicPoint_create["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["uri"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["uri"]
#             assert publicPoint_create["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["id"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["id"]
#             assert publicPoint_create["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["scheme"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["scheme"]
#             assert publicPoint_create["releases"][0]["parties"][0]["address"]["addressDetails"]["region"][
#                        "description"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["description"]
#             assert publicPoint_create["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["uri"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["uri"]
#             assert publicPoint_create["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["id"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["id"]
#             assert publicPoint_create["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["scheme"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["scheme"]
#             assert publicPoint_create["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
#                        "description"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
#                        "description"]
#             assert publicPoint_create["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["uri"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["uri"]
#             assert publicPoint_create["releases"][0]["parties"][0]["additionalIdentifiers"][0]["scheme"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["additionalIdentifiers"][0]["scheme"]
#             assert publicPoint_create["releases"][0]["parties"][0]["additionalIdentifiers"][0]["id"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["additionalIdentifiers"][0]["id"]
#             assert publicPoint_create["releases"][0]["parties"][0]["additionalIdentifiers"][0]["legalName"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["additionalIdentifiers"][0]["legalName"]
#             assert publicPoint_create["releases"][0]["parties"][0]["additionalIdentifiers"][0]["uri"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["additionalIdentifiers"][0]["uri"]
#             assert publicPoint_create["releases"][0]["parties"][0]["contactPoint"]["name"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["contactPoint"]["name"]
#             assert publicPoint_create["releases"][0]["parties"][0]["contactPoint"]["email"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["contactPoint"]["email"]
#             assert publicPoint_create["releases"][0]["parties"][0]["contactPoint"]["telephone"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["contactPoint"]["telephone"]
#             assert publicPoint_create["releases"][0]["parties"][0]["contactPoint"]["faxNumber"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["contactPoint"]["faxNumber"]
#             assert publicPoint_create["releases"][0]["parties"][0]["contactPoint"]["url"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["contactPoint"]["url"]
#         elif publicPoint_update["releases"][0]["parties"][1]["roles"][0] == "payer":
#             assert publicPoint_create["releases"][0]["parties"][1]["name"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["name"]
#             assert publicPoint_create["releases"][0]["parties"][1]["identifier"]["scheme"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["identifier"]["scheme"]
#             assert publicPoint_create["releases"][0]["parties"][1]["identifier"]["id"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["identifier"]["id"]
#             assert publicPoint_create["releases"][0]["parties"][1]["identifier"]["legalName"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["identifier"]["legalName"]
#             assert publicPoint_create["releases"][0]["parties"][1]["identifier"]["uri"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["identifier"]["uri"]
#             assert publicPoint_create["releases"][0]["parties"][1]["address"]["streetAddress"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["address"]["streetAddress"]
#             assert publicPoint_create["releases"][0]["parties"][1]["address"]["postalCode"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["address"]["postalCode"]
#             assert publicPoint_create["releases"][0]["parties"][1]["address"]["addressDetails"]["country"]["id"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["country"]["id"]
#             assert publicPoint_create["releases"][0]["parties"][1]["address"]["addressDetails"]["country"]["scheme"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["country"]["scheme"]
#             assert publicPoint_create["releases"][0]["parties"][1]["address"]["addressDetails"]["country"][
#                        "description"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["country"][
#                        "description"]
#             assert publicPoint_create["releases"][0]["parties"][1]["address"]["addressDetails"]["country"]["uri"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["country"]["uri"]
#             assert publicPoint_create["releases"][0]["parties"][1]["address"]["addressDetails"]["region"]["id"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["region"]["id"]
#             assert publicPoint_create["releases"][0]["parties"][1]["address"]["addressDetails"]["region"]["scheme"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["region"]["scheme"]
#             assert publicPoint_create["releases"][0]["parties"][1]["address"]["addressDetails"]["region"][
#                        "description"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["region"]["description"]
#             assert publicPoint_create["releases"][0]["parties"][1]["address"]["addressDetails"]["region"]["uri"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["region"]["uri"]
#             assert publicPoint_create["releases"][0]["parties"][1]["address"]["addressDetails"]["locality"]["id"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["locality"]["id"]
#             assert publicPoint_create["releases"][0]["parties"][1]["address"]["addressDetails"]["locality"]["scheme"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["locality"]["scheme"]
#             assert publicPoint_create["releases"][0]["parties"][1]["address"]["addressDetails"]["locality"][
#                        "description"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["locality"][
#                        "description"]
#             assert publicPoint_create["releases"][0]["parties"][1]["address"]["addressDetails"]["locality"]["uri"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["locality"]["uri"]
#             assert publicPoint_create["releases"][0]["parties"][1]["additionalIdentifiers"][0]["scheme"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["additionalIdentifiers"][0]["scheme"]
#             assert publicPoint_create["releases"][0]["parties"][1]["additionalIdentifiers"][0]["id"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["additionalIdentifiers"][0]["id"]
#             assert publicPoint_create["releases"][0]["parties"][1]["additionalIdentifiers"][0]["legalName"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["additionalIdentifiers"][0]["legalName"]
#             assert publicPoint_create["releases"][0]["parties"][1]["additionalIdentifiers"][0]["uri"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["additionalIdentifiers"][0]["uri"]
#             assert publicPoint_create["releases"][0]["parties"][1]["contactPoint"]["name"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["contactPoint"]["name"]
#             assert publicPoint_create["releases"][0]["parties"][1]["contactPoint"]["email"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["contactPoint"]["email"]
#             assert publicPoint_create["releases"][0]["parties"][1]["contactPoint"]["telephone"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["contactPoint"]["telephone"]
#             assert publicPoint_create["releases"][0]["parties"][1]["contactPoint"]["faxNumber"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["contactPoint"]["faxNumber"]
#             assert publicPoint_create["releases"][0]["parties"][1]["contactPoint"]["url"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["contactPoint"]["url"]
#
#     @pytestrail.case("25534")
#     def test_25534_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["buyer"]["name"] = "update value of funder"
#         payload["buyer"]["identifier"]["id"] = "update value of funder"
#         payload["buyer"]["identifier"]["scheme"] = "update value of funder"
#         payload["buyer"]["identifier"]["legalName"] = "update value of funder"
#         payload["buyer"]["identifier"]["uri"] = "update value of funder"
#         payload["buyer"]["additionalIdentifiers"][0]["id"] = "update value of funder"
#         payload["buyer"]["additionalIdentifiers"][0]["scheme"] = "update value of funder"
#         payload["buyer"]["additionalIdentifiers"][0]["legalName"] = "update value of funder"
#         payload["buyer"]["additionalIdentifiers"][0]["uri"] = "update value of funder"
#         payload["buyer"]["address"]["streetAddress"] = "update value of funder"
#         payload["buyer"]["address"]["postalCode"] = "update value of funder"
#         payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "update value of funder"
#         payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "update value of funder"
#         payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = "update value of funder"
#         payload["buyer"]["address"]["addressDetails"]["locality"][
#             "scheme"] = "update value of funder"
#         payload["buyer"]["address"]["addressDetails"]["locality"][
#             "description"] = "update value of funder"
#         payload["buyer"]["contactPoint"]["name"] = "update value of funder"
#         payload["buyer"]["contactPoint"]["email"] = "update value of funder"
#         payload["buyer"]["contactPoint"]["telephone"] = "update value of funder"
#         payload["buyer"]["contactPoint"]["faxNumber"] = "update value of funder"
#         payload["buyer"]["contactPoint"]["url"] = "update value of funder"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25534")
#     def test_25534_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["buyer"]["name"] = "update value of funder"
#         payload["buyer"]["identifier"]["id"] = "update value of funder"
#         payload["buyer"]["identifier"]["scheme"] = "update value of funder"
#         payload["buyer"]["identifier"]["legalName"] = "update value of funder"
#         payload["buyer"]["identifier"]["uri"] = "update value of funder"
#         payload["buyer"]["additionalIdentifiers"][0]["id"] = "update value of funder"
#         payload["buyer"]["additionalIdentifiers"][0]["scheme"] = "update value of funder"
#         payload["buyer"]["additionalIdentifiers"][0]["legalName"] = "update value of funder"
#         payload["buyer"]["additionalIdentifiers"][0]["uri"] = "update value of funder"
#         payload["buyer"]["address"]["streetAddress"] = "update value of funder"
#         payload["buyer"]["address"]["postalCode"] = "update value of funder"
#         payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "update value of funder"
#         payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "update value of funder"
#         payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = "update value of funder"
#         payload["buyer"]["address"]["addressDetails"]["locality"][
#             "scheme"] = "update value of funder"
#         payload["buyer"]["address"]["addressDetails"]["locality"][
#             "description"] = "update value of funder"
#         payload["buyer"]["contactPoint"]["name"] = "update value of funder"
#         payload["buyer"]["contactPoint"]["email"] = "update value of funder"
#         payload["buyer"]["contactPoint"]["telephone"] = "update value of funder"
#         payload["buyer"]["contactPoint"]["faxNumber"] = "update value of funder"
#         payload["buyer"]["contactPoint"]["url"] = "update value of funder"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25534")
#     def test_25534_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         publicPoint_create = requests.get(url=create_fs_response[0]).json()
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["buyer"]["name"] = "update value of funder"
#         payload["buyer"]["identifier"]["id"] = "update value of funder"
#         payload["buyer"]["identifier"]["scheme"] = "update value of funder"
#         payload["buyer"]["identifier"]["legalName"] = "update value of funder"
#         payload["buyer"]["identifier"]["uri"] = "update value of funder"
#         payload["buyer"]["additionalIdentifiers"][0]["id"] = "update value of funder"
#         payload["buyer"]["additionalIdentifiers"][0]["scheme"] = "update value of funder"
#         payload["buyer"]["additionalIdentifiers"][0]["legalName"] = "update value of funder"
#         payload["buyer"]["additionalIdentifiers"][0]["uri"] = "update value of funder"
#         payload["buyer"]["address"]["streetAddress"] = "update value of funder"
#         payload["buyer"]["address"]["postalCode"] = "update value of funder"
#         payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "update value of funder"
#         payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "update value of funder"
#         payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = "update value of funder"
#         payload["buyer"]["address"]["addressDetails"]["locality"][
#             "scheme"] = "update value of funder"
#         payload["buyer"]["address"]["addressDetails"]["locality"][
#             "description"] = "update value of funder"
#         payload["buyer"]["contactPoint"]["name"] = "update value of funder"
#         payload["buyer"]["contactPoint"]["email"] = "update value of funder"
#         payload["buyer"]["contactPoint"]["telephone"] = "update value of funder"
#         payload["buyer"]["contactPoint"]["faxNumber"] = "update value of funder"
#         payload["buyer"]["contactPoint"]["url"] = "update value of funder"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         time.sleep(2)
#         url_update = update_fs_response[1]["data"]["url"]
#         publicPoint_update = requests.get(url=url_update).json()
#         if publicPoint_update["releases"][0]["parties"][0]["roles"][0] == "funder":
#             assert publicPoint_create["releases"][0]["parties"][0]["name"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["name"]
#             assert publicPoint_create["releases"][0]["parties"][0]["identifier"]["scheme"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["identifier"]["scheme"]
#             assert publicPoint_create["releases"][0]["parties"][0]["identifier"]["id"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["identifier"]["id"]
#             assert publicPoint_create["releases"][0]["parties"][0]["identifier"]["legalName"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["identifier"]["legalName"]
#             assert publicPoint_create["releases"][0]["parties"][0]["identifier"]["uri"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["identifier"]["uri"]
#             assert publicPoint_create["releases"][0]["parties"][0]["address"]["streetAddress"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["address"]["streetAddress"]
#             assert publicPoint_create["releases"][0]["parties"][0]["address"]["postalCode"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["address"]["postalCode"]
#             assert publicPoint_create["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["id"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["id"]
#             assert publicPoint_create["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["scheme"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["scheme"]
#             assert publicPoint_create["releases"][0]["parties"][0]["address"]["addressDetails"]["country"][
#                        "description"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["country"][
#                        "description"]
#             assert publicPoint_create["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["uri"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["uri"]
#             assert publicPoint_create["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["id"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["id"]
#             assert publicPoint_create["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["scheme"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["scheme"]
#             assert publicPoint_create["releases"][0]["parties"][0]["address"]["addressDetails"]["region"][
#                        "description"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["description"]
#             assert publicPoint_create["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["uri"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["uri"]
#             assert publicPoint_create["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["id"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["id"]
#             assert publicPoint_create["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["scheme"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["scheme"]
#             assert publicPoint_create["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
#                        "description"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
#                        "description"]
#             assert publicPoint_create["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["uri"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["uri"]
#             assert publicPoint_create["releases"][0]["parties"][0]["additionalIdentifiers"][0]["scheme"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["additionalIdentifiers"][0]["scheme"]
#             assert publicPoint_create["releases"][0]["parties"][0]["additionalIdentifiers"][0]["id"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["additionalIdentifiers"][0]["id"]
#             assert publicPoint_create["releases"][0]["parties"][0]["additionalIdentifiers"][0]["legalName"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["additionalIdentifiers"][0]["legalName"]
#             assert publicPoint_create["releases"][0]["parties"][0]["additionalIdentifiers"][0]["uri"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["additionalIdentifiers"][0]["uri"]
#             assert publicPoint_create["releases"][0]["parties"][0]["contactPoint"]["name"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["contactPoint"]["name"]
#             assert publicPoint_create["releases"][0]["parties"][0]["contactPoint"]["email"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["contactPoint"]["email"]
#             assert publicPoint_create["releases"][0]["parties"][0]["contactPoint"]["telephone"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["contactPoint"]["telephone"]
#             assert publicPoint_create["releases"][0]["parties"][0]["contactPoint"]["faxNumber"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["contactPoint"]["faxNumber"]
#             assert publicPoint_create["releases"][0]["parties"][0]["contactPoint"]["url"] == \
#                    publicPoint_update["releases"][0]["parties"][0]["contactPoint"]["url"]
#         elif publicPoint_update["releases"][0]["parties"][1]["roles"][0] == "funder":
#             assert publicPoint_create["releases"][0]["parties"][1]["name"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["name"]
#             assert publicPoint_create["releases"][0]["parties"][1]["identifier"]["scheme"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["identifier"]["scheme"]
#             assert publicPoint_create["releases"][0]["parties"][1]["identifier"]["id"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["identifier"]["id"]
#             assert publicPoint_create["releases"][0]["parties"][1]["identifier"]["legalName"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["identifier"]["legalName"]
#             assert publicPoint_create["releases"][0]["parties"][1]["identifier"]["uri"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["identifier"]["uri"]
#             assert publicPoint_create["releases"][0]["parties"][1]["address"]["streetAddress"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["address"]["streetAddress"]
#             assert publicPoint_create["releases"][0]["parties"][1]["address"]["postalCode"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["address"]["postalCode"]
#             assert publicPoint_create["releases"][0]["parties"][1]["address"]["addressDetails"]["country"]["id"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["country"]["id"]
#             assert publicPoint_create["releases"][0]["parties"][1]["address"]["addressDetails"]["country"]["scheme"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["country"]["scheme"]
#             assert publicPoint_create["releases"][0]["parties"][1]["address"]["addressDetails"]["country"][
#                        "description"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["country"][
#                        "description"]
#             assert publicPoint_create["releases"][0]["parties"][1]["address"]["addressDetails"]["country"]["uri"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["country"]["uri"]
#             assert publicPoint_create["releases"][0]["parties"][1]["address"]["addressDetails"]["region"]["id"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["region"]["id"]
#             assert publicPoint_create["releases"][0]["parties"][1]["address"]["addressDetails"]["region"]["scheme"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["region"]["scheme"]
#             assert publicPoint_create["releases"][0]["parties"][1]["address"]["addressDetails"]["region"][
#                        "description"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["region"]["description"]
#             assert publicPoint_create["releases"][0]["parties"][1]["address"]["addressDetails"]["region"]["uri"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["region"]["uri"]
#             assert publicPoint_create["releases"][0]["parties"][1]["address"]["addressDetails"]["locality"]["id"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["locality"]["id"]
#             assert publicPoint_create["releases"][0]["parties"][1]["address"]["addressDetails"]["locality"]["scheme"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["locality"]["scheme"]
#             assert publicPoint_create["releases"][0]["parties"][1]["address"]["addressDetails"]["locality"][
#                        "description"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["locality"][
#                        "description"]
#             assert publicPoint_create["releases"][0]["parties"][1]["address"]["addressDetails"]["locality"]["uri"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["locality"]["uri"]
#             assert publicPoint_create["releases"][0]["parties"][1]["additionalIdentifiers"][0]["scheme"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["additionalIdentifiers"][0]["scheme"]
#             assert publicPoint_create["releases"][0]["parties"][1]["additionalIdentifiers"][0]["id"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["additionalIdentifiers"][0]["id"]
#             assert publicPoint_create["releases"][0]["parties"][1]["additionalIdentifiers"][0]["legalName"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["additionalIdentifiers"][0]["legalName"]
#             assert publicPoint_create["releases"][0]["parties"][1]["additionalIdentifiers"][0]["uri"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["additionalIdentifiers"][0]["uri"]
#             assert publicPoint_create["releases"][0]["parties"][1]["contactPoint"]["name"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["contactPoint"]["name"]
#             assert publicPoint_create["releases"][0]["parties"][1]["contactPoint"]["email"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["contactPoint"]["email"]
#             assert publicPoint_create["releases"][0]["parties"][1]["contactPoint"]["telephone"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["contactPoint"]["telephone"]
#             assert publicPoint_create["releases"][0]["parties"][1]["contactPoint"]["faxNumber"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["contactPoint"]["faxNumber"]
#             assert publicPoint_create["releases"][0]["parties"][1]["contactPoint"]["url"] == \
#                    publicPoint_update["releases"][0]["parties"][1]["contactPoint"]["url"]
#
#     @pytestrail.case("25536")
#     def test_25536_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["id"] = "update value for updating"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25536")
#     def test_25536_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["id"] = "update value for updating"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25536")
#     def test_25536_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         publicPoint_create = requests.get(url=create_fs_response[0]).json()
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["id"] = "update value for updating"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         time.sleep(2)
#         url_update = update_fs_response[1]["data"]["url"]
#         publicPoint_update = requests.get(url=url_update).json()
#         assert publicPoint_create["releases"][0]["tender"]["status"] == \
#                publicPoint_update["releases"][0]["tender"]["status"]
#
#     @pytestrail.case("25536")
#     def test_25536_4(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         publicPoint_create = requests.get(url=create_fs_response[0]).json()
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["id"] = "update value for updating"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         time.sleep(2)
#         url_update = update_fs_response[1]["data"]["url"]
#         publicPoint_update = requests.get(url=url_update).json()
#         assert publicPoint_create["releases"][0]["tender"]["statusDetails"] == \
#                publicPoint_update["releases"][0]["tender"]["statusDetails"]
#
#     @pytestrail.case("25536")
#     def test_25536_5(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         publicPoint_create = requests.get(url=create_fs_response[0]).json()
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["id"] = "update value for updating"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         time.sleep(2)
#         url_update = update_fs_response[1]["data"]["url"]
#         publicPoint_update = requests.get(url=url_update).json()
#         assert publicPoint_create["releases"][0]["planning"]["budget"]["id"] == \
#                publicPoint_update["releases"][0]["planning"]["budget"]["id"]
#
#     @pytestrail.case("25536")
#     def test_25536_6(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         publicPoint_create = requests.get(url=create_fs_response[0]).json()
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["id"] = "update value for updating"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         time.sleep(2)
#         url_update = update_fs_response[1]["data"]["url"]
#         publicPoint_update = requests.get(url=url_update).json()
#         assert publicPoint_create["releases"][0]["planning"]["budget"]["verified"] == \
#                publicPoint_update["releases"][0]["planning"]["budget"]["verified"]
#
#     @pytestrail.case("25518")
#     def test_25518_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_obligatory_own_money)
#         payload["planning"]["budget"]["amount"]["amount"] = 6000.66
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25518")
#     def test_25518_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_obligatory_own_money)
#         payload["planning"]["budget"]["amount"]["amount"] = 6000.66
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25518")
#     def test_25518_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_obligatory_own_money)
#         payload["planning"]["budget"]["amount"]["amount"] = 6000.66
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         time.sleep(2)
#         url_update = update_fs_response[1]["data"]["url"]
#         publicPoint_update = requests.get(url=url_update).json()
#         assert publicPoint_update["releases"][0]["planning"]["budget"]["amount"]["amount"] == \
#                payload["planning"]["budget"]["amount"]["amount"]
#
#     @pytestrail.case("25519")
#     def test_25519_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_treasury_money)
#         payload["planning"]["budget"]["description"] = "for FS updating"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case('25519')
#     def test_25519_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_treasury_money)
#         payload['planning']['budget']['description'] = "for FS updating"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25519")
#     def test_25519_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_treasury_money)
#         payload["planning"]["budget"]["description"] = "for FS updating"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         time.sleep(2)
#         url_update = update_fs_response[1]["data"]["url"]
#         publicPoint_update = requests.get(url=url_update).json()
#         assert publicPoint_update["releases"][0]["planning"]["budget"]["description"] == payload["planning"]["budget"][
#             "description"]
#
#     @pytestrail.case("25520")
#     def test_25520_1(self):
#         period = get_new_period()
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_obligatory_treasury_money)
#         payload["planning"]["budget"]["period"]["startDate"] = period[0]
#         payload["planning"]["budget"]["period"]["endDate"] = period[1]
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case('25520')
#     def test_25520_2(self):
#         period = get_new_period()
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_obligatory_treasury_money)
#         payload["planning"]["budget"]["period"]["startDate"] = period[0]
#         payload["planning"]["budget"]["period"]["endDate"] = period[1]
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25520")
#     def test_25520_3(self):
#         period = get_new_period()
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_obligatory_treasury_money)
#         payload["planning"]["budget"]["period"]["startDate"] = period[0]
#         payload["planning"]["budget"]["period"]["endDate"] = period[1]
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         time.sleep(2)
#         url_update = update_fs_response[1]["data"]["url"]
#         publicPoint_update = requests.get(url=url_update).json()
#         assert publicPoint_update["releases"][0]["planning"]["budget"]["period"]["startDate"] == \
#                payload["planning"]["budget"]["period"]["startDate"]
#         assert publicPoint_update["releases"][0]["planning"]["budget"]["period"]["endDate"] == \
#                payload["planning"]["budget"]["period"]["endDate"]
#
#     @pytestrail.case("25522")
#     def test_25522_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["europeanUnionFunding"]["projectName"] = "this is new value for FS updating"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case('25522')
#     def test_25522_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["europeanUnionFunding"]["projectName"] = "this is new value for FS updating"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25522")
#     def test_25522_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["europeanUnionFunding"]["projectName"] = "this is new value for FS updating"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         time.sleep(2)
#         url_update = update_fs_response[1]["data"]["url"]
#         publicPoint_update = requests.get(url=url_update).json()
#         assert publicPoint_update["releases"][0]["planning"]["budget"]["europeanUnionFunding"]["projectName"] == \
#                payload["planning"]["budget"]["europeanUnionFunding"]["projectName"]
#
#     @pytestrail.case("25523")
#     def test_25523_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["europeanUnionFunding"]["projectIdentifier"] = "this is new value for FS updating"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case('25523')
#     def test_25523_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["europeanUnionFunding"]["projectIdentifier"] = "this is new value for FS updating"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25523")
#     def test_25523_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["europeanUnionFunding"]["projectIdentifier"] = "this is new value for FS updating"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         time.sleep(2)
#         url_update = update_fs_response[1]["data"]["url"]
#         publicPoint_update = requests.get(url=url_update).json()
#         assert publicPoint_update["releases"][0]["planning"]["budget"]["europeanUnionFunding"][
#                    "projectIdentifier"] == payload["planning"]["budget"]["europeanUnionFunding"]["projectIdentifier"]
#
#     @pytestrail.case("25524")
#     def test_25524_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["europeanUnionFunding"]["uri"] = "this is new value for FS updating"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25524")
#     def test_25524_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["europeanUnionFunding"]["uri"] = "this is new value for FS updating"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25524")
#     def test_25524_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["europeanUnionFunding"]["uri"] = "this is new value for FS updating"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         time.sleep(2)
#         url_update = update_fs_response[1]["data"]["url"]
#         publicPoint_update = requests.get(url=url_update).json()
#         assert publicPoint_update["releases"][0]["planning"]["budget"]["europeanUnionFunding"]["uri"] == \
#                payload["planning"]["budget"]["europeanUnionFunding"]["uri"]
#
#     @pytestrail.case("25525")
#     def test_25525_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["project"] = "this is new value for FS updating"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25525")
#     def test_25525_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["project"] = "this is new value for FS updating"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25525")
#     def test_25525_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["project"] = "this is new value for FS updating"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         time.sleep(2)
#         url_update = update_fs_response[1]["data"]["url"]
#         publicPoint_update = requests.get(url=url_update).json()
#         assert publicPoint_update["releases"][0]["planning"]["budget"]["project"] == \
#                payload["planning"]["budget"]["project"]
#
#     @pytestrail.case("25526")
#     def test_25526_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["projectID"] = "this is new value for FS updating"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25526")
#     def test_25526_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["projectID"] = "this is new value for FS updating"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25526")
#     def test_25526_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["projectID"] = "this is new value for FS updating"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         time.sleep(2)
#         url_update = update_fs_response[1]["data"]["url"]
#         publicPoint_update = requests.get(url=url_update).json()
#         assert publicPoint_update["releases"][0]["planning"]["budget"]["projectID"] == \
#                payload["planning"]["budget"]["projectID"]
#
#     @pytestrail.case("25527")
#     def test_25527_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["uri"] = "this is new value for FS updating"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25527")
#     def test_25527_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["uri"] = "this is new value for FS updating"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25527")
#     def test_25527_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["uri"] = "this is new value for FS updating"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         time.sleep(2)
#         url_update = update_fs_response[1]["data"]["url"]
#         publicPoint_update = requests.get(url=url_update).json()
#         assert publicPoint_update["releases"][0]["planning"]["budget"]["uri"] == \
#                payload["planning"]["budget"]["uri"]
#
#     @pytestrail.case("26990")
#     def test_26990_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["rationale"] = "for FS updating"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("26990")
#     def test_26990_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["rationale"] = "for FS updating"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("26990")
#     def test_26990_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["rationale"] = "for FS updating"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         time.sleep(2)
#         url_update = update_fs_response[1]["data"]["url"]
#         publicPoint_update = requests.get(url=url_update).json()
#         assert publicPoint_update["releases"][0]["planning"]["rationale"] == payload["planning"]["rationale"]
#
#     @pytestrail.case("25529")
#     def test_25529_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["isEuropeanUnionFunded"] = False
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25529")
#     def test_25529_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["isEuropeanUnionFunded"] = False
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25529")
#     def test_25529_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         publicPoint_create = requests.get(url=create_fs_response[0]).json()
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["isEuropeanUnionFunded"] = False
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         time.sleep(2)
#         url_update = update_fs_response[1]["data"]["url"]
#         publicPoint_update = requests.get(url=url_update).json()
#         assert publicPoint_create["releases"][0]["planning"]["budget"]["isEuropeanUnionFunded"] == True
#         assert publicPoint_update["releases"][0]["planning"]["budget"]["isEuropeanUnionFunded"] == \
#                payload["planning"]["budget"]["isEuropeanUnionFunded"]
#
#     @pytestrail.case("25558")
#     def test_25558_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["buyer"]["name"] = "value for funder 2021"
#         payload["buyer"]["identifier"]["id"] = "value for funder 2021"
#         payload["buyer"]["identifier"]["scheme"] = "value for funder 2021"
#         payload["buyer"]["identifier"]["legalName"] = "value for funder 2021"
#         payload["buyer"]["identifier"]["uri"] = "value for funder 2021"
#         payload["buyer"]["address"]["streetAddress"] = "value for funder 2021"
#         payload["buyer"]["address"]["postalCode"] = "value for funder 2021"
#         payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "value for funder 2021"
#         payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "value for funder 2021"
#         payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "value for funder 2021"
#         payload["buyer"]["address"]["addressDetails"]["locality"]["description"] = "value for funder 2021"
#         payload["buyer"]["additionalIdentifiers"][0]["id"] = "value for funder 2021"
#         payload["buyer"]["additionalIdentifiers"][0]["scheme"] = "value for funder 2021"
#         payload["buyer"]["additionalIdentifiers"][0]["legalName"] = "value for funder 2021"
#         payload["buyer"]["additionalIdentifiers"][0]["uri"] = "value for funder 2021"
#         payload["buyer"]["contactPoint"]["name"] = "value for funder 2021"
#         payload["buyer"]["contactPoint"]["email"] = "value for funder 2021"
#         payload["buyer"]["contactPoint"]["telephone"] = "value for funder 2021"
#         payload["buyer"]["contactPoint"]["faxNumber"] = "value for funder 2021"
#         payload["buyer"]["contactPoint"]["url"] = "value for funder 2021"
#
#         payload["tender"]["procuringEntity"]["name"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["identifier"]["id"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["identifier"]["scheme"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["identifier"]["legalName"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["identifier"]["uri"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["streetAddress"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["postalCode"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]["id"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["scheme"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"][
#             "description"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["id"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["scheme"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["legalName"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["uri"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["contactPoint"]["name"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["contactPoint"]["email"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["contactPoint"]["telephone"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["contactPoint"]["faxNumber"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["contactPoint"]["url"] = "value for payer 2021"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25558")
#     def test_25558_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["buyer"]["name"] = "value for funder 2021"
#         payload["buyer"]["identifier"]["id"] = "value for funder 2021"
#         payload["buyer"]["identifier"]["scheme"] = "value for funder 2021"
#         payload["buyer"]["identifier"]["legalName"] = "value for funder 2021"
#         payload["buyer"]["identifier"]["uri"] = "value for funder 2021"
#         payload["buyer"]["address"]["streetAddress"] = "value for funder 2021"
#         payload["buyer"]["address"]["postalCode"] = "value for funder 2021"
#         payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "value for funder 2021"
#         payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "value for funder 2021"
#         payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "value for funder 2021"
#         payload["buyer"]["address"]["addressDetails"]["locality"]["description"] = "value for funder 2021"
#         payload["buyer"]["additionalIdentifiers"][0]["id"] = "value for funder 2021"
#         payload["buyer"]["additionalIdentifiers"][0]["scheme"] = "value for funder 2021"
#         payload["buyer"]["additionalIdentifiers"][0]["legalName"] = "value for funder 2021"
#         payload["buyer"]["additionalIdentifiers"][0]["uri"] = "value for funder 2021"
#         payload["buyer"]["contactPoint"]["name"] = "value for funder 2021"
#         payload["buyer"]["contactPoint"]["email"] = "value for funder 2021"
#         payload["buyer"]["contactPoint"]["telephone"] = "value for funder 2021"
#         payload["buyer"]["contactPoint"]["faxNumber"] = "value for funder 2021"
#         payload["buyer"]["contactPoint"]["url"] = "value for funder 2021"
#
#         payload["tender"]["procuringEntity"]["name"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["identifier"]["id"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["identifier"]["scheme"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["identifier"]["legalName"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["identifier"]["uri"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["streetAddress"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["postalCode"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]["id"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["scheme"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"][
#             "description"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["id"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["scheme"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["legalName"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["uri"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["contactPoint"]["name"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["contactPoint"]["email"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["contactPoint"]["telephone"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["contactPoint"]["faxNumber"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["contactPoint"]["url"] = "value for payer 2021"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25558")
#     def test_25558_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["buyer"]["name"] = "value for funder 2021"
#         payload["buyer"]["identifier"]["id"] = "value for funder 2021"
#         payload["buyer"]["identifier"]["scheme"] = "value for funder 2021"
#         payload["buyer"]["identifier"]["legalName"] = "value for funder 2021"
#         payload["buyer"]["identifier"]["uri"] = "value for funder 2021"
#         payload["buyer"]["address"]["streetAddress"] = "value for funder 2021"
#         payload["buyer"]["address"]["postalCode"] = "value for funder 2021"
#         payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "value for funder 2021"
#         payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "value for funder 2021"
#         payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "value for funder 2021"
#         payload["buyer"]["address"]["addressDetails"]["locality"]["description"] = "value for funder 2021"
#         payload["buyer"]["additionalIdentifiers"][0]["id"] = "value for funder 2021"
#         payload["buyer"]["additionalIdentifiers"][0]["scheme"] = "value for funder 2021"
#         payload["buyer"]["additionalIdentifiers"][0]["legalName"] = "value for funder 2021"
#         payload["buyer"]["additionalIdentifiers"][0]["uri"] = "value for funder 2021"
#         payload["buyer"]["contactPoint"]["name"] = "value for funder 2021"
#         payload["buyer"]["contactPoint"]["email"] = "value for funder 2021"
#         payload["buyer"]["contactPoint"]["telephone"] = "value for funder 2021"
#         payload["buyer"]["contactPoint"]["faxNumber"] = "value for funder 2021"
#         payload["buyer"]["contactPoint"]["url"] = "value for funder 2021"
#
#         payload["tender"]["procuringEntity"]["name"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["identifier"]["id"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["identifier"]["scheme"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["identifier"]["legalName"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["identifier"]["uri"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["streetAddress"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["postalCode"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]["id"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["scheme"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"][
#             "description"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["id"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["scheme"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["legalName"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["uri"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["contactPoint"]["name"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["contactPoint"]["email"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["contactPoint"]["telephone"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["contactPoint"]["faxNumber"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["contactPoint"]["url"] = "value for payer 2021"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         parties_before_update = requests.get(url=create_fs_response[0]).json()["releases"][0][
#             "parties"]
#         parties_after_update = requests.get(url=update_fs_response[1]["data"]["url"]).json()["releases"][0][
#             "parties"]
#         assert parties_after_update == parties_before_update
#
#     @pytestrail.case("26999")
#     def test_26999_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["amount"]["amount"] = 5.55
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("26999")
#     def test_26999_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["amount"]["amount"] = 5.55
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("26999")
#     def test_26999_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         create_fs_amount = \
#             requests.get(url=create_fs_response[0]).json()["releases"][0]["planning"]["budget"]["amount"]["amount"]
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["amount"]["amount"] = 5.55
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         time.sleep(2)
#         url_update = update_fs_response[1]["data"]["url"]
#         publicPoint_update = requests.get(url=url_update).json()
#         assert publicPoint_update["releases"][0]["planning"]["budget"]["amount"]["amount"] == \
#                payload["planning"]["budget"]["amount"]["amount"]
#         assert publicPoint_update["releases"][0]["planning"]["budget"]["amount"]["amount"] != create_fs_amount
#
#
#     @pytestrail.case("26999")
#     def test_26999_4(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["amount"]["amount"] = 5.55
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         time.sleep(2)
#         ei_url = update_fs_response[1]["data"]["url"]
#         cpid_url = requests.get(url=ei_url).json()["releases"][0]["relatedProcesses"][0]["uri"]
#         ei_releases_id_after_update = \
#             requests.get(url=cpid_url).json()["releases"][0]["planning"]["budget"]["amount"]["amount"]
#         assert ei_releases_id_after_update == payload["planning"]["budget"]["amount"]["amount"]
#
#     @pytestrail.case("25521")
#     def test_25521_1(self):
#         period = get_new_period()
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_obligatory_own_money)
#         payload["planning"]["budget"]["period"]["startDate"] = period[2]
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25521")
#     def test_25521_2(self):
#         period = get_new_period()
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_obligatory_own_money)
#         payload["planning"]["budget"]["period"]["startDate"] = period[2]
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert update_fs_response[1]["errors"][0]["code"] == "400.10.01.01"
#         assert update_fs_response[1]["errors"][0]["description"] == "Invalid period."
#
#     @pytestrail.case("26991")
#     def test_26991_1(self):
#         period = get_new_period()
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_obligatory_own_money)
#         payload["planning"]["budget"]["period"]["endDate"] = period[3]
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("26991")
#     def test_26991_2(self):
#         period = get_new_period()
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_obligatory_own_money)
#         payload["planning"]["budget"]["period"]["endDate"] = period[3]
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert update_fs_response[1]["errors"][0]["code"] == "400.10.01.01"
#         assert update_fs_response[1]["errors"][0]["description"] == "Invalid period."
#
#     @pytestrail.case("26992")
#     def test_26992_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_obligatory_own_money)
#         payload["planning"]["budget"]["period"]["startDate"] = "2021-14-14T14:14:14Z"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("26992")
#     def test_26992_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_obligatory_own_money)
#         payload["planning"]["budget"]["period"]["startDate"] = "2021-14-14T14:14:14Z"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert update_fs_response[1]["errors"][0]["code"] == "400.10.00"
#         assert update_fs_response[1]["errors"][0][
#                    "description"] == f"com.fasterxml.jackson.databind.JsonMappingException: " \
#                                      f"Text '{payload['planning']['budget']['period']['startDate']}' " \
#                                      f"could not be parsed: Invalid value for MonthOfYear (valid values 1 - 12): " \
#                                      f"14 (through reference chain: com.procurement.budget.model.dto.fs.request." \
#                                      f"FsUpdate[\"planning\"]->com.procurement.budget.model.dto.fs.request." \
#                                      f"PlanningFsUpdate[\"budget\"]->com.procurement.budget.model.dto.fs.request." \
#                                      f"BudgetFsUpdate[\"period\"]->com.procurement.budget.model.dto.ocds." \
#                                      f"Period[\"startDate\"])"
#
#     @pytestrail.case("26993")
#     def test_26993_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_obligatory_own_money)
#         payload["planning"]["budget"]["period"]["endDate"] = "2021-14-14T14:14:14Z"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("26993")
#     def test_26993_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_obligatory_own_money)
#         payload["planning"]["budget"]["period"]["endDate"] = "2021-14-14T14:14:14Z"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert update_fs_response[1]["errors"][0]["code"] == "400.10.00"
#         assert update_fs_response[1]["errors"][0][
#                    "description"] == f"com.fasterxml.jackson.databind.JsonMappingException: " \
#                                      f"Text '{payload['planning']['budget']['period']['endDate']}' could not be " \
#                                      f"parsed: Invalid value for MonthOfYear (valid values 1 - 12): 14 (through " \
#                                      f"reference chain: com.procurement.budget.model.dto.fs.request.FsUpdate" \
#                                      f"[\"planning\"]->com.procurement.budget.model.dto.fs.request." \
#                                      f"PlanningFsUpdate[\"budget\"]->com.procurement.budget.model.dto.fs." \
#                                      f"request.BudgetFsUpdate[\"period\"]->com.procurement.budget.model." \
#                                      f"dto.ocds.Period[\"endDate\"])"
#
#     @pytestrail.case("26998")
#     def test_26998_1(self):
#         period = get_period()
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_obligatory_own_money)
#
#         payload["planning"]["budget"]["period"]["endDate"] = period[0]
#         payload["planning"]["budget"]["period"]["startDate"] = period[1]
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("26998")
#     def test_26998_2(self):
#         period = get_new_period()
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_obligatory_own_money)
#         payload["planning"]["budget"]["period"]["endDate"] = period[0]
#         payload["planning"]["budget"]["period"]["startDate"] = period[1]
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert update_fs_response[1]["errors"][0]["code"] == "400.10.01.01"
#         assert update_fs_response[1]["errors"][0]["description"] == "Invalid period."
#
#     @pytestrail.case("25539")
#     def test_25539_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["amount"]["amount"] = 0
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25539")
#     def test_25539_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["amount"]["amount"] = 0
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25539")
#     def test_25539_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         create_fs_amount = \
#             requests.get(url=create_fs_response[0]).json()["releases"][0]["planning"]["budget"]["amount"]["amount"]
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["amount"]["amount"] = 0
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         time.sleep(2)
#         url_update = update_fs_response[1]["data"]["url"]
#         publicPoint_update = requests.get(url=url_update).json()
#         assert publicPoint_update["releases"][0]["planning"]["budget"]["amount"]["amount"] == \
#                payload["planning"]["budget"]["amount"]["amount"]
#         assert publicPoint_update["releases"][0]["planning"]["budget"]["amount"]["amount"] != create_fs_amount
#
#     @pytestrail.case("25540")
#     def test_25540_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["amount"]["amount"] = -5
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25540")
#     def test_25540_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["amount"]["amount"] = -5
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert update_fs_response[1]["errors"][0]["code"] == "400.10.00.00"
#         assert update_fs_response[1]["errors"][0]["description"] == "Invalid json type"
#
#     @pytestrail.case("26994")
#     def test_26994_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["isEuropeanUnionFunded"] = True
#         del payload["planning"]["budget"]["europeanUnionFunding"]["projectName"]
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("26994")
#     def test_26994_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["isEuropeanUnionFunded"] = True
#         del payload["planning"]["budget"]["europeanUnionFunding"]["projectName"]
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert update_fs_response[1]["errors"][0]["code"] == "400.10.00"
#         assert update_fs_response[1]["errors"][0][
#                    "description"] == f"com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
#                                      f"Instantiation of [simple type, class com.procurement.budget.model.dto." \
#                                      f"ocds.EuropeanUnionFunding] value failed for JSON property projectName " \
#                                      f"due to missing (therefore NULL) value for creator parameter projectName " \
#                                      f"which is a non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1] " \
#                                      f"(through reference chain: com.procurement.budget.model.dto.fs.request." \
#                                      f"FsUpdate[\"planning\"]->com.procurement.budget.model.dto.fs.request." \
#                                      f"PlanningFsUpdate[\"budget\"]->com.procurement.budget.model.dto.fs." \
#                                      f"request.BudgetFsUpdate[\"europeanUnionFunding\"]->com.procurement." \
#                                      f"budget.model.dto.ocds.EuropeanUnionFunding[\"projectName\"])"
#
#     @pytestrail.case("26995")
#     def test_26995_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["isEuropeanUnionFunded"] = True
#         del payload["planning"]["budget"]["europeanUnionFunding"]["projectIdentifier"]
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("26995")
#     def test_26995_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["isEuropeanUnionFunded"] = True
#         del payload["planning"]["budget"]["europeanUnionFunding"]["projectIdentifier"]
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert update_fs_response[1]["errors"][0]["code"] == "400.10.00"
#         assert update_fs_response[1]["errors"][0][
#                    "description"] == f"com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
#                                      f"Instantiation of [simple type, class com.procurement.budget.model.dto.ocds." \
#                                      f"EuropeanUnionFunding] value failed for JSON property projectIdentifier due " \
#                                      f"to missing (therefore NULL) value for creator parameter projectIdentifier " \
#                                      f"which is a non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1] " \
#                                      f"(through reference chain: com.procurement.budget.model.dto.fs.request." \
#                                      f"FsUpdate[\"planning\"]->com.procurement.budget.model.dto.fs.request." \
#                                      f"PlanningFsUpdate[\"budget\"]->com.procurement.budget.model.dto.fs.request." \
#                                      f"BudgetFsUpdate[\"europeanUnionFunding\"]->com.procurement.budget.model.dto." \
#                                      f"ocds.EuropeanUnionFunding[\"projectIdentifier\"])"
#
#     @pytestrail.case("26996")
#     def test_26996_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["isEuropeanUnionFunded"] = True
#         del payload["planning"]["budget"]["europeanUnionFunding"]["projectIdentifier"]
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("26996")
#     def test_26996_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["isEuropeanUnionFunded"] = True
#         del payload["planning"]["budget"]["europeanUnionFunding"]
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert update_fs_response[1]["errors"][0]["code"] == "400.10.01.04"
#         assert update_fs_response[1]["errors"][0][
#                    "description"] == "EuropeanUnionFunding must not be empty."
#
#     @pytestrail.case("25542")
#     def test_25542_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         fake_token = uuid4()
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{fake_token}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25542")
#     def test_25542_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         fake_token = uuid4()
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{fake_token}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert update_fs_response[1]["errors"][0]["code"] == "400.10.00.02"
#         assert update_fs_response[1]["errors"][0]["description"] == "FS not found."
#
#     @pytestrail.case("25541")
#     def test_25541_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         access_token = get_access_token_for_platform_two()
#         x_operation_id = get_x_operation_id(access_token)
#         time.sleep(2)
#         host = set_instance_for_request()
#         request_to_update_fs = requests.post(
#             url=host + update_fs + cpid + "/" + create_fs_response[2],
#             headers={
#                 'Authorization': 'Bearer ' + access_token,
#                 'X-OPERATION-ID': x_operation_id,
#                 'X-TOKEN': f"{create_fs_response[1]}",
#                 'Content-Type': 'application/json'},
#             json=payload)
#         assert request_to_update_fs.text == 'ok'
#         assert request_to_update_fs.status_code == 202
#
#     @pytestrail.case("25541")
#     def test_25541_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         access_token = get_access_token_for_platform_two()
#         x_operation_id = get_x_operation_id(access_token)
#         time.sleep(2)
#         host = set_instance_for_request()
#         requests.post(
#             url=host + update_fs + cpid + "/" + create_fs_response[2],
#             headers={
#                 'Authorization': 'Bearer ' + access_token,
#                 'X-OPERATION-ID': x_operation_id,
#                 'X-TOKEN': f"{create_fs_response[1]}",
#                 'Content-Type': 'application/json'},
#             json=payload)
#         error_from_DB = execute_cql_from_orchestrator_operation_step(cpid, 'BudgetUpdateFsTask')
#         assert error_from_DB['errors'][0]['code'] == '400.10.00.03'
#         assert error_from_DB['errors'][0]['description'] == 'Invalid owner.'
#
#
#
#     @pytestrail.case("27000")
#     def test_27000_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid, status="cancelled")
#         payload = copy.deepcopy(fs_update_full_own_money)
#         fake_token = uuid4()
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("27000")
#     def test_27000_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid, status="cancelled")
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert update_fs_response[1]["errors"][0]["code"] == "400.10.00.08"
#         assert update_fs_response[1]["errors"][0]["description"] == "Financial source status invalid."
#
#     @pytestrail.case("27001")
#     def test_27001_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid, statusDetails="cancelled")
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("27001")
#     def test_27001_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid, statusDetails="cancelled")
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert update_fs_response[1]["errors"][0]["code"] == "400.10.00.08"
#         assert update_fs_response[1]["errors"][0]["description"] == "Financial source status invalid."
#
#     @pytestrail.case("27002")
#     def test_27002_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["amount"]["amount"] = 123.44
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("27002")
#     def test_27002_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["amount"]["amount"] = 123.49
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("27002")
#     def test_27002_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["amount"]["amount"] = 123.49
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         time.sleep(2)
#         url_update = update_fs_response[1]["data"]["url"]
#         publicPoint_update = requests.get(url=url_update).json()
#         uri = fnmatch.fnmatch(publicPoint_update["uri"], "*")
#         version = fnmatch.fnmatch(publicPoint_update["version"], "*")
#         extensions_0 = fnmatch.fnmatch(publicPoint_update["extensions"][0], "*")
#         extensions_1 = fnmatch.fnmatch(publicPoint_update["extensions"][1], "*")
#         publisher_name = fnmatch.fnmatch(publicPoint_update["publisher"]["name"], "*")
#         publisher_uri = fnmatch.fnmatch(publicPoint_update["publisher"]["name"], "*")
#         license = fnmatch.fnmatch(publicPoint_update["license"], "*")
#         publicationPolicy = fnmatch.fnmatch(publicPoint_update["publicationPolicy"], "*")
#         publishedDate = fnmatch.fnmatch(publicPoint_update["publishedDate"], "*")
#         release_ocid = fnmatch.fnmatch(publicPoint_update["releases"][0]["ocid"], "*")
#         release_id = fnmatch.fnmatch(publicPoint_update["releases"][0]["id"], "*")
#         release_date = fnmatch.fnmatch(publicPoint_update["releases"][0]["date"], "*")
#         release_tag = fnmatch.fnmatch(publicPoint_update["releases"][0]["tag"][0], "*")
#         release_initiation = fnmatch.fnmatch(publicPoint_update["releases"][0]["initiationType"], "*")
#         release_tender_id = fnmatch.fnmatch(publicPoint_update["releases"][0]["tender"]["id"], "*")
#         release_tender_status = fnmatch.fnmatch(publicPoint_update["releases"][0]["tender"]["status"], "*")
#         release_tender_status_details = fnmatch.fnmatch(publicPoint_update["releases"][0]["tender"]["statusDetails"],
#                                                         "*")
#         release_parties_id_f = fnmatch.fnmatch(publicPoint_update["releases"][0]["parties"][0]["id"], "*")
#         release_parties_name_f = fnmatch.fnmatch(publicPoint_update["releases"][0]["parties"][0]["name"], "*")
#         release_identifier_scheme_f = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][0]["identifier"]["scheme"], "*")
#         release_identifier_id_f = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][0]["identifier"]["id"], "*")
#         release_identifier_legal_name_f = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][0]["identifier"]["legalName"], "*")
#         release_identifier_legal_uri_f = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][0]["identifier"]["uri"], "*")
#         release_address_street_f = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][0]["address"]["streetAddress"], "*")
#         release_address_postal_f = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][0]["address"]["postalCode"], "*")
#         release_address_country_scheme_f = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["scheme"], "*")
#         release_address_country_id_f = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["id"], "*")
#         release_address_country_description_f = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["description"], "*")
#         release_address_country_uri_f = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["uri"], "*")
#         release_address_region_scheme_f = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["scheme"], "*")
#         release_address_region_id_f = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["id"], "*")
#         release_address_region_description_f = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["description"], "*")
#         release_address_region_uri_f = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["uri"], "*")
#         release_address_locality_scheme_f = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["scheme"], "*")
#         release_address_locality_id_f = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["id"], "*")
#         release_address_locality_description_f = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["description"],
#             "*")
#         release_address_locality_uri_f = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["uri"], "*")
#         release_additional_scheme_f = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][0]["additionalIdentifiers"][0]["scheme"], "*")
#         release_additional_id_f = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][0]["additionalIdentifiers"][0]["id"], "*")
#         release_additional_legal_f = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][0]["additionalIdentifiers"][0]["legalName"], "*")
#         release_additional_uri_f = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][0]["additionalIdentifiers"][0]["uri"], "*")
#         release_contact_name_f = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][0]["contactPoint"]["name"], "*")
#         release_contact_email_f = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][0]["contactPoint"]["email"], "*")
#         release_contact_telephone_f = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][0]["contactPoint"]["telephone"], "*")
#         release_contact_uri_f = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][0]["contactPoint"]["url"], "*")
#         release_contact_fax_f = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][0]["contactPoint"]["faxNumber"], "*")
#         release_parties_role_0 = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][0]["roles"][0], "*")
#
#         release_parties_id_p = fnmatch.fnmatch(publicPoint_update["releases"][0]["parties"][1]["id"], "*")
#         release_parties_name_p = fnmatch.fnmatch(publicPoint_update["releases"][0]["parties"][1]["name"], "*")
#         release_identifier_scheme_p = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][1]["identifier"]["scheme"], "*")
#         release_identifier_id_p = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][1]["identifier"]["id"], "*")
#         release_identifier_legal_name_p = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][1]["identifier"]["legalName"], "*")
#         release_identifier_legal_uri_p = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][1]["identifier"]["uri"], "*")
#         release_address_street_p = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][1]["address"]["streetAddress"], "*")
#         release_address_postal_p = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][1]["address"]["postalCode"], "*")
#         release_address_country_scheme_p = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["country"]["scheme"], "*")
#         release_address_country_id_p = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["country"]["id"], "*")
#         release_address_country_description_p = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["country"]["description"], "*")
#         release_address_country_uri_p = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["country"]["uri"], "*")
#         release_address_region_scheme_p = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["region"]["scheme"], "*")
#         release_address_region_id_p = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["region"]["id"], "*")
#         release_address_region_description_p = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["region"]["description"], "*")
#         release_address_region_uri_p = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["region"]["uri"], "*")
#         release_address_locality_scheme_p = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["locality"]["scheme"], "*")
#         release_address_locality_id_p = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["locality"]["id"], "*")
#         release_address_locality_description_p = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["locality"]["description"],
#             "*")
#         release_address_locality_uri_p = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][1]["address"]["addressDetails"]["locality"]["uri"], "*")
#         release_additional_scheme_p = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][1]["additionalIdentifiers"][0]["scheme"], "*")
#         release_additional_id_p = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][1]["additionalIdentifiers"][0]["id"], "*")
#         release_additional_legal_p = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][1]["additionalIdentifiers"][0]["legalName"], "*")
#         release_additional_uri_p = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][1]["additionalIdentifiers"][0]["uri"], "*")
#         release_contact_name_p = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][1]["contactPoint"]["name"], "*")
#         release_contact_email_p = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][1]["contactPoint"]["email"], "*")
#         release_contact_telephone_p = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][1]["contactPoint"]["telephone"], "*")
#         release_contact_uri_p = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][1]["contactPoint"]["url"], "*")
#         release_contact_fax_p = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][1]["contactPoint"]["faxNumber"], "*")
#         release_parties_role_1 = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["parties"][1]["roles"][0], "*")
#         release_planning_budget_id = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["planning"]["budget"]["id"], "*")
#         release_planning_budget_description = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["planning"]["budget"]["description"], "*")
#         release_planning_budget_period_st = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["planning"]["budget"]["period"]["startDate"], "*")
#         release_planning_budget_period_en = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["planning"]["budget"]["period"]["endDate"], "*")
#         release_planning_budget_amount_cur = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["planning"]["budget"]["amount"]["currency"], "*")
#         release_planning_budget_projectIdentifier = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["planning"]["budget"]["europeanUnionFunding"]["projectIdentifier"], "*")
#         release_planning_budget_project_name = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["planning"]["budget"]["europeanUnionFunding"]["projectName"], "*")
#         release_planning_budget_uri = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["planning"]["budget"]["europeanUnionFunding"]["uri"], "*")
#         release_planning_budget_source_entity_id = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["planning"]["budget"]["sourceEntity"]["id"], "*")
#         release_planning_budget_source_entity_name = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["planning"]["budget"]["sourceEntity"]["name"], "*")
#         release_planning_budget_project = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["planning"]["budget"]["project"], "*")
#         release_planning_budget_project_id = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["planning"]["budget"]["projectID"], "*")
#
#         release_planning_rationale = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["planning"]["rationale"], "*")
#         release_planning_relatedProcesses_id = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["relatedProcesses"][0]["id"], "*")
#         release_planning_related_processes_relationship = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["relatedProcesses"][0]["relationship"][0], "*")
#         release_planning_related_processes_scheme = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["relatedProcesses"][0]["scheme"], "*")
#         release_planning_related_processes_identifier = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["relatedProcesses"][0]["identifier"], "*")
#         release_planning_related_processes_uri = fnmatch.fnmatch(
#             publicPoint_update["releases"][0]["relatedProcesses"][0]["uri"], "*")
#
#         assert publicPoint_update["releases"][0]["planning"]["budget"]["verified"] == True
#         assert publicPoint_update["releases"][0]["planning"]["budget"]["amount"]["amount"] == \
#                payload["planning"]["budget"]["amount"]["amount"]
#         assert publicPoint_update["releases"][0]["planning"]["budget"]["isEuropeanUnionFunded"] == True
#         assert uri == True
#         assert version == True
#         assert extensions_0 == True
#         assert extensions_1 == True
#         assert publisher_name == True
#         assert publisher_uri == True
#         assert license == True
#         assert publicationPolicy == True
#         assert publishedDate == True
#         assert release_ocid == True
#         assert release_id == True
#         assert release_date == True
#         assert release_tag == True
#         assert release_initiation == True
#         assert release_tender_id == True
#         assert release_tender_status == True
#         assert release_tender_status_details == True
#         assert release_parties_id_f == True
#         assert release_parties_name_f == True
#         assert release_identifier_scheme_f == True
#         assert release_identifier_id_f == True
#         assert release_identifier_legal_name_f == True
#         assert release_identifier_legal_uri_f == True
#         assert release_address_street_f == True
#         assert release_address_postal_f == True
#         assert release_address_country_scheme_f == True
#         assert release_address_country_id_f == True
#         assert release_address_country_description_f == True
#         assert release_address_country_uri_f == True
#         assert release_address_region_scheme_f == True
#         assert release_address_region_id_f == True
#         assert release_address_region_description_f == True
#         assert release_address_region_uri_f == True
#         assert release_address_locality_scheme_f == True
#         assert release_address_locality_id_f == True
#         assert release_address_locality_description_f == True
#         assert release_address_locality_uri_f == True
#         assert release_additional_scheme_f == True
#         assert release_additional_id_f == True
#         assert release_additional_legal_f == True
#         assert release_additional_uri_f == True
#         assert release_contact_name_f == True
#         assert release_contact_email_f == True
#         assert release_contact_telephone_f == True
#         assert release_contact_uri_f == True
#         assert release_contact_fax_f == True
#         assert release_parties_role_0 == True
#         assert release_parties_id_p == True
#         assert release_parties_name_p == True
#         assert release_identifier_scheme_p == True
#         assert release_identifier_id_p == True
#         assert release_identifier_legal_name_p == True
#         assert release_identifier_legal_uri_p == True
#         assert release_address_street_p == True
#         assert release_address_postal_p == True
#         assert release_address_country_scheme_p == True
#         assert release_address_country_id_p == True
#         assert release_address_country_description_p == True
#         assert release_address_country_uri_p == True
#         assert release_address_region_scheme_p == True
#         assert release_address_region_id_p == True
#         assert release_address_region_description_p == True
#         assert release_address_region_uri_p == True
#         assert release_address_locality_scheme_p == True
#         assert release_address_locality_id_p == True
#         assert release_address_locality_description_p == True
#         assert release_address_locality_uri_p == True
#         assert release_additional_scheme_p == True
#         assert release_additional_id_p == True
#         assert release_additional_legal_p == True
#         assert release_additional_uri_p == True
#         assert release_contact_name_p == True
#         assert release_contact_email_p == True
#         assert release_contact_telephone_p == True
#         assert release_contact_uri_p == True
#         assert release_contact_fax_p == True
#         assert release_parties_role_1 == True
#         assert release_planning_budget_id == True
#         assert release_planning_budget_description == True
#         assert release_planning_budget_period_st == True
#         assert release_planning_budget_period_en == True
#         assert release_planning_budget_amount_cur == True
#         assert release_planning_budget_projectIdentifier == True
#         assert release_planning_budget_project_name == True
#         assert release_planning_budget_uri == True
#         assert release_planning_budget_source_entity_id == True
#         assert release_planning_budget_source_entity_name == True
#         assert release_planning_budget_project == True
#         assert release_planning_budget_project_id == True
#         assert release_planning_budget_uri == True
#         assert release_planning_rationale == True
#         assert release_planning_relatedProcesses_id == True
#         assert release_planning_related_processes_relationship == True
#         assert release_planning_related_processes_scheme == True
#         assert release_planning_related_processes_identifier == True
#         assert release_planning_related_processes_uri == True
#
#     @pytestrail.case("27004")
#     def test_27004_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("27004")
#     def test_27004_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("27004")
#     def test_27004_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["amount"]["amount"] = 75.75
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ei_cpid_after_update = \
#             requests.get(url=update_fs_response[1]["data"]["url"]).json()["releases"][0]["relatedProcesses"][0]["uri"]
#         ei_after_buyer_section = requests.get(url=ei_cpid_after_update).json()
#         uri = fnmatch.fnmatch(ei_after_buyer_section["uri"], "*")
#         version = fnmatch.fnmatch(ei_after_buyer_section["version"], "*")
#         extensions_0 = fnmatch.fnmatch(ei_after_buyer_section["extensions"][0], "*")
#         extensions_1 = fnmatch.fnmatch(ei_after_buyer_section["extensions"][1], "*")
#         publisher_name = fnmatch.fnmatch(ei_after_buyer_section["publisher"]["name"], "*")
#         publisher_uri = fnmatch.fnmatch(ei_after_buyer_section["publisher"]["name"], "*")
#         license = fnmatch.fnmatch(ei_after_buyer_section["license"], "*")
#         publicationPolicy = fnmatch.fnmatch(ei_after_buyer_section["publicationPolicy"], "*")
#         publishedDate = fnmatch.fnmatch(ei_after_buyer_section["publishedDate"], "*")
#         release_ocid = fnmatch.fnmatch(ei_after_buyer_section["releases"][0]["ocid"], "*")
#         release_id = fnmatch.fnmatch(ei_after_buyer_section["releases"][0]["id"], "*")
#         release_date = fnmatch.fnmatch(ei_after_buyer_section["releases"][0]["date"], "*")
#         release_tag = fnmatch.fnmatch(ei_after_buyer_section["releases"][0]["tag"][0], "*")
#         release_initiation = fnmatch.fnmatch(ei_after_buyer_section["releases"][0]["initiationType"], "*")
#         release_tender_id = fnmatch.fnmatch(ei_after_buyer_section["releases"][0]["tender"]["id"], "*")
#         release_tender_title = fnmatch.fnmatch(ei_after_buyer_section["releases"][0]["tender"]["title"], "*")
#         release_tender_description = fnmatch.fnmatch(ei_after_buyer_section["releases"][0]["tender"]["description"],
#                                                      "*")
#         release_tender_status = fnmatch.fnmatch(ei_after_buyer_section["releases"][0]["tender"]["status"], "*")
#         release_tender_status_det = fnmatch.fnmatch(ei_after_buyer_section["releases"][0]["tender"]["statusDetails"],
#                                                     "*")
#         release_tender_mainProcurementCategory = fnmatch.fnmatch(ei_after_buyer_section["releases"][0]["tender"]
#                                                                  ["mainProcurementCategory"], "*")
#         release_tender_classification_scheme = fnmatch.fnmatch(ei_after_buyer_section["releases"][0]["tender"]
#                                                                ["classification"]["scheme"], "*")
#         release_tender_classification_id = fnmatch.fnmatch(ei_after_buyer_section["releases"][0]["tender"]
#                                                            ["classification"]["id"], "*")
#         release_tender_classification_description = fnmatch.fnmatch(ei_after_buyer_section["releases"][0]["tender"]
#                                                                     ["classification"]["description"], "*")
#         release_buyer_id = fnmatch.fnmatch(ei_after_buyer_section["releases"][0]["buyer"]["id"], "*")
#         release_buyer_name = fnmatch.fnmatch(ei_after_buyer_section["releases"][0]["buyer"]["name"], "*")
#         release_parties_id_b = fnmatch.fnmatch(ei_after_buyer_section["releases"][0]["parties"][0]["id"], "*")
#         release_parties_name_b = fnmatch.fnmatch(ei_after_buyer_section["releases"][0]["parties"][0]["name"], "*")
#         release_identifier_scheme_b = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["parties"][0]["identifier"]["scheme"], "*")
#         release_identifier_id_b = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["parties"][0]["identifier"]["id"], "*")
#         release_identifier_legal_name_b = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["parties"][0]["identifier"]["legalName"], "*")
#         release_identifier_legal_uri_b = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["parties"][0]["identifier"]["uri"], "*")
#         release_address_street_b = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["parties"][0]["address"]["streetAddress"], "*")
#         release_address_postal_b = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["parties"][0]["address"]["postalCode"], "*")
#         release_address_country_scheme_b = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["scheme"], "*")
#         release_address_country_id_b = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["id"], "*")
#         release_address_country_description_b = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["description"],
#             "*")
#         release_address_country_uri_b = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["uri"], "*")
#         release_address_region_scheme_b = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["scheme"], "*")
#         release_address_region_id_b = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["id"], "*")
#         release_address_region_description_b = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["description"],
#             "*")
#         release_address_region_uri_b = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["uri"], "*")
#         release_address_locality_scheme_b = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["scheme"], "*")
#         release_address_locality_id_b = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["id"], "*")
#         release_address_locality_description_b = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["description"],
#             "*")
#         release_address_locality_uri_b = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["uri"], "*")
#         release_additional_scheme_b = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["parties"][0]["additionalIdentifiers"][0]["scheme"], "*")
#         release_additional_id_b = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["parties"][0]["additionalIdentifiers"][0]["id"], "*")
#         release_additional_legal_b = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["parties"][0]["additionalIdentifiers"][0]["legalName"], "*")
#         release_additional_uri_b = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["parties"][0]["additionalIdentifiers"][0]["uri"], "*")
#         release_contact_name_b = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["parties"][0]["contactPoint"]["name"], "*")
#         release_contact_email_b = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["parties"][0]["contactPoint"]["email"], "*")
#         release_contact_telephone_b = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["parties"][0]["contactPoint"]["telephone"], "*")
#         release_contact_uri_b = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["parties"][0]["contactPoint"]["url"], "*")
#         release_contact_fax_b = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["parties"][0]["contactPoint"]["faxNumber"], "*")
#         release_details_type_b = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["parties"][0]["details"]["typeOfBuyer"], "*")
#         release_details_general_b = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["parties"][0]["details"]["mainGeneralActivity"], "*")
#         release_details_sectoral_b = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["parties"][0]["details"]["mainSectoralActivity"], "*")
#         release_parties_role_b = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["parties"][0]["roles"][0], "*")
#         release_planning_budget_id = fnmatch.fnmatch(ei_after_buyer_section["releases"][0]["planning"]["budget"]["id"],
#                                                      "*")
#         release_planning_budget_period_st = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["planning"]["budget"]["period"]["startDate"], "*")
#         release_planning_budget_period_en = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["planning"]["budget"]["period"]["endDate"], "*")
#         release_planning_budget_amount_currency = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["planning"]["budget"]["amount"]["currency"], "*")
#         release_planning_budget_rationale = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["planning"]["rationale"], "*")
#         release_relatedProcesses_id = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["relatedProcesses"][0]["id"], "*")
#         release_related_processes_relationship = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["relatedProcesses"][0]["relationship"][0], "*")
#         release_related_processes_scheme = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["relatedProcesses"][0]["scheme"], "*")
#         release_related_processes_identifier = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["relatedProcesses"][0]["identifier"], "*")
#         release_related_processes_uri = fnmatch.fnmatch(
#             ei_after_buyer_section["releases"][0]["relatedProcesses"][0]["uri"], "*")
#
#         assert ei_after_buyer_section["releases"][0]["planning"]["budget"]["amount"]["amount"] == \
#                payload["planning"]["budget"]["amount"]["amount"]
#         assert uri == True
#         assert version == True
#         assert extensions_0 == True
#         assert extensions_1 == True
#         assert publisher_name == True
#         assert publisher_name == True
#         assert publisher_uri == True
#         assert license == True
#         assert publicationPolicy == True
#         assert publishedDate == True
#         assert release_ocid == True
#         assert release_id == True
#         assert release_date == True
#         assert release_tag == True
#         assert release_initiation == True
#         assert release_tender_id == True
#         assert release_tender_title == True
#         assert release_tender_description == True
#         assert release_tender_status == True
#         assert release_tender_status_det == True
#         assert release_tender_mainProcurementCategory == True
#         assert release_tender_classification_scheme == True
#         assert release_tender_classification_id == True
#         assert release_tender_classification_description == True
#         assert release_buyer_id == True
#         assert release_buyer_name == True
#         assert release_parties_id_b == True
#         assert release_parties_name_b == True
#         assert release_identifier_scheme_b == True
#         assert release_identifier_id_b == True
#         assert release_identifier_legal_name_b == True
#         assert release_identifier_legal_uri_b == True
#         assert release_address_street_b == True
#         assert release_address_postal_b == True
#         assert release_address_country_scheme_b == True
#         assert release_address_country_id_b == True
#         assert release_address_country_description_b == True
#         assert release_address_country_uri_b == True
#         assert release_address_region_scheme_b == True
#         assert release_address_region_id_b == True
#         assert release_address_region_description_b == True
#         assert release_address_region_uri_b == True
#         assert release_address_locality_scheme_b == True
#         assert release_address_locality_id_b == True
#         assert release_address_locality_description_b == True
#         assert release_address_locality_uri_b == True
#         assert release_additional_scheme_b == True
#         assert release_additional_id_b == True
#         assert release_additional_legal_b == True
#         assert release_additional_uri_b == True
#         assert release_contact_name_b == True
#         assert release_contact_email_b == True
#         assert release_contact_telephone_b == True
#         assert release_contact_uri_b == True
#         assert release_contact_fax_b == True
#         assert release_parties_role_b == True
#         assert release_details_type_b == True
#         assert release_details_general_b == True
#         assert release_details_sectoral_b == True
#         assert release_planning_budget_id == True
#         assert release_planning_budget_period_st == True
#         assert release_planning_budget_period_en == True
#         assert release_planning_budget_amount_currency == True
#         assert release_planning_budget_rationale == True
#         assert release_relatedProcesses_id == True
#         assert release_related_processes_relationship == True
#         assert release_related_processes_scheme == True
#         assert release_related_processes_identifier == True
#         assert release_related_processes_uri == True
#
#     @pytestrail.case("25543")
#     def test_25543_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25543")
#     def test_25543_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25543")
#     def test_25543_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         time.sleep(2)
#         url_update = update_fs_response[1]["data"]["url"]
#         publicPoint_update = requests.get(url=url_update).json()
#         assert publicPoint_update["releases"][0]["tag"][0] == "planning"
#
#     @pytestrail.case("25544")
#     def test_25544_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25544")
#     def test_25544_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25544")
#     def test_25544_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         time.sleep(2)
#         operation_id = update_fs_response[1]["X-OPERATION-ID"]
#         url_update = update_fs_response[1]["data"]["url"]
#         publicPoint_update = requests.get(url=url_update).json()
#         release_date_from_database = get_date_execute_cql_from_orchestrator_operation_step_by_oper_id \
#             (operation_id, 'NoticeCreateReleaseTask').strftime('%Y-%m-%dT%H:%M:%SZ')
#         assert publicPoint_update["releases"][0]["date"] == release_date_from_database
#
#     @pytestrail.case("25545")
#     def test_25545_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25545")
#     def test_25545_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25545")
#     def test_25545_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         time.sleep(2)
#         url_update = update_fs_response[1]["data"]["url"]
#         release_timestamp_from_fs_record = int(requests.get(url=url_update).json()["releases"][0]["id"][46:59])
#         release_date_from_fs_record = requests.get(url=url_update).json()["releases"][0]["date"]
#         transform_timestamp_to_date = get_human_date_in_utc_format(release_timestamp_from_fs_record)
#         assert release_date_from_fs_record == transform_timestamp_to_date
#
#     @pytestrail.case("25546")
#     def test_25546_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25546")
#     def test_25546_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25546")
#     def test_25546_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         time.sleep(2)
#         url_update = update_fs_response[1]["data"]["url"]
#         release_id = requests.get(url=url_update).json()["releases"][0]["id"]
#         release_date = get_release_date(cpid, "FS")
#         duration_end_date = release_date + datetime.timedelta(hours=2)
#         human_date = duration_end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
#         release_date_as_timestamp = int(get_timestamp_from_human_date(human_date))
#         assert release_id[0:28] == cpid
#         assert release_id[0:45] == create_fs_response[2]
#         assert int(release_id[46:59]) // 1000 == release_date_as_timestamp
#
#     @pytestrail.case("25553")
#     def test_25553_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25553")
#     def test_25553_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25553")
#     def test_25553_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         fs_initiaation_type = requests.get(url=update_fs_response[1]["data"]["url"]).json()["releases"][0][
#             "initiationType"]
#         assert fs_initiaation_type == "tender"
#
#     @pytestrail.case("25554")
#     def test_25554_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25554")
#     def test_25554_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25554")
#     def test_25554_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         fs_ocid_before_update = requests.get(url=create_fs_response[0]).json()["releases"][0]["ocid"]
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         fs_ocid_after_update = requests.get(url=update_fs_response[1]["data"]["url"]).json()["releases"][0]["ocid"]
#         assert fs_ocid_before_update == fs_ocid_after_update
#
#     @pytestrail.case("25555")
#     def test_25555_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25555")
#     def test_25555_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25555")
#     def test_25555_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         planning_from_database = \
#             (execute_cql_from_orchestrator_operation_step_by_oper_id(update_fs_response[2], "NoticeCreateReleaseTask"))[
#                 0]["data"]["fs"]["planning"]
#         del planning_from_database["budget"]["verificationDetails"]
#         planning_from_public_point = requests.get(url=update_fs_response[1]["data"]["url"]).json()["releases"][0][
#             "planning"]
#         assert planning_from_public_point == planning_from_database
#
#     @pytestrail.case("25556")
#     def test_25556_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25556")
#     def test_25556_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25556")
#     def test_25556_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         tender_from_database = \
#             (execute_cql_from_orchestrator_operation_step_by_oper_id(update_fs_response[2], "BudgetUpdateFsTask"))[1][
#                 "fs"]["tender"]
#         tender_from_public_point = requests.get(url=update_fs_response[1]["data"]["url"]).json()["releases"][0][
#             "tender"]
#         assert tender_from_public_point == tender_from_database
#
#     @pytestrail.case("25557")
#     def test_25557_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25557")
#     def test_25557_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25557")
#     def test_25557_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#
#         related_processes_before_update = requests.get(url=create_fs_response[0]).json()["releases"][0][
#             "relatedProcesses"]
#         related_processes_after_update = requests.get(url=update_fs_response[1]["data"]["url"]).json()["releases"][0][
#             "relatedProcesses"]
#         assert related_processes_after_update == related_processes_before_update
#
#     @pytestrail.case("25559")
#     def test_25559_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25559")
#     def test_25559_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25559")
#     def test_25559_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         get_ei_cpid = \
#             requests.get(url=update_fs_response[1]["data"]["url"]).json()["releases"][0]["relatedProcesses"][0]["uri"]
#         release_tag_from_ei = requests.get(url=get_ei_cpid).json()["releases"][0]["tag"][0]
#         assert release_tag_from_ei == "compiled"
#
#     @pytestrail.case("25560")
#     def test_25560_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25560")
#     def test_25560_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25560")
#     def test_25560_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         initiationType_before_update = requests.get(url=create_fs_response[0]).json()["releases"][0]["initiationType"]
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         initiationType_after_update = \
#             requests.get(url=update_fs_response[1]["data"]["url"]).json()["releases"][0]["initiationType"]
#         assert initiationType_after_update == initiationType_before_update
#
#     @pytestrail.case("25561")
#     def test_25561_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25561")
#     def test_25561_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25561")
#     def test_25561_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         ocid_before_update = requests.get(url=create_fs_response[0]).json()["releases"][0]["ocid"]
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid_after_update = \
#             requests.get(url=update_fs_response[1]["data"]["url"]).json()["releases"][0]["ocid"]
#         assert ocid_after_update == ocid_before_update
#
#     @pytestrail.case("25562")
#     def test_25562_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25562")
#     def test_25562_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25562")
#     def test_25562_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         release_date_from_database = \
#             execute_cql_from_orchestrator_operation_step_by_oper_id(update_fs_response[2], "NoticeCreateReleaseTask")[
#                 0]["context"]["startDate"]
#         cpid_ei_release = requests.get(url=update_fs_response[1]["data"]["url"]).json()["releases"][0][
#             "relatedProcesses"][0]["uri"]
#         release_date_from_ei_release = requests.get(url=cpid_ei_release).json()["releases"][0]["date"]
#         assert release_date_from_ei_release == release_date_from_database
#
#     @pytestrail.case("25547")
#     def test_25547_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25547")
#     def test_25547_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25547")
#     def test_25547_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         time.sleep(2)
#         url_update = update_fs_response[1]["data"]["url"]
#         cpid_url = requests.get(url=url_update).json()["releases"][0]["relatedProcesses"][0]["uri"]
#         cpid_releases_id = requests.get(url=cpid_url).json()["releases"][0]["id"]
#         release_date = get_release_date(cpid, "FS")
#         duration_end_date = release_date + datetime.timedelta(hours=2)
#         human_date = duration_end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
#         release_date_as_timestamp = int(get_timestamp_from_human_date(human_date))
#         assert cpid_releases_id[0:28] == cpid
#         assert int(cpid_releases_id[29:42]) // 1000 == release_date_as_timestamp
#
#     @pytestrail.case("25564")
#     def test_25564_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["buyer"]["name"] = "value for funder 2021"
#         payload["buyer"]["identifier"]["id"] = "value for funder 2021"
#         payload["buyer"]["identifier"]["scheme"] = "value for funder 2021"
#         payload["buyer"]["identifier"]["legalName"] = "value for funder 2021"
#         payload["buyer"]["identifier"]["uri"] = "value for funder 2021"
#         payload["buyer"]["address"]["streetAddress"] = "value for funder 2021"
#         payload["buyer"]["address"]["postalCode"] = "value for funder 2021"
#         payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "value for funder 2021"
#         payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "value for funder 2021"
#         payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "value for funder 2021"
#         payload["buyer"]["address"]["addressDetails"]["locality"]["description"] = "value for funder 2021"
#         payload["buyer"]["additionalIdentifiers"][0]["id"] = "value for funder 2021"
#         payload["buyer"]["additionalIdentifiers"][0]["scheme"] = "value for funder 2021"
#         payload["buyer"]["additionalIdentifiers"][0]["legalName"] = "value for funder 2021"
#         payload["buyer"]["additionalIdentifiers"][0]["uri"] = "value for funder 2021"
#         payload["buyer"]["contactPoint"]["name"] = "value for funder 2021"
#         payload["buyer"]["contactPoint"]["email"] = "value for funder 2021"
#         payload["buyer"]["contactPoint"]["telephone"] = "value for funder 2021"
#         payload["buyer"]["contactPoint"]["faxNumber"] = "value for funder 2021"
#         payload["buyer"]["contactPoint"]["url"] = "value for funder 2021"
#
#         payload["tender"]["procuringEntity"]["name"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["identifier"]["id"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["identifier"]["scheme"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["identifier"]["legalName"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["identifier"]["uri"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["streetAddress"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["postalCode"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]["id"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["scheme"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"][
#             "description"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["id"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["scheme"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["legalName"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["uri"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["contactPoint"]["name"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["contactPoint"]["email"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["contactPoint"]["telephone"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["contactPoint"]["faxNumber"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["contactPoint"]["url"] = "value for payer 2021"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25564")
#     def test_25564_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["buyer"]["name"] = "value for funder 2021"
#         payload["buyer"]["identifier"]["id"] = "value for funder 2021"
#         payload["buyer"]["identifier"]["scheme"] = "value for funder 2021"
#         payload["buyer"]["identifier"]["legalName"] = "value for funder 2021"
#         payload["buyer"]["identifier"]["uri"] = "value for funder 2021"
#         payload["buyer"]["address"]["streetAddress"] = "value for funder 2021"
#         payload["buyer"]["address"]["postalCode"] = "value for funder 2021"
#         payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "value for funder 2021"
#         payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "value for funder 2021"
#         payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "value for funder 2021"
#         payload["buyer"]["address"]["addressDetails"]["locality"]["description"] = "value for funder 2021"
#         payload["buyer"]["additionalIdentifiers"][0]["id"] = "value for funder 2021"
#         payload["buyer"]["additionalIdentifiers"][0]["scheme"] = "value for funder 2021"
#         payload["buyer"]["additionalIdentifiers"][0]["legalName"] = "value for funder 2021"
#         payload["buyer"]["additionalIdentifiers"][0]["uri"] = "value for funder 2021"
#         payload["buyer"]["contactPoint"]["name"] = "value for funder 2021"
#         payload["buyer"]["contactPoint"]["email"] = "value for funder 2021"
#         payload["buyer"]["contactPoint"]["telephone"] = "value for funder 2021"
#         payload["buyer"]["contactPoint"]["faxNumber"] = "value for funder 2021"
#         payload["buyer"]["contactPoint"]["url"] = "value for funder 2021"
#
#         payload["tender"]["procuringEntity"]["name"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["identifier"]["id"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["identifier"]["scheme"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["identifier"]["legalName"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["identifier"]["uri"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["streetAddress"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["postalCode"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]["id"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["scheme"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"][
#             "description"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["id"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["scheme"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["legalName"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["uri"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["contactPoint"]["name"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["contactPoint"]["email"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["contactPoint"]["telephone"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["contactPoint"]["faxNumber"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["contactPoint"]["url"] = "value for payer 2021"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25564")
#     def test_25564_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         ei_cpid_before_update = \
#             requests.get(url=create_fs_response[0]).json()["releases"][0]["relatedProcesses"][0]["uri"]
#         parties_from_ei_before_update = requests.get(url=ei_cpid_before_update).json()["releases"][0]["parties"]
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["buyer"]["name"] = "value for funder 2021"
#         payload["buyer"]["identifier"]["id"] = "value for funder 2021"
#         payload["buyer"]["identifier"]["scheme"] = "value for funder 2021"
#         payload["buyer"]["identifier"]["legalName"] = "value for funder 2021"
#         payload["buyer"]["identifier"]["uri"] = "value for funder 2021"
#         payload["buyer"]["address"]["streetAddress"] = "value for funder 2021"
#         payload["buyer"]["address"]["postalCode"] = "value for funder 2021"
#         payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "value for funder 2021"
#         payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "value for funder 2021"
#         payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "value for funder 2021"
#         payload["buyer"]["address"]["addressDetails"]["locality"]["description"] = "value for funder 2021"
#         payload["buyer"]["additionalIdentifiers"][0]["id"] = "value for funder 2021"
#         payload["buyer"]["additionalIdentifiers"][0]["scheme"] = "value for funder 2021"
#         payload["buyer"]["additionalIdentifiers"][0]["legalName"] = "value for funder 2021"
#         payload["buyer"]["additionalIdentifiers"][0]["uri"] = "value for funder 2021"
#         payload["buyer"]["contactPoint"]["name"] = "value for funder 2021"
#         payload["buyer"]["contactPoint"]["email"] = "value for funder 2021"
#         payload["buyer"]["contactPoint"]["telephone"] = "value for funder 2021"
#         payload["buyer"]["contactPoint"]["faxNumber"] = "value for funder 2021"
#         payload["buyer"]["contactPoint"]["url"] = "value for funder 2021"
#
#         payload["tender"]["procuringEntity"]["name"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["identifier"]["id"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["identifier"]["scheme"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["identifier"]["legalName"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["identifier"]["uri"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["streetAddress"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["postalCode"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]["id"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["scheme"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"][
#             "description"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["id"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["scheme"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["legalName"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["uri"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["contactPoint"]["name"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["contactPoint"]["email"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["contactPoint"]["telephone"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["contactPoint"]["faxNumber"] = "value for payer 2021"
#         payload["tender"]["procuringEntity"]["contactPoint"]["url"] = "value for payer 2021"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ei_cpid_after_update = \
#             requests.get(url=update_fs_response[1]["data"]["url"]).json()["releases"][0]["relatedProcesses"][0]["uri"]
#         parties_from_ei_after_update = requests.get(url=ei_cpid_after_update).json()["releases"][0]["parties"]
#         assert parties_from_ei_after_update == parties_from_ei_before_update
#
#     @pytestrail.case("27003")
#     def test_27003_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("27003")
#     def test_27003_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("27003")
#     def test_27003_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         ei_cpid_before_update = \
#             requests.get(url=create_fs_response[0]).json()["releases"][0]["relatedProcesses"][0]["uri"]
#         ei_before_buyer_section = requests.get(url=ei_cpid_before_update).json()["releases"][0]["buyer"]
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ei_cpid_after_update = \
#             requests.get(url=update_fs_response[1]["data"]["url"]).json()["releases"][0]["relatedProcesses"][0]["uri"]
#         ei_after_buyer_section = requests.get(url=ei_cpid_after_update).json()["releases"][0]["buyer"]
#         assert ei_before_buyer_section["id"] == ei_after_buyer_section["id"]
#         assert ei_before_buyer_section["name"] == ei_after_buyer_section["name"]
#
#     @pytestrail.case("25565")
#     def test_25565_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25565")
#     def test_25565_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25565")
#     def test_25565_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         ei_cpid_before_update = \
#             requests.get(url=create_fs_response[0]).json()["releases"][0]["relatedProcesses"][0]["uri"]
#         ei_release_before_update = requests.get(url=ei_cpid_before_update).json()
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ei_cpid_before_update = \
#             requests.get(url=update_fs_response[1]["data"]["url"]).json()["releases"][0]["relatedProcesses"][0]["uri"]
#         ei_release_after_update = requests.get(url=ei_cpid_before_update).json()
#         assert ei_release_after_update["releases"][0]["tender"]["id"] == \
#                ei_release_before_update["releases"][0]["tender"]["id"]
#         assert ei_release_after_update["releases"][0]["tender"]["title"] == \
#                ei_release_before_update["releases"][0]["tender"]["title"]
#         assert ei_release_after_update["releases"][0]["tender"]["status"] == \
#                ei_release_before_update["releases"][0]["tender"]["status"]
#         assert ei_release_after_update["releases"][0]["tender"]["statusDetails"] == \
#                ei_release_before_update["releases"][0]["tender"]["statusDetails"]
#         assert ei_release_after_update["releases"][0]["tender"]["mainProcurementCategory"] == \
#                ei_release_before_update["releases"][0]["tender"]["mainProcurementCategory"]
#         assert ei_release_after_update["releases"][0]["tender"]["classification"]["scheme"] == \
#                ei_release_before_update["releases"][0]["tender"]["classification"]["scheme"]
#         assert ei_release_after_update["releases"][0]["tender"]["classification"]["id"] == \
#                ei_release_before_update["releases"][0]["tender"]["classification"]["id"]
#         assert ei_release_after_update["releases"][0]["tender"]["classification"]["description"] == \
#                ei_release_before_update["releases"][0]["tender"]["classification"]["description"]
#
#     @pytestrail.case("25550")
#     def test_25550_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25550")
#     def test_25550_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25550")
#     def test_25550_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         related_processes_section_before_update = requests.get(url=create_fs_response[0]).json()["releases"][0][
#             "relatedProcesses"]
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         tender_section_after_update = requests.get(url=update_fs_response[1]["data"]["url"]).json()["releases"][0][
#             "relatedProcesses"]
#         assert related_processes_section_before_update == tender_section_after_update
#
#     @pytestrail.case("25551")
#     def test_25551_1(self):
#         time.sleep(5)
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["id"] = "update"
#
#         payload["planning"]["budget"]["amount"]["currency"] = "EUR"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25551")
#     def test_25551_2(self):
#
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["id"] = "update"
#
#         payload["planning"]["budget"]["amount"]["currency"] = "EUR"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25551")
#     def test_25551_3(self):
#
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         planning_section_before_update = requests.get(url=create_fs_response[0]).json()["releases"][0]
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["id"] = "update"
#         payload["planning"]["budget"]["amount"]["currency"] = "EUR"
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         planning_after_update = requests.get(url=update_fs_response[1]["data"]["url"]).json()["releases"][0]
#         assert planning_section_before_update["planning"]["budget"]["id"] == planning_after_update[
#             "planning"]["budget"]["id"]
#         assert planning_section_before_update["tender"]["id"] == planning_after_update["tender"]["id"]
#         assert planning_section_before_update["planning"]["budget"]["amount"]["currency"] == \
#                planning_after_update["planning"]["budget"]["amount"]["currency"]
#
#     @pytestrail.case("25552")
#     def test_25552_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["amount"]["amount"] = 99.99
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25552")
#     def test_25552_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["amount"]["amount"] = 99.99
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25552")
#     def test_25552_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         cpid_url_before_update = requests.get(url=create_fs_response[0]).json()["releases"][0]["relatedProcesses"][0][
#             "uri"]
#         ei_amount_before_update = \
#             requests.get(url=cpid_url_before_update).json()["releases"][0]["planning"]["budget"]["amount"][
#                 "amount"]
#         payload = copy.deepcopy(fs_update_full_own_money)
#         payload["planning"]["budget"]["amount"]["amount"] = 99.99
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         time.sleep(2)
#         url_update = update_fs_response[1]["data"]["url"]
#         cpid_url_after_update = requests.get(url=url_update).json()["releases"][0]["relatedProcesses"][0]["uri"]
#         ei_amount_after_update = \
#             requests.get(url=cpid_url_after_update).json()["releases"][0]["planning"]["budget"]["amount"][
#                 "amount"]
#         assert ei_amount_after_update != ei_amount_before_update
#         assert ei_amount_after_update == payload["planning"]["budget"]["amount"]["amount"]
#
#     @pytestrail.case("25569")
#     def test_25569_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("25569")
#     def test_25569_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("25569")
#     def test_25569_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ei_cpid = \
#             requests.get(url=update_fs_response[1]["data"]["url"]).json()["releases"][0]["relatedProcesses"][0]["uri"]
#         ei_release_after_update = requests.get(url=ei_cpid).json()
#         check_relatedProcesses_id = is_it_uuid(ei_release_after_update["releases"][0]["relatedProcesses"][0]["id"], 1)
#         assert ei_release_after_update["releases"][0]["relatedProcesses"][0]["relationship"][0] == "x_fundingSource"
#         assert check_relatedProcesses_id == True
#         assert ei_release_after_update["releases"][0]["relatedProcesses"][0][
#                    "uri"] == f"http://dev.public.eprocurement.systems/budgets/{cpid}/{update_fs_response[3]}"
#         assert ei_release_after_update["releases"][0]["relatedProcesses"][0][
#                    "identifier"] == update_fs_response[3]
#         assert ei_release_after_update["releases"][0]["relatedProcesses"][0][
#                    "scheme"] == "ocid"
#
#     @pytestrail.case("26989")
#     def test_26989_1(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         assert update_fs_response[0].text == "ok"
#         assert update_fs_response[0].status_code == 202
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#
#     @pytestrail.case("26989")
#     def test_26989_2(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
#         assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
#         assert ocid == True
#
#     @pytestrail.case("26989")
#     def test_26989_3(self):
#         cpid = prepared_cpid()
#         create_fs_response = insert_into_db_create_fs(cpid)
#         payload = copy.deepcopy(fs_update_full_own_money)
#         update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
#         fs_release_after_update = requests.get(url=update_fs_response[1]["data"]["url"]).json()
#         check_relatedProcesses_id = is_it_uuid(fs_release_after_update["releases"][0]["relatedProcesses"][0]["id"], 1)
#         assert fs_release_after_update["releases"][0]["relatedProcesses"][0]["relationship"][0] == "parent"
#         assert check_relatedProcesses_id == True
#         assert fs_release_after_update["releases"][0]["relatedProcesses"][0][
#                    "uri"] == f"http://dev.public.eprocurement.systems/budgets/{cpid}/{cpid}"
#         assert fs_release_after_update["releases"][0]["relatedProcesses"][0][
#                    "identifier"] == cpid
#         assert fs_release_after_update["releases"][0]["relatedProcesses"][0][
#                    "scheme"] == "ocid"
