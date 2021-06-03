import copy
from uuid import uuid4
import requests
from deepdiff import DeepDiff
from pytest_testrail.plugin import pytestrail
from tests.conftest import CreatePn
from tests.essences.pn import PN
from tests.iMDM_service.get_information import MdmService
from tests.payloads.pn_payload import create_pn_payload_obligatory_data_model_without_documents, \
    create_pn_payload_full_data_model_with_documents
from useful_functions import prepared_cp_id, compare_actual_result_and_expected_result, get_human_date_in_utc_format, \
    is_it_uuid, get_value_from_classification_cpv_dictionary_xls, get_new_classification_id, \
    get_value_from_classification_unit_dictionary_csv, get_value_from_cpvs_dictionary_csv


class TestCheckThePossibilityOfPlanningNoticeCreationWithoutOptionalFields(object):
    @pytestrail.case("27585")
    def test_send_request_see_result_in_feed_point_27585_1(self, country, language, instance, cassandra_username,
                                                           cassandra_password, pmd):
        ei_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_pn_payload_obligatory_data_model_without_documents)
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["scheme"] = "other"
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["id"] = "test_value_for_locality"
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["description"] = "desc"
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["uri"] = "www segodnya"
        pn = PN(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd
        )
        create_fs_response = pn.insert_fs_treasury_obligatory_ei_obligatory_without_items(
            cp_id=ei_id,
            ei_token=ei_token
        )
        pn.create_pn(fs_id=create_fs_response[1])
        pn.get_message_from_kafka()
        CreatePn.message_from_kafka = pn.get_message_from_kafka()
        CreatePn.payload = payload
        CreatePn.ei_id = ei_id
        CreatePn.fs_id = create_fs_response[1]
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(pn.check_on_that_message_is_successfully_create_pn())
        )

    @pytestrail.case("27585")
    def test_check_uri_on_pp_pn_release_27585_3(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        cp_id = CreatePn.message_from_kafka['data']['ocid']
        pn_id = CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        assert compare_actual_result_and_expected_result(
            expected_result=f"http://dev.public.eprocurement.systems/tenders/{cp_id}/{pn_id}",
            actual_result=pn_release["uri"]
        )

    @pytestrail.case("27585")
    def test_check_version_on_pp_pn_release_27585_4(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="1.1",
            actual_result=pn_release["version"]
        )

    @pytestrail.case("27585")
    def test_check_extensions_array_on_pp_pn_release_27585_5(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="https://raw.githubusercontent.com/open-contracting/ocds_bid_extension/v1.1.1/"
                            "extension.json",
            actual_result=pn_release["extensions"][0]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="https://raw.githubusercontent.com/open-contracting/ocds_enquiry_extension/v1.1.1/"
                            "extension.js",
            actual_result=pn_release["extensions"][1]
        )

    @pytestrail.case("27585")
    def test_check_publisher_name_on_pp_pn_release_27585_6(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="M-Tender",
            actual_result=pn_release["publisher"]["name"]
        )

    @pytestrail.case("27585")
    def test_check_publisher_uri_on_pp_pn_release_27585_7(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="https://www.mtender.gov.md",
            actual_result=pn_release["publisher"]["uri"]
        )

    @pytestrail.case("27585")
    def test_check_license_on_pp_pn_release_27585_8(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="http://opendefinition.org/licenses/",
            actual_result=pn_release["license"]
        )

    @pytestrail.case("27585")
    def test_check_publication_policy_on_pp_pn_release_27585_9(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="http://opendefinition.org/licenses/",
            actual_result=pn_release["publicationPolicy"]
        )

    @pytestrail.case("27585")
    def test_check_published_date_on_pp_pn_release_27585_10(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=CreatePn.message_from_kafka["data"]["operationDate"],
            actual_result=pn_release["publishedDate"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_oc_id_on_pp_pn_release_27585_11(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id'],
            actual_result=pn_release["releases"][0]["ocid"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_id_on_pp_pn_release_27585_12(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id'],
            actual_result=pn_release["releases"][0]["id"][0:45]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=get_human_date_in_utc_format(int(pn_release["releases"][0]["id"][46:59]))[0],
            actual_result=pn_release["releases"][0]["date"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_date_on_pp_pn_release_27585_13(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=CreatePn.message_from_kafka['data']['operationDate'],
            actual_result=pn_release["releases"][0]["date"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tag_pn_release_27585_14(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(["planning"]),
            actual_result=str(pn_release["releases"][0]["tag"])
        )

    @pytestrail.case("27585")
    def test_check_releases_0_language_on_pp_pn_release_27585_15(self, language):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=language,
            actual_result=pn_release["releases"][0]["language"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_initiation_type_on_pp_pn_release_27585_16(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="tender",
            actual_result=pn_release["releases"][0]["initiationType"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_id_on_pp_pn_release_27585_17(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(is_it_uuid(pn_release["releases"][0]["tender"]["id"], 4))
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_title_on_pp_pn_release_27585_18(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="Planning Notice",
            actual_result=pn_release["releases"][0]["tender"]["title"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_description_on_pp_pn_release_27585_19(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="Contracting process is planned",
            actual_result=pn_release["releases"][0]["tender"]["description"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_status_on_pp_pn_release_27585_20(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="planning",
            actual_result=pn_release["releases"][0]["tender"]["status"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_status_details_on_pp_pn_release_27585_21(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="planning",
            actual_result=pn_release["releases"][0]["tender"]["statusDetails"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_lot_groups_0_option_to_combine_on_pp_pn_release_27585_22(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(False),
            actual_result=str(pn_release["releases"][0]["tender"]["lotGroups"][0]["optionToCombine"])
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_tender_period_start_date_on_pp_pn_release_27585_23(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=CreatePn.payload["tender"]["tenderPeriod"]["startDate"],
            actual_result=str(pn_release["releases"][0]["tender"]["tenderPeriod"]["startDate"])
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_has_enquiries_on_pp_pn_release_27585_24(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(False),
            actual_result=str(pn_release["releases"][0]["tender"]["hasEnquiries"])
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_submission_method_0_on_pp_pn_release_27585_25(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="electronicSubmission",
            actual_result=pn_release["releases"][0]["tender"]["submissionMethod"][0]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_submission_method_details_0_on_pp_pn_release_27585_26(self, pmd):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        mdm = MdmService(
            instance="dev",
            lang="ro",
            procuring_address_details_country_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["country"]["id"],
            procuring_address_details_region_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["region"]["id"],
            procuring_address_details_locality_scheme=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["scheme"],
            procuring_address_details_locality_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["id"]
        )
        data = mdm.process_tender_data(pmd).json()
        submission_method_details_from_mdm = data["data"]["tender"]["submissionMethodDetails"]
        assert compare_actual_result_and_expected_result(
            expected_result=submission_method_details_from_mdm,
            actual_result=pn_release["releases"][0]["tender"]["submissionMethodDetails"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_submission_method_rationale_0_on_pp_pn_release_27585_27(self, pmd):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        mdm = MdmService(
            instance="dev",
            lang="ro",
            procuring_address_details_country_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["country"]["id"],
            procuring_address_details_region_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["region"]["id"],
            procuring_address_details_locality_scheme=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["scheme"],
            procuring_address_details_locality_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["id"]
        )
        data = mdm.process_tender_data(pmd).json()
        submission_method_rationale_from_mdm = data["data"]["tender"]["submissionMethodRationale"]
        assert compare_actual_result_and_expected_result(
            expected_result=submission_method_rationale_from_mdm[0],
            actual_result=pn_release["releases"][0]["tender"]["submissionMethodRationale"][0]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_requires_electronic_catalogue_on_pp_pn_release_27585_28(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(False),
            actual_result=str(pn_release["releases"][0]["tender"]["requiresElectronicCatalogue"])
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_classification_id_on_pp_pn_release_27585_29(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        pn_record = requests.get(url=CreatePn.message_from_kafka['data']['url']).json()["records"]
        related_processes_list = list()
        for d in pn_record:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["tender"]["classification"]["id"],
            actual_result=pn_release["releases"][0]["tender"]["classification"]["id"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_classification_scheme_on_pp_pn_release_27585_30(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        pn_record = requests.get(url=CreatePn.message_from_kafka['data']['url']).json()["records"]
        related_processes_list = list()
        for d in pn_record:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["tender"]["classification"]["scheme"],
            actual_result=pn_release["releases"][0]["tender"]["classification"]["scheme"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_classification_description_on_pp_pn_release_27585_31(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        pn_record = requests.get(url=CreatePn.message_from_kafka['data']['url']).json()["records"]
        related_processes_list = list()
        for d in pn_record:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["tender"]["classification"]["description"],
            actual_result=pn_release["releases"][0]["tender"]["classification"]["description"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_value_amount_on_pp_pn_release_27585_32(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(CreatePn.payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["amount"]),
            actual_result=str(pn_release["releases"][0]["tender"]["value"]["amount"])
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_value_currency_on_pp_pn_release_27585_33(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=CreatePn.payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["currency"],
            actual_result=pn_release["releases"][0]["tender"]["value"]["currency"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_has_previous_notice_on_pp_pn_release_27585_34(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(False),
            actual_result=str(pn_release["releases"][0]["hasPreviousNotice"])
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_purpose_of_notice_is_a_call_for_competition_on_pp_pn_release_27585_35(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(False),
            actual_result=str(pn_release["releases"][0]["purposeOfNotice"]["isACallForCompetition"])
        )

    @pytestrail.case("27585")
    def test_check_releases_0_related_processes_0_id_on_pp_pn_release_27585_36(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(is_it_uuid(pn_release["releases"][0]["relatedProcesses"][0]["id"], 1))
        )

    @pytestrail.case("27585")
    def test_check_releases_0_related_processes_0_relationship_0_on_pp_pn_release_27585_37(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in pn_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    related_processes_list.append(d_1)
        assert compare_actual_result_and_expected_result(
            expected_result="parent",
            actual_result=related_processes_list[0]["relationship"][0]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_related_processes_0_scheme_on_pp_pn_release_27585_38(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in pn_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    related_processes_list.append(d_1)
        assert compare_actual_result_and_expected_result(
            expected_result="ocid",
            actual_result=related_processes_list[0]["scheme"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_related_processes_0_identifier_on_pp_pn_release_27585_39(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in pn_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    related_processes_list.append(d_1)
        assert compare_actual_result_and_expected_result(
            expected_result=CreatePn.message_from_kafka['data']['ocid'],
            actual_result=related_processes_list[0]["identifier"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_related_processes_0_uri_on_pp_pn_release_27585_40(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in pn_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    related_processes_list.append(d_1)
        assert compare_actual_result_and_expected_result(
            expected_result=CreatePn.message_from_kafka['data']['url'] + "/" + CreatePn.message_from_kafka["data"][
                'ocid'],
            actual_result=related_processes_list[0]["uri"]
        )

    @pytestrail.case("27585")
    def test_check_uri_on_pp_ms_release_27585_42(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=f"http://dev.public.eprocurement.systems/tenders/"
                            f"{CreatePn.message_from_kafka['data']['ocid']}/"
                            f"{CreatePn.message_from_kafka['data']['ocid']}",
            actual_result=ms_release["uri"]
        )

    @pytestrail.case("27585")
    def test_check_version_on_pp_ms_release_27585_43(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="1.1",
            actual_result=ms_release["version"]
        )

    @pytestrail.case("27585")
    def test_check_extensions_array_on_pp_ms_release_27585_44(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="https://raw.githubusercontent.com/open-contracting/ocds_bid_extension/v1.1.1/"
                            "extension.json",
            actual_result=ms_release["extensions"][0]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="https://raw.githubusercontent.com/open-contracting/ocds_enquiry_extension/v1.1.1/"
                            "extension.js",
            actual_result=ms_release["extensions"][1]
        )

    @pytestrail.case("27585")
    def test_check_publisher_name_on_pp_ms_release_27585_45(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="M-Tender",
            actual_result=ms_release["publisher"]["name"]
        )

    @pytestrail.case("27585")
    def test_check_publisher_uri_on_pp_ms_release_27585_46(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="https://www.mtender.gov.md",
            actual_result=ms_release["publisher"]["uri"]
        )

    @pytestrail.case("27585")
    def test_check_publication_policy_on_pp_ms_release_27585_47(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="http://opendefinition.org/licenses/",
            actual_result=ms_release["publicationPolicy"]
        )

    @pytestrail.case("27585")
    def test_check_license_on_pp_ms_release_27585_48(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="http://opendefinition.org/licenses/",
            actual_result=ms_release["license"]
        )

    @pytestrail.case("27585")
    def test_check_published_date_on_pp_ms_release_27585_49(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=CreatePn.message_from_kafka["data"]["operationDate"],
            actual_result=ms_release["publishedDate"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_oc_id_on_pp_ms_release_27585_50(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=CreatePn.message_from_kafka['data']['ocid'],
            actual_result=ms_release['releases'][0]['ocid']
        )

    @pytestrail.case("27585")
    def test_check_releases_0_id_on_pp_ms_release_27585_51(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=CreatePn.message_from_kafka['data']['ocid'],
            actual_result=ms_release["releases"][0]["id"][0:28]

        )
        assert compare_actual_result_and_expected_result(
            expected_result=get_human_date_in_utc_format(int(ms_release["releases"][0]["id"][29:42]))[0],
            actual_result=ms_release["releases"][0]["date"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_date_on_pp_ms_release_27585_52(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=CreatePn.message_from_kafka['data']['operationDate'],
            actual_result=ms_release["releases"][0]["date"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tag_0_on_pp_ms_release_27585_53(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="compiled",
            actual_result=ms_release["releases"][0]["tag"][0]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_language_on_pp_ms_release_27585_54(self, language):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=language,
            actual_result=ms_release["releases"][0]["language"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_initiation_type_on_pp_ms_release_27585_55(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="tender",
            actual_result=ms_release["releases"][0]["initiationType"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_planning_budget_amount_amount_on_pp_ms_release_27585_56(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(CreatePn.payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["amount"]),
            actual_result=str(ms_release["releases"][0]["planning"]["budget"]["amount"]["amount"])
        )

    @pytestrail.case("27585")
    def test_check_releases_0_planning_budget_amount_currency_on_pp_ms_release_27585_57(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(CreatePn.payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["currency"]),
            actual_result=str(ms_release["releases"][0]["planning"]["budget"]["amount"]["currency"])
        )

    @pytestrail.case("27585")
    def test_check_releases_0_planning_budget_is_european_union_funded_on_pp_ms_release_27585_58(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(fs_release["releases"][0]["planning"]["budget"]["isEuropeanUnionFunded"]),
            actual_result=str(ms_release["releases"][0]["planning"]["budget"]["isEuropeanUnionFunded"])
        )

    @pytestrail.case("27585")
    def test_check_releases_0_planning_budget_breakdown_0_id_on_pp_ms_release_27585_59(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        assert compare_actual_result_and_expected_result(
            expected_result=payload['planning']['budget']['budgetBreakdown'][0]['id'],
            actual_result=ms_release["releases"][0]["planning"]["budget"]['budgetBreakdown'][0]['id']
        )

    @pytestrail.case("27585")
    def test_check_releases_0_planning_budget_budget_breakdown_0_amount_amount_on_pp_ms_release_27585_60(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(CreatePn.payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["amount"]),
            actual_result=str(ms_release["releases"][0]["planning"]["budget"]["budgetBreakdown"][0]["amount"]["amount"])
        )

    @pytestrail.case("27585")
    def test_check_releases_0_planning_budget_budget_breakdown_0_amount_currency_on_pp_ms_release_27585_61(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(CreatePn.payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["currency"]),
            actual_result=str(
                ms_release["releases"][0]["planning"]["budget"]["budgetBreakdown"][0]["amount"]["currency"])
        )

    @pytestrail.case("27585")
    def test_check_releases_0_planning_budget_budget_breakdown_0_period_start_date_on_pp_ms_release_27585_62(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release["releases"][0]["planning"]["budget"]["period"]["startDate"],
            actual_result=ms_release["releases"][0]["planning"]["budget"]["budgetBreakdown"][0]["period"]["startDate"]

        )

    @pytestrail.case("27585")
    def test_check_releases_0_planning_budget_budget_breakdown_0_period_end_date_on_pp_ms_release_27585_63(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release["releases"][0]["planning"]["budget"]["period"]["endDate"],
            actual_result=ms_release["releases"][0]["planning"]["budget"]["budgetBreakdown"][0]["period"]["endDate"]

        )

    @pytestrail.case("27585")
    def test_check_releases_0_planning_budget_budget_breakdown_0_source_party_id_on_pp_ms_release_27585_64(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release["releases"][0]["planning"]["budget"]["sourceEntity"]["id"],
            actual_result=ms_release["releases"][0]["planning"]["budget"]["budgetBreakdown"][0]["sourceParty"]["id"]

        )

    @pytestrail.case("27585")
    def test_check_releases_0_planning_budget_budget_breakdown_0_source_party_name_on_pp_ms_release_27585_65(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release["releases"][0]["planning"]["budget"]["sourceEntity"]["name"],
            actual_result=ms_release["releases"][0]["planning"]["budget"]["budgetBreakdown"][0]["sourceParty"]["name"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_id_on_pp_ms_release_27585_66(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(is_it_uuid(ms_release["releases"][0]["tender"]["id"], 4))
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_title_on_pp_ms_release_27585_67(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["title"],
            actual_result=ms_release["releases"][0]["tender"]["title"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_description_on_pp_ms_release_27585_68(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["description"],
            actual_result=ms_release["releases"][0]["tender"]["description"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_status_on_pp_ms_release_27585_69(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="planning",
            actual_result=ms_release["releases"][0]["tender"]["status"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_status_details_on_pp_ms_release_27585_70(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="planning notice",
            actual_result=ms_release["releases"][0]["tender"]["statusDetails"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_value_amount_on_pp_ms_release_27585_71(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        assert compare_actual_result_and_expected_result(
            expected_result=str(payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["amount"]),
            actual_result=str(ms_release["releases"][0]["tender"]["value"]["amount"])
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_value_currency_on_pp_ms_release_27585_72(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["currency"],
            actual_result=ms_release["releases"][0]["tender"]["value"]["currency"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_procurement_method_on_pp_ms_release_27585_73(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="open",
            actual_result=ms_release["releases"][0]["tender"]["procurementMethod"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_procurement_method_details_on_pp_ms_release_27585_74(self, pmd):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        mdm = MdmService(
            instance="dev",
            lang="ro",
            procuring_address_details_country_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["country"]["id"],
            procuring_address_details_region_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["region"]["id"],
            procuring_address_details_locality_scheme=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["scheme"],
            procuring_address_details_locality_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["id"]
        )
        data = mdm.process_tender_data(pmd).json()
        procurement_method_details_from_mdm = data["data"]["tender"]["procurementMethodDetails"]
        assert compare_actual_result_and_expected_result(
            expected_result=procurement_method_details_from_mdm,
            actual_result=ms_release["releases"][0]["tender"]["procurementMethodDetails"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_main_procurement_category_on_pp_ms_release_27585_75(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        # Should get 'mainProcurementCategory' from related EI -> VR-10.5.8
        pn_record = requests.get(url=CreatePn.message_from_kafka['data']['url']).json()["records"]
        related_processes_list = list()
        for d in pn_record:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        procurement_method_details_from_ei_release = ei_release["releases"][0]["tender"]["mainProcurementCategory"]
        assert compare_actual_result_and_expected_result(
            expected_result=procurement_method_details_from_ei_release,
            actual_result=ms_release["releases"][0]["tender"]["mainProcurementCategory"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_has_enquiries_on_pp_ms_release_27585_76(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(False),
            actual_result=str(ms_release["releases"][0]["tender"]["hasEnquiries"])
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_eligibility_criteria_on_pp_ms_release_27585_77(self, pmd):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        mdm = MdmService(
            instance="dev",
            lang="ro",
            procuring_address_details_country_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["country"]["id"],
            procuring_address_details_region_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["region"]["id"],
            procuring_address_details_locality_scheme=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["scheme"],
            procuring_address_details_locality_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["id"]
        )
        data = mdm.process_tender_data(pmd).json()
        eligibility_criteria_from_mdm = data["data"]["tender"]["eligibilityCriteria"]
        assert compare_actual_result_and_expected_result(
            expected_result=eligibility_criteria_from_mdm,
            actual_result=ms_release["releases"][0]["tender"]["eligibilityCriteria"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_procuring_entity_id_on_pp_ms_release_27585_78(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        assert compare_actual_result_and_expected_result(
            expected_result=f"{payload['tender']['procuringEntity']['identifier']['scheme']}-"
                            f"{payload['tender']['procuringEntity']['identifier']['id']}",
            actual_result=ms_release["releases"][0]["tender"]["procuringEntity"]["id"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_procuring_entity_id_on_pp_ms_release_27585_79(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        assert compare_actual_result_and_expected_result(
            expected_result=payload['tender']['procuringEntity']['name'],
            actual_result=ms_release["releases"][0]["tender"]["procuringEntity"]["name"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_accelerated_procedure_is_accelerated_procedure_on_pp_ms_release_27585_80(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(False),
            actual_result=str(ms_release["releases"][0]["tender"]["acceleratedProcedure"]["isAcceleratedProcedure"])
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_classification_id_on_pp_ms_release_27585_81(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        pn_record = requests.get(url=CreatePn.message_from_kafka['data']['url']).json()["records"]
        related_processes_list = list()
        for d in pn_record:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        tender_classification_id_from_ei_release = ei_release["releases"][0]["tender"]["classification"]["id"]
        assert compare_actual_result_and_expected_result(
            expected_result=tender_classification_id_from_ei_release,
            actual_result=ms_release["releases"][0]["tender"]["classification"]["id"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_classification_scheme_on_pp_ms_release_27585_82(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        pn_record = requests.get(url=CreatePn.message_from_kafka['data']['url']).json()["records"]
        related_processes_list = list()
        for d in pn_record:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        tender_classification_id_from_ei_release = ei_release["releases"][0]["tender"]["classification"]["scheme"]
        assert compare_actual_result_and_expected_result(
            expected_result=tender_classification_id_from_ei_release,
            actual_result=ms_release["releases"][0]["tender"]["classification"]["scheme"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_classification_description_on_pp_ms_release_27585_83(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        pn_record = requests.get(url=CreatePn.message_from_kafka['data']['url']).json()["records"]
        related_processes_list = list()
        for d in pn_record:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        tender_classification_id_from_ei_release = ei_release["releases"][0]["tender"]["classification"]["description"]
        assert compare_actual_result_and_expected_result(
            expected_result=tender_classification_id_from_ei_release,
            actual_result=ms_release["releases"][0]["tender"]["classification"]["description"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_design_contest_service_contract_award_on_pp_ms_release_27585_84(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(False),
            actual_result=str(ms_release["releases"][0]["tender"]["designContest"]["serviceContractAward"])
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_electronic_workflows_use_ordering_on_pp_ms_release_27585_85(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(False),
            actual_result=str(ms_release["releases"][0]["tender"]["electronicWorkflows"]["useOrdering"])
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_electronic_workflows_use_payment_on_pp_ms_release_27585_86(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(False),
            actual_result=str(ms_release["releases"][0]["tender"]["electronicWorkflows"]["usePayment"])
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_electronic_workflows_accept_invoicing_on_pp_ms_release_27585_87(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(False),
            actual_result=str(ms_release["releases"][0]["tender"]["electronicWorkflows"]["acceptInvoicing"])
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_joint_procurement_is_joint_procurement_on_pp_ms_release_27585_88(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(False),
            actual_result=str(ms_release["releases"][0]["tender"]["jointProcurement"]["isJointProcurement"])
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_legal_basis_on_pp_ms_release_27585_89(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["legalBasis"],
            actual_result=ms_release["releases"][0]["tender"]["legalBasis"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_procedure_outsourcing_procedure_outsourced_on_pp_ms_release_27585_90(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(False),
            actual_result=str(ms_release["releases"][0]["tender"]["procedureOutsourcing"]["procedureOutsourced"])
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_dynamic_purchasing_system_has_dynamic_purchasing_system_on_pp_ms__27585_91(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(False),
            actual_result=str(
                ms_release["releases"][0]["tender"]["dynamicPurchasingSystem"]["hasDynamicPurchasingSystem"])
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_framework_is_a_framework_on_pp_ms_release_27585_92(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(False),
            actual_result=str(
                ms_release["releases"][0]["tender"]["framework"]["isAFramework"])
        )

    @pytestrail.case("27585")
    def test_buyer_check_releases_0_parties_id_on_pp_ms_release_27585_94(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["id"],
            actual_result=parties_with_buyer_role[0]["id"]
        )

    @pytestrail.case("27585")
    def test_buyer_check_releases_0_parties_name_on_pp_ms_release_27585_95(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["name"],
            actual_result=parties_with_buyer_role[0]["name"]
        )

    @pytestrail.case("27585")
    def test_buyer_check_releases_0_parties_identifier_id_on_pp_ms_release_27585_96(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["identifier"]["id"],
            actual_result=parties_with_buyer_role[0]["identifier"]["id"]
        )

    @pytestrail.case("27585")
    def test_buyer_check_releases_0_parties_identifier_scheme_on_pp_ms_release_27585_97(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["identifier"]["scheme"],
            actual_result=parties_with_buyer_role[0]["identifier"]["scheme"]
        )

    @pytestrail.case("27585")
    def test_buyer_check_releases_0_parties_identifier_legal_name_on_pp_ms_release_27585_98(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["identifier"]["legalName"],
            actual_result=parties_with_buyer_role[0]["identifier"]["legalName"]
        )

    @pytestrail.case("27585")
    def test_buyer_check_releases_0_parties_address_street_address_on_pp_ms_release_27585_99(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["address"]["streetAddress"],
            actual_result=parties_with_buyer_role[0]["address"]["streetAddress"]
        )

    @pytestrail.case("27585")
    def test_buyer_check_releases_0_parties_address_address_detail_country_id_on_pp_ms_release_27585_100(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["id"],
            actual_result=parties_with_buyer_role[0]["address"]["addressDetails"]["country"]["id"]
        )

    @pytestrail.case("27585")
    def test_buyer_check_releases_0_parties_address_address_detail_country_scheme_on_pp_ms_release_27585_101(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["scheme"],
            actual_result=parties_with_buyer_role[0]["address"]["addressDetails"]["country"]["scheme"]
        )

    @pytestrail.case("27585")
    def test_buyer_check_releases_0_parties_address_address_detail_country_description_on_pp_ms_release_27585_102(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"][
                "description"],
            actual_result=parties_with_buyer_role[0]["address"]["addressDetails"]["country"]["description"]
        )

    @pytestrail.case("27585")
    def test_buyer_check_releases_0_parties_address_address_detail_country_uri_on_pp_ms_release_27585_103(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["uri"],
            actual_result=parties_with_buyer_role[0]["address"]["addressDetails"]["country"]["uri"]
        )

    @pytestrail.case("27585")
    def test_buyer_check_releases_0_parties_address_address_detail_region_id_on_pp_ms_release_27585_104(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["id"],
            actual_result=parties_with_buyer_role[0]["address"]["addressDetails"]["region"]["id"]
        )

    @pytestrail.case("27585")
    def test_buyer_check_releases_0_parties_address_address_detail_region_scheme_on_pp_ms_release_27585_105(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["scheme"],
            actual_result=parties_with_buyer_role[0]["address"]["addressDetails"]["region"]["scheme"]
        )

    @pytestrail.case("27585")
    def test_buyer_check_releases_0_parties_address_address_detail_region_description_on_pp_ms_release_27585_106(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"][
                "description"],
            actual_result=parties_with_buyer_role[0]["address"]["addressDetails"]["region"]["description"]
        )

    @pytestrail.case("27585")
    def test_buyer_check_releases_0_parties_address_address_detail_region_uri_on_pp_ms_release_27585_107(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["uri"],
            actual_result=parties_with_buyer_role[0]["address"]["addressDetails"]["region"]["uri"]
        )

    @pytestrail.case("27585")
    def test_buyer_check_releases_0_parties_address_address_detail_locality_id_on_pp_ms_release_27585_108(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["id"],
            actual_result=parties_with_buyer_role[0]["address"]["addressDetails"]["locality"]["id"]
        )

    @pytestrail.case("27585")
    def test_buyer_check_releases_0_parties_address_address_detail_locality_scheme_on_pp_ms_release_27585_109(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["scheme"],
            actual_result=parties_with_buyer_role[0]["address"]["addressDetails"]["locality"]["scheme"]
        )

    @pytestrail.case("27585")
    def test_buyer_check_releases_0_parties_address_address_detail_locality_description_on_pp_ms_release_27585_110(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
                "description"],
            actual_result=parties_with_buyer_role[0]["address"]["addressDetails"]["locality"]["description"]
        )

    @pytestrail.case("27585")
    def test_buyer_check_releases_0_parties_address_address_detail_locality_uri_on_pp_ms_release_27585_111(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["uri"],
            actual_result=parties_with_buyer_role[0]["address"]["addressDetails"]["locality"]["uri"]
        )

    @pytestrail.case("27585")
    def test_buyer_check_releases_0_parties_contact_point_name_on_pp_on_pp_ms_release_27585_112(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["contactPoint"]["name"],
            actual_result=parties_with_buyer_role[0]["contactPoint"]["name"]
        )

    @pytestrail.case("27585")
    def test_buyer_check_releases_0_parties_contact_point_email_on_pp_on_pp_ms_release_27585_113(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["contactPoint"]["email"],
            actual_result=parties_with_buyer_role[0]["contactPoint"]["email"]
        )

    @pytestrail.case("27585")
    def test_buyer_check_releases_0_parties_contact_point_telephone_on_pp_on_pp_ms_release_27585_114(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["contactPoint"]["telephone"],
            actual_result=parties_with_buyer_role[0]["contactPoint"]["telephone"]
        )

    @pytestrail.case("27585")
    def test_buyer_check_releases_0_parties_roles_on_pp_ms_release_27585_115(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["roles"][0],
            actual_result=parties_with_buyer_role[0]["roles"][0]
        )

    @pytestrail.case("27585")
    def test_payer_check_releases_0_parties_id_on_pp_ms_release_27585_117(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release["releases"][0]["parties"][0]["id"],
            actual_result=parties_with_payer_role[0]["id"]
        )

    @pytestrail.case("27585")
    def test_payer_check_releases_0_parties_name_on_pp_ms_release_27585_118(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release["releases"][0]["parties"][0]["name"],
            actual_result=parties_with_payer_role[0]["name"]
        )

    @pytestrail.case("27585")
    def test_payer_check_releases_0_parties_identifier_id_on_pp_ms_release_27585_119(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release["releases"][0]["parties"][0]["identifier"]["id"],
            actual_result=parties_with_payer_role[0]["identifier"]["id"]
        )

    @pytestrail.case("27585")
    def test_payer_check_releases_0_parties_identifier_scheme_on_pp_ms_release_27585_120(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release["releases"][0]["parties"][0]["identifier"]["scheme"],
            actual_result=parties_with_payer_role[0]["identifier"]["scheme"]
        )

    @pytestrail.case("27585")
    def test_payer_check_releases_0_parties_identifier_legal_name_on_pp_ms_release_27585_121(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release["releases"][0]["parties"][0]["identifier"]["legalName"],
            actual_result=parties_with_payer_role[0]["identifier"]["legalName"]
        )

    @pytestrail.case("27585")
    def test_payer_check_releases_0_parties_address_street_address_on_pp_ms_release_27585_122(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release["releases"][0]["parties"][0]["address"]["streetAddress"],
            actual_result=parties_with_payer_role[0]["address"]["streetAddress"]
        )

    @pytestrail.case("27585")
    def test_payer_check_releases_0_parties_address_address_details_country_id_on_pp_ms_release_27585_123(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["id"],
            actual_result=parties_with_payer_role[0]["address"]["addressDetails"]["country"]["id"]
        )

    @pytestrail.case("27585")
    def test_payer_check_releases_0_parties_address_address_details_country_scheme_on_pp_ms_release_27585_124(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["scheme"],
            actual_result=parties_with_payer_role[0]["address"]["addressDetails"]["country"]["scheme"]
        )

    @pytestrail.case("27585")
    def test_payer_check_releases_0_parties_address_address_details_country_description_on_pp_ms_release_27585_125(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"][
                "description"],
            actual_result=parties_with_payer_role[0]["address"]["addressDetails"]["country"]["description"]
        )

    @pytestrail.case("27585")
    def test_payer_check_releases_0_parties_address_address_details_country_uri_on_pp_ms_release_27585_126(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["uri"],
            actual_result=parties_with_payer_role[0]["address"]["addressDetails"]["country"]["uri"]
        )

    @pytestrail.case("27585")
    def test_payer_check_releases_0_parties_address_address_details_region_id_on_pp_ms_release_27585_127(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["id"],
            actual_result=parties_with_payer_role[0]["address"]["addressDetails"]["region"]["id"]
        )

    @pytestrail.case("27585")
    def test_payer_check_releases_0_parties_address_address_details_region_scheme_on_pp_ms_release_27585_128(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["scheme"],
            actual_result=parties_with_payer_role[0]["address"]["addressDetails"]["region"]["scheme"]
        )

    @pytestrail.case("27585")
    def test_payer_check_releases_0_parties_address_address_details_region_description_on_pp_ms_release_27585_129(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"][
                "description"],
            actual_result=parties_with_payer_role[0]["address"]["addressDetails"]["region"]["description"]
        )

    @pytestrail.case("27585")
    def test_payer_check_releases_0_parties_address_address_details_region_uri_on_pp_ms_release_27585_130(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"][
                "uri"],
            actual_result=parties_with_payer_role[0]["address"]["addressDetails"]["region"]["uri"]
        )

    @pytestrail.case("27585")
    def test_payer_check_releases_0_parties_address_address_details_locality_uri_on_pp_ms_release_27585_131(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
                "uri"],
            actual_result=parties_with_payer_role[0]["address"]["addressDetails"]["locality"]["uri"]
        )

    @pytestrail.case("27585")
    def test_payer_check_releases_0_parties_address_address_details_locality_id_on_pp_ms_release_27585_132(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["id"],
            actual_result=parties_with_payer_role[0]["address"]["addressDetails"]["locality"]["id"]
        )

    @pytestrail.case("27585")
    def test_payer_check_releases_0_parties_address_address_details_locality_description_on_pp_ms_release_27585_133(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
                "description"],
            actual_result=parties_with_payer_role[0]["address"]["addressDetails"]["locality"]["description"]
        )

    @pytestrail.case("27585")
    def test_payer_check_releases_0_parties_address_address_details_locality_scheme_on_pp_ms_release_27585_134(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
                "scheme"],
            actual_result=parties_with_payer_role[0]["address"]["addressDetails"]["locality"]["scheme"]
        )

    @pytestrail.case("27585")
    def test_payer_check_releases_0_parties_contact_point_name_on_pp_ms_release_27585_135(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release["releases"][0]["parties"][0]["contactPoint"]["name"],
            actual_result=parties_with_payer_role[0]["contactPoint"]["name"]
        )

    @pytestrail.case("27585")
    def test_payer_check_releases_0_parties_contact_point_email_on_pp_ms_release_27585_136(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release["releases"][0]["parties"][0]["contactPoint"]["email"],
            actual_result=parties_with_payer_role[0]["contactPoint"]["email"]
        )

    @pytestrail.case("27585")
    def test_payer_check_releases_0_parties_contact_point_telephone_on_pp_ms_release_27585_137(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release["releases"][0]["parties"][0]["contactPoint"]["telephone"],
            actual_result=parties_with_payer_role[0]["contactPoint"]["telephone"]
        )

    @pytestrail.case("27585")
    def test_payer_check_releases_0_parties_roles_0_on_pp_ms_release_27585_138(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release["releases"][0]["parties"][0]["roles"][0],
            actual_result=parties_with_payer_role[0]["roles"][0]
        )

    @pytestrail.case("27585")
    def test_procuring_entity_check_releases_0_parties_id_on_pp_ms_release_27585_140(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=f"{payload['tender']['procuringEntity']['identifier']['scheme']}-"
                            f"{payload['tender']['procuringEntity']['identifier']['id']}",
            actual_result=parties_with_procuring_entity_role[0]["id"]
        )

    @pytestrail.case("27585")
    def test_procuring_entity_check_releases_0_parties_name_on_pp_ms_release_27585_141(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=payload['tender']['procuringEntity']['name'],
            actual_result=parties_with_procuring_entity_role[0]["name"]
        )

    @pytestrail.case("27585")
    def test_procuring_entity_check_releases_0_parties_identifier_scheme_on_pp_ms_release_27585_142(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=payload['tender']['procuringEntity']['identifier']['scheme'],
            actual_result=parties_with_procuring_entity_role[0]['identifier']['scheme']
        )

    @pytestrail.case("27585")
    def test_procuring_entity_check_releases_0_parties_identifier_id_on_pp_ms_release_27585_143(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=payload['tender']['procuringEntity']['identifier']['id'],
            actual_result=parties_with_procuring_entity_role[0]['identifier']['id']
        )

    @pytestrail.case("27585")
    def test_procuring_entity_check_releases_0_parties_identifier_legal_name_on_pp_ms_release_27585_144(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=payload['tender']['procuringEntity']['identifier']['legalName'],
            actual_result=parties_with_procuring_entity_role[0]['identifier']['legalName']
        )

    @pytestrail.case("27585")
    def test_procuring_entity_check_releases_0_parties_address_street_address_on_pp_ms_release_27585_145(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=payload['tender']['procuringEntity']['address']['streetAddress'],
            actual_result=parties_with_procuring_entity_role[0]['address']['streetAddress']
        )

    @pytestrail.case("27585")
    def test_procuring_entity_check_releases_0_parties_address_address_details_country_id_on_pp_ms_release_27585_146(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=payload['tender']['procuringEntity']['address']['addressDetails']['country']['id'],
            actual_result=parties_with_procuring_entity_role[0]['address']['addressDetails']['country']['id']
        )

    @pytestrail.case("27585")
    def test_procuring_entity_check_releases_0_parties_address_address_details_country_scheme_on_pp_ms_27585_147(
            self, pmd, language, instance):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        mdm = MdmService(
            instance=instance,
            lang=language,
            procuring_address_details_country_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["country"]["id"],
            procuring_address_details_region_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["region"]["id"],
            procuring_address_details_locality_scheme=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["scheme"],
            procuring_address_details_locality_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["id"]
        )
        data = mdm.process_tender_data(pmd).json()
        country_from_mdm = data["data"]["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]
        assert compare_actual_result_and_expected_result(
            expected_result=country_from_mdm['scheme'],
            actual_result=parties_with_procuring_entity_role[0]['address']['addressDetails']['country']['scheme']
        )

    @pytestrail.case("27585")
    def test_procuring_entity_check_releases_0_parties_address_address_details_country_description_on_pp_ms_27585_148(
            self, pmd, language, instance):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        mdm = MdmService(
            instance=instance,
            lang=language,
            procuring_address_details_country_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["country"]["id"],
            procuring_address_details_region_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["region"]["id"],
            procuring_address_details_locality_scheme=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["scheme"],
            procuring_address_details_locality_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["id"]
        )
        data = mdm.process_tender_data(pmd).json()
        country_from_mdm = data["data"]["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]
        assert compare_actual_result_and_expected_result(
            expected_result=country_from_mdm['description'],
            actual_result=parties_with_procuring_entity_role[0]['address']['addressDetails']['country']['description']
        )

    @pytestrail.case("27585")
    def test_procuring_entity_check_releases_0_parties_address_address_details_country_uri_on_pp_ms_27585_149(
            self, pmd, language, instance):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        mdm = MdmService(
            instance=instance,
            lang=language,
            procuring_address_details_country_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["country"]["id"],
            procuring_address_details_region_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["region"]["id"],
            procuring_address_details_locality_scheme=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["scheme"],
            procuring_address_details_locality_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["id"]
        )
        data = mdm.process_tender_data(pmd).json()
        country_from_mdm = data["data"]["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]
        assert compare_actual_result_and_expected_result(
            expected_result=country_from_mdm['uri'],
            actual_result=parties_with_procuring_entity_role[0]['address']['addressDetails']['country']['uri']
        )

    @pytestrail.case("27585")
    def test_procuring_entity_check_releases_0_parties_address_address_details_region_uri_on_pp_ms_27585_150(
            self, pmd, language, instance):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        mdm = MdmService(
            instance=instance,
            lang=language,
            procuring_address_details_country_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["country"]["id"],
            procuring_address_details_region_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["region"]["id"],
            procuring_address_details_locality_scheme=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["scheme"],
            procuring_address_details_locality_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["id"]
        )
        data = mdm.process_tender_data(pmd).json()
        region_from_mdm = data["data"]["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]
        assert compare_actual_result_and_expected_result(
            expected_result=region_from_mdm['uri'],
            actual_result=parties_with_procuring_entity_role[0]['address']['addressDetails']['region']['uri']
        )

    @pytestrail.case("27585")
    def test_procuring_entity_check_releases_0_parties_address_address_details_region_id_on_pp_ms_27585_151(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"],
            actual_result=parties_with_procuring_entity_role[0]['address']['addressDetails']['region']['id']
        )

    @pytestrail.case("27585")
    def test_procuring_entity_check_releases_0_parties_address_address_details_region_scheme_on_pp_ms_27585_152(
            self, pmd, language, instance):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        mdm = MdmService(
            instance=instance,
            lang=language,
            procuring_address_details_country_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["country"]["id"],
            procuring_address_details_region_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["region"]["id"],
            procuring_address_details_locality_scheme=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["scheme"],
            procuring_address_details_locality_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["id"]
        )
        data = mdm.process_tender_data(pmd).json()
        region_from_mdm = data["data"]["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]
        assert compare_actual_result_and_expected_result(
            expected_result=region_from_mdm['scheme'],
            actual_result=parties_with_procuring_entity_role[0]['address']['addressDetails']['region']['scheme']
        )

    @pytestrail.case("27585")
    def test_procuring_entity_check_releases_0_parties_address_address_details_region_description_on_pp_ms_27585_153(
            self, pmd, language, instance):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        mdm = MdmService(
            instance=instance,
            lang=language,
            procuring_address_details_country_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["country"]["id"],
            procuring_address_details_region_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["region"]["id"],
            procuring_address_details_locality_scheme=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["scheme"],
            procuring_address_details_locality_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["id"]
        )
        data = mdm.process_tender_data(pmd).json()
        region_from_mdm = data["data"]["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]
        assert compare_actual_result_and_expected_result(
            expected_result=region_from_mdm['description'],
            actual_result=parties_with_procuring_entity_role[0]['address']['addressDetails']['region']['description']
        )

    @pytestrail.case("27585")
    def test_procuring_entity_check_releases_0_parties_address_address_details_locality_description_on_pp_ms_27585_154(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"][
                "description"],
            actual_result=parties_with_procuring_entity_role[0]['address']['addressDetails']['locality']['description']
        )

    @pytestrail.case("27585")
    def test_procuring_entity_check_releases_0_parties_address_address_details_locality_id_on_pp_ms_27585_155(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=payload['tender']['procuringEntity']['address']['addressDetails']['locality']['id'],
            actual_result=parties_with_procuring_entity_role[0]['address']['addressDetails']['locality']['id']
        )

    @pytestrail.case("27585")
    def test_procuring_entity_check_releases_0_parties_address_address_details_locality_scheme_on_pp_ms_27585_156(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=payload['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'],
            actual_result=parties_with_procuring_entity_role[0]['address']['addressDetails']['locality']['scheme']
        )

    @pytestrail.case("27585")
    def test_procuring_entity_check_releases_0_parties_address_address_details_locality_uri_on_pp_ms_27585_157(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        if "uri" in parties_with_procuring_entity_role[0]['address']['addressDetails']['locality']:
            check_locality_uri = True
        else:
            check_locality_uri = False
        assert compare_actual_result_and_expected_result(
            expected_result=str(False),
            actual_result=str(check_locality_uri)
        )

    @pytestrail.case("27585")
    def test_procuring_entity_check_releases_0_parties_contact_point_name_on_pp_ms_release_27585_158(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=payload['tender']['procuringEntity']['contactPoint']['name'],
            actual_result=parties_with_procuring_entity_role[0]['contactPoint']['name']
        )

    @pytestrail.case("27585")
    def test_procuring_entity_check_releases_0_parties_contact_point_email_on_pp_ms_release_27585_159(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=payload['tender']['procuringEntity']['contactPoint']['email'],
            actual_result=parties_with_procuring_entity_role[0]['contactPoint']['email']
        )

    @pytestrail.case("27585")
    def test_procuring_entity_check_releases_0_parties_contact_point_telephone_on_pp_ms_release_27585_160(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=payload['tender']['procuringEntity']['contactPoint']['telephone'],
            actual_result=parties_with_procuring_entity_role[0]['contactPoint']['telephone']
        )

    @pytestrail.case("27585")
    def test_procuring_entity_check_releases_0_parties_roles_0_on_pp_ms_release_27585_161(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result="procuringEntity",
            actual_result=parties_with_procuring_entity_role[0]['roles'][0]
        )

    @pytestrail.case("27585")
    def test_relationship_planning_check_releases_0_related_processes_id_on_pp_ms_release_27585_163(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_with_relationship_planning = list()
        for p in ms_release["releases"][0]["relatedProcesses"]:
            if p["relationship"] == ["planning"]:
                related_processes_with_relationship_planning.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(is_it_uuid(related_processes_with_relationship_planning[0]['id'], 1))
        )

    @pytestrail.case("27585")
    def test_relationship_planning_check_releases_0_related_processes_relationship_on_pp_ms_release_27585_164(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_with_relationship_planning = list()
        for p in ms_release["releases"][0]["relatedProcesses"]:
            if p["relationship"] == ["planning"]:
                related_processes_with_relationship_planning.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result="planning",
            actual_result=related_processes_with_relationship_planning[0]['relationship'][0]
        )

    @pytestrail.case("27585")
    def test_relationship_planning_check_releases_0_related_processes_scheme_on_pp_ms_release_27585_165(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_with_relationship_planning = list()
        for p in ms_release["releases"][0]["relatedProcesses"]:
            if p["relationship"] == ["planning"]:
                related_processes_with_relationship_planning.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result="ocid",
            actual_result=related_processes_with_relationship_planning[0]['scheme']
        )

    @pytestrail.case("27585")
    def test_relationship_planning_check_releases_0_related_processes_identifier_on_pp_ms_release_27585_166(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_with_relationship_planning = list()
        for p in ms_release["releases"][0]["relatedProcesses"]:
            if p["relationship"] == ["planning"]:
                related_processes_with_relationship_planning.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id'],
            actual_result=related_processes_with_relationship_planning[0]['identifier']
        )

    @pytestrail.case("27585")
    def test_relationship_planning_check_releases_0_related_processes_uri_on_pp_ms_release_27585_167(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_with_relationship_planning = list()
        for p in ms_release["releases"][0]["relatedProcesses"]:
            if p["relationship"] == ["planning"]:
                related_processes_with_relationship_planning.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=f"{CreatePn.message_from_kafka['data']['url']}/"
                            f"{CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']}",
            actual_result=related_processes_with_relationship_planning[0]['uri']
        )

    @pytestrail.case("27585")
    def test_relationship_x_expenditure_item_check_releases_0_related_processes_id_on_pp_ms_release_27585_169(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_with_relationship_x_expenditure_item = list()
        for p in ms_release["releases"][0]["relatedProcesses"]:
            if p["relationship"] == ["x_expenditureItem"]:
                related_processes_with_relationship_x_expenditure_item.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(is_it_uuid(related_processes_with_relationship_x_expenditure_item[0]['id'], 1))
        )

    @pytestrail.case("27585")
    def test_relationship_x_expenditure_item_check_releases_0_related_processes_relationship_on_pp_ms_release_27585_170(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_with_relationship_x_expenditure_item = list()
        for p in ms_release["releases"][0]["relatedProcesses"]:
            if p["relationship"] == ["x_expenditureItem"]:
                related_processes_with_relationship_x_expenditure_item.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result="x_expenditureItem",
            actual_result=related_processes_with_relationship_x_expenditure_item[0]['relationship'][0]
        )

    @pytestrail.case("27585")
    def test_relationship_x_expenditure_item_check_releases_0_related_processes_scheme_on_pp_ms_release_27585_171(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_with_relationship_x_expenditure_item = list()
        for p in ms_release["releases"][0]["relatedProcesses"]:
            if p["relationship"] == ["x_expenditureItem"]:
                related_processes_with_relationship_x_expenditure_item.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result="ocid",
            actual_result=related_processes_with_relationship_x_expenditure_item[0]['scheme']
        )

    @pytestrail.case("27585")
    def test_relationship_x_expenditure_item_check_releases_0_related_processes_identifier_on_pp_ms_release_27585_172(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_with_relationship_x_expenditure_item = list()
        for p in ms_release["releases"][0]["relatedProcesses"]:
            if p["relationship"] == ["x_expenditureItem"]:
                related_processes_with_relationship_x_expenditure_item.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=CreatePn.ei_id,
            actual_result=related_processes_with_relationship_x_expenditure_item[0]['identifier']
        )

    @pytestrail.case("27585")
    def test_relationship_x_expenditure_item_check_releases_0_related_processes_uri_on_pp_ms_release_27585_173(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_with_relationship_x_expenditure_item = list()
        for p in ms_release["releases"][0]["relatedProcesses"]:
            if p["relationship"] == ["x_expenditureItem"]:
                related_processes_with_relationship_x_expenditure_item.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=f"http://dev.public.eprocurement.systems/budgets/{CreatePn.ei_id}/{CreatePn.ei_id}",
            actual_result=related_processes_with_relationship_x_expenditure_item[0]['uri']
        )

    @pytestrail.case("27585")
    def test_relationship_x_funding_source_check_releases_0_related_processes_id_on_pp_ms_release_27585_175(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_with_relationship_x_funding_source = list()
        for p in ms_release["releases"][0]["relatedProcesses"]:
            if p["relationship"] == ["x_fundingSource"]:
                related_processes_with_relationship_x_funding_source.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(is_it_uuid(related_processes_with_relationship_x_funding_source[0]['id'], 1))
        )

    @pytestrail.case("27585")
    def test_relationship_x_funding_source_check_releases_0_related_processes_relationship_on_pp_ms_release_27585_176(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_with_relationship_x_funding_source = list()
        for p in ms_release["releases"][0]["relatedProcesses"]:
            if p["relationship"] == ["x_fundingSource"]:
                related_processes_with_relationship_x_funding_source.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result="x_fundingSource",
            actual_result=related_processes_with_relationship_x_funding_source[0]['relationship'][0]
        )

    @pytestrail.case("27585")
    def test_relationship_x_funding_source_check_releases_0_related_processes_scheme_on_pp_ms_release_27585_177(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_with_relationship_x_funding_source = list()
        for p in ms_release["releases"][0]["relatedProcesses"]:
            if p["relationship"] == ["x_fundingSource"]:
                related_processes_with_relationship_x_funding_source.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result="ocid",
            actual_result=related_processes_with_relationship_x_funding_source[0]['scheme']
        )

    @pytestrail.case("27585")
    def test_relationship_x_funding_source_check_releases_0_related_processes_identifier_on_pp_ms_release_27585_178(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_with_relationship_x_funding_source = list()
        for p in ms_release["releases"][0]["relatedProcesses"]:
            if p["relationship"] == ["x_fundingSource"]:
                related_processes_with_relationship_x_funding_source.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=CreatePn.fs_id,
            actual_result=related_processes_with_relationship_x_funding_source[0]['identifier']
        )

    @pytestrail.case("27585")
    def test_relationship_x_funding_source_check_releases_0_related_processes_uri_on_pp_ms_release_27585_179(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_with_relationship_x_funding_source = list()
        for p in ms_release["releases"][0]["relatedProcesses"]:
            if p["relationship"] == ["x_fundingSource"]:
                related_processes_with_relationship_x_funding_source.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=f"http://dev.public.eprocurement.systems/budgets/{CreatePn.ei_id}/{CreatePn.fs_id}",
            actual_result=related_processes_with_relationship_x_funding_source[0]['uri']
        )

    @pytestrail.case("27585")
    def test_check_on_the_platform_data_has_been_transferred_and_displayed_correctly_in_the_ms_release_27585_180(
            self, language, pmd):
        ei_id = CreatePn.ei_id
        message_from_kafka = CreatePn.message_from_kafka
        url_create_ms = message_from_kafka['data']['url'] + "/" + message_from_kafka['data']['ocid']
        payload = CreatePn.payload
        ms_release = requests.get(url=url_create_ms).json()
        related_processes_list_fs = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list_fs.append(d_1)
        fs_release = requests.get(url=related_processes_list_fs[0]["uri"]).json()
        related_processes_list_ei = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list_ei.append(d_1)
        ei_release = requests.get(url=related_processes_list_ei[0]["uri"]).json()
        mdm = MdmService(
            instance="dev",
            lang="ro",
            procuring_address_details_country_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["country"]["id"],
            procuring_address_details_region_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["region"]["id"],
            procuring_address_details_locality_scheme=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["scheme"],
            procuring_address_details_locality_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["id"]
        )
        data = mdm.process_tender_data(pmd).json()
        country_from_mdm = data["data"]["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]
        region_from_mdm = data["data"]["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]
        procurement_method_details_from_mdm = data["data"]["tender"]["procurementMethodDetails"]
        eligibility_criteria_from_mdm = data["data"]["tender"]["eligibilityCriteria"]
        parties_with_buyer_role_ei = list()
        for p in ei_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role_ei.append(p)
        parties_with_payer_role_fs = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role_fs.append(p)
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                raise Exception("Treasury money model was used -> BR-10.3.15")
        actual_result = ms_release
        expected_result = {
            "uri": f"http://dev.public.eprocurement.systems/tenders/"
                   f"{message_from_kafka['data']['ocid']}/{message_from_kafka['data']['ocid']}",
            "version": "1.1",
            "extensions": [
                "https://raw.githubusercontent.com/open-contracting/ocds_bid_extension/v1.1.1/extension.json",
                "https://raw.githubusercontent.com/open-contracting/ocds_enquiry_extension/v1.1.1/extension.js"],
            "publisher": {
                "name": "M-Tender",
                "uri": "https://www.mtender.gov.md"
            },
            "license": "http://opendefinition.org/licenses/",
            "publicationPolicy": "http://opendefinition.org/licenses/",
            "publishedDate": message_from_kafka['data']['operationDate'],
            "releases": [{
                "ocid": message_from_kafka['data']['ocid'],
                "id": f"{message_from_kafka['data']['ocid']}-"
                      f"{message_from_kafka['data']['outcomes']['pn'][0]['id'][32:45]}",
                "date": message_from_kafka['data']['operationDate'],
                "tag": ["compiled"],
                "language": language,
                "initiationType": "tender",
                "planning": {
                    "budget": {
                        "amount": {
                            "amount": payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["amount"],
                            "currency": payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["currency"]
                        },
                        "isEuropeanUnionFunded": fs_release['releases'][0]['planning']['budget'][
                            'isEuropeanUnionFunded'],
                        "budgetBreakdown": [{
                            "id": payload["planning"]["budget"]["budgetBreakdown"][0]['id'],
                            "amount": {
                                "amount": payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["amount"],
                                "currency": payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["currency"]
                            },
                            "period": {
                                "startDate": fs_release['releases'][0]['planning']['budget']['period']['startDate'],
                                "endDate": fs_release['releases'][0]['planning']['budget']['period']['endDate']
                            },
                            "sourceParty": {
                                "id": fs_release['releases'][0]['planning']['budget']['sourceEntity']['id'],
                                "name": fs_release['releases'][0]['planning']['budget']['sourceEntity']['name']
                            }
                        }]
                    }
                },
                "tender": {
                    "id": actual_result['releases'][0]['tender']['id'],
                    "title": payload['tender']['title'],
                    "description": payload['tender']['description'],
                    "status": "planning",
                    "statusDetails": "planning notice",
                    "value": {
                        "amount": payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["amount"],
                        "currency": payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["currency"]
                    },
                    "procurementMethod": "open",
                    "procurementMethodDetails": procurement_method_details_from_mdm,
                    "mainProcurementCategory": ei_release['releases'][0]['tender']['mainProcurementCategory'],
                    "hasEnquiries": False,
                    "eligibilityCriteria": eligibility_criteria_from_mdm,
                    "procuringEntity": {
                        "id": f"{payload['tender']['procuringEntity']['identifier']['scheme']}-"
                              f"{payload['tender']['procuringEntity']['identifier']['id']}",
                        "name": payload['tender']['procuringEntity']['name']
                    },
                    "acceleratedProcedure": {
                        "isAcceleratedProcedure": False
                    },
                    "classification": {
                        "scheme": ei_release['releases'][0]['tender']['classification']['scheme'],
                        "id": ei_release['releases'][0]['tender']['classification']['id'],
                        "description": ei_release['releases'][0]['tender']['classification']['description']
                    },
                    "designContest": {
                        "serviceContractAward": False
                    },
                    "electronicWorkflows": {
                        "useOrdering": False,
                        "usePayment": False,
                        "acceptInvoicing": False
                    },
                    "jointProcurement": {
                        "isJointProcurement": False
                    },
                    "legalBasis": payload['tender']['legalBasis'],
                    "procedureOutsourcing": {
                        "procedureOutsourced": False
                    },
                    "dynamicPurchasingSystem": {
                        "hasDynamicPurchasingSystem": False
                    },
                    "framework": {
                        "isAFramework": False
                    }
                },
                "parties": [{
                    "id": parties_with_buyer_role_ei[0]['id'],
                    "name": parties_with_buyer_role_ei[0]['name'],
                    "identifier": {
                        "scheme": parties_with_buyer_role_ei[0]['identifier']['scheme'],
                        "id": parties_with_buyer_role_ei[0]['identifier']['id'],
                        "legalName": parties_with_buyer_role_ei[0]['identifier']['legalName']
                    },
                    "address": {
                        "streetAddress": parties_with_buyer_role_ei[0]['address']['streetAddress'],
                        "addressDetails": {
                            "country": {
                                "scheme": parties_with_buyer_role_ei[0]['address']['addressDetails']['country'][
                                    'scheme'],
                                "id": parties_with_buyer_role_ei[0]['address']['addressDetails']['country']['id'],
                                "description": parties_with_buyer_role_ei[0]['address']['addressDetails']['country'][
                                    'description'],
                                "uri": parties_with_buyer_role_ei[0]['address']['addressDetails']['country']['uri']
                            },
                            "region": {
                                "scheme": parties_with_buyer_role_ei[0]['address']['addressDetails']['region'][
                                    'scheme'],
                                "id": parties_with_buyer_role_ei[0]['address']['addressDetails']['region']['id'],
                                "description": parties_with_buyer_role_ei[0]['address']['addressDetails']['region'][
                                    'description'],
                                "uri": parties_with_buyer_role_ei[0]['address']['addressDetails']['region']['uri']
                            },
                            "locality": {
                                "scheme": parties_with_buyer_role_ei[0]['address']['addressDetails']['locality'][
                                    'scheme'],
                                "id": parties_with_buyer_role_ei[0]['address']['addressDetails']['locality']['id'],
                                "description": parties_with_buyer_role_ei[0]['address']['addressDetails']['locality'][
                                    'description'],
                                "uri": parties_with_buyer_role_ei[0]['address']['addressDetails']['locality']['uri']
                            }
                        }
                    },
                    "contactPoint": {
                        "name": parties_with_buyer_role_ei[0]['contactPoint']['name'],
                        "email": parties_with_buyer_role_ei[0]['contactPoint']['email'],
                        "telephone": parties_with_buyer_role_ei[0]['contactPoint']['telephone']
                    },
                    "roles": ["buyer"]
                }, {
                    "id": parties_with_payer_role_fs[0]['id'],
                    "name": parties_with_payer_role_fs[0]['name'],
                    "identifier": {
                        "scheme": parties_with_payer_role_fs[0]['identifier']['scheme'],
                        "id": parties_with_payer_role_fs[0]['identifier']['id'],
                        "legalName": parties_with_payer_role_fs[0]['identifier']['legalName']

                    },
                    "address": {
                        "streetAddress": parties_with_payer_role_fs[0]['address']['streetAddress'],
                        "addressDetails": {
                            "country": {
                                "scheme": parties_with_payer_role_fs[0]['address']['addressDetails']['country'][
                                    'scheme'],
                                "id": parties_with_payer_role_fs[0]['address']['addressDetails']['country']['id'],
                                "description": parties_with_payer_role_fs[0]['address']['addressDetails']['country'][
                                    'description'],
                                "uri": parties_with_payer_role_fs[0]['address']['addressDetails']['country']['uri']
                            },
                            "region": {
                                "scheme": parties_with_payer_role_fs[0]['address']['addressDetails']['region'][
                                    'scheme'],
                                "id": parties_with_payer_role_fs[0]['address']['addressDetails']['region']['id'],
                                "description": parties_with_payer_role_fs[0]['address']['addressDetails']['region'][
                                    'description'],
                                "uri": parties_with_payer_role_fs[0]['address']['addressDetails']['region']['uri']
                            },
                            "locality": {
                                "scheme": parties_with_payer_role_fs[0]['address']['addressDetails']['locality'][
                                    'scheme'],
                                "id": parties_with_payer_role_fs[0]['address']['addressDetails']['locality']['id'],
                                "description": parties_with_payer_role_fs[0]['address']['addressDetails']['locality'][
                                    'description'],
                                "uri": parties_with_payer_role_fs[0]['address']['addressDetails']['locality']['uri']
                            }
                        }
                    },
                    "contactPoint": {
                        "name": parties_with_payer_role_fs[0]['contactPoint']['name'],
                        "email": parties_with_payer_role_fs[0]['contactPoint']['email'],
                        "telephone": parties_with_payer_role_fs[0]['contactPoint']['telephone']

                    },
                    "roles": ["payer"]
                }, {
                    "id": f"{payload['tender']['procuringEntity']['identifier']['scheme']}-"
                          f"{payload['tender']['procuringEntity']['identifier']['id']}",
                    "name": payload['tender']['procuringEntity']['name'],
                    "identifier": {
                        "scheme": payload['tender']['procuringEntity']['identifier']['scheme'],
                        "id": payload['tender']['procuringEntity']['identifier']['id'],
                        "legalName": payload['tender']['procuringEntity']['identifier']['legalName']
                    },
                    "address": {
                        "streetAddress": payload['tender']['procuringEntity']['address']['streetAddress'],
                        "addressDetails": {
                            "country": {
                                "scheme": country_from_mdm['scheme'],
                                "id": payload['tender']['procuringEntity']['address']['addressDetails']['country'][
                                    'id'],
                                "description": country_from_mdm['description'],
                                "uri": country_from_mdm['uri']
                            },
                            "region": {
                                "scheme": region_from_mdm['scheme'],
                                "id": payload['tender']['procuringEntity']['address']['addressDetails']['region']['id'],
                                "description": region_from_mdm['description'],
                                "uri": region_from_mdm['uri']
                            },
                            "locality": {
                                "scheme": payload['tender']['procuringEntity']['address']['addressDetails']['locality'][
                                    'scheme'],
                                "id": payload['tender']['procuringEntity']['address']['addressDetails']['locality'][
                                    'id'],
                                "description":
                                    payload['tender']['procuringEntity']['address']['addressDetails']['locality'][
                                        'description']
                            }
                        }
                    },
                    "contactPoint": {
                        "name": payload['tender']['procuringEntity']['contactPoint']['name'],
                        "email": payload['tender']['procuringEntity']['contactPoint']['email'],
                        "telephone": payload['tender']['procuringEntity']['contactPoint']['telephone']
                    },
                    "roles": ["procuringEntity"]
                }],
                "relatedProcesses": [{
                    "id": actual_result['releases'][0]['relatedProcesses'][0]['id'],
                    "relationship": ["planning"],
                    "scheme": "ocid",
                    "identifier": message_from_kafka['data']['outcomes']['pn'][0]['id'],
                    "uri": f"{message_from_kafka['data']['url']}/"
                           f"{message_from_kafka['data']['outcomes']['pn'][0]['id']}"
                }, {
                    "id": actual_result['releases'][0]['relatedProcesses'][1]['id'],
                    "relationship": ["x_expenditureItem"],
                    "scheme": "ocid",
                    "identifier": ei_id,
                    "uri": f"http://dev.public.eprocurement.systems/budgets/{ei_id}/{ei_id}"
                }, {
                    "id": actual_result['releases'][0]['relatedProcesses'][2]['id'],
                    "relationship": ["x_fundingSource"],
                    "scheme": "ocid",
                    "identifier": payload["planning"]["budget"]["budgetBreakdown"][0]['id'],
                    "uri": f"http://dev.public.eprocurement.systems/budgets/{ei_id}/"
                           f"{payload['planning']['budget']['budgetBreakdown'][0]['id']}"
                }]
            }]
        }
        compare_releases = DeepDiff(expected_result, actual_result)
        assert compare_actual_result_and_expected_result(
            expected_result={},
            actual_result=compare_releases
        )

    @pytestrail.case("27585")
    def test_check_on_the_platform_data_has_been_transferred_and_displayed_correctly_in_the_pn_release_27585_181(
            self, language, pmd):
        message_from_kafka = CreatePn.message_from_kafka
        url_create_ms = message_from_kafka['data']['url'] + "/" + message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create_ms).json()
        related_processes_list_ei = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list_ei.append(d_1)
        ei_release = requests.get(url=related_processes_list_ei[0]["uri"]).json()
        url_create_pn = message_from_kafka['data']['url'] + "/" + message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create_pn).json()
        payload = CreatePn.payload
        mdm = MdmService(
            instance="dev",
            lang="ro",
            procuring_address_details_country_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["country"]["id"],
            procuring_address_details_region_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["region"]["id"],
            procuring_address_details_locality_scheme=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["scheme"],
            procuring_address_details_locality_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["id"]
        )
        data = mdm.process_tender_data(pmd).json()
        submissionMethodDetails = data["data"]["tender"]["submissionMethodDetails"]
        submissionMethodRationale = data["data"]["tender"]["submissionMethodRationale"]
        actual_result = pn_release
        expected_result = {
            "uri": f"http://dev.public.eprocurement.systems/tenders/{message_from_kafka['data']['ocid']}/"
                   f"{message_from_kafka['data']['outcomes']['pn'][0]['id']}",
            "version": "1.1",
            "extensions": [
                "https://raw.githubusercontent.com/open-contracting/ocds_bid_extension/v1.1.1/extension.json",
                "https://raw.githubusercontent.com/open-contracting/ocds_enquiry_extension/v1.1.1/extension.js"],
            "publisher": {
                "name": "M-Tender",
                "uri": "https://www.mtender.gov.md"
            },
            "license": "http://opendefinition.org/licenses/",
            "publicationPolicy": "http://opendefinition.org/licenses/",
            "publishedDate": message_from_kafka['data']['operationDate'],
            "releases": [{
                "ocid": message_from_kafka['data']['outcomes']['pn'][0]['id'],
                "id": f"{message_from_kafka['data']['outcomes']['pn'][0]['id']}-"
                      f"{message_from_kafka['data']['outcomes']['pn'][0]['id'][32:45]}",
                "date": message_from_kafka['data']['operationDate'],
                "tag": ["planning"],
                "language": language,
                "initiationType": "tender",
                "tender": {
                    "id": actual_result['releases'][0]['tender']['id'],
                    "title": "Planning Notice",
                    "description": "Contracting process is planned",
                    "status": "planning",
                    "statusDetails": "planning",
                    "lotGroups": [{
                        "optionToCombine": False
                    }],
                    "tenderPeriod": {
                        "startDate": payload['tender']['tenderPeriod']['startDate']
                    },
                    "hasEnquiries": False,
                    "submissionMethod": ["electronicSubmission"],
                    "submissionMethodDetails": submissionMethodDetails,
                    "submissionMethodRationale": submissionMethodRationale,
                    "requiresElectronicCatalogue": False,
                    "classification": {
                        "scheme": "CPV",
                        "id": ei_release['releases'][0]['tender']['classification']['id'],
                        "description": ei_release['releases'][0]['tender']['classification']['description']
                    },
                    "value": {
                        "amount": payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["amount"],
                        "currency": payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["currency"]
                    }
                },
                "hasPreviousNotice": False,
                "purposeOfNotice": {
                    "isACallForCompetition": False
                },
                "relatedProcesses": [{
                    "id": actual_result['releases'][0]['relatedProcesses'][0]['id'],
                    "relationship": ["parent"],
                    "scheme": "ocid",
                    "identifier": message_from_kafka['data']['ocid'],
                    "uri": f"http://dev.public.eprocurement.systems/tenders/{message_from_kafka['data']['ocid']}/"
                           f"{message_from_kafka['data']['ocid']}"
                }]
            }]
        }
        compare_releases = DeepDiff(expected_result, actual_result)
        assert compare_actual_result_and_expected_result(
            expected_result={},
            actual_result=compare_releases
        )


class TestCheckThePossibilityOfPlanningNoticeCreationWithFullDataModel(object):
    @pytestrail.case("27588")
    def test_send_request_see_result_in_feed_point_27588_1(self, country, language, instance, cassandra_username,
                                                           cassandra_password, pmd):
        ei_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_pn_payload_full_data_model_with_documents)
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["scheme"] = "other"
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["id"] = "test_value_for_locality"
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["description"] = "desc"
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["uri"] = "www segodnya"
        pn = PN(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd
        )
        create_fs_response = pn.insert_fs_own_full_ei_full_with_items(
            cp_id=ei_id,
            ei_token=ei_token
        )
        pn.create_pn(fs_id=create_fs_response[1])
        pn.get_message_from_kafka()
        CreatePn.message_from_kafka = pn.get_message_from_kafka()
        CreatePn.payload = payload
        CreatePn.ei_id = ei_id
        CreatePn.fs_id = create_fs_response[1]
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(pn.check_on_that_message_is_successfully_create_pn())
        )

    @pytestrail.case("27588")
    def test_check_uri_on_pp_ms_release_27588_141(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=f"http://dev.public.eprocurement.systems/tenders/"
                            f"{CreatePn.message_from_kafka['data']['ocid']}/"
                            f"{CreatePn.message_from_kafka['data']['ocid']}",
            actual_result=ms_release["uri"]
        )

    @pytestrail.case("27588")
    def test_check_version_on_pp_ms_release_27588_142(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="1.1",
            actual_result=ms_release["version"]
        )

    @pytestrail.case("27588")
    def test_check_extensions_array_on_pp_ms_release_27588_143(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="https://raw.githubusercontent.com/open-contracting/ocds_enquiry_extension/v1.1.1/"
                            "extension.js",
            actual_result=ms_release["extensions"][0]
        )
        assert compare_actual_result_and_expected_result(
            expected_result="https://raw.githubusercontent.com/open-contracting/ocds_enquiry_extension/v1.1.1/"
                            "extension.js",
            actual_result=ms_release["extensions"][1]
        )

    @pytestrail.case("27588")
    def test_check_publisher_name_on_pp_ms_release_27588_144(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="M-Tender",
            actual_result=ms_release["publisher"]["name"]
        )

    @pytestrail.case("27588")
    def test_check_publisher_uri_on_pp_ms_release_27588_145(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="https://www.mtender.gov.md",
            actual_result=ms_release["publisher"]["uri"]
        )

    @pytestrail.case("27588")
    def test_check_publication_policy_on_pp_ms_release_27588_146(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="http://opendefinition.org/licenses/",
            actual_result=ms_release["publicationPolicy"]
        )

    @pytestrail.case("27588")
    def test_check_license_on_pp_ms_release_27588_147(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="http://opendefinition.org/licenses/",
            actual_result=ms_release["license"]
        )

    @pytestrail.case("27588")
    def test_check_published_date_on_pp_ms_release_27588_148(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=CreatePn.message_from_kafka["data"]["operationDate"],
            actual_result=ms_release["publishedDate"]
        )

    @pytestrail.case("27588")
    def test_check_releases_0_oc_id_on_pp_ms_release_27588_149(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=CreatePn.message_from_kafka['data']['ocid'],
            actual_result=ms_release['releases'][0]['ocid']
        )

    @pytestrail.case("27588")
    def test_check_releases_0_id_on_pp_ms_release_27588_150(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=CreatePn.message_from_kafka['data']['ocid'],
            actual_result=ms_release["releases"][0]["id"][0:28]

        )
        assert compare_actual_result_and_expected_result(
            expected_result=get_human_date_in_utc_format(int(ms_release["releases"][0]["id"][29:42]))[0],
            actual_result=ms_release["releases"][0]["date"]
        )

    @pytestrail.case("27588")
    def test_check_releases_0_date_on_pp_ms_release_27588_151(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=CreatePn.message_from_kafka['data']['operationDate'],
            actual_result=ms_release["releases"][0]["date"]
        )

    @pytestrail.case("27588")
    def test_check_releases_0_tag_0_on_pp_ms_release_27588_152(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="compiled",
            actual_result=ms_release["releases"][0]["tag"][0]
        )

    @pytestrail.case("27588")
    def test_check_releases_0_language_on_pp_ms_release_27588_153(self, language):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=language,
            actual_result=ms_release["releases"][0]["language"]
        )

    @pytestrail.case("27588")
    def test_check_releases_0_initiation_type_on_pp_ms_release_27588_154(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="tender",
            actual_result=ms_release["releases"][0]["initiationType"]
        )

    @pytestrail.case("27588")
    def test_check_releases_0_planning_budget_description_on_pp_ms_release_27588_155(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        assert compare_actual_result_and_expected_result(
            expected_result=payload['planning']['budget']['description'],
            actual_result=ms_release['releases'][0]['planning']['budget']['description']
        )

    @pytestrail.case("27588")
    def test_check_releases_0_planning_budget_amount_amount_on_pp_ms_release_27588_156(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(CreatePn.payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["amount"]),
            actual_result=str(ms_release["releases"][0]["planning"]["budget"]["amount"]["amount"])
        )

    @pytestrail.case("27588")
    def test_check_releases_0_planning_budget_amount_currency_on_pp_ms_release_27588_157(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(CreatePn.payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["currency"]),
            actual_result=str(ms_release["releases"][0]["planning"]["budget"]["amount"]["currency"])
        )

    @pytestrail.case("27588")
    def test_check_releases_0_planning_budget_is_european_union_funded_on_pp_ms_release_27588_158(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release["releases"][0]["planning"]["budget"]["isEuropeanUnionFunded"],
            actual_result=ms_release["releases"][0]["planning"]["budget"]["isEuropeanUnionFunded"]
        )

    @pytestrail.case("27588")
    def test_check_releases_0_planning_budget_breakdown_0_id_on_pp_ms_release_27588_159(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        assert compare_actual_result_and_expected_result(
            expected_result=payload['planning']['budget']['budgetBreakdown'][0]['id'],
            actual_result=ms_release["releases"][0]["planning"]["budget"]['budgetBreakdown'][0]['id']
        )

    @pytestrail.case("27588")
    def test_check_releases_0_planning_budget_breakdown_0_description_on_pp_ms_release_27588_160(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release['releases'][0]['planning']['budget']['description'],
            actual_result=ms_release['releases'][0]['planning']['budget']['budgetBreakdown'][0]['description']
        )

    @pytestrail.case("27588")
    def test_check_releases_0_planning_budget_budget_breakdown_0_amount_amount_on_pp_ms_release_27588_161(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(CreatePn.payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["amount"]),
            actual_result=str(ms_release["releases"][0]["planning"]["budget"]["budgetBreakdown"][0]["amount"]["amount"])
        )

    @pytestrail.case("27588")
    def test_check_releases_0_planning_budget_budget_breakdown_0_amount_currency_on_pp_ms_release_27588_162(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(CreatePn.payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["currency"]),
            actual_result=str(
                ms_release["releases"][0]["planning"]["budget"]["budgetBreakdown"][0]["amount"]["currency"])
        )

    @pytestrail.case("27588")
    def test_check_releases_0_planning_budget_budget_breakdown_0_period_start_date_on_pp_ms_release_27588_163(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release["releases"][0]["planning"]["budget"]["period"]["startDate"],
            actual_result=ms_release["releases"][0]["planning"]["budget"]["budgetBreakdown"][0]["period"]["startDate"]

        )

    @pytestrail.case("27588")
    def test_check_releases_0_planning_budget_budget_breakdown_0_period_end_date_on_pp_ms_release_27588_164(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release["releases"][0]["planning"]["budget"]["period"]["endDate"],
            actual_result=ms_release["releases"][0]["planning"]["budget"]["budgetBreakdown"][0]["period"]["endDate"]

        )

    @pytestrail.case("27588")
    def test_check_releases_0_planning_budget_budget_breakdown_0_source_party_id_on_pp_ms_release_27588_165(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release["releases"][0]["planning"]["budget"]["sourceEntity"]["id"],
            actual_result=ms_release["releases"][0]["planning"]["budget"]["budgetBreakdown"][0]["sourceParty"]["id"]

        )

    @pytestrail.case("27588")
    def test_check_releases_0_planning_budget_budget_breakdown_0_source_party_name_on_pp_ms_release_27588_166(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release["releases"][0]["planning"]["budget"]["sourceEntity"]["name"],
            actual_result=ms_release["releases"][0]["planning"]["budget"]["budgetBreakdown"][0]["sourceParty"]["name"]
        )

    @pytestrail.case("27588")
    def test_check_budget_breakdown_0_european_union_funding_project_identifier_on_pp_ms_release_27588_167(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release["releases"][0]["planning"]["budget"]["europeanUnionFunding"][
                "projectIdentifier"],
            actual_result=ms_release["releases"][0]["planning"]["budget"]["budgetBreakdown"][0]["europeanUnionFunding"][
                "projectIdentifier"]
        )

    @pytestrail.case("27588")
    def test_check_budget_breakdown_0_european_union_funding_project_name_on_pp_ms_release_27588_168(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release["releases"][0]["planning"]["budget"]["europeanUnionFunding"][
                "projectName"],
            actual_result=ms_release["releases"][0]["planning"]["budget"]["budgetBreakdown"][0]["europeanUnionFunding"][
                "projectName"]
        )

    @pytestrail.case("27588")
    def test_check_budget_breakdown_0_european_union_funding_uri_on_pp_ms_release_27588_169(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        assert compare_actual_result_and_expected_result(
            expected_result=fs_release["releases"][0]["planning"]["budget"]["europeanUnionFunding"][
                "uri"],
            actual_result=ms_release["releases"][0]["planning"]["budget"]["budgetBreakdown"][0]["europeanUnionFunding"][
                "uri"]
        )

    @pytestrail.case("27588")
    def test_check_releases_0_planning_rationale_on_pp_ms_release_27588_170(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["rationale"],
            actual_result=ms_release["releases"][0]["planning"]["rationale"]
        )

    @pytestrail.case("27588")
    def test_check_releases_0_tender_id_on_pp_ms_release_27588_171(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(is_it_uuid(ms_release["releases"][0]["tender"]["id"], 4))
        )

    @pytestrail.case("27588")
    def test_check_releases_0_tender_title_on_pp_ms_release_27588_172(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["title"],
            actual_result=ms_release["releases"][0]["tender"]["title"]
        )

    @pytestrail.case("27588")
    def test_check_releases_0_tender_description_on_pp_ms_release_27588_173(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["description"],
            actual_result=ms_release["releases"][0]["tender"]["description"]
        )

    @pytestrail.case("27588")
    def test_check_releases_0_tender_status_on_pp_ms_release_27588_174(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="planning",
            actual_result=ms_release["releases"][0]["tender"]["status"]
        )

    @pytestrail.case("27588")
    def test_check_releases_0_tender_status_details_on_pp_ms_release_27588_175(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="planning notice",
            actual_result=ms_release["releases"][0]["tender"]["statusDetails"]
        )

    @pytestrail.case("27588")
    def test_check_releases_0_tender_value_amount_on_pp_ms_release_27588_176(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        assert compare_actual_result_and_expected_result(
            expected_result=str(
                payload["tender"]["lots"][0]["value"]["amount"] + payload["tender"]["lots"][1]["value"]["amount"]),
            actual_result=str(ms_release["releases"][0]["tender"]["value"]["amount"])
        )

    @pytestrail.case("27588")
    def test_check_releases_0_tender_value_currency_on_pp_ms_release_27588_177(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["lots"][0]["value"]["currency"],
            actual_result=ms_release["releases"][0]["tender"]["value"]["currency"]
        )

    @pytestrail.case("27588")
    def test_check_releases_0_tender_procurement_method_on_pp_ms_release_27588_178(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="open",
            actual_result=ms_release["releases"][0]["tender"]["procurementMethod"]
        )

    @pytestrail.case("27588")
    def test_check_releases_0_tender_procurement_method_details_on_pp_ms_release_27588_179(self, pmd):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        mdm = MdmService(
            instance="dev",
            lang="ro",
            procuring_address_details_country_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["country"]["id"],
            procuring_address_details_region_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["region"]["id"],
            procuring_address_details_locality_scheme=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["scheme"],
            procuring_address_details_locality_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["id"]
        )
        data = mdm.process_tender_data(pmd).json()
        procurement_method_details_from_mdm = data["data"]["tender"]["procurementMethodDetails"]
        assert compare_actual_result_and_expected_result(
            expected_result=procurement_method_details_from_mdm,
            actual_result=ms_release["releases"][0]["tender"]["procurementMethodDetails"]
        )

    @pytestrail.case("27588")
    def test_check_releases_0_tender_procurement_method_rationale_on_pp_ms_release_27588_180(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload

        assert compare_actual_result_and_expected_result(
            expected_result=payload['tender']['procurementMethodRationale'],
            actual_result=ms_release["releases"][0]["tender"]["procurementMethodRationale"]
        )

    @pytestrail.case("27588")
    def test_check_releases_0_tender_main_procurement_category_on_pp_ms_release_27588_181(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        # Should get 'mainProcurementCategory' from related EI -> VR-10.5.8
        pn_record = requests.get(url=CreatePn.message_from_kafka['data']['url']).json()["records"]
        related_processes_list = list()
        for d in pn_record:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        procurement_method_details_from_ei_release = ei_release["releases"][0]["tender"]["mainProcurementCategory"]
        assert compare_actual_result_and_expected_result(
            expected_result=procurement_method_details_from_ei_release,
            actual_result=ms_release["releases"][0]["tender"]["mainProcurementCategory"]
        )

    @pytestrail.case("27588")
    def test_check_releases_0_tender_has_enquiries_on_pp_ms_release_27588_182(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(False),
            actual_result=str(ms_release["releases"][0]["tender"]["hasEnquiries"])
        )

    @pytestrail.case("27588")
    def test_check_releases_0_tender_eligibility_criteria_on_pp_ms_release_27588_183(self, pmd):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        mdm = MdmService(
            instance="dev",
            lang="ro",
            procuring_address_details_country_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["country"]["id"],
            procuring_address_details_region_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["region"]["id"],
            procuring_address_details_locality_scheme=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["scheme"],
            procuring_address_details_locality_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["id"]
        )
        data = mdm.process_tender_data(pmd).json()
        eligibility_criteria_from_mdm = data["data"]["tender"]["eligibilityCriteria"]
        assert compare_actual_result_and_expected_result(
            expected_result=eligibility_criteria_from_mdm,
            actual_result=ms_release["releases"][0]["tender"]["eligibilityCriteria"]
        )

    @pytestrail.case("27588")
    def test_check_releases_0_tender_contract_start_date_on_pp_ms_release_27588_184(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        if payload['tender']['lots'][0]['contractPeriod']['startDate'] <= \
                payload['tender']['lots'][1]['contractPeriod']['startDate']:
            start_date = payload['tender']['lots'][0]['contractPeriod']['startDate']
        elif payload['tender']['lots'][0]['contractPeriod']['startDate'] >= \
                payload['tender']['lots'][1]['contractPeriod']['startDate']:
            start_date = payload['tender']['lots'][1]['contractPeriod']['startDate']
        else:
            raise Exception("Can not get startDate for tender.contractPeriod")
        assert compare_actual_result_and_expected_result(
            expected_result=start_date,
            actual_result=ms_release["releases"][0]["tender"]["contractPeriod"]['startDate']
        )

    @pytestrail.case("27588")
    def test_check_releases_0_tender_contract_end_date_on_pp_ms_release_27588_185(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        if payload['tender']['lots'][0]['contractPeriod']['endDate'] <= \
                payload['tender']['lots'][1]['contractPeriod']['endDate']:
            end_date = payload['tender']['lots'][1]['contractPeriod']['endDate']
        elif payload['tender']['lots'][0]['contractPeriod']['endDate'] >= \
                payload['tender']['lots'][1]['contractPeriod']['endDate']:
            end_date = payload['tender']['lots'][0]['contractPeriod']['endDate']
        else:
            raise Exception("Can not get endDate for tender.contractPeriod")
        assert compare_actual_result_and_expected_result(
            expected_result=end_date,
            actual_result=ms_release["releases"][0]["tender"]["contractPeriod"]['endDate']
        )

    @pytestrail.case("27588")
    def test_check_releases_0_tender_procuring_entity_id_on_pp_ms_release_27588_186(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        assert compare_actual_result_and_expected_result(
            expected_result=f"{payload['tender']['procuringEntity']['identifier']['scheme']}-"
                            f"{payload['tender']['procuringEntity']['identifier']['id']}",
            actual_result=ms_release["releases"][0]["tender"]["procuringEntity"]["id"]
        )

    @pytestrail.case("27588")
    def test_check_releases_0_tender_procuring_entity_id_on_pp_ms_release_27588_187(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        assert compare_actual_result_and_expected_result(
            expected_result=payload['tender']['procuringEntity']['name'],
            actual_result=ms_release["releases"][0]["tender"]["procuringEntity"]["name"]
        )

    @pytestrail.case("27588")
    def test_check_releases_0_tender_accelerated_procedure_is_accelerated_procedure_on_pp_ms_release_27588_188(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(False),
            actual_result=str(ms_release["releases"][0]["tender"]["acceleratedProcedure"]["isAcceleratedProcedure"])
        )

    @pytestrail.case("27588")
    def test_check_releases_0_tender_classification_id_on_pp_ms_release_27588_189(self, language):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        classification_first_item = payload['tender']['items'][0]['classification']['id']
        classification_second_item = payload['tender']['items'][1]['classification']['id']
        make_tender_classification_id = get_new_classification_id(classification_first_item, classification_second_item)
        get_value_by_classification_id = get_value_from_classification_cpv_dictionary_xls(
            cpv=make_tender_classification_id,
            language=language.upper()
        )
        assert compare_actual_result_and_expected_result(
            expected_result=get_value_by_classification_id[0],
            actual_result=ms_release["releases"][0]["tender"]["classification"]["id"]
        )

    @pytestrail.case("27588")
    def test_check_releases_0_tender_classification_scheme_on_pp_ms_release_27588_190(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="CPV",
            actual_result=ms_release["releases"][0]["tender"]["classification"]["scheme"]
        )

    @pytestrail.case("27588")
    def test_check_releases_0_tender_classification_description_on_pp_ms_release_27588_191(self, language):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        classification_first_item = payload['tender']['items'][0]['classification']['id']
        classification_second_item = payload['tender']['items'][1]['classification']['id']
        make_tender_classification_id = get_new_classification_id(classification_first_item, classification_second_item)
        get_value_by_classification_id = get_value_from_classification_cpv_dictionary_xls(
            cpv=make_tender_classification_id,
            language=language.upper()
        )
        assert compare_actual_result_and_expected_result(
            expected_result=get_value_by_classification_id[1],
            actual_result=ms_release["releases"][0]["tender"]["classification"]["description"]
        )

    @pytestrail.case("27588")
    def test_check_releases_0_tender_design_contest_service_contract_award_on_pp_ms_release_27588_192(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(False),
            actual_result=str(ms_release["releases"][0]["tender"]["designContest"]["serviceContractAward"])
        )

    @pytestrail.case("27588")
    def test_check_releases_0_tender_electronic_workflows_use_ordering_on_pp_ms_release_27588_193(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(False),
            actual_result=str(ms_release["releases"][0]["tender"]["electronicWorkflows"]["useOrdering"])
        )

    @pytestrail.case("27588")
    def test_check_releases_0_tender_electronic_workflows_use_payment_on_pp_ms_release_27588_194(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(False),
            actual_result=str(ms_release["releases"][0]["tender"]["electronicWorkflows"]["usePayment"])
        )

    @pytestrail.case("27588")
    def test_check_releases_0_tender_electronic_workflows_accept_invoicing_on_pp_ms_release_27588_195(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(False),
            actual_result=str(ms_release["releases"][0]["tender"]["electronicWorkflows"]["acceptInvoicing"])
        )

    @pytestrail.case("27588")
    def test_check_releases_0_tender_joint_procurement_is_joint_procurement_on_pp_ms_release_27588_196(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(False),
            actual_result=str(ms_release["releases"][0]["tender"]["jointProcurement"]["isJointProcurement"])
        )

    @pytestrail.case("27588")
    def test_check_releases_0_tender_legal_basis_on_pp_ms_release_27588_197(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["legalBasis"],
            actual_result=ms_release["releases"][0]["tender"]["legalBasis"]
        )

    @pytestrail.case("27588")
    def test_check_releases_0_tender_procedure_outsourcing_procedure_outsourced_on_pp_ms_release_27588_198(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(False),
            actual_result=str(ms_release["releases"][0]["tender"]["procedureOutsourcing"]["procedureOutsourced"])
        )

    @pytestrail.case("27588")
    def test_check_releases_0_tender_procurement_method_aditional_info_on_pp_ms_release_27588_199(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        assert compare_actual_result_and_expected_result(
            expected_result=payload['tender']['procurementMethodAdditionalInfo'],
            actual_result=ms_release["releases"][0]["tender"]['procurementMethodAdditionalInfo']
        )

    @pytestrail.case("27588")
    def test_check_releases_0_tender_dynamic_purchasing_system_has_dynamic_purchasing_system_on_pp_ms__27588_200(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(False),
            actual_result=str(
                ms_release["releases"][0]["tender"]["dynamicPurchasingSystem"]["hasDynamicPurchasingSystem"])
        )

    @pytestrail.case("27588")
    def test_check_releases_0_tender_framework_is_a_framework_on_pp_ms_release_27588_201(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(False),
            actual_result=str(
                ms_release["releases"][0]["tender"]["framework"]["isAFramework"])
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_id_on_pp_ms_release_27588_203(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["id"],
            actual_result=parties_with_buyer_role[0]["id"]
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_name_on_pp_ms_release_27588_204(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["name"],
            actual_result=parties_with_buyer_role[0]["name"]
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_identifier_id_on_pp_ms_release_27588_205(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["identifier"]["id"],
            actual_result=parties_with_buyer_role[0]["identifier"]["id"]
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_identifier_scheme_on_pp_ms_release_27588_206(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["identifier"]["scheme"],
            actual_result=parties_with_buyer_role[0]["identifier"]["scheme"]
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_identifier_legal_name_on_pp_ms_release_27588_207(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["identifier"]["legalName"],
            actual_result=parties_with_buyer_role[0]["identifier"]["legalName"]
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_identifier_uri_on_pp_ms_release_27588_208(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["identifier"]["uri"],
            actual_result=parties_with_buyer_role[0]["identifier"]["uri"]
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_address_street_address_on_pp_ms_release_27588_209(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["address"]["streetAddress"],
            actual_result=parties_with_buyer_role[0]["address"]["streetAddress"]
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_address_postal_code_on_pp_ms_release_27588_210(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["address"]["postalCode"],
            actual_result=parties_with_buyer_role[0]["address"]["postalCode"]
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_address_address_detail_country_id_on_pp_ms_release_27588_211(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["id"],
            actual_result=parties_with_buyer_role[0]["address"]["addressDetails"]["country"]["id"]
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_address_address_detail_country_scheme_on_pp_ms_release_27588_212(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["scheme"],
            actual_result=parties_with_buyer_role[0]["address"]["addressDetails"]["country"]["scheme"]
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_address_address_detail_country_description_on_pp_ms_release_27588_213(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"][
                "description"],
            actual_result=parties_with_buyer_role[0]["address"]["addressDetails"]["country"]["description"]
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_address_address_detail_country_uri_on_pp_ms_release_27588_214(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["uri"],
            actual_result=parties_with_buyer_role[0]["address"]["addressDetails"]["country"]["uri"]
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_address_address_detail_region_id_on_pp_ms_release_27588_215(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["id"],
            actual_result=parties_with_buyer_role[0]["address"]["addressDetails"]["region"]["id"]
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_address_address_detail_region_scheme_on_pp_ms_release_27588_216(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["scheme"],
            actual_result=parties_with_buyer_role[0]["address"]["addressDetails"]["region"]["scheme"]
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_address_address_detail_region_description_on_pp_ms_release_27588_217(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"][
                "description"],
            actual_result=parties_with_buyer_role[0]["address"]["addressDetails"]["region"]["description"]
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_address_address_detail_region_uri_on_pp_ms_release_27588_218(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["uri"],
            actual_result=parties_with_buyer_role[0]["address"]["addressDetails"]["region"]["uri"]
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_address_address_detail_locality_id_on_pp_ms_release_27588_219(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["id"],
            actual_result=parties_with_buyer_role[0]["address"]["addressDetails"]["locality"]["id"]
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_address_address_detail_locality_scheme_on_pp_ms_release_27588_220(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["scheme"],
            actual_result=parties_with_buyer_role[0]["address"]["addressDetails"]["locality"]["scheme"]
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_address_address_detail_locality_description_on_pp_ms_release_27588_221(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
                "description"],
            actual_result=parties_with_buyer_role[0]["address"]["addressDetails"]["locality"]["description"]
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_address_address_detail_locality_uri_on_pp_ms_release_27588_222(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["uri"],
            actual_result=parties_with_buyer_role[0]["address"]["addressDetails"]["locality"]["uri"]
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_additional_identifiers_0_scheme_on_pp_ms_release_27588_223(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["additionalIdentifiers"][0]['scheme'],
            actual_result=parties_with_buyer_role[0]["additionalIdentifiers"][0]['scheme']
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_additional_identifiers_0_id_on_pp_ms_release_27588_224(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["additionalIdentifiers"][0]['id'],
            actual_result=parties_with_buyer_role[0]["additionalIdentifiers"][0]['id']
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_additional_identifiers_0_legal_name_on_pp_ms_release_27588_225(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["additionalIdentifiers"][0]['legalName'],
            actual_result=parties_with_buyer_role[0]["additionalIdentifiers"][0]['legalName']
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_additional_identifiers_0_uri_on_pp_ms_release_27588_226(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["additionalIdentifiers"][0]['uri'],
            actual_result=parties_with_buyer_role[0]["additionalIdentifiers"][0]['uri']
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_contact_point_name_on_pp_on_pp_ms_release_27588_227(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["contactPoint"]["name"],
            actual_result=parties_with_buyer_role[0]["contactPoint"]["name"]
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_contact_point_email_on_pp_on_pp_ms_release_27588_228(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["contactPoint"]["email"],
            actual_result=parties_with_buyer_role[0]["contactPoint"]["email"]
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_contact_point_telephone_on_pp_on_pp_ms_release_27588_229(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["contactPoint"]["telephone"],
            actual_result=parties_with_buyer_role[0]["contactPoint"]["telephone"]
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_contact_point_fax_number_on_pp_on_pp_ms_release_27588_230(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["contactPoint"]["faxNumber"],
            actual_result=parties_with_buyer_role[0]["contactPoint"]["faxNumber"]
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_contact_point_url_on_pp_on_pp_ms_release_27588_231(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["contactPoint"]["url"],
            actual_result=parties_with_buyer_role[0]["contactPoint"]["url"]
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_details_type_of_buyer_on_pp_on_pp_ms_release_27588_232(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["details"]["typeOfBuyer"],
            actual_result=parties_with_buyer_role[0]["details"]["typeOfBuyer"]
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_details_main_general_activity_on_pp_on_pp_ms_release_27588_233(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["details"]["mainGeneralActivity"],
            actual_result=parties_with_buyer_role[0]["details"]["mainGeneralActivity"]
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_details_main_sectoral_activity_on_pp_on_pp_ms_release_27588_234(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["details"]["mainSectoralActivity"],
            actual_result=parties_with_buyer_role[0]["details"]["mainSectoralActivity"]
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_roles_on_pp_ms_release_27588_235(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list.append(d_1)
        ei_release = requests.get(url=related_processes_list[0]["uri"]).json()
        parties_with_buyer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=ei_release["releases"][0]["parties"][0]["roles"][0],
            actual_result=parties_with_buyer_role[0]["roles"][0]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_id_on_pp_ms_release_27588_237(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_payer_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                fs_parties_with_payer_role.append(p)
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_payer_role[0]["id"],
            actual_result=parties_with_payer_role[0]["id"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_name_on_pp_ms_release_27588_238(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_payer_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                fs_parties_with_payer_role.append(p)
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_payer_role[0]["name"],
            actual_result=parties_with_payer_role[0]["name"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_identifier_id_on_pp_ms_release_27588_239(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_payer_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                fs_parties_with_payer_role.append(p)
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_payer_role[0]["identifier"]["id"],
            actual_result=parties_with_payer_role[0]["identifier"]["id"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_identifier_scheme_on_pp_ms_release_27588_240(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_payer_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                fs_parties_with_payer_role.append(p)
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_payer_role[0]["identifier"]["scheme"],
            actual_result=parties_with_payer_role[0]["identifier"]["scheme"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_identifier_legal_name_on_pp_ms_release_27588_241(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_payer_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                fs_parties_with_payer_role.append(p)
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_payer_role[0]["identifier"]["legalName"],
            actual_result=parties_with_payer_role[0]["identifier"]["legalName"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_identifier_uri_on_pp_ms_release_27588_242(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_payer_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                fs_parties_with_payer_role.append(p)
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_payer_role[0]["identifier"]["uri"],
            actual_result=parties_with_payer_role[0]["identifier"]["uri"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_address_street_address_on_pp_ms_release_27588_243(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_payer_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                fs_parties_with_payer_role.append(p)
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_payer_role[0]["address"]["streetAddress"],
            actual_result=parties_with_payer_role[0]["address"]["streetAddress"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_address_postal_code_on_pp_ms_release_27588_244(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_payer_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                fs_parties_with_payer_role.append(p)
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_payer_role[0]["address"]["postalCode"],
            actual_result=parties_with_payer_role[0]["address"]["postalCode"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_address_address_details_country_id_on_pp_ms_release_27588_245(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_payer_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                fs_parties_with_payer_role.append(p)
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_payer_role[0]["address"]["addressDetails"]["country"]["id"],
            actual_result=parties_with_payer_role[0]["address"]["addressDetails"]["country"]["id"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_address_address_details_country_scheme_on_pp_ms_release_27588_246(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_payer_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                fs_parties_with_payer_role.append(p)
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_payer_role[0]["address"]["addressDetails"]["country"]["scheme"],
            actual_result=parties_with_payer_role[0]["address"]["addressDetails"]["country"]["scheme"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_address_address_details_country_description_on_pp_ms_release_27588_247(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_payer_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                fs_parties_with_payer_role.append(p)
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_payer_role[0]["address"]["addressDetails"]["country"]["description"],
            actual_result=parties_with_payer_role[0]["address"]["addressDetails"]["country"]["description"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_address_address_details_country_uri_on_pp_ms_release_27588_248(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_payer_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                fs_parties_with_payer_role.append(p)
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_payer_role[0]["address"]["addressDetails"]["country"]["uri"],
            actual_result=parties_with_payer_role[0]["address"]["addressDetails"]["country"]["uri"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_address_address_details_region_id_on_pp_ms_release_27588_249(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_payer_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                fs_parties_with_payer_role.append(p)
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_payer_role[0]["address"]["addressDetails"]["region"]["id"],
            actual_result=parties_with_payer_role[0]["address"]["addressDetails"]["region"]["id"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_address_address_details_region_scheme_on_pp_ms_release_27588_250(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_payer_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                fs_parties_with_payer_role.append(p)
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_payer_role[0]["address"]["addressDetails"]["region"]["scheme"],
            actual_result=parties_with_payer_role[0]["address"]["addressDetails"]["region"]["scheme"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_address_address_details_region_description_on_pp_ms_release_27588_251(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_payer_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                fs_parties_with_payer_role.append(p)
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_payer_role[0]["address"]["addressDetails"]["region"][
                "description"],
            actual_result=parties_with_payer_role[0]["address"]["addressDetails"]["region"]["description"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_address_address_details_region_uri_on_pp_ms_release_27588_252(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_payer_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                fs_parties_with_payer_role.append(p)
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_payer_role[0]["address"]["addressDetails"]["region"]["uri"],
            actual_result=parties_with_payer_role[0]["address"]["addressDetails"]["region"]["uri"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_address_address_details_locality_uri_on_pp_ms_release_27588_253(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_payer_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                fs_parties_with_payer_role.append(p)
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_payer_role[0]["address"]["addressDetails"]["locality"]["uri"],
            actual_result=parties_with_payer_role[0]["address"]["addressDetails"]["locality"]["uri"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_address_address_details_locality_id_on_pp_ms_release_27588_254(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_payer_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                fs_parties_with_payer_role.append(p)
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_payer_role[0]["address"]["addressDetails"]["locality"]["id"],
            actual_result=parties_with_payer_role[0]["address"]["addressDetails"]["locality"]["id"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_address_address_details_locality_description_on_pp_ms_release_27588_255(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_payer_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                fs_parties_with_payer_role.append(p)
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_payer_role[0]["address"]["addressDetails"]["locality"][
                "description"],
            actual_result=parties_with_payer_role[0]["address"]["addressDetails"]["locality"]["description"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_address_address_details_locality_scheme_on_pp_ms_release_27588_256(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_payer_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                fs_parties_with_payer_role.append(p)
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_payer_role[0]["address"]["addressDetails"]["locality"][
                "scheme"],
            actual_result=parties_with_payer_role[0]["address"]["addressDetails"]["locality"]["scheme"]
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_additional_identifiers_0_scheme_on_pp_ms_release_27588_257(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_payer_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                fs_parties_with_payer_role.append(p)
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_payer_role[0]["additionalIdentifiers"][0]['scheme'],
            actual_result=parties_with_payer_role[0]["additionalIdentifiers"][0]['scheme']
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_additional_identifiers_0_id_on_pp_ms_release_27588_258(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_payer_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                fs_parties_with_payer_role.append(p)
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_payer_role[0]["additionalIdentifiers"][0]['id'],
            actual_result=parties_with_payer_role[0]["additionalIdentifiers"][0]['id']
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_additional_identifiers_0_legal_name_on_pp_ms_release_27588_259(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_payer_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                fs_parties_with_payer_role.append(p)
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_payer_role[0]["additionalIdentifiers"][0]['legalName'],
            actual_result=parties_with_payer_role[0]["additionalIdentifiers"][0]['legalName']
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_additional_identifiers_0_uri_on_pp_ms_release_27588_260(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_payer_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                fs_parties_with_payer_role.append(p)
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_payer_role[0]["additionalIdentifiers"][0]['uri'],
            actual_result=parties_with_payer_role[0]["additionalIdentifiers"][0]['uri']
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_contact_point_name_on_pp_ms_release_27588_261(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_payer_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                fs_parties_with_payer_role.append(p)
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_payer_role[0]["contactPoint"]["name"],
            actual_result=parties_with_payer_role[0]["contactPoint"]["name"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_contact_point_email_on_pp_ms_release_27588_262(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_payer_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                fs_parties_with_payer_role.append(p)
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_payer_role[0]["contactPoint"]["email"],
            actual_result=parties_with_payer_role[0]["contactPoint"]["email"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_contact_point_telephone_on_pp_ms_release_27588_263(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_payer_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                fs_parties_with_payer_role.append(p)
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_payer_role[0]["contactPoint"]["telephone"],
            actual_result=parties_with_payer_role[0]["contactPoint"]["telephone"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_contact_point_fax_number_on_pp_ms_release_27588_264(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_payer_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                fs_parties_with_payer_role.append(p)
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_payer_role[0]["contactPoint"]["faxNumber"],
            actual_result=parties_with_payer_role[0]["contactPoint"]["faxNumber"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_contact_point_fax_number_on_pp_ms_release_27588_265(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_payer_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                fs_parties_with_payer_role.append(p)
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_payer_role[0]["contactPoint"]["url"],
            actual_result=parties_with_payer_role[0]["contactPoint"]["url"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_roles_0_on_pp_ms_release_27588_266(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_payer_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                fs_parties_with_payer_role.append(p)
        parties_with_payer_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_payer_role[0]["roles"][0],
            actual_result=parties_with_payer_role[0]["roles"][0]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_id_on_pp_ms_release_27588_268(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_funder_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                fs_parties_with_funder_role.append(p)
        parties_with_funder_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                parties_with_funder_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_funder_role[0]["id"],
            actual_result=parties_with_funder_role[0]["id"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_name_on_pp_ms_release_27588_269(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_funder_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                fs_parties_with_funder_role.append(p)
        parties_with_funder_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                parties_with_funder_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_funder_role[0]["name"],
            actual_result=parties_with_funder_role[0]["name"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_identifier_id_on_pp_ms_release_27588_270(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_funder_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                fs_parties_with_funder_role.append(p)
        parties_with_funder_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                parties_with_funder_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_funder_role[0]["identifier"]["id"],
            actual_result=parties_with_funder_role[0]["identifier"]["id"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_identifier_scheme_on_pp_ms_release_27588_271(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_funder_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                fs_parties_with_funder_role.append(p)
        parties_with_funder_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                parties_with_funder_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_funder_role[0]["identifier"]["scheme"],
            actual_result=parties_with_funder_role[0]["identifier"]["scheme"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_identifier_legal_name_on_pp_ms_release_27588_272(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_funder_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                fs_parties_with_funder_role.append(p)
        parties_with_funder_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                parties_with_funder_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_funder_role[0]["identifier"]["legalName"],
            actual_result=parties_with_funder_role[0]["identifier"]["legalName"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_identifier_uri_on_pp_ms_release_27588_273(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_funder_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                fs_parties_with_funder_role.append(p)
        parties_with_funder_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                parties_with_funder_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_funder_role[0]["identifier"]["uri"],
            actual_result=parties_with_funder_role[0]["identifier"]["uri"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_address_street_address_on_pp_ms_release_27588_274(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_funder_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                fs_parties_with_funder_role.append(p)
        parties_with_funder_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                parties_with_funder_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_funder_role[0]["address"]["streetAddress"],
            actual_result=parties_with_funder_role[0]["address"]["streetAddress"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_address_postal_code_on_pp_ms_release_27588_275(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_funder_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                fs_parties_with_funder_role.append(p)
        parties_with_funder_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                parties_with_funder_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_funder_role[0]["address"]["postalCode"],
            actual_result=parties_with_funder_role[0]["address"]["postalCode"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_address_address_details_country_id_on_pp_ms_release_27588_276(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_funder_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                fs_parties_with_funder_role.append(p)
        parties_with_funder_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                parties_with_funder_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_funder_role[0]["address"]["addressDetails"]["country"]["id"],
            actual_result=parties_with_funder_role[0]["address"]["addressDetails"]["country"]["id"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_address_address_details_country_scheme_on_pp_ms_release_27588_277(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_funder_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                fs_parties_with_funder_role.append(p)
        parties_with_funder_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                parties_with_funder_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_funder_role[0]["address"]["addressDetails"]["country"]["scheme"],
            actual_result=parties_with_funder_role[0]["address"]["addressDetails"]["country"]["scheme"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_address_address_details_country_description_on_pp_ms_release_27588_278(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_funder_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                fs_parties_with_funder_role.append(p)
        parties_with_funder_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                parties_with_funder_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_funder_role[0]["address"]["addressDetails"]["country"]["description"],
            actual_result=parties_with_funder_role[0]["address"]["addressDetails"]["country"]["description"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_address_address_details_country_uri_on_pp_ms_release_27588_279(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_funder_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                fs_parties_with_funder_role.append(p)
        parties_with_funder_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                parties_with_funder_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_funder_role[0]["address"]["addressDetails"]["country"]["uri"],
            actual_result=parties_with_funder_role[0]["address"]["addressDetails"]["country"]["uri"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_address_address_details_region_id_on_pp_ms_release_27588_280(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_funder_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                fs_parties_with_funder_role.append(p)
        parties_with_funder_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                parties_with_funder_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_funder_role[0]["address"]["addressDetails"]["region"]["id"],
            actual_result=parties_with_funder_role[0]["address"]["addressDetails"]["region"]["id"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_address_address_details_region_scheme_on_pp_ms_release_27588_281(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_funder_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                fs_parties_with_funder_role.append(p)
        parties_with_funder_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                parties_with_funder_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_funder_role[0]["address"]["addressDetails"]["region"]["scheme"],
            actual_result=parties_with_funder_role[0]["address"]["addressDetails"]["region"]["scheme"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_address_address_details_region_description_on_pp_ms_release_27588_282(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_funder_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                fs_parties_with_funder_role.append(p)
        parties_with_funder_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                parties_with_funder_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_funder_role[0]["address"]["addressDetails"]["region"][
                "description"],
            actual_result=parties_with_funder_role[0]["address"]["addressDetails"]["region"]["description"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_address_address_details_region_uri_on_pp_ms_release_27588_283(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_funder_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                fs_parties_with_funder_role.append(p)
        parties_with_funder_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                parties_with_funder_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_funder_role[0]["address"]["addressDetails"]["region"]["uri"],
            actual_result=parties_with_funder_role[0]["address"]["addressDetails"]["region"]["uri"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_address_address_details_locality_uri_on_pp_ms_release_27588_284(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_funder_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                fs_parties_with_funder_role.append(p)
        parties_with_funder_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                parties_with_funder_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_funder_role[0]["address"]["addressDetails"]["locality"]["uri"],
            actual_result=parties_with_funder_role[0]["address"]["addressDetails"]["locality"]["uri"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_address_address_details_locality_id_on_pp_ms_release_27588_285(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_funder_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                fs_parties_with_funder_role.append(p)
        parties_with_funder_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                parties_with_funder_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_funder_role[0]["address"]["addressDetails"]["locality"]["id"],
            actual_result=parties_with_funder_role[0]["address"]["addressDetails"]["locality"]["id"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_address_address_details_locality_description_on_pp_ms_release_27588_286(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_funder_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                fs_parties_with_funder_role.append(p)
        parties_with_funder_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                parties_with_funder_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_funder_role[0]["address"]["addressDetails"]["locality"][
                "description"],
            actual_result=parties_with_funder_role[0]["address"]["addressDetails"]["locality"]["description"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_address_address_details_locality_scheme_on_pp_ms_release_27588_287(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_funder_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                fs_parties_with_funder_role.append(p)
        parties_with_funder_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                parties_with_funder_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_funder_role[0]["address"]["addressDetails"]["locality"][
                "scheme"],
            actual_result=parties_with_funder_role[0]["address"]["addressDetails"]["locality"]["scheme"]
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_additional_identifiers_0_scheme_on_pp_ms_release_27588_288(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_funder_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                fs_parties_with_funder_role.append(p)
        parties_with_funder_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                parties_with_funder_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_funder_role[0]["additionalIdentifiers"][0]['scheme'],
            actual_result=parties_with_funder_role[0]["additionalIdentifiers"][0]['scheme']
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_additional_identifiers_0_id_on_pp_ms_release_27588_289(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_funder_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                fs_parties_with_funder_role.append(p)
        parties_with_funder_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                parties_with_funder_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_funder_role[0]["additionalIdentifiers"][0]['id'],
            actual_result=parties_with_funder_role[0]["additionalIdentifiers"][0]['id']
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_additional_identifiers_0_legal_name_on_pp_ms_release_27588_290(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_funder_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                fs_parties_with_funder_role.append(p)
        parties_with_funder_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                parties_with_funder_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_funder_role[0]["additionalIdentifiers"][0]['legalName'],
            actual_result=parties_with_funder_role[0]["additionalIdentifiers"][0]['legalName']
        )

    @pytestrail.case("27588")
    def test_buyer_check_releases_0_parties_additional_identifiers_0_uri_on_pp_ms_release_27588_291(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_funder_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                fs_parties_with_funder_role.append(p)
        parties_with_funder_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                parties_with_funder_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_funder_role[0]["additionalIdentifiers"][0]['uri'],
            actual_result=parties_with_funder_role[0]["additionalIdentifiers"][0]['uri']
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_contact_point_name_on_pp_ms_release_27588_292(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_funder_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                fs_parties_with_funder_role.append(p)
        parties_with_funder_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                parties_with_funder_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_funder_role[0]["contactPoint"]["name"],
            actual_result=parties_with_funder_role[0]["contactPoint"]["name"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_contact_point_email_on_pp_ms_release_27588_293(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_funder_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                fs_parties_with_funder_role.append(p)
        parties_with_funder_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                parties_with_funder_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_funder_role[0]["contactPoint"]["email"],
            actual_result=parties_with_funder_role[0]["contactPoint"]["email"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_contact_point_telephone_on_pp_ms_release_27588_294(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_funder_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                fs_parties_with_funder_role.append(p)
        parties_with_funder_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                parties_with_funder_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_funder_role[0]["contactPoint"]["telephone"],
            actual_result=parties_with_funder_role[0]["contactPoint"]["telephone"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_contact_point_fax_number_on_pp_ms_release_27588_295(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_funder_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                fs_parties_with_funder_role.append(p)
        parties_with_funder_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                parties_with_funder_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_funder_role[0]["contactPoint"]["faxNumber"],
            actual_result=parties_with_funder_role[0]["contactPoint"]["faxNumber"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_contact_point_fax_number_on_pp_ms_release_27588_296(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_funder_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                fs_parties_with_funder_role.append(p)
        parties_with_funder_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                parties_with_funder_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_funder_role[0]["contactPoint"]["url"],
            actual_result=parties_with_funder_role[0]["contactPoint"]["url"]
        )

    @pytestrail.case("27588")
    def test_payer_check_releases_0_parties_roles_0_on_pp_ms_release_27588_297(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_list = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
        fs_release = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_parties_with_funder_role = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                fs_parties_with_funder_role.append(p)
        parties_with_funder_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                parties_with_funder_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=fs_parties_with_funder_role[0]["roles"][0],
            actual_result=parties_with_funder_role[0]["roles"][0]
        )

    @pytestrail.case("27588")
    def test_procuring_entity_check_releases_0_parties_id_on_pp_ms_release_27588_299(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=f"{payload['tender']['procuringEntity']['identifier']['scheme']}-"
                            f"{payload['tender']['procuringEntity']['identifier']['id']}",
            actual_result=parties_with_procuring_entity_role[0]["id"]
        )

    @pytestrail.case("27588")
    def test_procuring_entity_check_releases_0_parties_name_on_pp_ms_release_27588_300(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=payload['tender']['procuringEntity']['name'],
            actual_result=parties_with_procuring_entity_role[0]["name"]
        )

    @pytestrail.case("27588")
    def test_procuring_entity_check_releases_0_parties_identifier_scheme_on_pp_ms_release_27588_301(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=payload['tender']['procuringEntity']['identifier']['scheme'],
            actual_result=parties_with_procuring_entity_role[0]['identifier']['scheme']
        )

    @pytestrail.case("27588")
    def test_procuring_entity_check_releases_0_parties_identifier_id_on_pp_ms_release_27588_302(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=payload['tender']['procuringEntity']['identifier']['id'],
            actual_result=parties_with_procuring_entity_role[0]['identifier']['id']
        )

    @pytestrail.case("27588")
    def test_procuring_entity_check_releases_0_parties_identifier_legal_name_on_pp_ms_release_27588_303(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=payload['tender']['procuringEntity']['identifier']['legalName'],
            actual_result=parties_with_procuring_entity_role[0]['identifier']['legalName']
        )

    @pytestrail.case("27588")
    def test_procuring_entity_check_releases_0_parties_identifier_uri_on_pp_ms_release_27588_304(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=payload['tender']['procuringEntity']['identifier']['uri'],
            actual_result=parties_with_procuring_entity_role[0]['identifier']['uri']
        )

    @pytestrail.case("27588")
    def test_procuring_entity_check_releases_0_parties_address_street_address_on_pp_ms_release_27588_305(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=payload['tender']['procuringEntity']['address']['streetAddress'],
            actual_result=parties_with_procuring_entity_role[0]['address']['streetAddress']
        )

    @pytestrail.case("27588")
    def test_procuring_entity_check_releases_0_parties_address_postal_code_on_pp_ms_release_27588_306(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=payload['tender']['procuringEntity']['address']['postalCode'],
            actual_result=parties_with_procuring_entity_role[0]['address']['postalCode']
        )

    @pytestrail.case("27588")
    def test_procuring_entity_check_releases_0_parties_address_address_details_country_id_on_pp_ms_release_27588_307(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=payload['tender']['procuringEntity']['address']['addressDetails']['country']['id'],
            actual_result=parties_with_procuring_entity_role[0]['address']['addressDetails']['country']['id']
        )

    @pytestrail.case("27588")
    def test_procuring_entity_check_releases_0_parties_address_address_details_country_scheme_on_pp_ms_27588_308(
            self, pmd, language, instance):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        mdm = MdmService(
            instance=instance,
            lang=language,
            procuring_address_details_country_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["country"]["id"],
            procuring_address_details_region_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["region"]["id"],
            procuring_address_details_locality_scheme=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["scheme"],
            procuring_address_details_locality_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["id"],
            pn_lot_address_details_country_id=payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['country']['id'],
            pn_lot_address_details_region_id=payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['region']['id'],
            pn_lot_address_details_locality_id=payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['locality']['id'],
            pn_lot_address_details_locality_scheme=payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['locality']['scheme']
        )
        data = mdm.process_tender_data(pmd).json()
        country_from_mdm = data["data"]["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]
        assert compare_actual_result_and_expected_result(
            expected_result=country_from_mdm['scheme'],
            actual_result=parties_with_procuring_entity_role[0]['address']['addressDetails']['country']['scheme']
        )

    @pytestrail.case("27588")
    def test_procuring_entity_check_releases_0_parties_address_address_details_country_description_on_pp_ms_27588_309(
            self, pmd, language, instance):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        mdm = MdmService(
            instance=instance,
            lang=language,
            procuring_address_details_country_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["country"]["id"],
            procuring_address_details_region_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["region"]["id"],
            procuring_address_details_locality_scheme=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["scheme"],
            procuring_address_details_locality_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["id"],
            pn_lot_address_details_country_id=payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['country']['id'],
            pn_lot_address_details_region_id=payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['region']['id'],
            pn_lot_address_details_locality_id=payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['locality']['id'],
            pn_lot_address_details_locality_scheme=payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['locality']['scheme']
        )
        data = mdm.process_tender_data(pmd).json()
        country_from_mdm = data["data"]["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]
        assert compare_actual_result_and_expected_result(
            expected_result=country_from_mdm['description'],
            actual_result=parties_with_procuring_entity_role[0]['address']['addressDetails']['country']['description']
        )

    @pytestrail.case("27588")
    def test_procuring_entity_check_releases_0_parties_address_address_details_country_uri_on_pp_ms_27588_310(
            self, pmd, language, instance):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        mdm = MdmService(
            instance=instance,
            lang=language,
            procuring_address_details_country_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["country"]["id"],
            procuring_address_details_region_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["region"]["id"],
            procuring_address_details_locality_scheme=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["scheme"],
            procuring_address_details_locality_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["id"],
            pn_lot_address_details_country_id=payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['country']['id'],
            pn_lot_address_details_region_id=payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['region']['id'],
            pn_lot_address_details_locality_id=payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['locality']['id'],
            pn_lot_address_details_locality_scheme=payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['locality']['scheme']
        )
        data = mdm.process_tender_data(pmd).json()
        country_from_mdm = data["data"]["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]
        assert compare_actual_result_and_expected_result(
            expected_result=country_from_mdm['uri'],
            actual_result=parties_with_procuring_entity_role[0]['address']['addressDetails']['country']['uri']
        )

    @pytestrail.case("27588")
    def test_procuring_entity_check_releases_0_parties_address_address_details_region_uri_on_pp_ms_27588_311(
            self, pmd, language, instance):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        mdm = MdmService(
            instance=instance,
            lang=language,
            procuring_address_details_country_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["country"]["id"],
            procuring_address_details_region_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["region"]["id"],
            procuring_address_details_locality_scheme=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["scheme"],
            procuring_address_details_locality_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["id"],
            pn_lot_address_details_country_id=payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['country']['id'],
            pn_lot_address_details_region_id=payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['region']['id'],
            pn_lot_address_details_locality_id=payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['locality']['id'],
            pn_lot_address_details_locality_scheme=payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['locality']['scheme']
        )
        data = mdm.process_tender_data(pmd).json()
        region_from_mdm = data["data"]["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]
        assert compare_actual_result_and_expected_result(
            expected_result=region_from_mdm['uri'],
            actual_result=parties_with_procuring_entity_role[0]['address']['addressDetails']['region']['uri']
        )

    @pytestrail.case("27588")
    def test_procuring_entity_check_releases_0_parties_address_address_details_region_id_on_pp_ms_27588_312(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"],
            actual_result=parties_with_procuring_entity_role[0]['address']['addressDetails']['region']['id']
        )

    @pytestrail.case("27588")
    def test_procuring_entity_check_releases_0_parties_address_address_details_region_scheme_on_pp_ms_27588_313(
            self, pmd, language, instance):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        mdm = MdmService(
            instance=instance,
            lang=language,
            procuring_address_details_country_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["country"]["id"],
            procuring_address_details_region_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["region"]["id"],
            procuring_address_details_locality_scheme=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["scheme"],
            procuring_address_details_locality_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["id"],
            pn_lot_address_details_country_id=payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['country']['id'],
            pn_lot_address_details_region_id=payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['region']['id'],
            pn_lot_address_details_locality_id=payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['locality']['id'],
            pn_lot_address_details_locality_scheme=payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['locality']['scheme']
        )
        data = mdm.process_tender_data(pmd).json()
        region_from_mdm = data["data"]["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]
        assert compare_actual_result_and_expected_result(
            expected_result=region_from_mdm['scheme'],
            actual_result=parties_with_procuring_entity_role[0]['address']['addressDetails']['region']['scheme']
        )

    @pytestrail.case("27588")
    def test_procuring_entity_check_releases_0_parties_address_address_details_region_description_on_pp_ms_27588_314(
            self, pmd, language, instance):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        mdm = MdmService(
            instance=instance,
            lang=language,
            procuring_address_details_country_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["country"]["id"],
            procuring_address_details_region_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["region"]["id"],
            procuring_address_details_locality_scheme=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["scheme"],
            procuring_address_details_locality_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["id"],
            pn_lot_address_details_country_id=payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['country']['id'],
            pn_lot_address_details_region_id=payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['region']['id'],
            pn_lot_address_details_locality_id=payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['locality']['id'],
            pn_lot_address_details_locality_scheme=payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['locality']['scheme']
        )
        data = mdm.process_tender_data(pmd).json()
        region_from_mdm = data["data"]["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]
        assert compare_actual_result_and_expected_result(
            expected_result=region_from_mdm['description'],
            actual_result=parties_with_procuring_entity_role[0]['address']['addressDetails']['region']['description']
        )

    @pytestrail.case("27588")
    def test_procuring_entity_check_releases_0_parties_address_address_details_locality_description_on_pp_ms_27588_315(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"][
                "description"],
            actual_result=parties_with_procuring_entity_role[0]['address']['addressDetails']['locality']['description']
        )

    @pytestrail.case("27588")
    def test_procuring_entity_check_releases_0_parties_address_address_details_locality_id_on_pp_ms_27588_316(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=payload['tender']['procuringEntity']['address']['addressDetails']['locality']['id'],
            actual_result=parties_with_procuring_entity_role[0]['address']['addressDetails']['locality']['id']
        )

    @pytestrail.case("27588")
    def test_procuring_entity_check_releases_0_parties_address_address_details_locality_scheme_on_pp_ms_27588_317(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=payload['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'],
            actual_result=parties_with_procuring_entity_role[0]['address']['addressDetails']['locality']['scheme']
        )

    @pytestrail.case("27588")
    def test_procuring_entity_check_releases_0_parties_address_address_details_locality_uri_on_pp_ms_27588_318(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        if "uri" in parties_with_procuring_entity_role[0]['address']['addressDetails']['locality']:
            check_locality_uri = True
        else:
            check_locality_uri = False
        assert compare_actual_result_and_expected_result(
            expected_result=str(False),
            actual_result=str(check_locality_uri)
        )

    @pytestrail.case("27588")
    def test_procuring_entity_check_releases_0_parties_contact_point_name_on_pp_ms_release_27588_319(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=payload['tender']['procuringEntity']['contactPoint']['name'],
            actual_result=parties_with_procuring_entity_role[0]['contactPoint']['name']
        )

    @pytestrail.case("27588")
    def test_procuring_entity_check_releases_0_parties_contact_point_email_on_pp_ms_release_27588_320(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=payload['tender']['procuringEntity']['contactPoint']['email'],
            actual_result=parties_with_procuring_entity_role[0]['contactPoint']['email']
        )

    @pytestrail.case("27588")
    def test_procuring_entity_check_releases_0_parties_contact_point_telephone_on_pp_ms_release_27588_321(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=payload['tender']['procuringEntity']['contactPoint']['telephone'],
            actual_result=parties_with_procuring_entity_role[0]['contactPoint']['telephone']
        )

    @pytestrail.case("27588")
    def test_procuring_entity_check_releases_0_parties_contact_point_fax_number_on_pp_ms_release_27588_322(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=payload['tender']['procuringEntity']['contactPoint']['faxNumber'],
            actual_result=parties_with_procuring_entity_role[0]['contactPoint']['faxNumber']
        )

    @pytestrail.case("27588")
    def test_procuring_entity_check_releases_0_parties_contact_point_url_on_pp_ms_release_27588_323(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        payload = CreatePn.payload
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=payload['tender']['procuringEntity']['contactPoint']['url'],
            actual_result=parties_with_procuring_entity_role[0]['contactPoint']['url']
        )

    @pytestrail.case("27588")
    def test_procuring_entity_check_releases_0_parties_roles_0_on_pp_ms_release_27588_324(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        parties_with_procuring_entity_role = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_with_procuring_entity_role.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result="procuringEntity",
            actual_result=parties_with_procuring_entity_role[0]['roles'][0]
        )

    @pytestrail.case("27588")
    def test_relationship_planning_check_releases_0_related_processes_id_on_pp_ms_release_27588_326(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_with_relationship_planning = list()
        for p in ms_release["releases"][0]["relatedProcesses"]:
            if p["relationship"] == ["planning"]:
                related_processes_with_relationship_planning.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(is_it_uuid(related_processes_with_relationship_planning[0]['id'], 1))
        )

    @pytestrail.case("27588")
    def test_relationship_planning_check_releases_0_related_processes_relationship_on_pp_ms_release_27588_327(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_with_relationship_planning = list()
        for p in ms_release["releases"][0]["relatedProcesses"]:
            if p["relationship"] == ["planning"]:
                related_processes_with_relationship_planning.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result="planning",
            actual_result=related_processes_with_relationship_planning[0]['relationship'][0]
        )

    @pytestrail.case("27588")
    def test_relationship_planning_check_releases_0_related_processes_scheme_on_pp_ms_release_27588_328(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_with_relationship_planning = list()
        for p in ms_release["releases"][0]["relatedProcesses"]:
            if p["relationship"] == ["planning"]:
                related_processes_with_relationship_planning.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result="ocid",
            actual_result=related_processes_with_relationship_planning[0]['scheme']
        )

    @pytestrail.case("27588")
    def test_relationship_planning_check_releases_0_related_processes_identifier_on_pp_ms_release_27588_329(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_with_relationship_planning = list()
        for p in ms_release["releases"][0]["relatedProcesses"]:
            if p["relationship"] == ["planning"]:
                related_processes_with_relationship_planning.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id'],
            actual_result=related_processes_with_relationship_planning[0]['identifier']
        )

    @pytestrail.case("27588")
    def test_relationship_planning_check_releases_0_related_processes_uri_on_pp_ms_release_27588_330(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_with_relationship_planning = list()
        for p in ms_release["releases"][0]["relatedProcesses"]:
            if p["relationship"] == ["planning"]:
                related_processes_with_relationship_planning.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=f"{CreatePn.message_from_kafka['data']['url']}/"
                            f"{CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']}",
            actual_result=related_processes_with_relationship_planning[0]['uri']
        )

    @pytestrail.case("27588")
    def test_relationship_x_expenditure_item_check_releases_0_related_processes_id_on_pp_ms_release_27588_332(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_with_relationship_x_expenditure_item = list()
        for p in ms_release["releases"][0]["relatedProcesses"]:
            if p["relationship"] == ["x_expenditureItem"]:
                related_processes_with_relationship_x_expenditure_item.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(is_it_uuid(related_processes_with_relationship_x_expenditure_item[0]['id'], 1))
        )

    @pytestrail.case("27588")
    def test_relationship_x_expenditure_item_check_releases_0_related_processes_relationship_on_pp_ms_release_27588_333(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_with_relationship_x_expenditure_item = list()
        for p in ms_release["releases"][0]["relatedProcesses"]:
            if p["relationship"] == ["x_expenditureItem"]:
                related_processes_with_relationship_x_expenditure_item.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result="x_expenditureItem",
            actual_result=related_processes_with_relationship_x_expenditure_item[0]['relationship'][0]
        )

    @pytestrail.case("27588")
    def test_relationship_x_expenditure_item_check_releases_0_related_processes_scheme_on_pp_ms_release_27588_334(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_with_relationship_x_expenditure_item = list()
        for p in ms_release["releases"][0]["relatedProcesses"]:
            if p["relationship"] == ["x_expenditureItem"]:
                related_processes_with_relationship_x_expenditure_item.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result="ocid",
            actual_result=related_processes_with_relationship_x_expenditure_item[0]['scheme']
        )

    @pytestrail.case("27588")
    def test_relationship_x_expenditure_item_check_releases_0_related_processes_identifier_on_pp_ms_release_27588_335(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_with_relationship_x_expenditure_item = list()
        for p in ms_release["releases"][0]["relatedProcesses"]:
            if p["relationship"] == ["x_expenditureItem"]:
                related_processes_with_relationship_x_expenditure_item.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=CreatePn.ei_id,
            actual_result=related_processes_with_relationship_x_expenditure_item[0]['identifier']
        )

    @pytestrail.case("27588")
    def test_relationship_x_expenditure_item_check_releases_0_related_processes_uri_on_pp_ms_release_27588_336(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_with_relationship_x_expenditure_item = list()
        for p in ms_release["releases"][0]["relatedProcesses"]:
            if p["relationship"] == ["x_expenditureItem"]:
                related_processes_with_relationship_x_expenditure_item.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=f"http://dev.public.eprocurement.systems/budgets/{CreatePn.ei_id}/{CreatePn.ei_id}",
            actual_result=related_processes_with_relationship_x_expenditure_item[0]['uri']
        )

    @pytestrail.case("27588")
    def test_relationship_x_funding_source_check_releases_0_related_processes_id_on_pp_ms_release_27588_338(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_with_relationship_x_funding_source = list()
        for p in ms_release["releases"][0]["relatedProcesses"]:
            if p["relationship"] == ["x_fundingSource"]:
                related_processes_with_relationship_x_funding_source.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(is_it_uuid(related_processes_with_relationship_x_funding_source[0]['id'], 1))
        )

    @pytestrail.case("27588")
    def test_relationship_x_funding_source_check_releases_0_related_processes_relationship_on_pp_ms_release_27588_339(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_with_relationship_x_funding_source = list()
        for p in ms_release["releases"][0]["relatedProcesses"]:
            if p["relationship"] == ["x_fundingSource"]:
                related_processes_with_relationship_x_funding_source.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result="x_fundingSource",
            actual_result=related_processes_with_relationship_x_funding_source[0]['relationship'][0]
        )

    @pytestrail.case("27588")
    def test_relationship_x_funding_source_check_releases_0_related_processes_scheme_on_pp_ms_release_27588_340(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_with_relationship_x_funding_source = list()
        for p in ms_release["releases"][0]["relatedProcesses"]:
            if p["relationship"] == ["x_fundingSource"]:
                related_processes_with_relationship_x_funding_source.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result="ocid",
            actual_result=related_processes_with_relationship_x_funding_source[0]['scheme']
        )

    @pytestrail.case("27588")
    def test_relationship_x_funding_source_check_releases_0_related_processes_identifier_on_pp_ms_release_27588_341(
            self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_with_relationship_x_funding_source = list()
        for p in ms_release["releases"][0]["relatedProcesses"]:
            if p["relationship"] == ["x_fundingSource"]:
                related_processes_with_relationship_x_funding_source.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=CreatePn.fs_id,
            actual_result=related_processes_with_relationship_x_funding_source[0]['identifier']
        )

    @pytestrail.case("27588")
    def test_relationship_x_funding_source_check_releases_0_related_processes_uri_on_pp_ms_release_27588_342(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        related_processes_with_relationship_x_funding_source = list()
        for p in ms_release["releases"][0]["relatedProcesses"]:
            if p["relationship"] == ["x_fundingSource"]:
                related_processes_with_relationship_x_funding_source.append(p)
        assert compare_actual_result_and_expected_result(
            expected_result=f"http://dev.public.eprocurement.systems/budgets/{CreatePn.ei_id}/{CreatePn.fs_id}",
            actual_result=related_processes_with_relationship_x_funding_source[0]['uri']
        )

    @pytestrail.case("27588")
    def test_check_on_the_platform_data_has_been_transferred_and_displayed_correctly_in_the_ms_release_27588_343(
            self, language, pmd):
        ei_id = CreatePn.ei_id
        message_from_kafka = CreatePn.message_from_kafka
        url_create_ms = message_from_kafka['data']['url'] + "/" + message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create_ms).json()
        related_processes_list_ei = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_processes_list_ei.append(d_1)
        ei_release = requests.get(url=related_processes_list_ei[0]["uri"]).json()

        related_processes_list_fs = list()
        for d in ms_release["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list_fs.append(d_1)
        fs_release = requests.get(url=related_processes_list_fs[0]["uri"]).json()

        parties_with_buyer_role_ei = list()
        for p in ei_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_with_buyer_role_ei.append(p)
        parties_with_payer_role_fs = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["payer"]:
                parties_with_payer_role_fs.append(p)

        parties_with_funder_role_fs = list()
        for p in fs_release["releases"][0]["parties"]:
            if p["roles"] == ["funder"]:
                parties_with_funder_role_fs.append(p)

        payload = CreatePn.payload
        if payload['tender']['lots'][0]['contractPeriod']['startDate'] <= \
                payload['tender']['lots'][1]['contractPeriod']['startDate']:
            start_date = payload['tender']['lots'][0]['contractPeriod']['startDate']
        elif payload['tender']['lots'][0]['contractPeriod']['startDate'] >= \
                payload['tender']['lots'][1]['contractPeriod']['startDate']:
            start_date = payload['tender']['lots'][1]['contractPeriod']['startDate']
        else:
            raise Exception("Can not get startDate for tender.contractPeriod")
        if payload['tender']['lots'][0]['contractPeriod']['endDate'] <= \
                payload['tender']['lots'][1]['contractPeriod']['endDate']:
            end_date = payload['tender']['lots'][1]['contractPeriod']['endDate']
        elif payload['tender']['lots'][0]['contractPeriod']['endDate'] >= \
                payload['tender']['lots'][1]['contractPeriod']['endDate']:
            end_date = payload['tender']['lots'][0]['contractPeriod']['endDate']
        else:
            raise Exception("Can not get endDate for tender.contractPeriod")

        mdm = MdmService(
            instance="dev",
            lang="ro",
            procuring_address_details_country_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["country"]["id"],
            procuring_address_details_region_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["region"]["id"],
            procuring_address_details_locality_scheme=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["scheme"],
            procuring_address_details_locality_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["id"],
            pn_lot_address_details_country_id=payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['country']['id'],
            pn_lot_address_details_region_id=payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['region']['id'],
            pn_lot_address_details_locality_id=payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['locality']['id'],
            pn_lot_address_details_locality_scheme=payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['locality']['scheme']
        )
        data = mdm.process_tender_data(pmd).json()
        country_from_mdm = data["data"]["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]
        region_from_mdm = data["data"]["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]
        procurement_method_details_from_mdm = data["data"]["tender"]["procurementMethodDetails"]
        eligibility_criteria_from_mdm = data["data"]["tender"]["eligibilityCriteria"]

        calculate_new_cpv_code = get_new_classification_id(
            payload['tender']['items'][0]['classification']['id'],
            payload['tender']['items'][1]['classification']['id']
        )
        get_value_by_new_cpv_code = get_value_from_classification_cpv_dictionary_xls(
            calculate_new_cpv_code,
            language
        )

        actual_result = ms_release
        expected_result = {
            "uri": f"http://dev.public.eprocurement.systems/tenders/"
                   f"{message_from_kafka['data']['ocid']}/{message_from_kafka['data']['ocid']}",
            "version": "1.1",
            "extensions": [
                "https://raw.githubusercontent.com/open-contracting/ocds_bid_extension/v1.1.1/extension.json",
                "https://raw.githubusercontent.com/open-contracting/ocds_enquiry_extension/v1.1.1/extension.js"],
            "publisher": {
                "name": "M-Tender",
                "uri": "https://www.mtender.gov.md"
            },
            "license": "http://opendefinition.org/licenses/",
            "publicationPolicy": "http://opendefinition.org/licenses/",
            "publishedDate": message_from_kafka['data']['operationDate'],
            "releases": [{
                "ocid": message_from_kafka['data']['ocid'],
                "id": f"{message_from_kafka['data']['ocid']}-"
                      f"{message_from_kafka['data']['outcomes']['pn'][0]['id'][32:45]}",
                "date": message_from_kafka['data']['operationDate'],
                "tag": ["compiled"],
                "language": language,
                "initiationType": "tender",
                "planning": {
                    "budget": {
                        "description": "description of budget",
                        "amount": {
                            "amount": payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["amount"],
                            "currency": payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["currency"]
                        },
                        "isEuropeanUnionFunded": fs_release['releases'][0]['planning']['budget'][
                            'isEuropeanUnionFunded'],
                        "budgetBreakdown": [{
                            "id": payload["planning"]["budget"]["budgetBreakdown"][0]['id'],
                            "description": "description",
                            "amount": {
                                "amount": payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["amount"],
                                "currency": payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["currency"]
                            },
                            "period": {
                                "startDate": fs_release['releases'][0]['planning']['budget']['period']['startDate'],
                                "endDate": fs_release['releases'][0]['planning']['budget']['period']['endDate']
                            },
                            "sourceParty": {
                                "id": fs_release['releases'][0]['planning']['budget']['sourceEntity']['id'],
                                "name": fs_release['releases'][0]['planning']['budget']['sourceEntity']['name']
                            },
                            "europeanUnionFunding": {
                                "projectIdentifier":
                                    fs_release['releases'][0]['planning']['budget']['europeanUnionFunding'][
                                        'projectIdentifier'],
                                "projectName": fs_release['releases'][0]['planning']['budget']['europeanUnionFunding'][
                                    'projectName'],
                                "uri": fs_release['releases'][0]['planning']['budget']['europeanUnionFunding'][
                                    'uri']
                            }
                        }]
                    },
                    "rationale": payload['planning']['rationale']
                },
                "tender": {
                    "id": actual_result['releases'][0]['tender']['id'],
                    "title": payload['tender']['title'],
                    "description": payload['tender']['description'],
                    "status": "planning",
                    "statusDetails": "planning notice",
                    "value": {
                        "amount": payload["tender"]["lots"][0]["value"]["amount"] + payload["tender"]["lots"][1][
                            "value"]["amount"],
                        "currency": payload["tender"]["lots"][0]["value"]["currency"]
                    },
                    "procurementMethod": "open",
                    "procurementMethodDetails": procurement_method_details_from_mdm,
                    "procurementMethodRationale": payload['tender']['procurementMethodRationale'],
                    "mainProcurementCategory": ei_release['releases'][0]['tender']['mainProcurementCategory'],
                    "hasEnquiries": False,
                    "eligibilityCriteria": eligibility_criteria_from_mdm,
                    "contractPeriod": {
                        "startDate": start_date,
                        "endDate": end_date
                    },
                    "procuringEntity": {
                        "id": f"{payload['tender']['procuringEntity']['identifier']['scheme']}-"
                              f"{payload['tender']['procuringEntity']['identifier']['id']}",
                        "name": payload['tender']['procuringEntity']['name']
                    },
                    "acceleratedProcedure": {
                        "isAcceleratedProcedure": False
                    },
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_new_cpv_code[0],
                        "description": get_value_by_new_cpv_code[1]
                    },
                    "designContest": {
                        "serviceContractAward": False
                    },
                    "electronicWorkflows": {
                        "useOrdering": False,
                        "usePayment": False,
                        "acceptInvoicing": False
                    },
                    "jointProcurement": {
                        "isJointProcurement": False
                    },
                    "legalBasis": payload['tender']['legalBasis'],
                    "procedureOutsourcing": {
                        "procedureOutsourced": False
                    },
                    "procurementMethodAdditionalInfo": payload['tender']['procurementMethodAdditionalInfo'],
                    "dynamicPurchasingSystem": {
                        "hasDynamicPurchasingSystem": False
                    },
                    "framework": {
                        "isAFramework": False
                    }
                },
                "parties": [{
                    "id": parties_with_buyer_role_ei[0]['id'],
                    "name": parties_with_buyer_role_ei[0]['name'],
                    "identifier": {
                        "scheme": parties_with_buyer_role_ei[0]['identifier']['scheme'],
                        "id": parties_with_buyer_role_ei[0]['identifier']['id'],
                        "legalName": parties_with_buyer_role_ei[0]['identifier']['legalName'],
                        "uri": parties_with_buyer_role_ei[0]['identifier']['uri']
                    },
                    "address": {
                        "streetAddress": parties_with_buyer_role_ei[0]['address']['streetAddress'],
                        "postalCode": "02217",
                        "addressDetails": {
                            "country": {
                                "scheme": parties_with_buyer_role_ei[0]['address']['addressDetails']['country'][
                                    'scheme'],
                                "id": parties_with_buyer_role_ei[0]['address']['addressDetails']['country']['id'],
                                "description": parties_with_buyer_role_ei[0]['address']['addressDetails']['country'][
                                    'description'],
                                "uri": parties_with_buyer_role_ei[0]['address']['addressDetails']['country']['uri']
                            },
                            "region": {
                                "scheme": parties_with_buyer_role_ei[0]['address']['addressDetails']['region'][
                                    'scheme'],
                                "id": parties_with_buyer_role_ei[0]['address']['addressDetails']['region']['id'],
                                "description": parties_with_buyer_role_ei[0]['address']['addressDetails']['region'][
                                    'description'],
                                "uri": parties_with_buyer_role_ei[0]['address']['addressDetails']['region']['uri']
                            },
                            "locality": {
                                "scheme": parties_with_buyer_role_ei[0]['address']['addressDetails']['locality'][
                                    'scheme'],
                                "id": parties_with_buyer_role_ei[0]['address']['addressDetails']['locality']['id'],
                                "description": parties_with_buyer_role_ei[0]['address']['addressDetails']['locality'][
                                    'description'],
                                "uri": parties_with_buyer_role_ei[0]['address']['addressDetails']['locality']['uri']
                            }
                        }
                    },
                    "additionalIdentifiers": [{
                        "scheme": parties_with_buyer_role_ei[0]['additionalIdentifiers'][0]['scheme'],
                        "id": parties_with_buyer_role_ei[0]['additionalIdentifiers'][0]['id'],
                        "legalName": parties_with_buyer_role_ei[0]['additionalIdentifiers'][0]['legalName'],
                        "uri": parties_with_buyer_role_ei[0]['additionalIdentifiers'][0]['uri']
                    }],
                    "contactPoint": {
                        "name": parties_with_buyer_role_ei[0]['contactPoint']['name'],
                        "email": parties_with_buyer_role_ei[0]['contactPoint']['email'],
                        "telephone": parties_with_buyer_role_ei[0]['contactPoint']['telephone'],
                        "faxNumber": parties_with_buyer_role_ei[0]['contactPoint']['faxNumber'],
                        "url": parties_with_buyer_role_ei[0]['contactPoint']['url']
                    },
                    "details": {
                        "typeOfBuyer": parties_with_buyer_role_ei[0]['details']['typeOfBuyer'],
                        "mainGeneralActivity": parties_with_buyer_role_ei[0]['details']['mainGeneralActivity'],
                        "mainSectoralActivity": parties_with_buyer_role_ei[0]['details']['mainSectoralActivity']
                    },
                    "roles": ["buyer"]
                }, {
                    "id": parties_with_payer_role_fs[0]['id'],
                    "name": parties_with_payer_role_fs[0]['name'],
                    "identifier": {
                        "scheme": parties_with_payer_role_fs[0]['identifier']['scheme'],
                        "id": parties_with_payer_role_fs[0]['identifier']['id'],
                        "legalName": parties_with_payer_role_fs[0]['identifier']['legalName'],
                        "uri": parties_with_payer_role_fs[0]['identifier']['uri']
                    },
                    "address": {
                        "streetAddress": parties_with_payer_role_fs[0]['address']['streetAddress'],
                        "postalCode": parties_with_payer_role_fs[0]['address']['postalCode'],
                        "addressDetails": {
                            "country": {
                                "scheme": parties_with_payer_role_fs[0]['address']['addressDetails']['country'][
                                    'scheme'],
                                "id": parties_with_payer_role_fs[0]['address']['addressDetails']['country']['id'],
                                "description": parties_with_payer_role_fs[0]['address']['addressDetails']['country'][
                                    'description'],
                                "uri": parties_with_payer_role_fs[0]['address']['addressDetails']['country']['uri']
                            },
                            "region": {
                                "scheme": parties_with_payer_role_fs[0]['address']['addressDetails']['region'][
                                    'scheme'],
                                "id": parties_with_payer_role_fs[0]['address']['addressDetails']['region']['id'],
                                "description": parties_with_payer_role_fs[0]['address']['addressDetails']['region'][
                                    'description'],
                                "uri": parties_with_payer_role_fs[0]['address']['addressDetails']['region']['uri']
                            },
                            "locality": {
                                "scheme": parties_with_payer_role_fs[0]['address']['addressDetails']['locality'][
                                    'scheme'],
                                "id": parties_with_payer_role_fs[0]['address']['addressDetails']['locality']['id'],
                                "description": parties_with_payer_role_fs[0]['address']['addressDetails']['locality'][
                                    'description'],
                                "uri": parties_with_payer_role_fs[0]['address']['addressDetails']['locality']['uri']
                            }
                        }
                    },
                    "additionalIdentifiers": [{
                        "scheme": parties_with_payer_role_fs[0]['additionalIdentifiers'][0]['scheme'],
                        "id": parties_with_payer_role_fs[0]['additionalIdentifiers'][0]['id'],
                        "legalName": parties_with_payer_role_fs[0]['additionalIdentifiers'][0]['legalName'],
                        "uri": parties_with_payer_role_fs[0]['additionalIdentifiers'][0]['uri']
                    }],
                    "contactPoint": {
                        "name": parties_with_payer_role_fs[0]['contactPoint']['name'],
                        "email": parties_with_payer_role_fs[0]['contactPoint']['email'],
                        "telephone": parties_with_payer_role_fs[0]['contactPoint']['telephone'],
                        "faxNumber": parties_with_payer_role_fs[0]['contactPoint']['faxNumber'],
                        "url": parties_with_payer_role_fs[0]['contactPoint']['url']
                    },
                    "roles": ["payer"]
                }, {
                    "id": parties_with_funder_role_fs[0]['id'],
                    "name": parties_with_funder_role_fs[0]['name'],
                    "identifier": {
                        "scheme": parties_with_funder_role_fs[0]['identifier']['scheme'],
                        "id": parties_with_funder_role_fs[0]['identifier']['id'],
                        "legalName": parties_with_funder_role_fs[0]['identifier']['legalName'],
                        "uri": parties_with_funder_role_fs[0]['identifier']['uri']
                    },
                    "address": {
                        "streetAddress": parties_with_funder_role_fs[0]['address']['streetAddress'],
                        "postalCode": parties_with_funder_role_fs[0]['address']['postalCode'],
                        "addressDetails": {
                            "country": {
                                "scheme": parties_with_funder_role_fs[0]['address']['addressDetails']['country'][
                                    'scheme'],
                                "id": parties_with_funder_role_fs[0]['address']['addressDetails']['country']['id'],
                                "description": parties_with_funder_role_fs[0]['address']['addressDetails']['country'][
                                    'description'],
                                "uri": parties_with_funder_role_fs[0]['address']['addressDetails']['country']['uri']
                            },
                            "region": {
                                "scheme": parties_with_funder_role_fs[0]['address']['addressDetails']['region'][
                                    'scheme'],
                                "id": parties_with_funder_role_fs[0]['address']['addressDetails']['region']['id'],
                                "description": parties_with_funder_role_fs[0]['address']['addressDetails']['region'][
                                    'description'],
                                "uri": parties_with_funder_role_fs[0]['address']['addressDetails']['region']['uri']
                            },
                            "locality": {
                                "scheme": parties_with_funder_role_fs[0]['address']['addressDetails']['locality'][
                                    'scheme'],
                                "id": parties_with_funder_role_fs[0]['address']['addressDetails']['locality']['id'],
                                "description": parties_with_funder_role_fs[0]['address']['addressDetails']['locality'][
                                    'description'],
                                "uri": parties_with_funder_role_fs[0]['address']['addressDetails']['locality']['uri']
                            }
                        }
                    },
                    "additionalIdentifiers": [{
                        "scheme": parties_with_funder_role_fs[0]['additionalIdentifiers'][0]['scheme'],
                        "id": parties_with_funder_role_fs[0]['additionalIdentifiers'][0]['id'],
                        "legalName": parties_with_funder_role_fs[0]['additionalIdentifiers'][0]['legalName'],
                        "uri": parties_with_funder_role_fs[0]['additionalIdentifiers'][0]['uri']
                    }],
                    "contactPoint": {
                        "name": parties_with_funder_role_fs[0]['contactPoint']['name'],
                        "email": parties_with_funder_role_fs[0]['contactPoint']['email'],
                        "telephone": parties_with_funder_role_fs[0]['contactPoint']['telephone'],
                        "faxNumber": parties_with_funder_role_fs[0]['contactPoint']['faxNumber'],
                        "url": parties_with_funder_role_fs[0]['contactPoint']['url']
                    },
                    "roles": ["funder"]
                }, {
                    "id": f"{payload['tender']['procuringEntity']['identifier']['scheme']}-"
                          f"{payload['tender']['procuringEntity']['identifier']['id']}",
                    "name": payload['tender']['procuringEntity']['name'],
                    "identifier": {
                        "scheme": payload['tender']['procuringEntity']['identifier']['scheme'],
                        "id": payload['tender']['procuringEntity']['identifier']['id'],
                        "legalName": payload['tender']['procuringEntity']['identifier']['legalName'],
                        "uri": payload['tender']['procuringEntity']['identifier']['uri']
                    },
                    "address": {
                        "streetAddress": payload['tender']['procuringEntity']['address']['streetAddress'],
                        "postalCode": payload['tender']['procuringEntity']['address']['postalCode'],
                        "addressDetails": {
                            "country": {
                                "scheme": country_from_mdm['scheme'],
                                "id": payload['tender']['procuringEntity']['address']['addressDetails']['country'][
                                    'id'],
                                "description": country_from_mdm['description'],
                                "uri": country_from_mdm['uri']
                            },
                            "region": {
                                "scheme": region_from_mdm['scheme'],
                                "id": payload['tender']['procuringEntity']['address']['addressDetails']['region']['id'],
                                "description": region_from_mdm['description'],
                                "uri": region_from_mdm['uri']
                            },
                            "locality": {
                                "scheme": payload['tender']['procuringEntity']['address']['addressDetails']['locality'][
                                    'scheme'],
                                "id": payload['tender']['procuringEntity']['address']['addressDetails']['locality'][
                                    'id'],
                                "description":
                                    payload['tender']['procuringEntity']['address']['addressDetails']['locality'][
                                        'description']
                            }
                        }
                    },
                    "additionalIdentifiers": [{
                        "scheme": payload['tender']['procuringEntity']['additionalIdentifiers'][0]['scheme'],
                        "id": payload['tender']['procuringEntity']['additionalIdentifiers'][0]['id'],
                        "legalName": payload['tender']['procuringEntity']['additionalIdentifiers'][0]['legalName'],
                        "uri": payload['tender']['procuringEntity']['additionalIdentifiers'][0]['uri']
                    }],
                    "contactPoint": {
                        "name": payload['tender']['procuringEntity']['contactPoint']['name'],
                        "email": payload['tender']['procuringEntity']['contactPoint']['email'],
                        "telephone": payload['tender']['procuringEntity']['contactPoint']['telephone'],
                        "faxNumber": payload['tender']['procuringEntity']['contactPoint']['faxNumber'],
                        "url": payload['tender']['procuringEntity']['contactPoint']['url']
                    },
                    "roles": ["procuringEntity"]
                }],
                "relatedProcesses": [{
                    "id": actual_result['releases'][0]['relatedProcesses'][0]['id'],
                    "relationship": ["planning"],
                    "scheme": "ocid",
                    "identifier": message_from_kafka['data']['outcomes']['pn'][0]['id'],
                    "uri": f"{message_from_kafka['data']['url']}/"
                           f"{message_from_kafka['data']['outcomes']['pn'][0]['id']}"
                }, {
                    "id": actual_result['releases'][0]['relatedProcesses'][1]['id'],
                    "relationship": ["x_expenditureItem"],
                    "scheme": "ocid",
                    "identifier": ei_id,
                    "uri": f"http://dev.public.eprocurement.systems/budgets/{ei_id}/{ei_id}"
                }, {
                    "id": actual_result['releases'][0]['relatedProcesses'][2]['id'],
                    "relationship": ["x_fundingSource"],
                    "scheme": "ocid",
                    "identifier": payload["planning"]["budget"]["budgetBreakdown"][0]['id'],
                    "uri": f"http://dev.public.eprocurement.systems/budgets/{ei_id}/"
                           f"{payload['planning']['budget']['budgetBreakdown'][0]['id']}"
                }]
            }]
        }
        compare_releases = DeepDiff(expected_result, actual_result)
        assert compare_actual_result_and_expected_result(
            expected_result={},
            actual_result=compare_releases
        )

    @pytestrail.case("27588")
    def test_check_on_the_platform_data_has_been_transferred_and_displayed_correctly_in_the_pn_release_27588_344(
            self, language, pmd):
        message_from_kafka = CreatePn.message_from_kafka
        url_create_pn = message_from_kafka['data']['url'] + "/" + message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create_pn).json()
        payload = CreatePn.payload
        mdm = MdmService(
            instance="dev",
            lang="ro",
            procuring_address_details_country_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["country"]["id"],
            procuring_address_details_region_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["region"]["id"],
            procuring_address_details_locality_scheme=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["scheme"],
            procuring_address_details_locality_id=payload["tender"]["procuringEntity"]["address"][
                "addressDetails"]["locality"]["id"],
            pn_lot_address_details_country_id=payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['country']['id'],
            pn_lot_address_details_region_id=payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['region']['id'],
            pn_lot_address_details_locality_id=payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['locality']['id'],
            pn_lot_address_details_locality_scheme=payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['locality']['scheme']
        )
        data = mdm.process_tender_data(pmd).json()
        first_lot_country_from_mdm = \
            data["data"]["tender"]["lots"][0]['placeOfPerformance']['address']['addressDetails']['country']
        first_lot_region_from_mdm = \
            data["data"]["tender"]["lots"][0]['placeOfPerformance']['address']['addressDetails']['region']
        first_lot_locality_from_mdm = \
            data["data"]["tender"]["lots"][0]['placeOfPerformance']['address']['addressDetails']['locality']
        second_lot_country_from_mdm = \
            data["data"]["tender"]["lots"][1]['placeOfPerformance']['address']['addressDetails']['country']
        second_lot_region_from_mdm = \
            data["data"]["tender"]["lots"][1]['placeOfPerformance']['address']['addressDetails']['region']
        second_lot_locality_from_mdm = \
            data["data"]["tender"]["lots"][1]['placeOfPerformance']['address']['addressDetails']['locality']

        submissionMethodDetails = data["data"]["tender"]["submissionMethodDetails"]
        submissionMethodRationale = data["data"]["tender"]["submissionMethodRationale"]
        calculate_new_cpv_code = get_new_classification_id(
            payload['tender']['items'][0]['classification']['id'],
            payload['tender']['items'][1]['classification']['id']
        )
        get_value_by_new_cpv_code = get_value_from_classification_cpv_dictionary_xls(
            calculate_new_cpv_code,
            language
        )
        get_value_by_first_item_cpv_code = get_value_from_classification_cpv_dictionary_xls(
            payload['tender']['items'][0]['classification']['id'],
            language
        )
        get_value_by_second_item_cpv_code = get_value_from_classification_cpv_dictionary_xls(
            payload['tender']['items'][1]['classification']['id'],
            language
        )
        get_value_by_first_item_cpvs_code = get_value_from_cpvs_dictionary_csv(
            payload['tender']['items'][0]['additionalClassifications'][0]['id'],
            language
        )
        get_value_by_second_item_cpvs_code = get_value_from_cpvs_dictionary_csv(
            payload['tender']['items'][1]['additionalClassifications'][0]['id'],
            language
        )
        get_value_by_first_item_unit_id = get_value_from_classification_unit_dictionary_csv(
            payload['tender']['items'][0]['unit']['id'],
            language
        )
        get_value_by_second_item_unit_id = get_value_from_classification_unit_dictionary_csv(
            payload['tender']['items'][1]['unit']['id'],
            language
        )
        actual_result = pn_release
        expected_result = {
            "uri": f"http://dev.public.eprocurement.systems/tenders/{message_from_kafka['data']['ocid']}/"
                   f"{message_from_kafka['data']['outcomes']['pn'][0]['id']}",
            "version": "1.1",
            "extensions": [
                "https://raw.githubusercontent.com/open-contracting/ocds_bid_extension/v1.1.1/extension.json",
                "https://raw.githubusercontent.com/open-contracting/ocds_enquiry_extension/v1.1.1/extension.js"],
            "publisher": {
                "name": "M-Tender",
                "uri": "https://www.mtender.gov.md"
            },
            "license": "http://opendefinition.org/licenses/",
            "publicationPolicy": "http://opendefinition.org/licenses/",
            "publishedDate": message_from_kafka['data']['operationDate'],
            "releases": [{
                "ocid": message_from_kafka['data']['outcomes']['pn'][0]['id'],
                "id": f"{message_from_kafka['data']['outcomes']['pn'][0]['id']}-"
                      f"{message_from_kafka['data']['outcomes']['pn'][0]['id'][32:45]}",
                "date": message_from_kafka['data']['operationDate'],
                "tag": ["planning"],
                "language": language,
                "initiationType": "tender",
                "tender": {
                    "id": actual_result['releases'][0]['tender']['id'],
                    "title": "Planning Notice",
                    "description": "Contracting process is planned",
                    "status": "planning",
                    "statusDetails": "planning",
                    "items": [{
                        "id": actual_result['releases'][0]['tender']['items'][0]['id'],
                        "internalId": payload['tender']['items'][0]['internalId'],
                        "description": payload['tender']['items'][0]['description'],
                        "classification": {
                            "scheme": "CPV",
                            "id": payload['tender']['items'][0]['classification']['id'],
                            "description": get_value_by_first_item_cpv_code[1]
                        },
                        "additionalClassifications": [{
                            "scheme": "CPVS",
                            "id": payload['tender']['items'][0]['additionalClassifications'][0]['id'],
                            "description": get_value_by_first_item_cpvs_code[2]
                        }],
                        "quantity": payload['tender']['items'][0]['quantity'],
                        "unit": {
                            "name": get_value_by_first_item_unit_id[1],
                            "id": payload['tender']['items'][0]['unit']['id']
                        },
                        "relatedLot": actual_result['releases'][0]['tender']['lots'][0]['id']
                    }, {
                        "id": actual_result['releases'][0]['tender']['items'][1]['id'],
                        "internalId": payload['tender']['items'][1]['internalId'],
                        "description": payload['tender']['items'][1]['description'],
                        "classification": {
                            "scheme": "CPV",
                            "id": payload['tender']['items'][1]['classification']['id'],
                            "description": get_value_by_second_item_cpv_code[1]
                        },
                        "additionalClassifications": [{
                            "scheme": "CPVS",
                            "id": payload['tender']['items'][1]['additionalClassifications'][0]['id'],
                            "description": get_value_by_second_item_cpvs_code[2]
                        }],
                        "quantity": payload['tender']['items'][1]['quantity'],
                        "unit": {
                            "name": get_value_by_second_item_unit_id[1],
                            "id": payload['tender']['items'][1]['unit']['id']
                        },
                        "relatedLot": actual_result['releases'][0]['tender']['lots'][1]['id']
                    }],
                    "lots": [{
                        "id": actual_result['releases'][0]['tender']['lots'][0]['id'],
                        "internalId": payload['tender']['lots'][0]['internalId'],
                        "title": payload['tender']['lots'][0]['title'],
                        "description": payload['tender']['lots'][0]['description'],
                        "status": "planning",
                        "statusDetails": "empty",
                        "value": {
                            "amount": payload['tender']['lots'][0]['value']['amount'],
                            "currency": payload['tender']['lots'][0]['value']['currency']
                        },
                        "recurrentProcurement": [{
                            "isRecurrent": False
                        }],
                        "renewals": [{
                            "hasRenewals": False
                        }],
                        "variants": [{
                            "hasVariants": False
                        }],
                        "contractPeriod": {
                            "startDate": payload['tender']['lots'][0]['contractPeriod']['startDate'],
                            "endDate": payload['tender']['lots'][0]['contractPeriod']['endDate']
                        },
                        "placeOfPerformance": {
                            "address": {
                                "streetAddress": payload['tender']['lots'][0]['placeOfPerformance']['address'][
                                    'streetAddress'],
                                "postalCode": payload['tender']['lots'][0]['placeOfPerformance']['address'][
                                    'postalCode'],
                                "addressDetails": {
                                    "country": {
                                        "scheme": first_lot_country_from_mdm['scheme'],
                                        "id": payload['tender']['lots'][0]['placeOfPerformance']['address'][
                                            'addressDetails']['country']['id'],
                                        "description": first_lot_country_from_mdm['description'],
                                        "uri": first_lot_country_from_mdm['uri']
                                    },
                                    "region": {
                                        "scheme": first_lot_region_from_mdm['scheme'],
                                        "id": payload['tender']['lots'][0]['placeOfPerformance']['address'][
                                            'addressDetails']['region']['id'],
                                        "description": first_lot_region_from_mdm['description'],
                                        "uri": first_lot_region_from_mdm['uri']
                                    },
                                    "locality": {
                                        "scheme": payload['tender']['lots'][0]['placeOfPerformance']['address'][
                                            'addressDetails']['locality']['scheme'],
                                        "id": payload['tender']['lots'][0]['placeOfPerformance']['address'][
                                            'addressDetails']['locality']['id'],
                                        "description": first_lot_locality_from_mdm['description'],
                                        "uri": first_lot_locality_from_mdm['uri']
                                    }
                                }
                            },
                            "description": payload['tender']['lots'][0]['placeOfPerformance']['description']
                        },
                        "options": [{
                            "hasOptions": False
                        }]
                    }, {
                        "id": actual_result['releases'][0]['tender']['lots'][1]['id'],
                        "internalId": payload['tender']['lots'][1]['internalId'],
                        "title": payload['tender']['lots'][1]['title'],
                        "description": payload['tender']['lots'][1]['description'],
                        "status": "planning",
                        "statusDetails": "empty",
                        "value": {
                            "amount": payload['tender']['lots'][1]['value']['amount'],
                            "currency": payload['tender']['lots'][1]['value']['currency']
                        },
                        "recurrentProcurement": [{
                            "isRecurrent": False
                        }],
                        "renewals": [{
                            "hasRenewals": False
                        }],
                        "variants": [{
                            "hasVariants": False
                        }],
                        "contractPeriod": {
                            "startDate": payload['tender']['lots'][1]['contractPeriod']['startDate'],
                            "endDate": payload['tender']['lots'][1]['contractPeriod']['endDate']
                        },
                        "placeOfPerformance": {
                            "address": {
                                "streetAddress": payload['tender']['lots'][1]['placeOfPerformance']['address'][
                                    'streetAddress'],
                                "postalCode": payload['tender']['lots'][1]['placeOfPerformance']['address'][
                                    'postalCode'],
                                "addressDetails": {
                                    "country": {
                                        "scheme": second_lot_country_from_mdm['scheme'],
                                        "id": payload['tender']['lots'][1]['placeOfPerformance']['address'][
                                            'addressDetails']['country']['id'],
                                        "description": second_lot_country_from_mdm['description'],
                                        "uri": second_lot_country_from_mdm['uri']
                                    },
                                    "region": {
                                        "scheme": second_lot_region_from_mdm['scheme'],
                                        "id": payload['tender']['lots'][1]['placeOfPerformance']['address'][
                                            'addressDetails']['region']['id'],
                                        "description": second_lot_region_from_mdm['description'],
                                        "uri": second_lot_region_from_mdm['uri']
                                    },
                                    "locality": {
                                        "scheme": payload['tender']['lots'][1]['placeOfPerformance']['address'][
                                            'addressDetails']['locality']['scheme'],
                                        "id": payload['tender']['lots'][1]['placeOfPerformance']['address'][
                                            'addressDetails']['locality']['id'],
                                        "description": second_lot_locality_from_mdm['description'],
                                        "uri": second_lot_locality_from_mdm['uri']
                                    }
                                }
                            },
                            "description": payload['tender']['lots'][1]['placeOfPerformance']['description']
                        },
                        "options": [{
                            "hasOptions": False
                        }]
                    }],
                    "lotGroups": [{
                        "optionToCombine": False
                    }],
                    "tenderPeriod": {
                        "startDate": payload['tender']['tenderPeriod']['startDate']
                    },
                    "hasEnquiries": False,
                    "documents": [{
                        "id": payload['tender']['documents'][0]['id'],
                        "documentType": payload['tender']['documents'][0]['documentType'],
                        "title": payload['tender']['documents'][0]['title'],
                        "description": payload['tender']['documents'][0]['description'],
                        "url": f"https://dev.bpe.eprocurement.systems/api/v1/storage/get/"
                               f"{payload['tender']['documents'][0]['id']}",
                        "datePublished": message_from_kafka['data']['operationDate'],
                        "relatedLots": [actual_result['releases'][0]['tender']['lots'][0]['id']]
                    }, {
                        "id": payload['tender']['documents'][1]['id'],
                        "documentType": payload['tender']['documents'][1]['documentType'],
                        "title": payload['tender']['documents'][1]['title'],
                        "description": payload['tender']['documents'][1]['description'],
                        "url": f"https://dev.bpe.eprocurement.systems/api/v1/storage/get/"
                               f"{payload['tender']['documents'][1]['id']}",
                        "datePublished": message_from_kafka['data']['operationDate'],
                        "relatedLots": [actual_result['releases'][0]['tender']['lots'][1]['id']]
                    }],
                    "submissionMethod": ["electronicSubmission"],
                    "submissionMethodDetails": submissionMethodDetails,
                    "submissionMethodRationale": submissionMethodRationale,
                    "requiresElectronicCatalogue": False,
                    "procurementMethodRationale": payload['tender']['procurementMethodRationale'],
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_new_cpv_code[0],
                        "description": get_value_by_new_cpv_code[1]
                    },
                    "value": {
                        "amount": payload['tender']['lots'][0]['value']['amount'] + payload['tender']['lots'][1][
                            'value']['amount'],
                        "currency": payload['tender']['lots'][0]['value']['currency']
                    }
                },
                "hasPreviousNotice": False,
                "purposeOfNotice": {
                    "isACallForCompetition": False
                },
                "relatedProcesses": [{
                    "id": actual_result['releases'][0]['relatedProcesses'][0]['id'],
                    "relationship": ["parent"],
                    "scheme": "ocid",
                    "identifier": message_from_kafka['data']['ocid'],
                    "uri": f"http://dev.public.eprocurement.systems/tenders/{message_from_kafka['data']['ocid']}/"
                           f"{message_from_kafka['data']['ocid']}"
                }]
            }]
        }
        compare_releases = DeepDiff(expected_result, actual_result)
        assert compare_actual_result_and_expected_result(
            expected_result={},
            actual_result=compare_releases
        )
