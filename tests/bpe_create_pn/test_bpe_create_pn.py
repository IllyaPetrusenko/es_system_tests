import copy
from uuid import uuid4
import requests
from pytest_testrail.plugin import pytestrail
from tests.conftest import CreatePn, language
from tests.essences.pn import PN
from tests.payloads.pn_payload import create_pn_payload_obligatory_data_model_without_documents
from useful_functions import prepared_cp_id, compare_actual_result_and_expected_result, get_human_date_in_utc_format, \
    is_it_uuid


class TestCheckThePossibilityOfPlanningNoticeCreationWithoutOptionalFields(object):
    @pytestrail.case("27585")
    def test_send_request_see_result_in_feed_point_27585_1(self, country, language, instance, cassandra_username,
                                                           cassandra_password, pmd):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(create_pn_payload_obligatory_data_model_without_documents)
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
            cp_id=cp_id,
            ei_token=ei_token
        )
        pn.create_pn(fs_id=create_fs_response[1])
        pn.get_message_from_kafka()
        CreatePn.message_from_kafka = pn.get_message_from_kafka()
        CreatePn.payload = payload
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
                            "extension.js222",
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
            actual_result=pn_release["releases"][0]["tender"]["submissionMethod"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_submission_method_details_0_on_pp_pn_release_27585_26(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="Lista platformelor: achizitii, ebs, licitatie, yptender",
            actual_result=pn_release["releases"][0]["tender"]["submissionMethodDetails"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_tender_submission_method_rationale_0_on_pp_pn_release_27585_27(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['outcomes']['pn'][0]['id']
        pn_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result="Ofertele vor fi primite prin intermediul unei platforme electronice de achiziții publice",
            actual_result=pn_release["releases"][0]["tender"]["submissionMethodRationale"]
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
            expected_result=f"http://dev.public.eprocurement.systems/tenders/{url_create}",
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
                            "extension.js222",
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
    def test_check_releases_0_language_on_pp_ms_release_27585_54(self):
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
            expected_result=fs_release["releases"][0]["planning"]["budget"]["isEuropeanUnionFunded"],
            actual_result=ms_release["releases"][0]["planning"]["budget"]["isEuropeanUnionFunded"]
        )

    @pytestrail.case("27585")
    def test_check_releases_0_planning_budget_is_european_union_funded_on_pp_ms_release_27585_59(self):
        url_create = CreatePn.message_from_kafka['data']['url'] + "/" + \
                     CreatePn.message_from_kafka['data']['ocid']
        ms_release = requests.get(url=url_create).json()
        assert compare_actual_result_and_expected_result(
            expected_result=str(False),
            actual_result=str(ms_release["releases"][0]["planning"]["budget"]["isEuropeanUnionFunded"])
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
