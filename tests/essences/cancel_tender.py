import fnmatch
import json
import uuid
from uuid import uuid4, uuid1

import allure
import requests
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster

from tests.authorization import get_access_token_for_platform_one, get_x_operation_id
from tests.iMDM_service.get_information import MdmService
from tests.iStorage import Document
from tests.kafka_messages import get_message_from_kafka
from tests.kafka_session import Kafka
from useful_functions import get_period, get_access_token_for_platform_two, is_it_uuid, prepared_fs_oc_id, \
    prepared_cp_id, prepared_pn_oc_id, get_new_classification_id, get_value_from_classification_cpv_dictionary_xls, \
    get_value_from_cpvs_dictionary_csv, get_value_from_classification_unit_dictionary_csv, get_contract_period, \
    get_human_date_in_utc_format, create_enquiry_and_tender_period, prepared_cn_oc_id, \
    time_at_now, get_auction_date, get_timestamp_from_human_date, get_period_for_amendment


class CancelTender:
    def __init__(self, instance, cassandra_username, cassandra_password, pmd, country='MD', payload=None,
                 lang='ro', tender_classification_id="45100000-8",
                 tender_item_classification_id="45100000-8", planning_budget_id="45100000-8",
                 platform="platform_one", amount=9000.00, currency="EUR",
                 tender_classification_scheme="CPV", planning_budget_period_start_date=get_period()[0],
                 tender_classification_description="Lucrări de pregătire a şantierului",
                 planning_budget_period_end_date=get_period()[1], buyer_name="LLC Petrusenko",
                 buyer_identifier_id="1", buyer_identifier_scheme="MD-IDNO",
                 buyer_identifier_legal_name="LLC Petrusenko", buyer_identifier_uri="http://petrusenko.com/fop",
                 buyer_address_street_address="Zakrevskogo", buyer_address_address_details_country_id="MD",
                 buyer_address_address_details_region_id="1700000", buyer_address_address_details_locality_id="1701000",
                 buyer_address_address_details_locality_scheme="CUATM", buyer_contact_point_email="svetik@gmail.com",
                 buyer_address_address_details_locality_description="mun.Cahul", buyer_contact_point_telephone="123",
                 buyer_contact_point_name="Petrusenko Svitlana", buyer_contact_point_fax_number="5552233",
                 buyer_contact_point_url="http://petrusenko.com/svetlana", buyer_address_postal_code="02217",
                 tender_description="description of finansical sourse", tender_title="EI_FULL_WORKS",
                 planning_rationale="planning.rationale", tender_items_description="item 1",
                 tender_items_additional_classifications_id="AA12-4", funder_name="Petro Oleksievich",
                 tender_items_delivery_details_country_id="MD", funder_identifier_scheme="MD-IDNO",
                 tender_items_delivery_details_country_scheme="iso-alpha2", funder_identifier_id="3",
                 tender_items_delivery_details_country_description="Moldova, Republica",
                 tender_items_delivery_details_country_uri="https://www.iso.org",
                 funder_identifier_uri="http://buyer.com",
                 tender_items_delivery_details_region_id="0101000", funder_identifier_legal_name="Petro",
                 tender_items_delivery_details_region_scheme="CUATM", funder_address_street="Baseyna",
                 tender_items_delivery_details_region_description="mun.Chişinău",
                 tender_items_delivery_details_region_uri="http://statistica.md",
                 tender_items_delivery_details_locality_id="0101000",
                 tender_items_delivery_details_locality_scheme="CUATM",
                 tender_items_delivery_details_locality_description="mun.Chişinău",
                 tender_items_delivery_details_locality_uri="http://statistica.md",
                 tender_items_delivery_street="Khreshchatyk", tender_items_delivery_postal="01124",
                 tender_items_unit_name="Parsec", tender_items_unit_id="10", tender_items_quantity=10.00,
                 tender_items_id="6a565c47-ff11-4e2d-8ea1-3f34c5d751f9", payer_identifier_uri="ww#tt",
                 funder_address_address_details_locality_description="mun.Cahul", payer_contact_point_url="777@hj",
                 funder_address_address_details_locality_id="1701000", payer_contact_point_fax_number="77777",
                 funder_address_address_details_locality_scheme="CUATM", payer_identifier_scheme="MD-IDNO",
                 funder_address_address_details_region_id="1700000", payer_identifier_id="2",
                 funder_address_address_details_country_id="MD", funder_contact_point_telephone="123",
                 funder_contact_point_fax="147", funder_contact_point_url="www@11,io",
                 funder_contact_point_name="OKSANA", funder_contact_point_email="OKSANA@gmail.com",
                 payer_contact_point_email="papa@gmail.com", payer_contact_point_name="KOliya",
                 payer_contact_point_telephone="0446789877", payer_address_address_details_country_id="MD",
                 payer_address_address_details_region_id="1700000", payer_name="Slava",
                 payer_address_address_details_locality_scheme="CUATM", payer_identifier_legal_name="ZamGar",
                 payer_address_address_details_locality_id="1701000", payer_address_street="Grisuka",
                 payer_address_address_details_locality_description="mun.Cahul",
                 payer_address_postal_code="44444", funder_address_postal_code="44444", first_item_cpv="45112350-3",
                 second_item_cpv="45112360-6", first_item_additional_classifications="AA12-4",
                 second_item_additional_classifications="AA12-4", first_item_unit_id="10", second_item_unit_id="10",
                 procuring_entity_address_address_details_country_id="MD",
                 procuring_entity_address_address_details_region_id="1700000",
                 procuring_entity_address_address_details_locality_id="1701000", document_one_id=None,
                 document_two_id=None, document_three_id=None, document_four_id=None, document_five_id=None):
        self.payload = payload
        self.amendment_token = f"{uuid4()}"
        self.amendment_id = f"{uuid4()}"
        self.procuring_entity_address_address_details_country_id = procuring_entity_address_address_details_country_id
        self.procuring_entity_address_address_details_region_id = procuring_entity_address_address_details_region_id
        self.procuring_entity_address_address_details_locality_id = procuring_entity_address_address_details_locality_id
        self.second_item_unit_id = second_item_unit_id
        self.first_item_unit_id = first_item_unit_id
        self.second_item_additional_classifications = second_item_additional_classifications
        self.first_item_additional_classifications = first_item_additional_classifications
        self.second_item_cpv = second_item_cpv
        self.first_item_cpv = first_item_cpv
        self.funder_identifier_uri = funder_identifier_uri
        self.funder_contact_point_url = funder_contact_point_url
        self.funder_contact_point_fax = funder_contact_point_fax
        self.funder_address_postal_code = funder_address_postal_code
        self.payer_contact_point_fax_number = payer_contact_point_fax_number
        self.payer_contact_point_url = payer_contact_point_url
        self.funder_contact_point_email = funder_contact_point_email
        self.funder_contact_point_name = funder_contact_point_name
        self.funder_contact_point_telephone = funder_contact_point_telephone
        self.funder_address_address_details_country_id = funder_address_address_details_country_id
        self.funder_address_address_details_region_id = funder_address_address_details_region_id
        self.funder_address_address_details_locality_scheme = funder_address_address_details_locality_scheme
        self.funder_address_address_details_locality_id = funder_address_address_details_locality_id
        self.funder_address_address_details_locality_description = funder_address_address_details_locality_description
        self.funder_address_street = funder_address_street
        self.funder_identifier_legal_name = funder_identifier_legal_name
        self.funder_name = funder_name
        self.funder_identifier_id = funder_identifier_id
        self.funder_identifier_scheme = funder_identifier_scheme

        self.payer_contact_point_email = payer_contact_point_email
        self.payer_contact_point_name = payer_contact_point_name
        self.payer_contact_point_telephone = payer_contact_point_telephone
        self.payer_address_address_details_country_id = payer_address_address_details_country_id
        self.payer_address_address_details_region_id = payer_address_address_details_region_id
        self.payer_address_address_details_locality_scheme = payer_address_address_details_locality_scheme
        self.payer_address_address_details_locality_id = payer_address_address_details_locality_id
        self.payer_address_address_details_locality_description = payer_address_address_details_locality_description
        self.payer_address_street = payer_address_street
        self.payer_address_postal_code = payer_address_postal_code
        self.payer_identifier_legal_name = payer_identifier_legal_name
        self.payer_identifier_uri = payer_identifier_uri
        self.payer_name = payer_name
        self.payer_identifier_id = payer_identifier_id
        self.payer_identifier_scheme = payer_identifier_scheme
        self.amount = amount
        self.currency = currency
        self.tender_items_id = tender_items_id
        self.tender_items_unit_name = tender_items_unit_name
        self.tender_items_unit_id = tender_items_unit_id
        self.tender_items_quantity = tender_items_quantity
        self.tender_items_delivery_postal = tender_items_delivery_postal
        self.tender_items_delivery_street = tender_items_delivery_street
        self.tender_items_delivery_details_locality_uri = tender_items_delivery_details_locality_uri
        self.tender_items_delivery_details_locality_description = tender_items_delivery_details_locality_description
        self.tender_items_delivery_details_locality_scheme = tender_items_delivery_details_locality_scheme
        self.tender_items_delivery_details_locality_id = tender_items_delivery_details_locality_id
        self.tender_items_delivery_details_region_uri = tender_items_delivery_details_region_uri
        self.tender_items_delivery_details_region_description = tender_items_delivery_details_region_description
        self.tender_items_delivery_details_region_scheme = tender_items_delivery_details_region_scheme
        self.tender_items_delivery_details_region_id = tender_items_delivery_details_region_id
        self.tender_items_delivery_details_country_uri = tender_items_delivery_details_country_uri
        self.tender_items_delivery_details_country_description = tender_items_delivery_details_country_description
        self.tender_items_delivery_details_country_scheme = tender_items_delivery_details_country_scheme
        self.tender_items_delivery_details_country_id = tender_items_delivery_details_country_id
        self.tender_items_additional_classifications_id = tender_items_additional_classifications_id
        self.tender_items_description = tender_items_description
        self.planning_rationale = planning_rationale
        self.tender_title = tender_title
        self.tender_description = tender_description
        self.buyer_address_postal_code = buyer_address_postal_code
        self.buyer_contact_point_url = buyer_contact_point_url
        self.buyer_contact_point_fax_number = buyer_contact_point_fax_number
        self.buyer_contact_point_telephone = buyer_contact_point_telephone
        self.buyer_contact_point_email = buyer_contact_point_email
        self.buyer_contact_point_name = buyer_contact_point_name
        self.buyer_address_address_details_locality_description = buyer_address_address_details_locality_description
        self.buyer_address_address_details_locality_id = buyer_address_address_details_locality_id
        self.buyer_address_address_details_locality_scheme = buyer_address_address_details_locality_scheme
        self.buyer_address_address_details_region_id = buyer_address_address_details_region_id
        self.buyer_address_address_details_country_id = buyer_address_address_details_country_id
        self.buyer_address_street_address = buyer_address_street_address
        self.buyer_identifier_uri = buyer_identifier_uri
        self.buyer_identifier_legal_name = buyer_identifier_legal_name
        self.buyer_identifier_scheme = buyer_identifier_scheme
        self.buyer_identifier_id = buyer_identifier_id
        self.buyer_name = buyer_name
        self.planning_budget_period_end_date = planning_budget_period_end_date
        self.planning_budget_period_start_date = planning_budget_period_start_date
        self.tender_classification_description = tender_classification_description
        self.tender_classification_scheme = tender_classification_scheme
        self.tender_classification_id = tender_classification_id
        self.tender_item_classification_id = tender_item_classification_id
        self.planning_budget_id = planning_budget_id
        self.country = country
        self.lang = lang
        self.instance = instance
        self.pmd = pmd
        self.cassandra_username = cassandra_username
        self.cassandra_password = cassandra_password
        if instance == "dev":
            self.cassandra_cluster = "10.0.20.104"
            self.host_of_request = "http://10.0.20.126:8900/api/v1"
            self.host_of_services = "http://10.0.20.126"
            if platform == "platform_one":
                self.access_token = get_access_token_for_platform_one(self.host_of_request)
                self.x_operation_id = get_x_operation_id(host=self.host_of_request, platform_token=self.access_token)
            elif platform == "platform_two":
                self.access_token = get_access_token_for_platform_two(self.host_of_request)
                self.x_operation_id = get_x_operation_id(host=self.host_of_request, platform_token=self.access_token)
            else:
                self.access_token = get_access_token_for_platform_one(self.host_of_request)
                self.x_operation_id = get_x_operation_id(host=self.host_of_request, platform_token=self.access_token)
                self.access_token = platform
        elif instance == "sandbox":
            self.cassandra_cluster = "10.0.10.106"
            self.host_of_request = "http://10.0.10.116:8900/api/v1"
            self.host_of_services = "http://10.0.10.116"
            if platform == "platform_one":
                self.access_token = get_access_token_for_platform_one(self.host_of_request)
                self.x_operation_id = get_x_operation_id(host=self.host_of_request, platform_token=self.access_token)
            elif platform == "platform_two":
                self.access_token = get_access_token_for_platform_two(self.host_of_request)
                self.x_operation_id = get_x_operation_id(host=self.host_of_request, platform_token=self.access_token)
            else:
                self.access_token = get_access_token_for_platform_two(self.host_of_request)
                self.x_operation_id = get_x_operation_id(host=self.host_of_request, platform_token=self.access_token)
                self.access_token = platform
        if document_one_id is None and document_two_id is None:
            document = Document(instance=instance)
            self.document_one_was_uploaded = document.uploading_document()[0]["data"]["id"]
            self.document_two_was_uploaded = document.uploading_document()[0]["data"]["id"]
        else:
            self.document_one_was_uploaded = document_one_id
            self.document_two_was_uploaded = document_two_id
        if document_three_id is None:
            document = Document(instance=instance)
            self.document_three_was_uploaded = document.uploading_document()[0]["data"]["id"]
        else:
            self.document_three_was_uploaded = document_three_id
        if document_four_id is None:
            document = Document(instance=instance)
            self.document_four_was_uploaded = document.uploading_document()[0]["data"]["id"]
        else:
            self.document_four_was_uploaded = document_four_id
        if document_five_id is None:
            document = Document(instance=instance)
            self.document_five_was_uploaded = document.uploading_document()[0]["data"]["id"]
        else:
            self.document_five_was_uploaded = document_four_id

    @allure.step('Cancel tender')
    def cancel_tender(self, cp_id, ev_id, pn_token):
        tender = requests.post(
            url=self.host_of_request + f"/cancel/tender/{cp_id}/{ev_id}",
            headers={
                'Authorization': 'Bearer ' + self.access_token,
                'X-OPERATION-ID': self.x_operation_id,
                'Content-Type': 'application/json',
                'X-TOKEN': f'{pn_token}'},
            json=self.payload)
        allure.attach(self.host_of_request + "/cancel/tender/", 'URL')
        allure.attach(json.dumps(self.payload), 'Prepared payload')
        return tender

    @allure.step('Cancel lot')
    def cancel_lot(self, cp_id, ev_id, pn_token, lot_id):
        tender = requests.post(
            url=self.host_of_request + f"/cancel/lot/{cp_id}/{ev_id}/{lot_id}",
            headers={
                'Authorization': 'Bearer ' + self.access_token,
                'X-OPERATION-ID': self.x_operation_id,
                'Content-Type': 'application/json',
                'X-TOKEN': f'{pn_token}'},
            json=self.payload)
        allure.attach(self.host_of_request + "/cancel/lot/", 'URL')
        allure.attach(json.dumps(self.payload), 'Prepared payload')
        return tender

    @allure.step('Confirm tender cancellation')
    def confirm_tender_cancellation(self, cp_id, ev_id):
        tender = requests.post(
            url=self.host_of_request + f"/confirm/amendment/{cp_id}/{ev_id}/{self.amendment_id}",
            headers={
                'Authorization': 'Bearer ' + self.access_token,
                'X-OPERATION-ID': self.x_operation_id,
                'Content-Type': 'application/json',
                'X-TOKEN': f'{self.amendment_token}'})
        allure.attach(self.host_of_request + "/confirm/amendment/", 'URL')
        return tender

    @allure.step('Cancel tender cancellation')
    def tender_amendment_cancellation(self, cp_id, ev_id):
        tender = requests.post(
            url=self.host_of_request + f"/cancel/amendment/{cp_id}/{ev_id}/{self.amendment_id}",
            headers={
                'Authorization': 'Bearer ' + self.access_token,
                'X-OPERATION-ID': self.x_operation_id,
                'Content-Type': 'application/json',
                'X-TOKEN': f'{self.amendment_token}'})
        allure.attach(self.host_of_request + "/cancel/amendment/", 'URL')
        return tender

    @allure.step('Receive message in feed-point')
    def get_message_from_kafka(self):
        message_from_kafka = get_message_from_kafka(self.x_operation_id)
        allure.attach(json.dumps(message_from_kafka), 'Message in feed-point')
        return message_from_kafka

    def check_on_that_message_is_successfully_cancel_tender(self, cp_id, ev_id):
        instance_url = None
        if self.instance == "dev":
            instance_url = "http://dev.public.eprocurement.systems/tenders/"
        if self.instance == "sandbox":
            instance_url = "http://public.eprocurement.systems/tenders/"
        message = get_message_from_kafka(self.x_operation_id)
        check_x_operation_id = is_it_uuid(message["X-OPERATION-ID"], 4)
        check_x_response_id = is_it_uuid(message["X-RESPONSE-ID"], 4)
        check_initiator = fnmatch.fnmatch(message["initiator"], "platform")
        check_oc_id = fnmatch.fnmatch(message["data"]["ocid"], f"{ev_id}")
        check_url = fnmatch.fnmatch(message["data"]["url"],
                                    f"{instance_url}{cp_id}/{ev_id}")
        check_operation_date = fnmatch.fnmatch(message["data"]["operationDate"], "202*-*-*T*:*:*Z")
        check_amendments = is_it_uuid(message["data"]['outcomes']['amendments'][0]['id'], 4)
        check_amendments_token = is_it_uuid(message["data"]['outcomes']['amendments'][0]["X-TOKEN"], 4)
        if check_x_operation_id is True and check_x_response_id is True and check_initiator is True and \
                check_oc_id is True and check_url is True and check_operation_date is True and \
                check_amendments is True and check_amendments_token is True:
            return True
        else:
            return False

    def check_on_that_message_is_successfully_tender_amendment_confirmation(self, cp_id, ev_id):
        instance_url = None
        if self.instance == "dev":
            instance_url = "http://dev.public.eprocurement.systems/tenders/"
        if self.instance == "sandbox":
            instance_url = "http://public.eprocurement.systems/tenders/"
        message = get_message_from_kafka(self.x_operation_id)
        check_x_operation_id = is_it_uuid(message["X-OPERATION-ID"], 4)
        check_x_response_id = is_it_uuid(message["X-RESPONSE-ID"], 4)
        check_initiator = fnmatch.fnmatch(message["initiator"], "platform")
        check_oc_id = fnmatch.fnmatch(message["data"]["ocid"], f"{ev_id}")
        check_url = fnmatch.fnmatch(message["data"]["url"],
                                    f"{instance_url}{cp_id}/{ev_id}")
        check_operation_date = fnmatch.fnmatch(message["data"]["operationDate"], "202*-*-*T*:*:*Z")
        for i in message["data"]:
            if i == 'outcomes':
                raise Exception("Check message in kafka topic")
        if check_x_operation_id is True and check_x_response_id is True and check_initiator is True and \
                check_oc_id is True and check_url is True and check_operation_date is True:
            return True
        else:
            return False

    def check_on_that_message_is_successfully_tender_amendment_cancellation(self, cp_id, ev_id):
        instance_url = None
        if self.instance == "dev":
            instance_url = "http://dev.public.eprocurement.systems/tenders/"
        if self.instance == "sandbox":
            instance_url = "http://public.eprocurement.systems/tenders/"
        message = get_message_from_kafka(self.x_operation_id)
        check_x_operation_id = is_it_uuid(message["X-OPERATION-ID"], 4)
        check_x_response_id = is_it_uuid(message["X-RESPONSE-ID"], 4)
        check_initiator = fnmatch.fnmatch(message["initiator"], "platform")
        check_oc_id = fnmatch.fnmatch(message["data"]["ocid"], f"{ev_id}")
        check_url = fnmatch.fnmatch(message["data"]["url"],
                                    f"{instance_url}{cp_id}/{ev_id}")
        check_operation_date = fnmatch.fnmatch(message["data"]["operationDate"], "202*-*-*T*:*:*Z")
        for i in message["data"]:
            if i == 'outcomes':
                raise Exception("Check message in kafka topic")
        if check_x_operation_id is True and check_x_response_id is True and check_initiator is True and \
                check_oc_id is True and check_url is True and check_operation_date is True:
            return True
        else:
            return False

    @allure.step('Insert CnOnPn: based on FS: own - full, based on EI: with items - full')
    def insert_cancel_tender_full(self, first_lot_id, second_lot_id, first_item_id, second_item_id,
                                  second_tender, second_enquiry):
        auth_provider = PlainTextAuthProvider(username=self.cassandra_username, password=self.cassandra_password)
        cluster = Cluster([self.cassandra_cluster], auth_provider=auth_provider)
        key_space_ocds = cluster.connect('ocds')
        key_space_access = cluster.connect('access')
        key_space_clarification = cluster.connect('clarification')
        key_space_submission = cluster.connect('submission')
        key_space_auctions = cluster.connect('auctions')
        key_space_revision = cluster.connect('revision')
        owner = "445f6851-c908-407d-9b45-14b92f3e964b"
        ei_id = prepared_cp_id()
        fs_id = prepared_fs_oc_id(ei_id)
        cp_id = prepared_cp_id()
        pn_id = prepared_pn_oc_id(cp_id)
        pn_token = uuid4()
        ev_id = prepared_cn_oc_id(cp_id)
        period = get_period()
        period_for_amendment = get_period_for_amendment()
        auction_date = get_auction_date()
        contract_period = get_contract_period()
        enquiry_and_tender_period = create_enquiry_and_tender_period(
            second_enquiry=second_enquiry,
            second_tender=second_tender
        )

        operation_date = time_at_now()
        calculate_new_cpv_code = get_new_classification_id(
            self.first_item_cpv,
            self.second_item_cpv
        )
        get_value_by_new_cpv_code = get_value_from_classification_cpv_dictionary_xls(
            calculate_new_cpv_code,
            self.lang
        )
        get_value_by_first_item_cpv_code = get_value_from_classification_cpv_dictionary_xls(
            self.first_item_cpv,
            self.lang
        )
        get_value_by_second_item_cpv_code = get_value_from_classification_cpv_dictionary_xls(
            self.second_item_cpv,
            self.lang
        )
        get_value_by_first_item_cpvs_code = get_value_from_cpvs_dictionary_csv(
            self.first_item_additional_classifications,
            self.lang
        )
        get_value_by_second_item_cpvs_code = get_value_from_cpvs_dictionary_csv(
            self.second_item_additional_classifications,
            self.lang
        )
        get_value_by_first_item_unit_id = get_value_from_classification_unit_dictionary_csv(
            self.first_item_unit_id,
            self.lang
        )
        get_value_by_second_item_unit_id = get_value_from_classification_unit_dictionary_csv(
            self.second_item_unit_id,
            self.lang
        )

        mdm = MdmService(
            instance=self.instance
        )
        data_pn = mdm.process_tender_data(self.pmd).json()
        submission_method_details = data_pn["data"]["tender"]["submissionMethodDetails"]
        submission_method_rationale = data_pn["data"]["tender"]["submissionMethodRationale"]

        procurement_method_details_from_mdm = data_pn["data"]["tender"]["procurementMethodDetails"]
        eligibility_criteria_from_mdm = data_pn["data"]["tender"]["eligibilityCriteria"]
        instance_tender_url = None
        instance_budget_url = None
        instance_storage_url = None
        if self.instance == "dev":
            instance_tender_url = "http://dev.public.eprocurement.systems/tenders/"
            instance_budget_url = "http://dev.public.eprocurement.systems/budgets/"
            instance_storage_url = "https://dev.bpe.eprocurement.systems/api/v1/storage/get/"
        if self.instance == "sandbox":
            instance_tender_url = "http://public.eprocurement.systems/tenders/"
            instance_budget_url = "http://public.eprocurement.systems/budgets/"
            instance_storage_url = "http://storage.eprocurement.systems/get/"
        json_orchestrator_context = {
            "cpid": cp_id,
            "ocid": ev_id,
            "operationId": f"{uuid4()}",
            "requestId": f"{uuid4()}",
            "owner": owner,
            "stage": "EV",
            "prevStage": "EV",
            "phase": "clarification",
            "processType": "cancelTender",
            "operationType": "tenderCancellation",
            "country": self.country,
            "language": self.lang,
            "pmd": self.pmd,
            "startDate": period_for_amendment[0],
            "timeStamp": period_for_amendment[1],
            "isAuction": True
        }

        json_access_tender = {
            "ocid": cp_id,
            "planning": {
                "rationale": "create Pn: planning.rationale",
                "budget": {
                    "description": "create Pn: planning.budget.description",
                    "amount": {
                        "amount": 2000.00,
                        "currency": "EUR"
                    },
                    "isEuropeanUnionFunded": True,
                    "budgetBreakdown": [{
                        "id": fs_id,
                        "description": "create Fs: planning.budget.description",
                        "amount": {
                            "amount": 2000.00,
                            "currency": "EUR"
                        },
                        "period": {
                            "startDate": period[0],
                            "endDate": period[1]
                        },
                        "sourceParty": {
                            "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                            "name": self.funder_name,
                        },
                        "europeanUnionFunding": {
                            "projectIdentifier": "create Fs: planning.budget.europeanUnionFunding.projectIdentifier",
                            "projectName": "create Fs: planning.budget.europeanUnionFunding.projectName",
                            "uri": "create Fs: planning.budget.europeanUnionFunding.uri"
                        }
                    }]
                }
            },
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "status": "active",
                "statusDetails": "clarification",
                "title": "create Pn: tender.title",
                "description": "create Pn: tender.description",
                "classification": {
                    "scheme": "CPV",
                    "id": get_value_by_new_cpv_code[0],
                    "description": get_value_by_new_cpv_code[1]
                },
                "tenderPeriod": {
                    "startDate": enquiry_and_tender_period[2],
                    "endDate": enquiry_and_tender_period[3]
                },
                "enquiryPeriod": {
                    "startDate": enquiry_and_tender_period[0],
                    "endDate": enquiry_and_tender_period[1]
                },
                "acceleratedProcedure": {
                    "isAcceleratedProcedure": False
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
                "procedureOutsourcing": {
                    "procedureOutsourced": False
                },
                "framework": {
                    "isAFramework": False
                },
                "dynamicPurchasingSystem": {
                    "hasDynamicPurchasingSystem": False
                },
                "legalBasis": "DIRECTIVE_2014_25_EU",
                "procurementMethod": "open",
                "procurementMethodDetails": procurement_method_details_from_mdm,
                "procurementMethodRationale": "create CNonPN: tender.procurementMethodRationale",
                "procurementMethodAdditionalInfo": "create CNonPN: tender.procurementMethodAdditionalInfo",
                "mainProcurementCategory": "works",
                "eligibilityCriteria": eligibility_criteria_from_mdm,
                "contractPeriod": {
                    "startDate": contract_period[0],
                    "endDate": contract_period[1]
                },
                "procurementMethodModalities": ["electronicAuction"],
                "electronicAuctions": {
                    "details": [{
                        "id": "503d6861-62d9-47f3-8939-4e4729df0cde",
                        "relatedLot": first_lot_id,
                        "electronicAuctionModalities": [{
                            "eligibleMinimumDifference": {
                                "amount": 100.00,
                                "currency": "EUR"
                            }
                        }]
                    }, {
                        "id": "f1a36bc8-ee22-4660-8a76-5b1671d34b0d",
                        "relatedLot": second_lot_id,
                        "electronicAuctionModalities": [{
                            "eligibleMinimumDifference": {
                                "amount": 10.00,
                                "currency": "EUR"
                            }
                        }]
                    }]
                },
                "procuringEntity": {
                    "id": "MD-IDNO-4",
                    "name": "create Pn: tender.procuringEntity.name",
                    "identifier": {
                        "scheme": "MD-IDNO",
                        "id": "4",
                        "legalName": "create Pn: tender.procuringEntity.identifier.legalName",
                        "uri": "create Pn: tender.procuringEntity.identifier.uri"
                    },
                    "additionalIdentifiers": [{
                        "scheme": "create Pn: tender.procuringEntity.additionalIdentifiers[0].scheme",
                        "id": "create Pn: tender.procuringEntity.additionalIdentifiers[0].id",
                        "legalName": "create Pn: tender.procuringEntity.additionalIdentifiers[0].legalName",
                        "uri": "create Pn: tender.procuringEntity.additionalIdentifiers[0].uri"
                    }],
                    "address": {
                        "streetAddress": "create Pn: tender.procuringEntity.address.streetAddress",
                        "postalCode": "create Pn: tender.procuringEntity.address.postalCode",
                        "addressDetails": {
                            "country": {
                                "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "country"]['scheme'],
                                "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "country"]['id'],
                                "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                    "addressDetails"]["country"]['description'],
                                "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "country"]['uri']
                            },
                            "region": {
                                "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "region"]['scheme'],
                                "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "region"]['id'],
                                "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                    "addressDetails"]["region"]['description'],
                                "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "region"]['uri']
                            },
                            "locality": {
                                "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "locality"]['scheme'],
                                "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "locality"]['id'],
                                "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                    "addressDetails"]["locality"]['description'],
                                "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "locality"]['uri']

                            }
                        }
                    },
                    "contactPoint": {
                        "name": "create Pn: tender.procuringEntity.contactPoint.name",
                        "email": "create Pn: tender.procuringEntity.contactPoint.email",
                        "telephone": "create Pn: tender.procuringEntity.contactPoint.telephone",
                        "faxNumber": "create Pn: tender.procuringEntity.contactPoint.faxNumber",
                        "url": "create Pn: tender.procuringEntity.contactPoint.url"
                    },
                    "persones": [{
                        "id": "create CNonPN: procuringEntity.persones[0].identifier.id",
                        "title": "create CNonPN: procuringEntity.persones[0].title",
                        "name": "create CNonPN: procuringEntity.persones[0].name",
                        "identifier": {
                            "scheme": "MD-IDNO",
                            "id": "create CNonPN: procuringEntity.persones[0].identifier.id",
                            "uri": "create CNonPN: procuringEntity.persones[0].identifier.uri"
                        },
                        "businessFunctions": [{
                            "id": "create CNonPN: procuringEntity.persones[0].businessFunctions[0].id",
                            "type": "contactPoint",
                            "jobTitle": "create CNonPN: procuringEntity.persones[0].businessFunctions[0].jobTitle",
                            "period": {
                                "startDate": period[0]
                            },
                            "documents": [{
                                "id": self.document_three_was_uploaded,
                                "documentType": "regulatoryDocument",
                                "title": "create CNonPN: procuringEntity.persones[0].businessFunctions[0].title",
                                "description": "create CNonPN: procuringEntity.persones[0].businessFunctions[0]."
                                               "description"
                            }]
                        }]
                    }]
                },
                "value": {
                    "amount": 1650.00,
                    "currency": "EUR"
                },
                "lotGroups": [{
                    "optionToCombine": False
                }],
                "criteria": [{
                    "id": "db6d8e23-5dce-4688-9b82-2e323994e709",
                    "title": "create CNonPN: tender.criteria[0].title =Bankruptcy",
                    "classification": {
                        "id": "CRITERION.EXCLUSION.CONVICTIONS.PARTICIPATION_IN_CRIMINAL_ORGANISATION",
                        "scheme": "ESPD"
                    },
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[0].description =Is the economic operator bankrupt? "
                                   "This information needs not be given if exclusion of economic operators in this "
                                   "case has been made mandatory under the applicable national law without any "
                                   "possibility of derogation where the economic operator is nevertheless able to "
                                   "perform the contract.",
                    "requirementGroups": [{
                        "id": "83af7655-a283-42ad-8151-ac2ff549e23e",
                        "description": "create CNonPN: tender.criteria[0].requirementGroups[0].description =approve "
                                       "that Bankruptcy requirement group",
                        "requirements": [{
                            "id": "86c15b70-0622-41e7-b333-457d14c770b6",
                            "title": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements.title",
                            "dataType": "boolean",
                            "description": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements."
                                           "description",
                            "status": "active",
                            "datePublished": operation_date,
                            "expectedValue": False,
                            "eligibleEvidences": [{
                                "id": "1",
                                "title": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements[0]."
                                         "eligibleEvidences[0].title",
                                "description": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements"
                                               "[0].eligibleEvidences[0].description",
                                "type": "document",
                                "relatedDocument": {
                                    "id": self.document_three_was_uploaded
                                }
                            }, {
                                "id": "2",
                                "title": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements[0]."
                                         "eligibleEvidences[1].title",
                                "description": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements"
                                               "[0].eligibleEvidences[1].description",
                                "type": "document",
                                "relatedDocument": {
                                    "id": self.document_three_was_uploaded
                                }
                            }]
                        }]
                    }],
                    "relatesTo": "tender"
                }, {
                    "id": "5ad0aa1e-ec8c-48d6-be0c-99fa777eaca9",
                    "title": "create CNonPN: tender.criteria[1].title",
                    "classification": {
                        "id": "CRITERION.SELECTION.ECONOMIC_FINANCIAL_STANDING.TURNOVER.GENERAL_YEARLY",
                        "scheme": "ESPD"
                    },
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[1].description",
                    "requirementGroups": [{
                        "id": "c3878528-b856-4a2d-92f9-6138dad28b51",
                        "description": "create CNonPN: tender.criteria[1].requirementGroups[0].description",
                        "requirements": [{
                            "id": "268877db-bfb9-45dc-9b0b-4a932f75c6ed",
                            "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[0].title",
                            "dataType": "boolean",
                            "description": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements."
                                           "description",
                            "status": "active",
                            "datePublished": operation_date,
                            "expectedValue": True
                        }, {
                            "id": "2aadefb6-869e-4695-9b2f-663c9a4acb37",
                            "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[1]."
                                     "title =The number of years for proposed product warranty",
                            "dataType": "number",
                            "description": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[1]."
                                           "description",
                            "status": "active",
                            "datePublished": operation_date,
                            "period": {
                                "startDate": period[0],
                                "endDate": period[1]
                            },
                            "minValue": 1.000,
                            "maxValue": 3.000,
                            "eligibleEvidences": [{
                                "id": "3",
                                "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[1]."
                                         "eligibleEvidences[0].title",
                                "description": "create CNonPN: tender.criteria[1].requirementGroups[0]."
                                               "requirements[1].eligibleEvidences[0].description",
                                "type": "document",
                                "relatedDocument": {
                                    "id": self.document_three_was_uploaded
                                }
                            }]
                        }]
                    }],
                    "relatesTo": "lot",
                    "relatedItem": first_lot_id
                }, {
                    "id": "1a600e32-354f-436c-bede-e3238ca1998d",
                    "title": "create CNonPN: tender.criteria[2].title",
                    "classification": {
                        "id": "CRITERION.EXCLUSION.NATIONAL.OTHER",
                        "scheme": "ESPD"
                    },
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[2].description",
                    "requirementGroups": [{
                        "id": "a2fa62cc-4ec3-4944-a091-bd158cded7ab",
                        "description": "create CNonPN: tender.criteria[2].requirementGroups[0].description",
                        "requirements": [{
                            "id": "5ac98f2b-9e55-4167-aa82-2d4baa1d01cb",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[0].requirements[0]."
                                     "title =Product has to be manufactured in the EU",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "expectedValue": True
                        }, {
                            "id": "5bfd430b-a663-4657-972f-788b8c7bffc5",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[0]..requirements[1]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }, {
                        "id": "eac18bd3-6c02-4245-a6e2-f839f80361ee",
                        "description": "create CNonPN: tender.criteria[2].requirementGroups[1].description",
                        "requirements": [{
                            "id": "6853dee4-1359-4522-87a6-ee50c00cb390",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[1].requirements[0]."
                                     "title =Product has to be manufactured in the EU",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "expectedValue": True
                        }, {
                            "id": "a470ea41-0825-44e2-89be-495d63a54f06",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[1]..requirements[1]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }],
                    "relatesTo": "tenderer"
                }, {
                    "id": "13e1682a-23bb-491d-ad6d-a9cbdba6ac80",
                    "title": "create CNonPN: tender.criteria[3].title",
                    "classification": {
                        "id": "CRITERION.OTHER.EO_DATA.RELIES_ON_OTHER_CAPACITIES",
                        "scheme": "ESPD"
                    },
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[3].description =A minimum product warranty "
                                   "of 1 year is required for all bids 2",
                    "requirementGroups": [{
                        "id": "8378bc93-9c06-47ae-9982-0b091e326728",
                        "description": "create CNonPN: tender.criteria[3].requirementGroups[0].description",
                        "requirements": [{
                            "id": "e64eb9e1-47dd-488f-acbe-ff13b7e258d8",
                            "title": "create CNonPN: tender.criteria[3].requirementGroups[0].requirements[0]."
                                     "title = The number of years for proposed product warranty",
                            "dataType": "number",
                            "status": "active",
                            "datePublished": operation_date,
                            "period": {
                                "startDate": period[0],
                                "endDate": period[1]
                            },
                            "minValue": 1.000,
                            "maxValue": 3.000
                        }]
                    }],
                    "relatesTo": "item",
                    "relatedItem": first_item_id
                }, {
                    "id": "50d6061e-5913-4bc4-a18b-3ad3261a2c88",
                    "title": "create CNonPN: tender.criteria[4].title",
                    "classification": {
                        "id": "CRITERION.EXCLUSION.NATIONAL.OTHER",
                        "scheme": "ESPD"
                    },
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[4].description",
                    "requirementGroups": [{
                        "id": "da026d11-3769-43ce-ba83-f93832b18409",
                        "description": "create CNonPN: tender.criteria[4].requirementGroups[0].description",
                        "requirements": [{
                            "id": "794ece62-28a9-4843-8241-6955d7020cde",
                            "title": "create CNonPN: tender.criteria[4].requirementGroups[0].requirements[0]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }],
                    "relatesTo": "tender"
                }, {
                    "id": "55a02e2f-dc9c-43ad-ad47-af0932cf0b89",
                    "title": "create CNonPN: tender.criteria[4].title",
                    "classification": {
                        "id": "CRITERION.OTHER.EO_DATA.RELIES_ON_OTHER_CAPACITIES",
                        "scheme": "ESPD"
                    },
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[4].description",
                    "requirementGroups": [{
                        "id": "735a5c8b-6adf-4256-ac73-104470b7b189",
                        "description": "create CNonPN: tender.criteria[4].requirementGroups[0].description",
                        "requirements": [{
                            "id": "ba9194d1-37a6-45ac-896c-faacd250eb72",
                            "title": "create CNonPN: tender.criteria[4].requirementGroups[0].requirements[0]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }],
                    "relatesTo": "tender"
                }],
                "conversions": [{
                    "id": "9eab3068-bcce-4f8a-a829-0181830f0636",
                    "relatesTo": "requirement",
                    "relatedItem": "268877db-bfb9-45dc-9b0b-4a932f75c6ed",
                    "rationale": "create CNonPN: tender.conversions[1].rationale",
                    "description": "create CNonPN: tender.conversions[1].description",
                    "coefficients": [{
                        "id": "e896f9d4-3f61-4370-97d0-25fd6e26b27a",
                        "value": False,
                        "coefficient": 1
                    }]
                }, {
                    "id": "4937c4b4-a50d-48f8-8363-7b02c48a12d9",
                    "relatesTo": "requirement",
                    "relatedItem": "2aadefb6-869e-4695-9b2f-663c9a4acb37",
                    "rationale": "create CNonPN: tender.conversions[3].rationale",
                    "description": "create CNonPN: tender.conversions[3].description",
                    "coefficients": [{
                        "id": "f09bf118-92fd-4702-a5ac-2393e2234dbb",
                        "value": 1.000,
                        "coefficient": 1
                    }, {
                        "id": "9b69b215-e75a-4d5b-b51a-2046a7207562",
                        "value": 2.000,
                        "coefficient": 1
                    }, {
                        "id": "9c985738-1903-49df-829d-a574a5021d35",
                        "value": 3.000,
                        "coefficient": 0.93
                    }]
                }, {
                    "id": "678dcf2c-2e9f-4a72-8cb6-8ecf067fcf75",
                    "relatesTo": "requirement",
                    "relatedItem": "e64eb9e1-47dd-488f-acbe-ff13b7e258d8",
                    "rationale": "create CNonPN: tender.conversions[6].rationale",
                    "description": "create CNonPN: tender.conversions[6].description",
                    "coefficients": [{
                        "id": "f4ab1b51-21ee-46d2-8e78-2d65c30fa3e2",
                        "value": 1.000,
                        "coefficient": 1
                    }, {
                        "id": "c5eb8b92-a1b5-41a0-a7ed-267b2a79bc91",
                        "value": 2.000,
                        "coefficient": 1
                    }, {
                        "id": "ab5e3241-0afd-40b1-86ac-887366caef2b",
                        "value": 3.000,
                        "coefficient": 0.93
                    }]
                }, {
                    "id": "89ac8671-0640-41c9-ba4b-fdfcc7aa9131",
                    "relatesTo": "requirement",
                    "relatedItem": "ba9194d1-37a6-45ac-896c-faacd250eb72",
                    "rationale": "create CNonPN: tender.conversions[6].rationale",
                    "description": "create CNonPN: tender.conversions[6].description",
                    "coefficients": [{
                        "id": "0728cc52-3c85-4283-a1f6-b3ae94ca6eae",
                        "relatedOption": "option_1",
                        "value": "option_1",
                        "coefficient": 1
                    }, {
                        "id": "66e52e5a-49fd-420f-936a-0ef9aeafae21",
                        "relatedOption": "option_2",
                        "value": "option_2",
                        "coefficient": 1
                    }, {
                        "id": "6151abc7-56e1-424b-a0ee-f9bba4205abf",
                        "relatedOption": "option_3",
                        "value": "option_3",
                        "coefficient": 0.93
                    }]
                }],
                "lots": [{
                    "id": first_lot_id,
                    "internalId": "create Pn: tender.lots[0].internalId",
                    "title": "create Pn: tender.lots[0].title",
                    "description": "create Pn: tender.lots[0].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 1500.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[0].placeOfPerformance.address.streetAddress",
                            "postalCode": "create Pn: tender.lots[0].placeOfPerformance.address.postalCode",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        },
                        "description": "create Pn: tender.lots[0].placeOfPerformance.description"
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }, {
                    "id": second_lot_id,
                    "internalId": "create Pn: tender.lots[1].internalId",
                    "title": "create Pn: tender.lots[1].title",
                    "description": "create Pn: tender.lots[1].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 150.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[1].placeOfPerformance.address.streetAddress",
                            "postalCode": "create Pn: tender.lots[1].placeOfPerformance.address.postalCode",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        },
                        "description": "create Pn: tender.lots[1].placeOfPerformance.description"
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }],
                "items": [{
                    "id": first_item_id,
                    "internalId": "create Pn: tender.items[0].internalId",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_first_item_cpv_code[0],
                        "description": get_value_by_first_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_first_item_cpvs_code[0],
                        "description": get_value_by_first_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_first_item_unit_id[0],
                        "name": get_value_by_first_item_unit_id[1]
                    },
                    "description": "create Pn: tender.items[0].description",
                    "relatedLot": first_lot_id
                }, {
                    "id": second_item_id,
                    "internalId": "create Pn: tender.items[1].internalId",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_second_item_cpv_code[0],
                        "description": get_value_by_second_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_second_item_cpvs_code[0],
                        "description": get_value_by_second_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_second_item_unit_id[0],
                        "name": get_value_by_second_item_unit_id[1]
                    },
                    "description": "create Pn: tender.items[1].description",
                    "relatedLot": second_lot_id
                }],
                "awardCriteria": "ratedCriteria",
                "awardCriteriaDetails": "automated",
                "requiresElectronicCatalogue": False,
                "submissionMethod": ["electronicSubmission"],
                "submissionMethodRationale": submission_method_rationale,
                "submissionMethodDetails": submission_method_details,
                "documents": [
                    {
                        "id": self.document_one_was_uploaded,
                        "documentType": "billOfQuantity",
                        "title": "create Pn: tender.documents[0].title",
                        "description": "create Pn: tender.documents[0].description",
                        "relatedLots": [
                            first_lot_id]
                    },
                    {
                        "id": self.document_two_was_uploaded,
                        "documentType": "billOfQuantity",
                        "title": "create Pn: tender.documents[1].title",
                        "description": "create Pn: tender.documents[1].description",
                        "relatedLots": [
                            second_lot_id]
                    },
                    {
                        "id": self.document_three_was_uploaded,
                        "documentType": "evaluationCriteria",
                        "title": "create CNonPN: tender.documents[2].title",
                        "description": "create CNonPN: tender.documents[2].description",
                        "relatedLots": [first_lot_id]
                    }
                ]
            }
        }

        json_auction_auctions = {
            "version": "1.0.0",
            "tender": {
                "id": ev_id,
                "country": self.country,
                "status": 1,
                "startDate": auction_date
            },
            "slots": ["917ba5a5-d39e-4c24-a465-4b7f5726d5f3"],
            "auctions": [{
                "id": "503d6861-62d9-47f3-8939-4e4729df0cde",
                "lotId": first_lot_id,
                "auctionPeriod": {
                    "startDate": auction_date
                },
                "modalities": [{
                    "url": f"https://eauction.eprocurement.systems/auctions/{ev_id}/{first_lot_id}",
                    "eligibleMinimumDifference": {
                        "amount": 100.00,
                        "currency": "EUR"
                    }
                }]
            }, {
                "id": "516f0bd4-7706-4dc8-bd37-894d93cac809",
                "lotId": second_lot_id,
                "auctionPeriod": {
                    "startDate": auction_date
                },
                "modalities": [{
                    "url": f"https://eauction.eprocurement.systems/auctions/{ev_id}/{second_lot_id}",
                    "eligibleMinimumDifference": {
                        "amount": 10.00,
                        "currency": "EUR"
                    }
                }]
            }]
        }
        json_amendments = {
            "id": self.amendment_id,
            "date": period_for_amendment[0],
            "rationale": "cancel_tender: amendments[0].rationale",
            "description": "cancel_tender: amendments[0].description",
            "status": "pending",
            "type": "cancellation",
            "relatesTo": "tender",
            "relatedItem": ev_id,
            "token": self.amendment_token,
            "owner": "445f6851-c908-407d-9b45-14b92f3e964b",
            "documents": [{
                "documentType": "cancellationDetails",
                "id": self.document_five_was_uploaded,
                "title": "cancel_tender: amendments[0].documents[0].title",
                "description": "cancel_tender: amendments[0].documents[0].description"
            }]
        }
        json_notice_release_ms = {
            "ocid": cp_id,
            "id": f"{cp_id}-{ev_id[32:45]}",
            "date": f"{get_human_date_in_utc_format(int(ev_id[32:45]))[0]}",
            "tag": ["compiled"],
            "language": self.lang,
            "initiationType": "tender",
            "planning": {
                "budget": {
                    "description": "create Pn: planning.budget.description",
                    "amount": {
                        "amount": 2000.00,
                        "currency": "EUR"
                    },
                    "isEuropeanUnionFunded": True,
                    "budgetBreakdown": [{
                        "id": fs_id,
                        "description": "create Fs: planning.budget.description",
                        "amount": {
                            "amount": 2000.00,
                            "currency": "EUR"
                        },
                        "period": {
                            "startDate": period[0],
                            "endDate": period[1]
                        },
                        "sourceParty": {
                            "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                            "name": self.funder_name,
                        },
                        "europeanUnionFunding": {
                            "projectIdentifier": "create Fs: planning.budget.europeanUnionFunding.projectIdentifier",
                            "projectName": "create Fs: planning.budget.europeanUnionFunding.projectName",
                            "uri": "create Fs: planning.budget.europeanUnionFunding.uri"
                        }
                    }]
                },
                "rationale": "create Pn: planning.rationale"
            },
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "title": "create Pn: tender.title",
                "description": "create Pn: tender.description",
                "status": "active",
                "statusDetails": "evaluation",
                "value": {
                    "amount": 1650.00,
                    "currency": "EUR"
                },
                "procurementMethod": "open",
                "procurementMethodDetails": procurement_method_details_from_mdm,
                "procurementMethodRationale": "create CNonPN: tender.procurementMethodRationale",
                "mainProcurementCategory": "works",
                "hasEnquiries": False,
                "eligibilityCriteria": eligibility_criteria_from_mdm,
                "contractPeriod": {
                    "startDate": contract_period[0],
                    "endDate": contract_period[1]
                },
                "procuringEntity": {
                    "id": "MD-IDNO-4",
                    "name": "create Pn: tender.procuringEntity.name"
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
                "legalBasis": "DIRECTIVE_2014_25_EU",
                "procedureOutsourcing": {
                    "procedureOutsourced": False
                },
                "procurementMethodAdditionalInfo": "create CNonPN: tender.procurementMethodAdditionalInfo",
                "dynamicPurchasingSystem": {
                    "hasDynamicPurchasingSystem": False
                },
                "framework": {
                    "isAFramework": False
                }
            },
            "parties": [{
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name,
                "identifier": {
                    "scheme": self.buyer_identifier_scheme,
                    "id": self.buyer_identifier_id,
                    "legalName": self.buyer_identifier_legal_name,
                    "uri": self.buyer_identifier_uri
                },
                "address": {
                    "streetAddress": self.buyer_address_street_address,
                    "postalCode": self.buyer_address_postal_code,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.buyer_address_address_details_country_id,
                            "description": "Moldova, Republica",
                            "uri": "https://www.iso.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": self.buyer_address_address_details_region_id,
                            "description": "Cahul",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": self.buyer_address_address_details_locality_scheme,
                            "id": self.buyer_address_address_details_locality_id,
                            "description": self.buyer_address_address_details_locality_description,
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "additionalIdentifiers": [
                    {
                        "scheme": "create Ei: buyer.additionalIdentifiers[0].scheme",
                        "id": "create Ei: buyer.additionalIdentifiers[0].id",
                        "legalName": "create Ei: buyer.additionalIdentifiers[0].legalName",
                        "uri": "create Ei: buyer.additionalIdentifiers[0].uri"
                    }],
                "contactPoint": {
                    "name": self.buyer_contact_point_name,
                    "email": self.buyer_contact_point_email,
                    "telephone": self.buyer_contact_point_telephone,
                    "faxNumber": self.buyer_contact_point_fax_number,
                    "url": self.buyer_contact_point_url
                },
                "details": {
                    "typeOfBuyer": "NATIONAL_AGENCY",
                    "mainGeneralActivity": "HEALTH",
                    "mainSectoralActivity": "WATER"
                },
                "roles": [
                    "buyer"]
            }, {
                "id": f"{self.payer_identifier_scheme}-{self.payer_identifier_id}",
                "name": self.payer_name,
                "identifier": {
                    "scheme": self.payer_identifier_scheme,
                    "id": self.payer_identifier_id,
                    "legalName": self.payer_identifier_legal_name,
                    "uri": self.payer_identifier_uri
                },
                "address": {
                    "streetAddress": self.payer_address_street,
                    "postalCode": self.payer_address_postal_code,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.payer_address_address_details_country_id,
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": self.payer_address_address_details_region_id,
                            "description": "Cahul",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": self.payer_address_address_details_locality_scheme,
                            "id": self.payer_address_address_details_locality_id,
                            "description": self.payer_address_address_details_locality_description,
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "additionalIdentifiers": [
                    {
                        "scheme": "create Fs: tender.procuringEntity.additionalIdentifiers[0].scheme",
                        "id": "create Fs: tender.procuringEntity.additionalIdentifiers[0].id",
                        "legalName": "create Fs: tender.procuringEntity.additionalIdentifiers[0].legalName",
                        "uri": "create Fs: tender.procuringEntity.additionalIdentifiers[0].uri"
                    }],
                "contactPoint": {
                    "name": self.payer_contact_point_name,
                    "email": self.payer_contact_point_email,
                    "telephone": self.payer_contact_point_telephone,
                    "faxNumber": self.payer_contact_point_fax_number,
                    "url": self.payer_contact_point_url
                },
                "roles": ["payer"]
            }, {
                "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                "name": self.funder_name,
                "identifier": {
                    "scheme": self.funder_identifier_scheme,
                    "id": self.funder_identifier_id,
                    "legalName": self.funder_identifier_legal_name,
                    "uri": self.funder_identifier_uri
                },
                "address": {
                    "streetAddress": self.funder_address_street,
                    "postalCode": self.funder_address_postal_code,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.funder_address_address_details_country_id,
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": self.funder_address_address_details_region_id,
                            "description": "Cahul",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": self.funder_address_address_details_locality_scheme,
                            "id": self.funder_address_address_details_locality_id,
                            "description": self.funder_address_address_details_locality_description,
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "additionalIdentifiers": [
                    {
                        "scheme": "create Fs: buyer.additionalIdentifiers[0].scheme",
                        "id": "create Fs: buyer.additionalIdentifiers[0].id",
                        "legalName": "create Fs: buyer.additionalIdentifiers[0].legalName",
                        "uri": "create Fs: buyer.additionalIdentifiers[0].uri"
                    }],
                "contactPoint": {
                    "name": self.funder_contact_point_name,
                    "email": self.funder_contact_point_email,
                    "telephone": self.funder_contact_point_telephone,
                    "faxNumber": self.funder_contact_point_fax,
                    "url": self.funder_contact_point_url
                },
                "roles": [
                    "funder"]
            }, {
                "id": "MD-IDNO-4",
                "name": "create Pn: tender.procuringEntity.name",
                "identifier": {
                    "scheme": "MD-IDNO",
                    "id": "4",
                    "legalName": "create Pn: tender.procuringEntity.identigfier.legalName",
                    "uri": "create Pn: tender.procuringEntity.identifier.uri"
                },
                "address": {
                    "streetAddress": "create Pn: tender.procuringEntity.address.streetAddress",
                    "postalCode": "create Pn: tender.procuringEntity.address.postalCode",
                    "addressDetails": {
                        "country": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["country"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['uri']
                        },
                        "region": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["region"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['uri']
                        },
                        "locality": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["locality"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['uri']

                        }
                    }
                },
                "additionalIdentifiers": [{
                    "scheme": "create Pn: tender.procuringEntity.additionalIdentifiers[0].scheme",
                    "id": "create Pn: tender.procuringEntity.additionalIdentifiers[0].id",
                    "legalName": "create Pn: tender.procuringEntity.additionalIdentifiers[0].legalName",
                    "uri": "create Pn: tender.procuringEntity.additionalIdentifiers[0].uri"
                }],
                "contactPoint": {
                    "name": "create Pn: tender.procuringEntity.contactPoint.name",
                    "email": "create Pn: tender.procuringEntity.contactPoint.email",
                    "telephone": "create Pn: tender.procuringEntity.contactPoint.telephone",
                    "faxNumber": "create Pn: tender.procuringEntity.contactPoint.faxNumber",
                    "url": "create Pn: tender.procuringEntity.contactPoint.url"
                },
                "persones": [{
                    "id": "MD-IDNO-create CNonPN: procuringEntity.persones[0].identifier.id",
                    "title": "create CNonPN: procuringEntity.persones[0].title",
                    "name": "create CNonPN: procuringEntity.persones[0].name",
                    "identifier": {
                        "scheme": "MD-IDNO",
                        "id": "create CNonPN: procuringEntity.persones[0].identifier.id",
                        "uri": "create CNonPN: procuringEntity.persones[0].identifier.uri"
                    },
                    "businessFunctions": [{
                        "id": "create CNonPN: procuringEntity.persones[0].businessFunctions[0].id",
                        "type": "procurementOfficer",
                        "jobTitle": "create CNonPN: procuringEntity.persones[0].businessFunctions[0].jobTitle",
                        "period": {
                            "startDate": period[0]
                        },
                        "documents": [{
                            "id": self.document_three_was_uploaded,
                            "documentType": "regulatoryDocument",
                            "title": "create CNonPN: procuringEntity.persones[0].businessFunctions[0].title",
                            "description": "create CNonPN: procuringEntity.persones[0].businessFunctions[0]."
                                           "description",
                            "url": f"{instance_storage_url}"
                                   f"{self.document_three_was_uploaded}",
                            "datePublished": operation_date
                        }]
                    }]
                }],
                "roles": ["procuringEntity"]
            }],
            "relatedProcesses": [{
                "id": "36b553f0-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["planning"],
                "scheme": "ocid",
                "identifier": pn_id,
                "uri": f"{instance_tender_url}{cp_id}/{pn_id}"
            }, {
                "id": "36b553f1-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["x_expenditureItem"],
                "scheme": "ocid",
                "identifier": ei_id,
                "uri": f"{instance_budget_url}{ei_id}/{ei_id}"
            }, {
                "id": "36b553f2-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["x_fundingSource"],
                "scheme": "ocid",
                "identifier": fs_id,
                "uri": f"{instance_budget_url}{ei_id}/{fs_id}"
            },
                {
                    "id": "164cf530-ceca-11eb-8aed-69d06bed4d57",
                    "relationship": ["x_evaluation"],
                    "scheme": "ocid",
                    "identifier": ev_id,
                    "uri": f"{instance_tender_url}{cp_id}/{ev_id}"
                }
            ]
        }
        json_notice_release_pn = {
            "ocid": pn_id,
            "id": f"{pn_id}-{ev_id[32:45]}",
            "date": f"{get_human_date_in_utc_format(int(ev_id[32:45]))[0]}",
            "tag": ["planningUpdate"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "title": "Planning Notice",
                "description": "Contracting process is planned",
                "status": "complete",
                "statusDetails": "empty",
                "items": [{
                    "id": first_item_id,
                    "internalId": "create Pn: tender.items[0].internalId",
                    "description": "create Pn: tender.items[0].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_first_item_cpv_code[0],
                        "description": get_value_by_first_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_first_item_cpvs_code[0],
                        "description": get_value_by_first_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_first_item_unit_id[0],
                        "name": get_value_by_first_item_unit_id[1]
                    },
                    "relatedLot": first_lot_id
                }, {
                    "id": second_item_id,
                    "internalId": "create Pn: tender.items[1].internalId",
                    "description": "create Pn: tender.items[1].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_second_item_cpv_code[0],
                        "description": get_value_by_second_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_second_item_cpvs_code[0],
                        "description": get_value_by_second_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_second_item_unit_id[0],
                        "name": get_value_by_second_item_unit_id[1]
                    },
                    "relatedLot": second_lot_id
                }],
                "lots": [{
                    "id": first_lot_id,
                    "internalId": "create Pn: tender.lots[0].internalId",
                    "title": "create Pn: tender.lots[0].title",
                    "description": "create Pn: tender.lots[0].internalId.description",
                    "status": "planning",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 1500.00,
                        "currency": "EUR"
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
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[0].placeOfPerformance.address.streetAddress",
                            "postalCode": "create Pn: tender.lots[0].placeOfPerformance.address.postalCode",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        },
                        "description": "create Pn: tender.lots[0].placeOfPerformance.description"
                    },
                    "options": [{
                        "hasOptions": False
                    }]
                }, {
                    "id": second_lot_id,
                    "internalId": "create Pn: tender.lots[1].internalId",
                    "title": "create Pn: tender.lots[1].title",
                    "description": "create Pn: tender.lots[1].internalId.description",
                    "status": "planning",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 150.00,
                        "currency": "EUR"
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
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[1].placeOfPerformance.address.streetAddress",
                            "postalCode": "create Pn: tender.lots[1].placeOfPerformance.address.postalCode",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        },
                        "description": "create Pn: tender.lots[1].placeOfPerformance.description"
                    },
                    "options": [{
                        "hasOptions": False
                    }]
                }],
                "lotGroups": [{
                    "optionToCombine": False
                }],
                "tenderPeriod": {
                    "startDate": period[3]
                },
                "hasEnquiries": False,
                "documents": [
                    {
                        "id": self.document_one_was_uploaded,
                        "documentType": "contractArrangements",
                        "title": "create Pn: tender.documents[0].title",
                        "description": "create Pn: tender.documents[0].description",
                        "url": f"{instance_storage_url}"
                               f"{self.document_one_was_uploaded}",
                        "datePublished": f"{get_human_date_in_utc_format(int(pn_id[32:45]))[0]}",
                        "relatedLots": [first_lot_id]
                    },
                    {
                        "id": self.document_two_was_uploaded,
                        "documentType": "contractArrangements",
                        "title": "create Pn: tender.documents[1].title",
                        "description": "create Pn: tender.documents[1].description",
                        "url": f"{instance_storage_url}"
                               f"{self.document_two_was_uploaded}",
                        "datePublished": f"{get_human_date_in_utc_format(int(pn_id[32:45]))[0]}",
                        "relatedLots": [second_lot_id]
                    }],
                "submissionMethod": ["electronicSubmission"],
                "submissionMethodDetails": submission_method_details,
                "submissionMethodRationale": submission_method_rationale,
                "requiresElectronicCatalogue": False,
                "procurementMethodRationale": "create Pn: tender.procurementMethodRationale",
                "classification": {
                    "scheme": "CPV",
                    "id": get_value_by_new_cpv_code[0],
                    "description": get_value_by_new_cpv_code[1]
                },
                "value": {
                    "amount": 1650.00,
                    "currency": "EUR"
                }
            },
            "hasPreviousNotice": False,
            "purposeOfNotice": {
                "isACallForCompetition": False
            },
            "relatedProcesses": [{
                "id": "36b553f3-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": cp_id,
                "uri": f"{instance_tender_url}{cp_id}/{cp_id}"
            }]
        }
        json_notice_release_ev = {
            "ocid": ev_id,
            "id": f"{ev_id}-{ev_id[32:45]}",
            "date": f"{get_human_date_in_utc_format(int(ev_id[32:45]))[0]}",
            "tag": ["tender"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "c36f9952-06d5-41ef-9fe6-36722f1da414",
                "title": "Planning Notice",
                "description": "Contracting process is planned",
                "status": "active",
                "statusDetails": "clarification",
                "criteria": [{
                    "id": "9b62d854-acd3-479f-b0a9-402fe8081480",
                    "title": "create CNonPN: tender.criteria[0].title =Bankruptcy",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[0].description =Is the economic operator bankrupt? "
                                   "This information needs not be given if exclusion of economic operators in this "
                                   "case has been made mandatory under the applicable national law without any "
                                   "possibility of derogation where the economic operator is nevertheless able to "
                                   "perform the contract.",
                    "requirementGroups": [{
                        "id": "f83633d5-6d4e-4b9f-9bc2-8770f8bfb9b6",
                        "description": "create CNonPN: tender.criteria[0].requirementGroups[0].description =approve "
                                       "that Bankruptcy requirement group",
                        "requirements": [{
                            "id": "d5366584-8e57-445f-b1f6-55063bb29ea2",
                            "title": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements.title",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "description": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements."
                                           "description",
                            "eligibleEvidences": [{
                                "id": "1",
                                "title": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements[0]."
                                         "eligibleEvidences[0].title",
                                "type": "document",
                                "description": "create CNonPN: tender.criteria[0].requirementGroups[0]."
                                               "requirements[0].eligibleEvidences[0].description",
                                "relatedDocument": {
                                    "id": self.document_three_was_uploaded
                                }
                            }, {
                                "id": "2",
                                "title": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements[0]."
                                         "eligibleEvidences[1].title",
                                "type": "document",
                                "description": "create CNonPN: tender.criteria[0].requirementGroups[0]."
                                               "requirements[0].eligibleEvidences[1].description",
                                "relatedDocument": {
                                    "id": self.document_three_was_uploaded
                                }
                            }],
                            "expectedValue": False
                        }]
                    }],
                    "relatesTo": "tender",
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.EXCLUSION.CONVICTIONS.PARTICIPATION_IN_CRIMINAL_ORGANISATION"
                    }
                }, {
                    "id": "0b607a5e-e432-4d60-bcff-40c4de9ee04b",
                    "title": "create CNonPN: tender.criteria[1].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[1].description",
                    "requirementGroups": [{
                        "id": "437c395a-7a92-48c3-94bd-fcd3fb238304",
                        "description": "create CNonPN: tender.criteria[1].requirementGroups[0].description",
                        "requirements": [{
                            "id": "7bcf3819-a328-4560-b256-24c89b70d436",
                            "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[0].title",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "description": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements."
                                           "description",
                            "expectedValue": True
                        }, {
                            "id": "5b761cae-5c26-4266-b81d-9178232e931e",
                            "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[1]."
                                     "title =The number of years for proposed product warranty",
                            "dataType": "number",
                            "status": "active",
                            "datePublished": operation_date,
                            "description": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[1]."
                                           "description",
                            "period": {
                                "startDate": period[0],
                                "endDate": period[1]
                            },
                            "eligibleEvidences": [{
                                "id": "3",
                                "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[1]."
                                         "eligibleEvidences[0].title",
                                "type": "document",
                                "description": "create CNonPN: tender.criteria[1].requirementGroups[0]."
                                               "requirements[1].eligibleEvidences[0].description",
                                "relatedDocument": {
                                    "id": self.document_three_was_uploaded
                                }
                            }],
                            "minValue": 1.000,
                            "maxValue": 3.000
                        }]
                    }],
                    "relatesTo": "lot",
                    "relatedItem": first_lot_id,
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.SELECTION.ECONOMIC_FINANCIAL_STANDING.TURNOVER.GENERAL_YEARLY"
                    }
                }, {
                    "id": "11a3595b-4327-4382-a72f-e663f937a206",
                    "title": "create CNonPN: tender.criteria[2].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[2].description",
                    "requirementGroups": [{
                        "id": "779894eb-41c2-4db0-825c-27d3dbd522a6",
                        "description": "create CNonPN: tender.criteria[2].requirementGroups[0].description",
                        "requirements": [{
                            "id": "e30b1213-f94d-4364-9a75-e9532d7c98ed",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[0].requirements[0]."
                                     "title =Product has to be manufactured in the EU",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "expectedValue": True
                        }, {
                            "id": "e95d0bce-acf6-4873-867f-7a26a6935146",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[0]..requirements[1]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }, {
                        "id": "c1021836-1fe1-49e1-8286-42badf1b62aa",
                        "description": "create CNonPN: tender.criteria[2].requirementGroups[1].description",
                        "requirements": [{
                            "id": "0cef779c-9039-4a87-838d-1f8775a14f57",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[1].requirements[0]."
                                     "title =Product has to be manufactured in the EU",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "expectedValue": True
                        }, {
                            "id": "53cade1e-112a-441e-a2d0-64c2bc547f43",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[1]..requirements[1]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }],
                    "relatesTo": "tenderer",
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.EXCLUSION.NATIONAL.OTHER"
                    }
                }, {
                    "id": "a8168d9a-34c8-44b7-8a59-d126d770ffa2",
                    "title": "create CNonPN: tender.criteria[3].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[3].description =A minimum product warranty "
                                   "of 1 year is required for all bids 2",
                    "requirementGroups": [{
                        "id": "1992b2ca-4ac2-43c2-b1ef-90d41860c718",
                        "description": "create CNonPN: tender.criteria[3].requirementGroups[0].description",
                        "requirements": [{
                            "id": "aaa2e373-2fee-4da4-a153-16c89127a633",
                            "title": "create CNonPN: tender.criteria[3].requirementGroups[0].requirements[0]."
                                     "title = The number of years for proposed product warranty",
                            "dataType": "number",
                            "status": "active",
                            "datePublished": operation_date,
                            "period": {
                                "startDate": period[0],
                                "endDate": period[1]
                            },
                            "minValue": 1.000,
                            "maxValue": 3.000
                        }]
                    }],
                    "relatesTo": "item",
                    "relatedItem": first_item_id,
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.OTHER.EO_DATA.RELIES_ON_OTHER_CAPACITIES"
                    }
                }, {
                    "id": "a5569789-616d-407b-844e-8974611db63d",
                    "title": "create CNonPN: tender.criteria[4].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[4].description",
                    "requirementGroups": [{
                        "id": "e2e4291b-7e9c-401c-b9a6-2ec6bee0c85c",
                        "description": "create CNonPN: tender.criteria[4].requirementGroups[0].description",
                        "requirements": [{
                            "id": "4d104276-47fc-4d93-a694-444457b825e4",
                            "title": "create CNonPN: tender.criteria[4].requirementGroups[0].requirements[0]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }],
                    "relatesTo": "tender",
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.EXCLUSION.NATIONAL.OTHER"
                    }
                }, {
                    "id": "dd056608-225f-4e1b-9e22-e8b927f50678",
                    "title": "create CNonPN: tender.criteria[4].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[4].description",
                    "requirementGroups": [{
                        "id": "c6f455a8-dcd3-40ae-8518-c07bc68603c0",
                        "description": "create CNonPN: tender.criteria[4].requirementGroups[0].description",
                        "requirements": [{
                            "id": "9529530c-bdeb-45db-b559-aa9f5fba7b05",
                            "title": "create CNonPN: tender.criteria[4].requirementGroups[0].requirements[0]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }],
                    "relatesTo": "tender",
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.OTHER.EO_DATA.RELIES_ON_OTHER_CAPACITIES"
                    }
                }],
                "conversions": [{
                    "id": "1e49348e-1a13-409e-95f8-371cb7430a6a",
                    "relatesTo": "requirement",
                    "relatedItem": "7bcf3819-a328-4560-b256-24c89b70d436",
                    "rationale": "create CNonPN: tender.conversions[1].rationale",
                    "description": "create CNonPN: tender.conversions[1].description",
                    "coefficients": [{
                        "id": "3344c418-c0cb-40f5-86bd-2e7aab5d5e19",
                        "value": False,
                        "coefficient": 1
                    }]
                }, {
                    "id": "b61c8d3f-54cb-48cf-94d3-6547db1b6584",
                    "relatesTo": "requirement",
                    "relatedItem": "5b761cae-5c26-4266-b81d-9178232e931e",
                    "rationale": "create CNonPN: tender.conversions[3].rationale",
                    "description": "create CNonPN: tender.conversions[3].description",
                    "coefficients": [{
                        "id": "8e1c5c9d-9fd5-4524-8ee7-1dc69c392e25",
                        "value": 1.000,
                        "coefficient": 1
                    }, {
                        "id": "eea59dc3-cf39-43e4-85ae-c25f4207c378",
                        "value": 2.000,
                        "coefficient": 1
                    }, {
                        "id": "2ef0e48a-5359-4c2b-b4a7-e2e209239173",
                        "value": 3.000,
                        "coefficient": 0.93
                    }]
                }, {
                    "id": "602f52cb-6257-479b-b637-85bd1b94a3cf",
                    "relatesTo": "requirement",
                    "relatedItem": "aaa2e373-2fee-4da4-a153-16c89127a633",
                    "rationale": "create CNonPN: tender.conversions[6].rationale",
                    "description": "create CNonPN: tender.conversions[6].description",
                    "coefficients": [{
                        "id": "0b1fd4bc-dcb9-460d-89fa-ce44387b76ef",
                        "value": 1.000,
                        "coefficient": 1
                    }, {
                        "id": "c9bcba0e-f235-40c4-9023-1c4e7813e7a0",
                        "value": 2.000,
                        "coefficient": 1
                    }, {
                        "id": "998f9ae4-86a0-4c80-8973-f7d7cdc78351",
                        "value": 3.000,
                        "coefficient": 0.93
                    }]
                }, {
                    "id": "df048f38-c201-4aae-a529-a721a7687430",
                    "relatesTo": "requirement",
                    "relatedItem": "9529530c-bdeb-45db-b559-aa9f5fba7b05",
                    "rationale": "create CNonPN: tender.conversions[6].rationale",
                    "description": "create CNonPN: tender.conversions[6].description",
                    "coefficients": [{
                        "id": "49f34ab3-c0ad-4509-b77f-ead756c50419",
                        "value": "option_1",
                        "coefficient": 1
                    }, {
                        "id": "39819b5c-2c5c-40db-af46-2e6b6b2f0dcb",
                        "value": "option_2",
                        "coefficient": 1
                    }, {
                        "id": "0cda7c91-e74d-4f57-91bd-cae195078dda",
                        "value": "option_3",
                        "coefficient": 0.93
                    }]
                }],
                "items": [{
                    "id": first_item_id,
                    "internalId": "create Pn: tender.items[0].internalId",
                    "description": "create Pn: tender.items[0].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_first_item_cpv_code[0],
                        "description": get_value_by_first_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_first_item_cpvs_code[0],
                        "description": get_value_by_first_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "name": get_value_by_first_item_unit_id[1],
                        "id": get_value_by_first_item_unit_id[0]
                    },
                    "relatedLot": first_lot_id
                }, {
                    "id": second_item_id,
                    "internalId": "create Pn: tender.items[1].internalId",
                    "description": "create Pn: tender.items[1].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_second_item_cpv_code[0],
                        "description": get_value_by_second_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_second_item_cpvs_code[0],
                        "description": get_value_by_second_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_first_item_unit_id[0],
                        "name": get_value_by_first_item_unit_id[1]
                    },
                    "relatedLot": second_lot_id
                }],
                "lots": [{
                    "id": first_lot_id,
                    "internalId": "create Pn: tender.lots[0].internalId",
                    "title": "create Pn: tender.lots[0].title",
                    "description": "create Pn: tender.lots[0].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 1500.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[0].placeOfPerformance.address.streetAddress",
                            "postalCode": "create Pn: tender.lots[0].placeOfPerformance.address.postalCode",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        },
                        "description": "create Pn: tender.lots[0].placeOfPerformance.description"
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }, {
                    "id": second_lot_id,
                    "internalId": "create Pn: tender.lots[1].internalId",
                    "title": "create Pn: tender.lots[1].title",
                    "description": "create Pn: tender.lots[1].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 150.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[1].placeOfPerformance.address.streetAddress",
                            "postalCode": "create Pn: tender.lots[1].placeOfPerformance.address.postalCode",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        },
                        "description": "create Pn: tender.lots[1].placeOfPerformance.description"
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }],
                "lotGroups": [{
                    "optionToCombine": False
                }],
                "tenderPeriod": {
                    "startDate": enquiry_and_tender_period[2],
                    "endDate": enquiry_and_tender_period[3]
                },
                "enquiryPeriod": {
                    "startDate": enquiry_and_tender_period[0],
                    "endDate": enquiry_and_tender_period[1]
                },
                "auctionPeriod": {
                    "startDate": auction_date
                },
                "hasEnquiries": False,
                "documents": [{
                    "id": self.document_one_was_uploaded,
                    "documentType": "contractArrangements",
                    "title": "create Pn: tender.documents[0].title",
                    "description": "create Pn: tender.documents[0].description",
                    "url": f"{instance_storage_url}{self.document_one_was_uploaded}",
                    "datePublished": operation_date,
                    "relatedLots": [first_lot_id]
                }, {
                    "id": self.document_two_was_uploaded,
                    "documentType": "contractArrangements",
                    "title": "create Pn: tender.documents[1].title",
                    "description": "create Pn: tender.documents[1].description",
                    "url": f"{instance_storage_url}{self.document_two_was_uploaded}",
                    "datePublished": operation_date,
                    "relatedLots": [second_lot_id]
                }, {
                    "id": self.document_three_was_uploaded,
                    "documentType": "illustration",
                    "title": "create CNonPN: tender.documents[2].title",
                    "description": "create CNonPN: tender.documents[2].description",
                    "url": f"{instance_storage_url}"
                           f"{self.document_three_was_uploaded}",
                    "datePublished": operation_date,
                    "relatedLots": [first_lot_id]
                }],
                "awardCriteria": "ratedCriteria",
                "awardCriteriaDetails": "automated",
                "submissionMethod": ["electronicSubmission"],
                "submissionMethodDetails": submission_method_details,
                "submissionMethodRationale": submission_method_rationale,
                "requiresElectronicCatalogue": False,
                "procurementMethodModalities": ["electronicAuction"],
                "electronicAuctions": {
                    "details": [{
                        "id": "2cbf1162-4e8b-48d7-b64b-680b5fa6b350",
                        "relatedLot": first_lot_id,
                        "auctionPeriod": {
                            "startDate": auction_date
                        },
                        "electronicAuctionModalities": [{
                            "url": f"https://eauction.eprocurement.systems/auctions/{ev_id}/{first_lot_id}",
                            "eligibleMinimumDifference": {
                                "amount": 100.00,
                                "currency": "EUR"
                            }
                        }]
                    }, {
                        "id": "c19b09d5-3dcb-43a8-a1fc-096948abb403",
                        "relatedLot": second_lot_id,
                        "auctionPeriod": {
                            "startDate": auction_date
                        },
                        "electronicAuctionModalities": [{
                            "url": f"https://eauction.eprocurement.systems/auctions/{ev_id}/{second_lot_id}",
                            "eligibleMinimumDifference": {
                                "amount": 10.00,
                                "currency": "EUR"
                            }
                        }]
                    }]
                },
                "procurementMethodRationale": "create CNonPN: tender.procurementMethodRationale"
            },
            "hasPreviousNotice": True,
            "purposeOfNotice": {
                "isACallForCompetition": True
            },
            "relatedProcesses": [{
                "id": "12a3ea63-ceca-11eb-8aed-69d06bed4d57",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": cp_id,
                "uri": f"{instance_tender_url}{cp_id}/{cp_id}"
            }, {
                "id": "164cf531-ceca-11eb-8aed-69d06bed4d57",
                "relationship": ["planning"],
                "scheme": "ocid",
                "identifier": pn_id,
                "uri": f"{instance_tender_url}{cp_id}/{pn_id}"
            }]
        }

        json_notice_release_ev_new = {
            "ocid": ev_id,
            "id": f"{ev_id}-{period_for_amendment[1]}",
            "date": period_for_amendment[0],
            "tag": ["tender"],
            "initiationType": "tender",
            "language": self.lang,
            "tender": {
                "id": "c36f9952-06d5-41ef-9fe6-36722f1da414",
                "title": "Evaluation",
                "description": "Evaluation stage of contracting process",
                "status": "active",
                "statusDetails": "clarification",
                "criteria": [{
                    "id": "9b62d854-acd3-479f-b0a9-402fe8081480",
                    "title": "create CNonPN: tender.criteria[0].title =Bankruptcy",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[0].description =Is the economic operator bankrupt? "
                                   "This information needs not be given if exclusion of economic operators in this "
                                   "case has been made mandatory under the applicable national law without any "
                                   "possibility of derogation where the economic operator is nevertheless able to "
                                   "perform the contract.",
                    "requirementGroups": [{
                        "id": "f83633d5-6d4e-4b9f-9bc2-8770f8bfb9b6",
                        "description": "create CNonPN: tender.criteria[0].requirementGroups[0].description =approve "
                                       "that Bankruptcy requirement group",
                        "requirements": [{
                            "id": "d5366584-8e57-445f-b1f6-55063bb29ea2",
                            "title": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements.title",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "description": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements."
                                           "description",
                            "eligibleEvidences": [{
                                "id": "1",
                                "title": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements[0]."
                                         "eligibleEvidences[0].title",
                                "type": "document",
                                "description": "create CNonPN: tender.criteria[0].requirementGroups[0]."
                                               "requirements[0].eligibleEvidences[0].description",
                                "relatedDocument": {
                                    "id": self.document_three_was_uploaded
                                }
                            }, {
                                "id": "2",
                                "title": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements[0]."
                                         "eligibleEvidences[1].title",
                                "type": "document",
                                "description": "create CNonPN: tender.criteria[0].requirementGroups[0]."
                                               "requirements[0].eligibleEvidences[1].description",
                                "relatedDocument": {
                                    "id": self.document_three_was_uploaded
                                }
                            }],
                            "expectedValue": False
                        }]
                    }],
                    "relatesTo": "tender",
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.EXCLUSION.CONVICTIONS.PARTICIPATION_IN_CRIMINAL_ORGANISATION"
                    }
                }, {
                    "id": "0b607a5e-e432-4d60-bcff-40c4de9ee04b",
                    "title": "create CNonPN: tender.criteria[1].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[1].description",
                    "requirementGroups": [{
                        "id": "437c395a-7a92-48c3-94bd-fcd3fb238304",
                        "description": "create CNonPN: tender.criteria[1].requirementGroups[0].description",
                        "requirements": [{
                            "id": "7bcf3819-a328-4560-b256-24c89b70d436",
                            "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[0].title",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "description": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements."
                                           "description",
                            "expectedValue": True
                        }, {
                            "id": "5b761cae-5c26-4266-b81d-9178232e931e",
                            "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[1]."
                                     "title =The number of years for proposed product warranty",
                            "dataType": "number",
                            "status": "active",
                            "datePublished": operation_date,
                            "description": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[1]."
                                           "description",
                            "period": {
                                "startDate": period[0],
                                "endDate": period[1]
                            },
                            "eligibleEvidences": [{
                                "id": "3",
                                "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[1]."
                                         "eligibleEvidences[0].title",
                                "type": "document",
                                "description": "create CNonPN: tender.criteria[1].requirementGroups[0]."
                                               "requirements[1].eligibleEvidences[0].description",
                                "relatedDocument": {
                                    "id": self.document_three_was_uploaded
                                }
                            }],
                            "minValue": 1.000,
                            "maxValue": 3.000
                        }]
                    }],
                    "relatesTo": "lot",
                    "relatedItem": first_lot_id,
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.SELECTION.ECONOMIC_FINANCIAL_STANDING.TURNOVER.GENERAL_YEARLY"
                    }
                }, {
                    "id": "11a3595b-4327-4382-a72f-e663f937a206",
                    "title": "create CNonPN: tender.criteria[2].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[2].description",
                    "requirementGroups": [{
                        "id": "779894eb-41c2-4db0-825c-27d3dbd522a6",
                        "description": "create CNonPN: tender.criteria[2].requirementGroups[0].description",
                        "requirements": [{
                            "id": "e30b1213-f94d-4364-9a75-e9532d7c98ed",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[0].requirements[0]."
                                     "title =Product has to be manufactured in the EU",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "expectedValue": True
                        }, {
                            "id": "e95d0bce-acf6-4873-867f-7a26a6935146",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[0]..requirements[1]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }, {
                        "id": "c1021836-1fe1-49e1-8286-42badf1b62aa",
                        "description": "create CNonPN: tender.criteria[2].requirementGroups[1].description",
                        "requirements": [{
                            "id": "0cef779c-9039-4a87-838d-1f8775a14f57",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[1].requirements[0]."
                                     "title =Product has to be manufactured in the EU",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "expectedValue": True
                        }, {
                            "id": "53cade1e-112a-441e-a2d0-64c2bc547f43",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[1]..requirements[1]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }],
                    "relatesTo": "tenderer",
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.EXCLUSION.NATIONAL.OTHER"
                    }
                }, {
                    "id": "a8168d9a-34c8-44b7-8a59-d126d770ffa2",
                    "title": "create CNonPN: tender.criteria[3].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[3].description =A minimum product warranty "
                                   "of 1 year is required for all bids 2",
                    "requirementGroups": [{
                        "id": "1992b2ca-4ac2-43c2-b1ef-90d41860c718",
                        "description": "create CNonPN: tender.criteria[3].requirementGroups[0].description",
                        "requirements": [{
                            "id": "aaa2e373-2fee-4da4-a153-16c89127a633",
                            "title": "create CNonPN: tender.criteria[3].requirementGroups[0].requirements[0]."
                                     "title = The number of years for proposed product warranty",
                            "dataType": "number",
                            "status": "active",
                            "datePublished": operation_date,
                            "period": {
                                "startDate": period[0],
                                "endDate": period[1]
                            },
                            "minValue": 1.000,
                            "maxValue": 3.000
                        }]
                    }],
                    "relatesTo": "item",
                    "relatedItem": first_item_id,
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.OTHER.EO_DATA.RELIES_ON_OTHER_CAPACITIES"
                    }
                }, {
                    "id": "a5569789-616d-407b-844e-8974611db63d",
                    "title": "create CNonPN: tender.criteria[4].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[4].description",
                    "requirementGroups": [{
                        "id": "e2e4291b-7e9c-401c-b9a6-2ec6bee0c85c",
                        "description": "create CNonPN: tender.criteria[4].requirementGroups[0].description",
                        "requirements": [{
                            "id": "4d104276-47fc-4d93-a694-444457b825e4",
                            "title": "create CNonPN: tender.criteria[4].requirementGroups[0].requirements[0]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }],
                    "relatesTo": "tender",
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.EXCLUSION.NATIONAL.OTHER"
                    }
                }, {
                    "id": "dd056608-225f-4e1b-9e22-e8b927f50678",
                    "title": "create CNonPN: tender.criteria[4].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[4].description",
                    "requirementGroups": [{
                        "id": "c6f455a8-dcd3-40ae-8518-c07bc68603c0",
                        "description": "create CNonPN: tender.criteria[4].requirementGroups[0].description",
                        "requirements": [{
                            "id": "9529530c-bdeb-45db-b559-aa9f5fba7b05",
                            "title": "create CNonPN: tender.criteria[4].requirementGroups[0].requirements[0]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }],
                    "relatesTo": "tender",
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.OTHER.EO_DATA.RELIES_ON_OTHER_CAPACITIES"
                    }
                }],
                "conversions": [{
                    "id": "1e49348e-1a13-409e-95f8-371cb7430a6a",
                    "relatesTo": "requirement",
                    "relatedItem": "7bcf3819-a328-4560-b256-24c89b70d436",
                    "rationale": "create CNonPN: tender.conversions[1].rationale",
                    "description": "create CNonPN: tender.conversions[1].description",
                    "coefficients": [{
                        "id": "3344c418-c0cb-40f5-86bd-2e7aab5d5e19",
                        "value": False,
                        "coefficient": 1
                    }]
                }, {
                    "id": "b61c8d3f-54cb-48cf-94d3-6547db1b6584",
                    "relatesTo": "requirement",
                    "relatedItem": "5b761cae-5c26-4266-b81d-9178232e931e",
                    "rationale": "create CNonPN: tender.conversions[3].rationale",
                    "description": "create CNonPN: tender.conversions[3].description",
                    "coefficients": [{
                        "id": "8e1c5c9d-9fd5-4524-8ee7-1dc69c392e25",
                        "value": 1.000,
                        "coefficient": 1
                    }, {
                        "id": "eea59dc3-cf39-43e4-85ae-c25f4207c378",
                        "value": 2.000,
                        "coefficient": 1
                    }, {
                        "id": "2ef0e48a-5359-4c2b-b4a7-e2e209239173",
                        "value": 3.000,
                        "coefficient": 0.93
                    }]
                }, {
                    "id": "602f52cb-6257-479b-b637-85bd1b94a3cf",
                    "relatesTo": "requirement",
                    "relatedItem": "aaa2e373-2fee-4da4-a153-16c89127a633",
                    "rationale": "create CNonPN: tender.conversions[6].rationale",
                    "description": "create CNonPN: tender.conversions[6].description",
                    "coefficients": [{
                        "id": "0b1fd4bc-dcb9-460d-89fa-ce44387b76ef",
                        "value": 1.000,
                        "coefficient": 1
                    }, {
                        "id": "c9bcba0e-f235-40c4-9023-1c4e7813e7a0",
                        "value": 2.000,
                        "coefficient": 1
                    }, {
                        "id": "998f9ae4-86a0-4c80-8973-f7d7cdc78351",
                        "value": 3.000,
                        "coefficient": 0.93
                    }]
                }, {
                    "id": "df048f38-c201-4aae-a529-a721a7687430",
                    "relatesTo": "requirement",
                    "relatedItem": "9529530c-bdeb-45db-b559-aa9f5fba7b05",
                    "rationale": "create CNonPN: tender.conversions[6].rationale",
                    "description": "create CNonPN: tender.conversions[6].description",
                    "coefficients": [{
                        "id": "49f34ab3-c0ad-4509-b77f-ead756c50419",
                        "value": "option_1",
                        "coefficient": 1
                    }, {
                        "id": "39819b5c-2c5c-40db-af46-2e6b6b2f0dcb",
                        "value": "option_2",
                        "coefficient": 1
                    }, {
                        "id": "0cda7c91-e74d-4f57-91bd-cae195078dda",
                        "value": "option_3",
                        "coefficient": 0.93
                    }]
                }],
                "items": [{
                    "id": first_item_id,
                    "internalId": "create Pn: tender.items[0].internalId",
                    "description": "create Pn: tender.items[0].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_first_item_cpv_code[0],
                        "description": get_value_by_first_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_first_item_cpvs_code[0],
                        "description": get_value_by_first_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "name": get_value_by_first_item_unit_id[1],
                        "id": get_value_by_first_item_unit_id[0]
                    },
                    "relatedLot": first_lot_id
                }, {
                    "id": second_item_id,
                    "internalId": "create Pn: tender.items[1].internalId",
                    "description": "create Pn: tender.items[1].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_second_item_cpv_code[0],
                        "description": get_value_by_second_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_second_item_cpvs_code[0],
                        "description": get_value_by_second_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_first_item_unit_id[0],
                        "name": get_value_by_first_item_unit_id[1]
                    },
                    "relatedLot": second_lot_id
                }],
                "lots": [{
                    "id": first_lot_id,
                    "internalId": "create Pn: tender.lots[0].internalId",
                    "title": "create Pn: tender.lots[0].title",
                    "description": "create Pn: tender.lots[0].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 1500.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[0].placeOfPerformance.address.streetAddress",
                            "postalCode": "create Pn: tender.lots[0].placeOfPerformance.address.postalCode",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        },
                        "description": "create Pn: tender.lots[0].placeOfPerformance.description"
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }, {
                    "id": second_lot_id,
                    "internalId": "create Pn: tender.lots[1].internalId",
                    "title": "create Pn: tender.lots[1].title",
                    "description": "create Pn: tender.lots[1].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 150.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[1].placeOfPerformance.address.streetAddress",
                            "postalCode": "create Pn: tender.lots[1].placeOfPerformance.address.postalCode",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        },
                        "description": "create Pn: tender.lots[1].placeOfPerformance.description"
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }],
                "lotGroups": [{
                    "optionToCombine": False
                }],
                "tenderPeriod": {
                    "startDate": enquiry_and_tender_period[2],
                    "endDate": enquiry_and_tender_period[3]
                },
                "enquiryPeriod": {
                    "startDate": enquiry_and_tender_period[0],
                    "endDate": enquiry_and_tender_period[1]
                },
                "auctionPeriod": {
                    "startDate": auction_date
                },
                "hasEnquiries": False,
                "amendments": [{
                    "id": self.amendment_id,
                    "type": "cancellation",
                    "status": "pending",
                    "relatesTo": "tender",
                    "relatedItem": ev_id,
                    "date": period_for_amendment[0],
                    "description": "cancel_tender: amendments[0].description",
                    "rationale": "cancel_tender: amendments[0].rationale",
                    "documents": [{
                        "documentType": "cancellationDetails",
                        "id": self.document_five_was_uploaded,
                        "title": "cancel_tender: amendments[0].documents[0].title",
                        "description": "cancel_tender: amendments[0].documents[0].description",
                        "url": f"{instance_storage_url}"
                               f"{self.document_five_was_uploaded}",
                        "datePublished": period[0]
                    }]
                }],
                "documents": [{
                    "id": self.document_one_was_uploaded,
                    "documentType": "contractArrangements",
                    "title": "create Pn: tender.documents[0].title",
                    "description": "create Pn: tender.documents[0].description",
                    "url": f"{instance_storage_url}{self.document_one_was_uploaded}",
                    "datePublished": operation_date,
                    "relatedLots": [first_lot_id]
                }, {
                    "id": self.document_two_was_uploaded,
                    "documentType": "contractArrangements",
                    "title": "create Pn: tender.documents[1].title",
                    "description": "create Pn: tender.documents[1].description",
                    "url": f"{instance_storage_url}"
                           f"{self.document_two_was_uploaded}",
                    "datePublished": operation_date,
                    "relatedLots": [second_lot_id]
                }, {
                    "id": self.document_three_was_uploaded,
                    "documentType": "illustration",
                    "title": "create CNonPN: tender.documents[2].title",
                    "description": "create CNonPN: tender.documents[2].description",
                    "url": f"{instance_storage_url}"
                           f"{self.document_three_was_uploaded}",
                    "datePublished": operation_date,
                    "relatedLots": [first_lot_id]
                }],
                "awardCriteria": "ratedCriteria",
                "awardCriteriaDetails": "automated",
                "submissionMethod": ["electronicSubmission"],
                "submissionMethodDetails": submission_method_details,
                "submissionMethodRationale": submission_method_rationale,
                "requiresElectronicCatalogue": False,
                "procurementMethodModalities": ["electronicAuction"],
                "electronicAuctions": {
                    "details": [{
                        "id": "2cbf1162-4e8b-48d7-b64b-680b5fa6b350",
                        "relatedLot": first_lot_id,
                        "auctionPeriod": {
                            "startDate": auction_date
                        },
                        "electronicAuctionModalities": [{
                            "url": f"https://eauction.eprocurement.systems/auctions/{ev_id}/{first_lot_id}",
                            "eligibleMinimumDifference": {
                                "amount": 100.00,
                                "currency": "EUR"
                            }
                        }]
                    }, {
                        "id": "c19b09d5-3dcb-43a8-a1fc-096948abb403",
                        "relatedLot": second_lot_id,
                        "auctionPeriod": {
                            "startDate": auction_date
                        },
                        "electronicAuctionModalities": [{
                            "url": f"https://eauction.eprocurement.systems/auctions/{ev_id}/{second_lot_id}",
                            "eligibleMinimumDifference": {
                                "amount": 10.00,
                                "currency": "EUR"
                            }
                        }]
                    }]
                },
                "procurementMethodRationale": "create CNonPN: tender.procurementMethodRationale"
            },
            "hasPreviousNotice": True,
            "purposeOfNotice": {
                "isACallForCompetition": True
            },
            "relatedProcesses": [{
                "id": "12a3ea63-ceca-11eb-8aed-69d06bed4d57",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": cp_id,
                "uri": f"{instance_tender_url}{cp_id}/{cp_id}"
            }, {
                "id": "164cf531-ceca-11eb-8aed-69d06bed4d57",
                "relationship": ["planning"],
                "scheme": "ocid",
                "identifier": pn_id,
                "uri": f"{instance_tender_url}{cp_id}/{pn_id}"
            }]
        }

        json_notice_compiled_release_ms = {
            "ocid": cp_id,
            "id": f"{cp_id}-{ev_id[32:45]}",
            "date": f"{get_human_date_in_utc_format(int(ev_id[32:45]))[0]}",
            "tag": ["compiled"],
            "language": self.lang,
            "initiationType": "tender",
            "planning": {
                "budget": {
                    "description": "create Pn: planning.budget.description",
                    "amount": {
                        "amount": 2000.00,
                        "currency": "EUR"
                    },
                    "isEuropeanUnionFunded": True,
                    "budgetBreakdown": [{
                        "id": fs_id,
                        "description": "create Fs: planning.budget.description",
                        "amount": {
                            "amount": 2000.00,
                            "currency": "EUR"
                        },
                        "period": {
                            "startDate": period[0],
                            "endDate": period[1]
                        },
                        "sourceParty": {
                            "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                            "name": self.funder_name,
                        },
                        "europeanUnionFunding": {
                            "projectIdentifier": "create Fs: planning.budget.europeanUnionFunding.projectIdentifier",
                            "projectName": "create Fs: planning.budget.europeanUnionFunding.projectName",
                            "uri": "create Fs: planning.budget.europeanUnionFunding.uri"
                        }
                    }]
                },
                "rationale": "create Pn: planning.rationale"
            },
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "title": "create Pn: tender.title",
                "description": "create Pn: tender.description",
                "status": "active",
                "statusDetails": "evaluation",
                "value": {
                    "amount": 1650.00,
                    "currency": "EUR"
                },
                "procurementMethod": "open",
                "procurementMethodDetails": procurement_method_details_from_mdm,
                "procurementMethodRationale": "create CNonPN: tender.procurementMethodRationale",
                "mainProcurementCategory": "works",
                "hasEnquiries": False,
                "eligibilityCriteria": eligibility_criteria_from_mdm,
                "contractPeriod": {
                    "startDate": contract_period[0],
                    "endDate": contract_period[1]
                },
                "procuringEntity": {
                    "id": "MD-IDNO-4",
                    "name": "create Pn: tender.procuringEntity.name"
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
                "legalBasis": "DIRECTIVE_2014_25_EU",
                "procedureOutsourcing": {
                    "procedureOutsourced": False
                },
                "procurementMethodAdditionalInfo": "create CNonPN: tender.procurementMethodAdditionalInfo",
                "dynamicPurchasingSystem": {
                    "hasDynamicPurchasingSystem": False
                },
                "framework": {
                    "isAFramework": False
                }
            },
            "parties": [{
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name,
                "identifier": {
                    "scheme": self.buyer_identifier_scheme,
                    "id": self.buyer_identifier_id,
                    "legalName": self.buyer_identifier_legal_name,
                    "uri": self.buyer_identifier_uri
                },
                "address": {
                    "streetAddress": self.buyer_address_street_address,
                    "postalCode": self.buyer_address_postal_code,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.buyer_address_address_details_country_id,
                            "description": "Moldova, Republica",
                            "uri": "https://www.iso.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": self.buyer_address_address_details_region_id,
                            "description": "mun.Chişinău",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": self.buyer_address_address_details_locality_scheme,
                            "id": self.buyer_address_address_details_locality_id,
                            "description": self.buyer_address_address_details_locality_description,
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "additionalIdentifiers": [{
                    "scheme": "create Ei: buyer.additionalIdentifiers[0].scheme",
                    "id": "create Ei: buyer.additionalIdentifiers[0].id",
                    "legalName": "create Ei: buyer.additionalIdentifiers[0].legalName",
                    "uri": "create Ei: buyer.additionalIdentifiers[0].uri"
                }],
                "contactPoint": {
                    "name": self.buyer_contact_point_name,
                    "email": self.buyer_contact_point_email,
                    "telephone": self.buyer_contact_point_telephone,
                    "faxNumber": self.buyer_contact_point_fax_number,
                    "url": self.buyer_contact_point_url
                },
                "details": {
                    "typeOfBuyer": "NATIONAL_AGENCY",
                    "mainGeneralActivity": "HEALTH",
                    "mainSectoralActivity": "WATER"
                },
                "roles": ["buyer"]
            }, {
                "id": f"{self.payer_identifier_scheme}-{self.payer_identifier_id}",
                "name": self.payer_name,
                "identifier": {
                    "scheme": self.payer_identifier_scheme,
                    "id": self.payer_identifier_id,
                    "legalName": self.payer_identifier_legal_name,
                    "uri": self.payer_identifier_uri
                },
                "address": {
                    "streetAddress": self.payer_address_street,
                    "postalCode": self.payer_address_postal_code,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.payer_address_postal_code,
                            "description": "Moldova, Republica",
                            "uri": "https://www.iso.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": self.payer_address_address_details_region_id,
                            "description": "Donduşeni",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": self.payer_address_address_details_locality_scheme,
                            "id": self.payer_address_address_details_locality_id,
                            "description": self.payer_address_address_details_locality_description,
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "additionalIdentifiers": [{
                    "scheme": "create Fs: tender.procuringEntity.additionalIdentifiers[0].scheme",
                    "id": "create Fs: tender.procuringEntity.additionalIdentifiers[0].id",
                    "legalName": "create Fs: tender.procuringEntity.additionalIdentifiers[0].legalName",
                    "uri": "create Fs: tender.procuringEntity.additionalIdentifiers[0].uri"
                }],
                "contactPoint": {
                    "name": self.payer_contact_point_name,
                    "email": self.payer_contact_point_email,
                    "telephone": self.payer_contact_point_telephone,
                    "faxNumber": self.payer_contact_point_fax_number,
                    "url": self.payer_contact_point_url
                },
                "roles": ["payer"]
            }, {
                "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                "name": self.funder_name,
                "identifier": {
                    "scheme": self.funder_identifier_scheme,
                    "id": self.funder_identifier_id,
                    "legalName": self.funder_identifier_legal_name,
                    "uri": self.funder_identifier_uri
                },
                "address": {
                    "streetAddress": self.funder_address_street,
                    "postalCode": self.funder_address_postal_code,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.funder_address_address_details_country_id,
                            "description": "Moldova, Republica",
                            "uri": "https://www.iso.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": self.funder_address_address_details_region_id,
                            "description": "Cahul",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": self.funder_address_address_details_locality_scheme,
                            "id": self.funder_address_address_details_locality_id,
                            "description": self.funder_address_address_details_locality_description,
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "additionalIdentifiers": [{
                    "scheme": "create Fs: buyer.additionalIdentifiers[0].scheme",
                    "id": "create Fs: buyer.additionalIdentifiers[0].id",
                    "legalName": "create Fs: buyer.additionalIdentifiers[0].legalName",
                    "uri": "create Fs: buyer.additionalIdentifiers[0].uri"
                }],
                "contactPoint": {
                    "name": self.funder_contact_point_name,
                    "email": self.funder_contact_point_email,
                    "telephone": self.funder_contact_point_telephone,
                    "faxNumber": self.funder_contact_point_fax,
                    "url": self.funder_contact_point_url
                },
                "roles": ["funder"]
            }, {
                "id": "MD-IDNO-4",
                "name": "create Pn: tender.procuringEntity.name",
                "identifier": {
                    "scheme": "MD-IDNO",
                    "id": "4",
                    "legalName": "create Pn: tender.procuringEntity.identigfier.legalName",
                    "uri": "create Pn: tender.procuringEntity.identifier.uri"
                },
                "address": {
                    "streetAddress": "street address",
                    "postalCode": "02232",
                    "addressDetails": {
                        "country": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["country"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['uri']
                        },
                        "region": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["region"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['uri']
                        },
                        "locality": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["locality"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['uri']
                        }
                    }
                },
                "additionalIdentifiers": [{
                    "scheme": "create Pn: tender.procuringEntity.additionalIdentifiers[0].scheme",
                    "id": "create Pn: tender.procuringEntity.additionalIdentifiers[0].id",
                    "legalName": "create Pn: tender.procuringEntity.additionalIdentifiers[0].legalName",
                    "uri": "create Pn: tender.procuringEntity.additionalIdentifiers[0].uri"
                }],
                "contactPoint": {
                    "name": "name",
                    "email": "email",
                    "telephone": "456-95-96",
                    "faxNumber": "fax-number",
                    "url": "url"
                },
                "persones": [{
                    "id": "MD-IDNO-create CNonPN: procuringEntity.persones[0].identifier.id",
                    "title": "create CNonPN: procuringEntity.persones[0].title",
                    "name": "create CNonPN: procuringEntity.persones[0].name",
                    "identifier": {
                        "scheme": "MD-IDNO",
                        "id": "create CNonPN: procuringEntity.persones[0].identifier.id",
                        "uri": "create CNonPN: procuringEntity.persones[0].identifier.uri"
                    },
                    "businessFunctions": [{
                        "id": "create CNonPN: procuringEntity.persones[0].businessFunctions[0].id",
                        "type": "procurementOfficer",
                        "jobTitle": "create CNonPN: procuringEntity.persones[0].businessFunctions[0].jobTitle",
                        "period": {
                            "startDate": period[0]
                        },
                        "documents": [{
                            "id": self.document_three_was_uploaded,
                            "documentType": "regulatoryDocument",
                            "title": "create CNonPN: procuringEntity.persones[0].businessFunctions[0].title",
                            "description": "create CNonPN: procuringEntity.persones[0].businessFunctions[0]."
                                           "description",
                            "url": f"{instance_storage_url}"
                                   f"{self.document_three_was_uploaded}",
                            "datePublished": operation_date
                        }]
                    }]
                }],
                "roles": ["procuringEntity"]
            }],
            "relatedProcesses": [{
                "id": "36b553f0-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["planning"],
                "scheme": "ocid",
                "identifier": pn_id,
                "uri": f"{instance_tender_url}{cp_id}/{pn_id}"
            }, {
                "id": "36b553f1-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["x_expenditureItem"],
                "scheme": "ocid",
                "identifier": ei_id,
                "uri": f"{instance_budget_url}{ei_id}/{ei_id}"
            }, {
                "id": "36b553f2-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["x_fundingSource"],
                "scheme": "ocid",
                "identifier": fs_id,
                "uri": f"{instance_budget_url}{ei_id}/{fs_id}"
            },
                {
                    "id": "ed0f7290-cee4-11eb-8aed-69d06bed4d57",
                    "relationship": ["x_evaluation"],
                    "scheme": "ocid",
                    "identifier": ev_id,
                    "uri": f"{instance_tender_url}{cp_id}/{ev_id}"
                }
            ]

        }
        json_notice_compiled_release_pn = {
            "ocid": pn_id,
            "id": f"{pn_id}-{ev_id[32:45]}",
            "date": f"{get_human_date_in_utc_format(int(ev_id[32:45]))[0]}",
            "tag": ["planningUpdate"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "title": "Planning Notice",
                "description": "Contracting process is planned",
                "status": "complete",
                "statusDetails": "empty",
                "items": [{
                    "id": first_item_id,
                    "internalId": "create Pn: tender.items[0].internalId",
                    "description": "create Pn: tender.items[0].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_first_item_cpv_code[0],
                        "description": get_value_by_first_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_first_item_cpvs_code[0],
                        "description": get_value_by_first_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_first_item_unit_id[0],
                        "name": get_value_by_first_item_unit_id[1]
                    },
                    "relatedLot": first_lot_id
                }, {
                    "id": second_item_id,
                    "internalId": "create Pn: tender.items[1].internalId",
                    "description": "create Pn: tender.items[1].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_second_item_cpv_code[0],
                        "description": get_value_by_second_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_second_item_cpvs_code[0],
                        "description": get_value_by_second_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_second_item_unit_id[0],
                        "name": get_value_by_second_item_unit_id[1]
                    },
                    "relatedLot": second_lot_id
                }],
                "lots": [{
                    "id": first_lot_id,
                    "internalId": "create Pn: tender.lots[0].internalId",
                    "title": "create Pn: tender.lots[0].title",
                    "description": "create Pn: tender.lots[0].internalId.description",
                    "status": "planning",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 1500.00,
                        "currency": "EUR"
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
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[0].placeOfPerformance.address.streetAddress",
                            "postalCode": "create Pn: tender.lots[0].placeOfPerformance.address.postalCode",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        },
                        "description": "create Pn: tender.lots[0].placeOfPerformance.description"
                    },
                    "options": [{
                        "hasOptions": False
                    }]
                }, {
                    "id": second_lot_id,
                    "internalId": "create Pn: tender.lots[1].internalId",
                    "title": "create Pn: tender.lots[1].title",
                    "description": "create Pn: tender.lots[1].internalId.description",
                    "status": "planning",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 150.00,
                        "currency": "EUR"
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
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[1].placeOfPerformance.address.streetAddress",
                            "postalCode": "create Pn: tender.lots[1].placeOfPerformance.address.postalCode",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        },
                        "description": "create Pn: tender.lots[1].placeOfPerformance.description"
                    },
                    "options": [{
                        "hasOptions": False
                    }]
                }],
                "lotGroups": [{
                    "optionToCombine": False
                }],
                "tenderPeriod": {
                    "startDate": period[3]
                },
                "hasEnquiries": False,
                "documents": [
                    {
                        "id": self.document_one_was_uploaded,
                        "documentType": "contractArrangements",
                        "title": "title of document",
                        "description": "descrition of document",
                        "url": f"{instance_storage_url}"
                               f"{self.document_one_was_uploaded}",
                        "datePublished": f"{get_human_date_in_utc_format(int(pn_id[32:45]))[0]}",
                        "relatedLots": [first_lot_id]
                    },
                    {
                        "id": self.document_two_was_uploaded,
                        "documentType": "contractArrangements",
                        "title": "title of document",
                        "description": "descrition of document",
                        "url": f"{instance_storage_url}"
                               f"{self.document_two_was_uploaded}",
                        "datePublished": f"{get_human_date_in_utc_format(int(pn_id[32:45]))[0]}",
                        "relatedLots": [second_lot_id]
                    }],
                "submissionMethod": ["electronicSubmission"],
                "submissionMethodDetails": submission_method_details,
                "submissionMethodRationale": submission_method_rationale,
                "requiresElectronicCatalogue": False,
                "procurementMethodRationale": "create Pn: tender.procurementMethodRationale",
                "classification": {
                    "scheme": "CPV",
                    "id": get_value_by_new_cpv_code[0],
                    "description": get_value_by_new_cpv_code[1]
                },
                "value": {
                    "amount": 1650.00,
                    "currency": "EUR"
                }
            },
            "hasPreviousNotice": False,
            "purposeOfNotice": {
                "isACallForCompetition": False
            },
            "relatedProcesses": [{
                "id": "36b553f3-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": cp_id,
                "uri": f"{instance_tender_url}/{cp_id}/{cp_id}"
            }]
        }
        json_notice_compiled_release_ev = {
            "ocid": ev_id,
            "id": f"{ev_id}-{period_for_amendment[1]}",
            "date": period_for_amendment[0],
            "tag": ["tender"],
            "initiationType": "tender",
            "language": self.lang,
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "title": "Evaluation",
                "description": "Evaluation stage of contracting process",
                "status": "active",
                "statusDetails": "clarification",
                "criteria": [{
                    "id": "58b814dc-ada7-40f1-b34e-fcb360830c2c",
                    "title": "create CNonPN: tender.criteria[0].title =Bankruptcy",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[0].description =Is the economic operator "
                                   "bankrupt? This information needs not be given if exclusion of economic "
                                   "operators in this case has been made mandatory under the applicable national "
                                   "law without any possibility of derogation where the economic operator is "
                                   "nevertheless able to perform the contract.",
                    "requirementGroups": [{
                        "id": "2f16e84f-aca2-4970-8a9a-6f253d20f8b3",
                        "description": "create CNonPN: tender.criteria[0].requirementGroups[0].description "
                                       "=approve that Bankruptcy requirement group",
                        "requirements": [{
                            "id": "01fcb528-6de6-4c07-9383-57c698116f18",
                            "title": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements.title",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "description": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements."
                                           "description",
                            "eligibleEvidences": [{
                                "id": "1",
                                "title": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements[0]."
                                         "eligibleEvidences[0].title",
                                "type": "document",
                                "description": "create CNonPN: tender.criteria[0].requirementGroups[0]."
                                               "requirements[0].eligibleEvidences[0].description",
                                "relatedDocument": {
                                    "id": self.document_three_was_uploaded
                                }
                            }, {
                                "id": "2",
                                "title": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements[0]."
                                         "eligibleEvidences[1].title",
                                "type": "document",
                                "description": "create CNonPN: tender.criteria[0].requirementGroups[0]."
                                               "requirements[0].eligibleEvidences[1].description",
                                "relatedDocument": {
                                    "id": self.document_three_was_uploaded
                                }
                            }],
                            "expectedValue": False
                        }]
                    }],
                    "relatesTo": "tender",
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.EXCLUSION.CONVICTIONS.PARTICIPATION_IN_CRIMINAL_ORGANISATION"
                    }
                }, {
                    "id": "a662195e-ad48-4ffc-9b51-7b01a3c04be0",
                    "title": "create CNonPN: tender.criteria[1].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[1].description",
                    "requirementGroups": [{
                        "id": "9ebb3a38-7835-48e2-84d5-c1debb0a4739",
                        "description": "create CNonPN: tender.criteria[1].requirementGroups[0].description",
                        "requirements": [{
                            "id": "1a149ebc-5d0c-4dd6-92b3-85ed9672a675",
                            "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[0].title",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "description": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements."
                                           "description",
                            "expectedValue": True
                        }, {
                            "id": "a4b456bb-32a6-4946-adf7-2ddaeb282c0e",
                            "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[1]."
                                     "title =The number of years for proposed product warranty",
                            "dataType": "number",
                            "status": "active",
                            "datePublished": operation_date,
                            "description": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements"
                                           "[1].description",
                            "period": {
                                "startDate": period[0],
                                "endDate": period[1]
                            },
                            "eligibleEvidences": [{
                                "id": "3",
                                "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[1]."
                                         "eligibleEvidences[0].title",
                                "type": "document",
                                "description": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements"
                                               "[1].eligibleEvidences[0].description",
                                "relatedDocument": {
                                    "id": self.document_three_was_uploaded
                                }
                            }],
                            "minValue": 1.000,
                            "maxValue": 3.000
                        }]
                    }],
                    "relatesTo": "lot",
                    "relatedItem": first_lot_id,
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.SELECTION.ECONOMIC_FINANCIAL_STANDING.TURNOVER.GENERAL_YEARLY"
                    }
                }, {
                    "id": "8e250762-2508-4175-af7e-1a5ca085a1e7",
                    "title": "create CNonPN: tender.criteria[2].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[2].description",
                    "requirementGroups": [{
                        "id": "ff3545aa-47ec-4666-8c8a-93c6e06f85d8",
                        "description": "create CNonPN: tender.criteria[2].requirementGroups[0].description",
                        "requirements": [{
                            "id": "e3f5ecdb-985d-42a0-97ca-85920a819095",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[0].requirements[0]."
                                     "title =Product has to be manufactured in the EU",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "expectedValue": True
                        }, {
                            "id": "22b9bb1f-692d-425a-bd11-3f4569ae35f3",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[0]..requirements[1]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }, {
                        "id": "31359580-435e-40d5-9a17-a40d03686a17",
                        "description": "create CNonPN: tender.criteria[2].requirementGroups[1].description",
                        "requirements": [{
                            "id": "9daba23f-510d-4f7f-a449-af17a3416081",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[1].requirements[0]."
                                     "title =Product has to be manufactured in the EU",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "expectedValue": True
                        }, {
                            "id": "03fc9deb-f9ca-4dcf-a9f0-e1dff43c6e42",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[1]..requirements[1]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }],
                    "relatesTo": "tenderer",
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.EXCLUSION.NATIONAL.OTHER"
                    }
                }, {
                    "id": "43fe2c58-14eb-47aa-9854-cbf594b1110e",
                    "title": "create CNonPN: tender.criteria[3].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[3].description =A minimum product warranty "
                                   "of 1 year is required for all bids 2",
                    "requirementGroups": [{
                        "id": "f18230c4-04e9-41af-b900-1a6521011c20",
                        "description": "create CNonPN: tender.criteria[3].requirementGroups[0].description",
                        "requirements": [{
                            "id": "25fe2901-8393-4198-88fc-01625039c48f",
                            "title": "create CNonPN: tender.criteria[3].requirementGroups[0].requirements[0]."
                                     "title = The number of years for proposed product warranty",
                            "dataType": "number",
                            "status": "active",
                            "datePublished": operation_date,
                            "period": {
                                "startDate": period[0],
                                "endDate": period[1]
                            },
                            "minValue": 1.000,
                            "maxValue": 3.000
                        }]
                    }],
                    "relatesTo": "item",
                    "relatedItem": first_item_id,
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.OTHER.EO_DATA.RELIES_ON_OTHER_CAPACITIES"
                    }
                }, {
                    "id": "5c8c1ce9-937c-41c6-a717-42db617da57b",
                    "title": "create CNonPN: tender.criteria[4].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[4].description",
                    "requirementGroups": [{
                        "id": "05f1412a-8cef-4534-b02f-2ecb8b82a34d",
                        "description": "create CNonPN: tender.criteria[4].requirementGroups[0].description",
                        "requirements": [{
                            "id": "4fde10c0-306f-4170-bc90-9290935c8ae1",
                            "title": "create CNonPN: tender.criteria[4].requirementGroups[0].requirements[0]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }],
                    "relatesTo": "tender",
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.EXCLUSION.NATIONAL.OTHER"
                    }
                }, {
                    "id": "6af5e886-b24d-4fa0-9e02-62c44833e609",
                    "title": "create CNonPN: tender.criteria[4].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[4].description",
                    "requirementGroups": [{
                        "id": "37fbcb8c-3cb5-4447-9597-04f161590ecd",
                        "description": "create CNonPN: tender.criteria[4].requirementGroups[0].description",
                        "requirements": [{
                            "id": "fb28d72b-4136-4535-8d5b-c0fae7a3bfcf",
                            "title": "create CNonPN: tender.criteria[4].requirementGroups[0].requirements[0]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }],
                    "relatesTo": "tender",
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.OTHER.EO_DATA.RELIES_ON_OTHER_CAPACITIES"
                    }
                }],
                "conversions": [{
                    "id": "72b46408-c9d1-40ff-ba93-ee8fdfa2a0f1",
                    "relatesTo": "requirement",
                    "relatedItem": "1a149ebc-5d0c-4dd6-92b3-85ed9672a675",
                    "rationale": "create CNonPN: tender.conversions[1].rationale",
                    "description": "create CNonPN: tender.conversions[1].description",
                    "coefficients": [{
                        "id": "05690b92-24b7-4422-9816-17fe8e3ed13b",
                        "value": False,
                        "coefficient": 1
                    }]
                }, {
                    "id": "7a93bc3b-f061-4f3b-a95a-9950bd577dcf",
                    "relatesTo": "requirement",
                    "relatedItem": "a4b456bb-32a6-4946-adf7-2ddaeb282c0e",
                    "rationale": "create CNonPN: tender.conversions[3].rationale",
                    "description": "create CNonPN: tender.conversions[3].description",
                    "coefficients": [{
                        "id": "0c8079ec-3c0e-4563-85f1-992975f7e04b",
                        "value": 1.000,
                        "coefficient": 1
                    }, {
                        "id": "f6f95e95-59af-42c1-9bc8-ecefcef27e7b",
                        "value": 2.000,
                        "coefficient": 1
                    }, {
                        "id": "a95aebf9-2d2c-41fa-9b43-1535682b20e8",
                        "value": 3.000,
                        "coefficient": 0.93
                    }]
                }, {
                    "id": "1b994f29-3341-4d21-a63a-22d430d40a13",
                    "relatesTo": "requirement",
                    "relatedItem": "25fe2901-8393-4198-88fc-01625039c48f",
                    "rationale": "create CNonPN: tender.conversions[6].rationale",
                    "description": "create CNonPN: tender.conversions[6].description",
                    "coefficients": [{
                        "id": "f25d0cf9-4787-44d7-b4b8-93e8db5a35c2",
                        "value": 1.000,
                        "coefficient": 1
                    }, {
                        "id": "ee713dff-62cd-4a36-abe3-53b332ed163d",
                        "value": 2.000,
                        "coefficient": 1
                    }, {
                        "id": "e1b625e7-28f1-4114-bf97-a5d5a4b4aaae",
                        "value": 3.000,
                        "coefficient": 0.93
                    }]
                }, {
                    "id": "4735af2c-766a-4c9a-891c-f2a84b5cb1b2",
                    "relatesTo": "requirement",
                    "relatedItem": "fb28d72b-4136-4535-8d5b-c0fae7a3bfcf",
                    "rationale": "create CNonPN: tender.conversions[6].rationale",
                    "description": "create CNonPN: tender.conversions[6].description",
                    "coefficients": [{
                        "id": "16acc108-d7cb-4ea4-af1c-c8bad67bda86",
                        "value": "option_1",
                        "coefficient": 1
                    }, {
                        "id": "231b3997-4c5f-4886-ae1d-1bd458801d54",
                        "value": "option_2",
                        "coefficient": 1
                    }, {
                        "id": "d248589c-55a4-4f74-817b-ddc7f8291805",
                        "value": "option_3",
                        "coefficient": 0.93
                    }]
                }],
                "items": [{
                    "id": first_item_id,
                    "internalId": "create Pn: tender.items[0].internalId",
                    "description": "create Pn: tender.items[0].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_first_item_cpv_code[0],
                        "description": get_value_by_first_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_first_item_cpvs_code[0],
                        "description": get_value_by_first_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_first_item_unit_id[0],
                        "name": get_value_by_first_item_unit_id[1]
                    },
                    "relatedLot": first_lot_id
                }, {
                    "id": second_item_id,
                    "internalId": "create Pn: tender.items[1].internalId",
                    "description": "create Pn: tender.items[1].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_second_item_cpv_code[0],
                        "description": get_value_by_second_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_second_item_cpvs_code[0],
                        "description": get_value_by_second_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_second_item_unit_id[0],
                        "name": get_value_by_second_item_unit_id[1]
                    },
                    "relatedLot": second_lot_id
                }],
                "lots": [{
                    "id": first_lot_id,
                    "internalId": "create Pn: tender.lots[0].internalId",
                    "title": "create Pn: tender.lots[0].title",
                    "description": "create Pn: tender.lots[0].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 1500.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[0].placeOfPerformance.address.streetAddress",
                            "postalCode": "create Pn: tender.lots[0].placeOfPerformance.address.postalCode",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        },
                        "description": "create Pn: tender.lots[0].placeOfPerformance.description"
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }, {
                    "id": second_lot_id,
                    "internalId": "create Pn: tender.lots[1].internalId",
                    "title": "create Pn: tender.lots[1].title",
                    "description": "create Pn: tender.lots[1].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 150.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[1].placeOfPerformance.address.streetAddress",
                            "postalCode": "create Pn: tender.lots[1].placeOfPerformance.address.postalCode",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        },
                        "description": "create Pn: tender.lots[1].placeOfPerformance.description"
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }],
                "lotGroups": [{
                    "optionToCombine": False
                }],
                "tenderPeriod": {
                    "startDate": enquiry_and_tender_period[2],
                    "endDate": enquiry_and_tender_period[3]
                },
                "enquiryPeriod": {
                    "startDate": enquiry_and_tender_period[0],
                    "endDate": enquiry_and_tender_period[1]
                },
                "auctionPeriod": {
                    "startDate": auction_date
                },
                "hasEnquiries": False,
                "amendments": [{
                    "id": self.amendment_id,
                    "type": "cancellation",
                    "status": "pending",
                    "relatesTo": "tender",
                    "relatedItem": ev_id,
                    "date": period_for_amendment[0],
                    "description": "cancel_tender: amendments[0].description",
                    "rationale": "cancel_tender: amendments[0].rationale",
                    "documents": [{
                        "documentType": "cancellationDetails",
                        "id": self.document_five_was_uploaded,
                        "title": "cancel_tender: amendments[0].documents[0].title",
                        "description": "cancel_tender: amendments[0].documents[0].description",
                        "url": f"{instance_storage_url}"
                               f"{self.document_five_was_uploaded}",
                        "datePublished": period[0]
                    }]
                }],
                "documents": [{
                    "id": self.document_one_was_uploaded,
                    "documentType": "contractArrangements",
                    "title": "create Pn: tender.documents[0].title",
                    "description": "create Pn: tender.documents[0].description",
                    "url": f"{instance_storage_url}{self.document_one_was_uploaded}",
                    "datePublished": operation_date,
                    "relatedLots": [first_lot_id]
                }, {
                    "id": self.document_two_was_uploaded,
                    "documentType": "contractArrangements",
                    "title": "create Pn: tender.documents[1].title",
                    "description": "create Pn: tender.documents[1].description",
                    "url": f"{instance_storage_url}"
                           f"{self.document_two_was_uploaded}",
                    "datePublished": operation_date,
                    "relatedLots": [second_lot_id]
                }, {
                    "id": self.document_three_was_uploaded,
                    "documentType": "illustration",
                    "title": "create CNonPN: tender.documents[2].title",
                    "description": "create CNonPN: tender.documents[2].description",
                    "url": f"{instance_storage_url}"
                           f"{self.document_three_was_uploaded}",
                    "datePublished": operation_date,
                    "relatedLots": [first_lot_id]
                }],
                "awardCriteria": "ratedCriteria",
                "awardCriteriaDetails": "automated",
                "submissionMethod": ["electronicSubmission"],
                "submissionMethodDetails": submission_method_details,
                "submissionMethodRationale": submission_method_rationale,
                "requiresElectronicCatalogue": False,
                "procurementMethodModalities": ["electronicAuction"],
                "electronicAuctions": {
                    "details": [{
                        "id": "9f8c8d7c-127a-42ab-b72d-d215e5cc6b40",
                        "relatedLot": first_lot_id,
                        "auctionPeriod": {
                            "startDate": auction_date
                        },
                        "electronicAuctionModalities": [{
                            "url": f"https://eauction.eprocurement.systems/auctions/{ev_id}/{first_lot_id}",
                            "eligibleMinimumDifference": {
                                "amount": 100.00,
                                "currency": "EUR"
                            }
                        }]
                    }, {
                        "id": "5f2caa86-b76b-410f-b181-8528b233f43c",
                        "relatedLot": second_lot_id,
                        "auctionPeriod": {
                            "startDate": auction_date
                        },
                        "electronicAuctionModalities": [{
                            "url": f"https://eauction.eprocurement.systems/auctions/{ev_id}/{second_lot_id}",
                            "eligibleMinimumDifference": {
                                "amount": 10.00,
                                "currency": "EUR"
                            }
                        }]
                    }]
                },
                "procurementMethodRationale": "create CNonPN: tender.procurementMethodRationale"
            },
            "hasPreviousNotice": True,
            "purposeOfNotice": {
                "isACallForCompetition": True
            },
            "relatedProcesses": [{
                "id": "e84a2253-cee4-11eb-8aed-69d06bed4d57",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": cp_id,
                "uri": f"{instance_tender_url}{cp_id}/{cp_id}"
            }, {
                "id": "ed0f7291-cee4-11eb-8aed-69d06bed4d57",
                "relationship": ["planning"],
                "scheme": "ocid",
                "identifier": pn_id,
                "uri": f"{instance_tender_url}{cp_id}/{pn_id}"
            }]
        }

        kafka = Kafka(instance=self.instance)
        kafka.connect_kafka_producer()
        kafka.publish_message_into_chronograph_in_clarification(
            cp_id=cp_id,
            ev_id=ev_id,
            enquiry_end=enquiry_and_tender_period[1]
        )
        kafka.publish_message_into_chronograph_in_submission(
            cp_id=cp_id,
            ev_id=ev_id,
            tender_end=enquiry_and_tender_period[3]
        )

        key_space_ocds.execute(f"INSERT INTO orchestrator_context (cp_id,context) VALUES ("
                               f"'{ev_id}','{json.dumps(json_orchestrator_context)}');").one()
        key_space_access.execute(f"INSERT INTO tenders (cpid, ocid, token_entity,created_date,json_data, owner) "
                                 f"VALUES ('{cp_id}', '{ev_id}', '{pn_token}', {ev_id[32:45]}, "
                                 f"'{json.dumps(json_access_tender)}','{owner}');").one()
        key_space_auctions.execute(
            f"INSERT INTO auctions (cpid, ocid, api_version, country, data, operation_id, row_version, status ) "
            f"VALUES ('{cp_id}', '{ev_id}', '1.0.0', '{self.country}', '{json.dumps(json_auction_auctions)}', "
            f"'{uuid.uuid1()}',{0}, {1});").one()
        key_space_clarification.execute(
            f"INSERT INTO periods (cpid, ocid, end_date, owner, start_date) "
            f"VALUES ('{cp_id}', '{ev_id}', {get_timestamp_from_human_date(enquiry_and_tender_period[1])}, '{owner}', "
            f"{ev_id[32:45]});").one()
        key_space_submission.execute(
            f"INSERT INTO periods (cpid, ocid, end_date, start_date) "
            f"VALUES ('{cp_id}', '{ev_id}', {get_timestamp_from_human_date(enquiry_and_tender_period[3])}, "
            f"{get_timestamp_from_human_date(enquiry_and_tender_period[1])});").one()
        key_space_ocds.execute(f"INSERT INTO notice_offset (cp_id,release_date, stage, status) "
                               f"VALUES ('{cp_id}', {ev_id[32:45]}, 'EV', 'active');").one()
        key_space_ocds.execute(
            f"INSERT INTO notice_release (cp_id,oc_id, release_id, json_data, release_date, stage) "
            f"VALUES ('{cp_id}', '{cp_id}', '{cp_id + '-' + ev_id[32:45]}' ,'{json.dumps(json_notice_release_ms)}',"
            f"{ev_id[32:45]},'');").one()
        key_space_ocds.execute(
            f"INSERT INTO notice_release (cp_id,oc_id, release_id, json_data, release_date, stage) "
            f"VALUES ('{cp_id}', '{pn_id}', '{pn_id + '-' + ev_id[32:45]}' ,'{json.dumps(json_notice_release_pn)}',"
            f"{ev_id[32:45]},'PN');").one()
        key_space_ocds.execute(
            f"INSERT INTO notice_release (cp_id,oc_id, release_id, json_data, release_date, stage) "
            f"VALUES ('{cp_id}', '{ev_id}', '{ev_id + '-' + ev_id[32:45]}','{json.dumps(json_notice_release_ev)}',"
            f"{ev_id[32:45]},'EV');").one()
        key_space_ocds.execute(
            f"INSERT INTO notice_release (cp_id,oc_id, release_id, json_data, release_date, stage) "
            f"VALUES ('{cp_id}', '{ev_id}', '{ev_id + '-' + str(period_for_amendment[1])}',"
            f"'{json.dumps(json_notice_release_ev_new)}',"
            f"{period_for_amendment[1]},'EV');").one()

        key_space_ocds.execute(
            f"INSERT INTO notice_compiled_release (cp_id,oc_id, json_data, publish_date, release_date, "
            f"release_id, stage, status) VALUES ('{cp_id}', '{cp_id}', '{json.dumps(json_notice_compiled_release_ms)}',"
            f"{ev_id[32:45]},{ev_id[32:45]}, '{cp_id + '-' + ev_id[32:45]}','', 'active');").one()
        key_space_ocds.execute(
            f"INSERT INTO notice_compiled_release (cp_id,oc_id, json_data, publish_date, release_date, "
            f"release_id, stage, status) VALUES ('{cp_id}', '{pn_id}', '{json.dumps(json_notice_compiled_release_pn)}',"
            f"{ev_id[32:45]},{ev_id[32:45]}, '{pn_id + '-' + ev_id[32:45]}','PN', 'active');").one()
        key_space_revision.execute(f"INSERT INTO amendments (cpid, ocid, id, data) "
                                   f"VALUES ('{cp_id}', '{ev_id}', {self.amendment_id}, "
                                   f"'{json.dumps(json_amendments)}');").one()

        key_space_ocds.execute(f"INSERT INTO notice_offset (cp_id,release_date, stage, status) "
                               f"VALUES ('{cp_id}', {period_for_amendment[1]}, 'EV', 'active');").one()

        key_space_ocds.execute(
            f"INSERT INTO notice_compiled_release (cp_id,oc_id, json_data, publish_date, release_date, "
            f"release_id, stage, status) VALUES ('{cp_id}', '{ev_id}', '{json.dumps(json_notice_compiled_release_ev)}',"
            f"{period[2]},{period_for_amendment[1]}, '{ev_id + '-' + str(period_for_amendment[1])}','EV', "
            f"'active');").one()
        record = f"{instance_tender_url}{cp_id}"
        ms_release = f"{instance_tender_url}{cp_id}/{cp_id}"
        pn_release = f"{instance_tender_url}{cp_id}/{pn_id}"
        ev_release = f"{instance_tender_url}{cp_id}/{ev_id}"
        return cp_id, pn_id, pn_token, ev_id, record, ms_release, pn_release, ev_release, self.amendment_id, \
               self.amendment_token

    @allure.step('Insert CnOnPn: based on FS: treasury - obligatory, based on EI: without items - obligatory')
    def insert_cancel_tender_obligatory(self, first_lot_id, second_lot_id, first_item_id, second_item_id,
                                        second_tender, second_enquiry):
        auth_provider = PlainTextAuthProvider(username=self.cassandra_username, password=self.cassandra_password)
        cluster = Cluster([self.cassandra_cluster], auth_provider=auth_provider)
        key_space_ocds = cluster.connect('ocds')
        key_space_access = cluster.connect('access')
        key_space_clarification = cluster.connect('clarification')
        key_space_submission = cluster.connect('submission')
        key_space_revision = cluster.connect('revision')
        owner = "445f6851-c908-407d-9b45-14b92f3e964b"
        ei_id = prepared_cp_id()
        fs_id = prepared_fs_oc_id(ei_id)
        cp_id = prepared_cp_id()
        pn_id = prepared_pn_oc_id(cp_id)
        pn_token = uuid4()
        ev_id = prepared_cn_oc_id(cp_id)
        period = get_period()
        period_for_amendment = get_period_for_amendment()
        contract_period = get_contract_period()
        enquiry_and_tender_period = create_enquiry_and_tender_period(
            second_enquiry=second_enquiry,
            second_tender=second_tender
        )

        operation_date = time_at_now()
        calculate_new_cpv_code = get_new_classification_id(
            self.first_item_cpv,
            self.second_item_cpv
        )
        get_value_by_new_cpv_code = get_value_from_classification_cpv_dictionary_xls(
            calculate_new_cpv_code,
            self.lang
        )
        get_value_by_first_item_cpv_code = get_value_from_classification_cpv_dictionary_xls(
            self.first_item_cpv,
            self.lang
        )
        get_value_by_second_item_cpv_code = get_value_from_classification_cpv_dictionary_xls(
            self.second_item_cpv,
            self.lang
        )
        get_value_by_first_item_cpvs_code = get_value_from_cpvs_dictionary_csv(
            self.first_item_additional_classifications,
            self.lang
        )
        get_value_by_second_item_cpvs_code = get_value_from_cpvs_dictionary_csv(
            self.second_item_additional_classifications,
            self.lang
        )
        get_value_by_first_item_unit_id = get_value_from_classification_unit_dictionary_csv(
            self.first_item_unit_id,
            self.lang
        )
        get_value_by_second_item_unit_id = get_value_from_classification_unit_dictionary_csv(
            self.second_item_unit_id,
            self.lang
        )

        mdm = MdmService(
            instance=self.instance
        )
        data_pn = mdm.process_tender_data(self.pmd).json()
        submission_method_details = data_pn["data"]["tender"]["submissionMethodDetails"]
        submission_method_rationale = data_pn["data"]["tender"]["submissionMethodRationale"]

        procurement_method_details_from_mdm = data_pn["data"]["tender"]["procurementMethodDetails"]
        eligibility_criteria_from_mdm = data_pn["data"]["tender"]["eligibilityCriteria"]
        instance_tender_url = None
        instance_budget_url = None
        instance_storage_url = None
        if self.instance == "dev":
            instance_tender_url = "http://dev.public.eprocurement.systems/tenders/"
            instance_budget_url = "http://dev.public.eprocurement.systems/budgets/"
            instance_storage_url = "https://dev.bpe.eprocurement.systems/api/v1/storage/get/"
        if self.instance == "sandbox":
            instance_tender_url = "http://public.eprocurement.systems/tenders/"
            instance_budget_url = "http://public.eprocurement.systems/budgets/"
            instance_storage_url = "http://storage.eprocurement.systems/get/"
        json_orchestrator_context = {
            "cpid": cp_id,
            "ocid": ev_id,
            "operationId": f"{uuid4()}",
            "requestId": f"{uuid4()}",
            "owner": owner,
            "stage": "EV",
            "prevStage": "EV",
            "phase": "clarification",
            "processType": "cancelTender",
            "operationType": "tenderCancellation",
            "country": self.country,
            "language": self.lang,
            "pmd": self.pmd,
            "startDate": period_for_amendment[0],
            "timeStamp": period_for_amendment[1],
            "isAuction": False
        }

        json_access_tender = {
            "ocid": cp_id,
            "planning": {
                "budget": {
                    "amount": {
                        "amount": 2000.00,
                        "currency": "EUR"
                    },
                    "isEuropeanUnionFunded": False,
                    "budgetBreakdown": [{
                        "id": fs_id,
                        "amount": {
                            "amount": 2000.00,
                            "currency": "EUR"
                        },
                        "period": {
                            "startDate": period[0],
                            "endDate": period[1]
                        },
                        "sourceParty": {
                            "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                            "name": self.buyer_name,
                        }
                    }]
                }
            },
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "status": "active",
                "statusDetails": "clarification",
                "title": "create Pn: tender.title",
                "description": "create Pn: tender.description",
                "classification": {
                    "scheme": "CPV",
                    "id": get_value_by_new_cpv_code[0],
                    "description": get_value_by_new_cpv_code[1]
                },
                "tenderPeriod": {
                    "startDate": enquiry_and_tender_period[2],
                    "endDate": enquiry_and_tender_period[3]
                },
                "enquiryPeriod": {
                    "startDate": enquiry_and_tender_period[0],
                    "endDate": enquiry_and_tender_period[1]
                },
                "acceleratedProcedure": {
                    "isAcceleratedProcedure": False
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
                "procedureOutsourcing": {
                    "procedureOutsourced": False
                },
                "framework": {
                    "isAFramework": False
                },
                "dynamicPurchasingSystem": {
                    "hasDynamicPurchasingSystem": False
                },
                "legalBasis": "DIRECTIVE_2014_25_EU",
                "procurementMethod": "open",
                "procurementMethodDetails": procurement_method_details_from_mdm,
                "mainProcurementCategory": "works",
                "eligibilityCriteria": eligibility_criteria_from_mdm,
                "contractPeriod": {
                    "startDate": contract_period[0],
                    "endDate": contract_period[1]
                },
                "procuringEntity": {
                    "id": "MD-IDNO-4",
                    "name": "create Pn: tender.procuringEntity.name",
                    "identifier": {
                        "scheme": "MD-IDNO",
                        "id": "4",
                        "legalName": "create Pn: tender.procuringEntity.identifier.legalName"
                    },
                    "address": {
                        "streetAddress": "create Pn: tender.procuringEntity.address.streetAddress",
                        "addressDetails": {
                            "country": {
                                "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "country"]['scheme'],
                                "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "country"]['id'],
                                "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                    "addressDetails"]["country"]['description'],
                                "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "country"]['uri']
                            },
                            "region": {
                                "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "region"]['scheme'],
                                "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "region"]['id'],
                                "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                    "addressDetails"]["region"]['description'],
                                "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "region"]['uri']
                            },
                            "locality": {
                                "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "locality"]['scheme'],
                                "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "locality"]['id'],
                                "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                    "addressDetails"]["locality"]['description'],
                                "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "locality"]['uri']

                            }
                        }
                    },
                    "contactPoint": {
                        "name": "create Pn: tender.procuringEntity.contactPoint.name",
                        "email": "create Pn: tender.procuringEntity.contactPoint.email",
                        "telephone": "create Pn: tender.procuringEntity.contactPoint.telephone"
                    }
                },
                "value": {
                    "amount": 1650.00,
                    "currency": "EUR"
                },
                "lotGroups": [{
                    "optionToCombine": False
                }],
                "lots": [{
                    "id": first_lot_id,
                    "title": "create Pn: tender.lots[0].title",
                    "description": "create Pn: tender.lots[0].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 1500.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[0].placeOfPerformance.address.streetAddress",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        }
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }, {
                    "id": second_lot_id,
                    "title": "create Pn: tender.lots[1].title",
                    "description": "create Pn: tender.lots[1].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 150.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[1].placeOfPerformance.address.streetAddress",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        }
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }],
                "items": [{
                    "id": first_item_id,
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_first_item_cpv_code[0],
                        "description": get_value_by_first_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_first_item_cpvs_code[0],
                        "description": get_value_by_first_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_first_item_unit_id[0],
                        "name": get_value_by_first_item_unit_id[1]
                    },
                    "description": "create Pn: tender.items[0].description",
                    "relatedLot": first_lot_id
                }, {
                    "id": second_item_id,
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_second_item_cpv_code[0],
                        "description": get_value_by_second_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_second_item_cpvs_code[0],
                        "description": get_value_by_second_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_second_item_unit_id[0],
                        "name": get_value_by_second_item_unit_id[1]
                    },
                    "description": "create Pn: tender.items[1].description",
                    "relatedLot": second_lot_id
                }],
                "awardCriteria": "ratedCriteria",
                "awardCriteriaDetails": "automated",
                "requiresElectronicCatalogue": False,
                "submissionMethod": ["electronicSubmission"],
                "submissionMethodRationale": submission_method_rationale,
                "submissionMethodDetails": submission_method_details,
                "documents": [
                    {
                        "id": self.document_three_was_uploaded,
                        "documentType": "evaluationCriteria",
                        "title": "create CNonPN: tender.documents[2].title"
                    }
                ]
            }
        }
        json_amendments = {
            "id": self.amendment_id,
            "date": period_for_amendment[0],
            "rationale": "cancel_tender: amendments[0].rationale",
            "status": "pending",
            "type": "cancellation",
            "relatesTo": "tender",
            "relatedItem": ev_id,
            "token": self.amendment_token,
            "owner": "445f6851-c908-407d-9b45-14b92f3e964b"
        }
        json_notice_release_ms = {
            "ocid": cp_id,
            "id": f"{cp_id}-{ev_id[32:45]}",
            "date": f"{get_human_date_in_utc_format(int(ev_id[32:45]))[0]}",
            "tag": ["compiled"],
            "language": self.lang,
            "initiationType": "tender",
            "planning": {
                "budget": {
                    "amount": {
                        "amount": 2000.00,
                        "currency": "EUR"
                    },
                    "isEuropeanUnionFunded": False,
                    "budgetBreakdown": [{
                        "id": fs_id,
                        "amount": {
                            "amount": 2000.00,
                            "currency": "EUR"
                        },
                        "period": {
                            "startDate": period[0],
                            "endDate": period[1]
                        },
                        "sourceParty": {
                            "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                            "name": self.buyer_name,
                        }
                    }]
                }
            },
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "title": "create Pn: tender.title",
                "description": "create Pn: tender.description",
                "status": "active",
                "statusDetails": "evaluation",
                "value": {
                    "amount": 1650.00,
                    "currency": "EUR"
                },
                "procurementMethod": "open",
                "procurementMethodDetails": procurement_method_details_from_mdm,
                "mainProcurementCategory": "works",
                "hasEnquiries": False,
                "eligibilityCriteria": eligibility_criteria_from_mdm,
                "contractPeriod": {
                    "startDate": contract_period[0],
                    "endDate": contract_period[1]
                },
                "procuringEntity": {
                    "id": "MD-IDNO-4",
                    "name": "create Pn: tender.procuringEntity.name"
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
                "legalBasis": "DIRECTIVE_2014_25_EU",
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
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name,
                "identifier": {
                    "scheme": self.buyer_identifier_scheme,
                    "id": self.buyer_identifier_id,
                    "legalName": self.buyer_identifier_legal_name
                },
                "address": {
                    "streetAddress": self.buyer_address_street_address,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.buyer_address_address_details_country_id,
                            "description": "Moldova, Republica",
                            "uri": "https://www.iso.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": self.buyer_address_address_details_region_id,
                            "description": "Cahul",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": self.buyer_address_address_details_locality_scheme,
                            "id": self.buyer_address_address_details_locality_id,
                            "description": self.buyer_address_address_details_locality_description,
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "contactPoint": {
                    "name": self.buyer_contact_point_name,
                    "email": self.buyer_contact_point_email,
                    "telephone": self.buyer_contact_point_telephone
                },
                "roles": [
                    "buyer"]
            }, {
                "id": f"{self.payer_identifier_scheme}-{self.payer_identifier_id}",
                "name": self.payer_name,
                "identifier": {
                    "scheme": self.payer_identifier_scheme,
                    "id": self.payer_identifier_id,
                    "legalName": self.payer_identifier_legal_name
                },
                "address": {
                    "streetAddress": self.payer_address_street,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.payer_address_address_details_country_id,
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": self.payer_address_address_details_region_id,
                            "description": "Cahul",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": self.payer_address_address_details_locality_scheme,
                            "id": self.payer_address_address_details_locality_id,
                            "description": self.payer_address_address_details_locality_description,
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "contactPoint": {
                    "name": self.payer_contact_point_name,
                    "email": self.payer_contact_point_email,
                    "telephone": self.payer_contact_point_telephone
                },
                "roles": ["payer"]
            }, {
                "id": "MD-IDNO-4",
                "name": "create Pn: tender.procuringEntity.name",
                "identifier": {
                    "scheme": "MD-IDNO",
                    "id": "4",
                    "legalName": "create Pn: tender.procuringEntity.identigfier.legalName"
                },
                "address": {
                    "streetAddress": "create Pn: tender.procuringEntity.address.streetAddress",
                    "addressDetails": {
                        "country": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["country"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['uri']
                        },
                        "region": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["region"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['uri']
                        },
                        "locality": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["locality"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['uri']

                        }
                    }
                },
                "contactPoint": {
                    "name": "create Pn: tender.procuringEntity.contactPoint.name",
                    "email": "create Pn: tender.procuringEntity.contactPoint.email",
                    "telephone": "create Pn: tender.procuringEntity.contactPoint.telephone"
                },
                "roles": ["procuringEntity"]
            }],
            "relatedProcesses": [{
                "id": "36b553f0-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["planning"],
                "scheme": "ocid",
                "identifier": pn_id,
                "uri": f"{instance_tender_url}{cp_id}/{pn_id}"
            }, {
                "id": "36b553f1-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["x_expenditureItem"],
                "scheme": "ocid",
                "identifier": ei_id,
                "uri": f"{instance_budget_url}{ei_id}/{ei_id}"
            }, {
                "id": "36b553f2-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["x_fundingSource"],
                "scheme": "ocid",
                "identifier": fs_id,
                "uri": f"{instance_budget_url}{ei_id}/{fs_id}"
            },
                {
                    "id": "164cf530-ceca-11eb-8aed-69d06bed4d57",
                    "relationship": ["x_evaluation"],
                    "scheme": "ocid",
                    "identifier": ev_id,
                    "uri": f"{instance_tender_url}{cp_id}/{ev_id}"
                }
            ]
        }
        json_notice_release_pn = {
            "ocid": pn_id,
            "id": f"{pn_id}-{ev_id[32:45]}",
            "date": f"{get_human_date_in_utc_format(int(ev_id[32:45]))[0]}",
            "tag": ["planningUpdate"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "title": "Planning Notice",
                "description": "Contracting process is planned",
                "status": "complete",
                "statusDetails": "empty",
                "lotGroups": [{
                    "optionToCombine": False
                }],
                "tenderPeriod": {
                    "startDate": period[3]
                },
                "hasEnquiries": False,
                "submissionMethod": ["electronicSubmission"],
                "submissionMethodDetails": submission_method_details,
                "submissionMethodRationale": submission_method_rationale,
                "requiresElectronicCatalogue": False,
                "procurementMethodRationale": "create Pn: tender.procurementMethodRationale",
                "classification": {
                    "scheme": "CPV",
                    "id": get_value_by_new_cpv_code[0],
                    "description": get_value_by_new_cpv_code[1]
                },
                "value": {
                    "amount": 1650.00,
                    "currency": "EUR"
                }
            },
            "hasPreviousNotice": False,
            "purposeOfNotice": {
                "isACallForCompetition": False
            },
            "relatedProcesses": [{
                "id": "36b553f3-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": cp_id,
                "uri": f"{instance_tender_url}{cp_id}/{cp_id}"
            }]
        }
        json_notice_release_ev = {
            "ocid": ev_id,
            "id": f"{ev_id}-{ev_id[32:45]}",
            "date": f"{get_human_date_in_utc_format(int(ev_id[32:45]))[0]}",
            "tag": ["tender"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "c36f9952-06d5-41ef-9fe6-36722f1da414",
                "title": "Planning Notice",
                "description": "Contracting process is planned",
                "status": "active",
                "statusDetails": "clarification",
                "items": [{
                    "id": first_item_id,
                    "description": "create Pn: tender.items[0].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_first_item_cpv_code[0],
                        "description": get_value_by_first_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_first_item_cpvs_code[0],
                        "description": get_value_by_first_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "name": get_value_by_first_item_unit_id[1],
                        "id": get_value_by_first_item_unit_id[0]
                    },
                    "relatedLot": first_lot_id
                }, {
                    "id": second_item_id,
                    "description": "create Pn: tender.items[1].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_second_item_cpv_code[0],
                        "description": get_value_by_second_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_second_item_cpvs_code[0],
                        "description": get_value_by_second_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_second_item_unit_id[0],
                        "name": get_value_by_second_item_unit_id[1]
                    },
                    "relatedLot": second_lot_id
                }],
                "lots": [{
                    "id": first_lot_id,
                    "title": "create Pn: tender.lots[0].title",
                    "description": "create Pn: tender.lots[0].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 1500.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[0].placeOfPerformance.address.streetAddress",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        }
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }, {
                    "id": second_lot_id,
                    "title": "create Pn: tender.lots[1].title",
                    "description": "create Pn: tender.lots[1].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 150.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[1].placeOfPerformance.address.streetAddress",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        }
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }],
                "lotGroups": [{
                    "optionToCombine": False
                }],
                "tenderPeriod": {
                    "startDate": enquiry_and_tender_period[2],
                    "endDate": enquiry_and_tender_period[3]
                },
                "enquiryPeriod": {
                    "startDate": enquiry_and_tender_period[0],
                    "endDate": enquiry_and_tender_period[1]
                },
                "hasEnquiries": False,
                "documents": [{
                    "id": self.document_three_was_uploaded,
                    "documentType": "illustration",
                    "title": "create CNonPN: tender.documents[2].title",
                    "url": f"{instance_storage_url}"
                           f"{self.document_three_was_uploaded}",
                    "datePublished": operation_date
                }],
                "awardCriteria": "ratedCriteria",
                "awardCriteriaDetails": "automated",
                "submissionMethod": ["electronicSubmission"],
                "submissionMethodDetails": submission_method_details,
                "submissionMethodRationale": submission_method_rationale,
                "requiresElectronicCatalogue": False
            },
            "hasPreviousNotice": True,
            "purposeOfNotice": {
                "isACallForCompetition": True
            },
            "relatedProcesses": [{
                "id": "12a3ea63-ceca-11eb-8aed-69d06bed4d57",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": cp_id,
                "uri": f"{instance_tender_url}{cp_id}/{cp_id}"
            }, {
                "id": "164cf531-ceca-11eb-8aed-69d06bed4d57",
                "relationship": ["planning"],
                "scheme": "ocid",
                "identifier": pn_id,
                "uri": f"{instance_tender_url}{cp_id}/{pn_id}"
            }]
        }
        json_notice_release_ev_new = {
            "ocid": ev_id,
            "id": f"{ev_id}-{period_for_amendment[1]}",
            "date": period_for_amendment[0],
            "tag": ["tender"],
            "initiationType": "tender",
            "language": self.lang,
            "tender": {
                "id": "c36f9952-06d5-41ef-9fe6-36722f1da414",
                "title": "Evaluation",
                "description": "Evaluation stage of contracting process",
                "status": "active",
                "statusDetails": "clarification",
                "items": [{
                    "id": first_item_id,
                    "description": "create Pn: tender.items[0].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_first_item_cpv_code[0],
                        "description": get_value_by_first_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_first_item_cpvs_code[0],
                        "description": get_value_by_first_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "name": get_value_by_first_item_unit_id[1],
                        "id": get_value_by_first_item_unit_id[0]
                    },
                    "relatedLot": first_lot_id
                }, {
                    "id": second_item_id,
                    "internalId": "create Pn: tender.items[1].internalId",
                    "description": "create Pn: tender.items[1].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_second_item_cpv_code[0],
                        "description": get_value_by_second_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_second_item_cpvs_code[0],
                        "description": get_value_by_second_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_first_item_unit_id[0],
                        "name": get_value_by_first_item_unit_id[1]
                    },
                    "relatedLot": second_lot_id
                }],
                "lots": [{
                    "id": first_lot_id,
                    "title": "create Pn: tender.lots[0].title",
                    "description": "create Pn: tender.lots[0].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 1500.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[0].placeOfPerformance.address.streetAddress",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        }
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }, {
                    "id": second_lot_id,
                    "title": "create Pn: tender.lots[1].title",
                    "description": "create Pn: tender.lots[1].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 150.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[1].placeOfPerformance.address.streetAddress",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        }
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }],
                "lotGroups": [{
                    "optionToCombine": False
                }],
                "tenderPeriod": {
                    "startDate": enquiry_and_tender_period[2],
                    "endDate": enquiry_and_tender_period[3]
                },
                "enquiryPeriod": {
                    "startDate": enquiry_and_tender_period[0],
                    "endDate": enquiry_and_tender_period[1]
                },
                "hasEnquiries": False,
                "amendments": [{
                    "id": self.amendment_id,
                    "type": "cancellation",
                    "status": "pending",
                    "relatesTo": "tender",
                    "relatedItem": ev_id,
                    "date": period_for_amendment[0],
                    "rationale": "cancel_tender: amendments[0].rationale"
                }],
                "documents": [{
                    "id": self.document_one_was_uploaded,
                    "documentType": "contractArrangements",
                    "title": "create Pn: tender.documents[0].title",
                    "description": "create Pn: tender.documents[0].description",
                    "url": f"{instance_storage_url}{self.document_one_was_uploaded}",
                    "datePublished": operation_date,
                    "relatedLots": [first_lot_id]
                }],
                "awardCriteria": "ratedCriteria",
                "awardCriteriaDetails": "automated",
                "submissionMethod": ["electronicSubmission"],
                "submissionMethodDetails": submission_method_details,
                "submissionMethodRationale": submission_method_rationale,
                "requiresElectronicCatalogue": False
            },
            "hasPreviousNotice": True,
            "purposeOfNotice": {
                "isACallForCompetition": True
            },
            "relatedProcesses": [{
                "id": "12a3ea63-ceca-11eb-8aed-69d06bed4d57",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": cp_id,
                "uri": f"{instance_tender_url}{cp_id}/{cp_id}"
            }, {
                "id": "164cf531-ceca-11eb-8aed-69d06bed4d57",
                "relationship": ["planning"],
                "scheme": "ocid",
                "identifier": pn_id,
                "uri": f"{instance_tender_url}{cp_id}/{pn_id}"
            }]
        }
        json_notice_compiled_release_ms = {
            "ocid": cp_id,
            "id": f"{cp_id}-{ev_id[32:45]}",
            "date": f"{get_human_date_in_utc_format(int(ev_id[32:45]))[0]}",
            "tag": ["compiled"],
            "language": self.lang,
            "initiationType": "tender",
            "planning": {
                "budget": {
                    "amount": {
                        "amount": 2000.00,
                        "currency": "EUR"
                    },
                    "isEuropeanUnionFunded": False,
                    "budgetBreakdown": [{
                        "id": fs_id,
                        "amount": {
                            "amount": 2000.00,
                            "currency": "EUR"
                        },
                        "period": {
                            "startDate": period[0],
                            "endDate": period[1]
                        },
                        "sourceParty": {
                            "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                            "name": self.buyer_name,
                        }
                    }]
                }
            },
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "title": "create Pn: tender.title",
                "description": "create Pn: tender.description",
                "status": "active",
                "statusDetails": "evaluation",
                "value": {
                    "amount": 1650.00,
                    "currency": "EUR"
                },
                "procurementMethod": "open",
                "procurementMethodDetails": procurement_method_details_from_mdm,
                "mainProcurementCategory": "works",
                "hasEnquiries": False,
                "eligibilityCriteria": eligibility_criteria_from_mdm,
                "contractPeriod": {
                    "startDate": contract_period[0],
                    "endDate": contract_period[1]
                },
                "procuringEntity": {
                    "id": "MD-IDNO-4",
                    "name": "create Pn: tender.procuringEntity.name"
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
                "legalBasis": "DIRECTIVE_2014_25_EU",
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
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name,
                "identifier": {
                    "scheme": self.buyer_identifier_scheme,
                    "id": self.buyer_identifier_id,
                    "legalName": self.buyer_identifier_legal_name
                },
                "address": {
                    "streetAddress": self.buyer_address_street_address,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.buyer_address_address_details_country_id,
                            "description": "Moldova, Republica",
                            "uri": "https://www.iso.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": self.buyer_address_address_details_region_id,
                            "description": "mun.Chişinău",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": self.buyer_address_address_details_locality_scheme,
                            "id": self.buyer_address_address_details_locality_id,
                            "description": self.buyer_address_address_details_locality_description,
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "contactPoint": {
                    "name": self.buyer_contact_point_name,
                    "email": self.buyer_contact_point_email,
                    "telephone": self.buyer_contact_point_telephone
                },
                "roles": ["buyer"]
            }, {
                "id": f"{self.payer_identifier_scheme}-{self.payer_identifier_id}",
                "name": self.payer_name,
                "identifier": {
                    "scheme": self.payer_identifier_scheme,
                    "id": self.payer_identifier_id,
                    "legalName": self.payer_identifier_legal_name
                },
                "address": {
                    "streetAddress": self.payer_address_street,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.payer_address_postal_code,
                            "description": "Moldova, Republica",
                            "uri": "https://www.iso.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": self.payer_address_address_details_region_id,
                            "description": "Donduşeni",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": self.payer_address_address_details_locality_scheme,
                            "id": self.payer_address_address_details_locality_id,
                            "description": self.payer_address_address_details_locality_description,
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "contactPoint": {
                    "name": self.payer_contact_point_name,
                    "email": self.payer_contact_point_email,
                    "telephone": self.payer_contact_point_telephone
                },
                "roles": ["payer"]
            }, {
                "id": "MD-IDNO-4",
                "name": "create Pn: tender.procuringEntity.name",
                "identifier": {
                    "scheme": "MD-IDNO",
                    "id": "4",
                    "legalName": "create Pn: tender.procuringEntity.identigfier.legalName"
                },
                "address": {
                    "streetAddress": "street address",
                    "addressDetails": {
                        "country": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["country"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['uri']
                        },
                        "region": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["region"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['uri']
                        },
                        "locality": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["locality"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['uri']
                        }
                    }
                },
                "contactPoint": {
                    "name": "name",
                    "email": "email",
                    "telephone": "456-95-96"
                },
                "roles": ["procuringEntity"]
            }],
            "relatedProcesses": [{
                "id": "36b553f0-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["planning"],
                "scheme": "ocid",
                "identifier": pn_id,
                "uri": f"{instance_tender_url}{cp_id}/{pn_id}"
            }, {
                "id": "36b553f1-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["x_expenditureItem"],
                "scheme": "ocid",
                "identifier": ei_id,
                "uri": f"{instance_budget_url}{ei_id}/{ei_id}"
            }, {
                "id": "36b553f2-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["x_fundingSource"],
                "scheme": "ocid",
                "identifier": fs_id,
                "uri": f"{instance_budget_url}{ei_id}/{fs_id}"
            },
                {
                    "id": "ed0f7290-cee4-11eb-8aed-69d06bed4d57",
                    "relationship": ["x_evaluation"],
                    "scheme": "ocid",
                    "identifier": ev_id,
                    "uri": f"{instance_tender_url}{cp_id}/{ev_id}"
                }
            ]

        }
        json_notice_compiled_release_pn = {
            "ocid": pn_id,
            "id": f"{pn_id}-{ev_id[32:45]}",
            "date": f"{get_human_date_in_utc_format(int(ev_id[32:45]))[0]}",
            "tag": ["planningUpdate"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "title": "Planning Notice",
                "description": "Contracting process is planned",
                "status": "complete",
                "statusDetails": "empty",
                "lotGroups": [{
                    "optionToCombine": False
                }],
                "tenderPeriod": {
                    "startDate": period[3]
                },
                "hasEnquiries": False,
                "submissionMethod": ["electronicSubmission"],
                "submissionMethodDetails": submission_method_details,
                "submissionMethodRationale": submission_method_rationale,
                "requiresElectronicCatalogue": False,
                "classification": {
                    "scheme": "CPV",
                    "id": get_value_by_new_cpv_code[0],
                    "description": get_value_by_new_cpv_code[1]
                },
                "value": {
                    "amount": 1650.00,
                    "currency": "EUR"
                }
            },
            "hasPreviousNotice": False,
            "purposeOfNotice": {
                "isACallForCompetition": False
            },
            "relatedProcesses": [{
                "id": "36b553f3-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": cp_id,
                "uri": f"{instance_tender_url}{cp_id}/{cp_id}"
            }]
        }
        json_notice_compiled_release_ev = {
            "ocid": ev_id,
            "id": f"{ev_id}-{period_for_amendment[1]}",
            "date": period_for_amendment[0],
            "tag": ["tender"],
            "initiationType": "tender",
            "language": self.lang,
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "title": "Evaluation",
                "description": "Evaluation stage of contracting process",
                "status": "active",
                "statusDetails": "clarification",
                "items": [{
                    "id": first_item_id,
                    "description": "create Pn: tender.items[0].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_first_item_cpv_code[0],
                        "description": get_value_by_first_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_first_item_cpvs_code[0],
                        "description": get_value_by_first_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_first_item_unit_id[0],
                        "name": get_value_by_first_item_unit_id[1]
                    },
                    "relatedLot": first_lot_id
                }, {
                    "id": second_item_id,
                    "description": "create Pn: tender.items[1].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_second_item_cpv_code[0],
                        "description": get_value_by_second_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_second_item_cpvs_code[0],
                        "description": get_value_by_second_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_second_item_unit_id[0],
                        "name": get_value_by_second_item_unit_id[1]
                    },
                    "relatedLot": second_lot_id
                }],
                "lots": [{
                    "id": first_lot_id,
                    "title": "create Pn: tender.lots[0].title",
                    "description": "create Pn: tender.lots[0].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 1500.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[0].placeOfPerformance.address.streetAddress",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        }
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }, {
                    "id": second_lot_id,
                    "title": "create Pn: tender.lots[1].title",
                    "description": "create Pn: tender.lots[1].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 150.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[1].placeOfPerformance.address.streetAddress",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        }
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }],
                "lotGroups": [{
                    "optionToCombine": False
                }],
                "tenderPeriod": {
                    "startDate": enquiry_and_tender_period[2],
                    "endDate": enquiry_and_tender_period[3]
                },
                "enquiryPeriod": {
                    "startDate": enquiry_and_tender_period[0],
                    "endDate": enquiry_and_tender_period[1]
                },
                "hasEnquiries": False,
                "amendments": [{
                    "id": self.amendment_id,
                    "type": "cancellation",
                    "status": "pending",
                    "relatesTo": "tender",
                    "relatedItem": ev_id,
                    "date": period_for_amendment[0],
                    "rationale": "cancel_tender: amendments[0].rationale"
                }],
                "documents": [{
                    "id": self.document_one_was_uploaded,
                    "documentType": "contractArrangements",
                    "title": "create Pn: tender.documents[0].title",
                    "url": f"{instance_storage_url}{self.document_one_was_uploaded}",
                    "datePublished": operation_date
                }],
                "awardCriteria": "ratedCriteria",
                "awardCriteriaDetails": "automated",
                "submissionMethod": ["electronicSubmission"],
                "submissionMethodDetails": submission_method_details,
                "submissionMethodRationale": submission_method_rationale,
                "requiresElectronicCatalogue": False
            },
            "hasPreviousNotice": True,
            "purposeOfNotice": {
                "isACallForCompetition": True
            },
            "relatedProcesses": [{
                "id": "e84a2253-cee4-11eb-8aed-69d06bed4d57",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": cp_id,
                "uri": f"{instance_tender_url}{cp_id}/{cp_id}"
            }, {
                "id": "ed0f7291-cee4-11eb-8aed-69d06bed4d57",
                "relationship": ["planning"],
                "scheme": "ocid",
                "identifier": pn_id,
                "uri": f"{instance_tender_url}{cp_id}/{pn_id}"
            }]
        }

        kafka = Kafka(instance=self.instance)
        kafka.connect_kafka_producer()
        kafka.publish_message_into_chronograph_in_clarification(
            cp_id=cp_id,
            ev_id=ev_id,
            enquiry_end=enquiry_and_tender_period[1]
        )
        kafka.publish_message_into_chronograph_in_submission(
            cp_id=cp_id,
            ev_id=ev_id,
            tender_end=enquiry_and_tender_period[3]
        )

        key_space_ocds.execute(f"INSERT INTO orchestrator_context (cp_id,context) VALUES ("
                               f"'{ev_id}','{json.dumps(json_orchestrator_context)}');").one()
        key_space_access.execute(f"INSERT INTO tenders (cpid, ocid, token_entity,created_date,json_data, owner) "
                                 f"VALUES ('{cp_id}', '{ev_id}', '{pn_token}', {ev_id[32:45]}, "
                                 f"'{json.dumps(json_access_tender)}','{owner}');").one()
        key_space_clarification.execute(
            f"INSERT INTO periods (cpid, ocid, end_date, owner, start_date) "
            f"VALUES ('{cp_id}', '{ev_id}', {get_timestamp_from_human_date(enquiry_and_tender_period[1])}, '{owner}', "
            f"{ev_id[32:45]});").one()
        key_space_submission.execute(
            f"INSERT INTO periods (cpid, ocid, end_date, start_date) "
            f"VALUES ('{cp_id}', '{ev_id}', {get_timestamp_from_human_date(enquiry_and_tender_period[3])}, "
            f"{get_timestamp_from_human_date(enquiry_and_tender_period[1])});").one()
        key_space_ocds.execute(f"INSERT INTO notice_offset (cp_id,release_date, stage, status) "
                               f"VALUES ('{cp_id}', {ev_id[32:45]}, 'EV', 'active');").one()
        key_space_ocds.execute(
            f"INSERT INTO notice_release (cp_id,oc_id, release_id, json_data, release_date, stage) "
            f"VALUES ('{cp_id}', '{cp_id}', '{cp_id + '-' + ev_id[32:45]}' ,'{json.dumps(json_notice_release_ms)}',"
            f"{ev_id[32:45]},'');").one()
        key_space_ocds.execute(
            f"INSERT INTO notice_release (cp_id,oc_id, release_id, json_data, release_date, stage) "
            f"VALUES ('{cp_id}', '{pn_id}', '{pn_id + '-' + ev_id[32:45]}' ,'{json.dumps(json_notice_release_pn)}',"
            f"{ev_id[32:45]},'PN');").one()
        key_space_ocds.execute(
            f"INSERT INTO notice_release (cp_id,oc_id, release_id, json_data, release_date, stage) "
            f"VALUES ('{cp_id}', '{ev_id}', '{ev_id + '-' + ev_id[32:45]}','{json.dumps(json_notice_release_ev)}',"
            f"{ev_id[32:45]},'EV');").one()
        key_space_ocds.execute(
            f"INSERT INTO notice_release (cp_id,oc_id, release_id, json_data, release_date, stage) "
            f"VALUES ('{cp_id}', '{ev_id}', '{ev_id + '-' + str(period_for_amendment[1])}',"
            f"'{json.dumps(json_notice_release_ev_new)}',"
            f"{period_for_amendment[1]},'EV');").one()

        key_space_ocds.execute(
            f"INSERT INTO notice_compiled_release (cp_id,oc_id, json_data, publish_date, release_date, "
            f"release_id, stage, status) VALUES ('{cp_id}', '{cp_id}', '{json.dumps(json_notice_compiled_release_ms)}',"
            f"{ev_id[32:45]},{ev_id[32:45]}, '{cp_id + '-' + ev_id[32:45]}','', 'active');").one()
        key_space_ocds.execute(
            f"INSERT INTO notice_compiled_release (cp_id,oc_id, json_data, publish_date, release_date, "
            f"release_id, stage, status) VALUES ('{cp_id}', '{pn_id}', '{json.dumps(json_notice_compiled_release_pn)}',"
            f"{ev_id[32:45]},{ev_id[32:45]}, '{pn_id + '-' + ev_id[32:45]}','PN', 'active');").one()
        key_space_revision.execute(f"INSERT INTO amendments (cpid, ocid, id, data) "
                                   f"VALUES ('{cp_id}', '{ev_id}', {self.amendment_id}, "
                                   f"'{json.dumps(json_amendments)}');").one()

        key_space_ocds.execute(f"INSERT INTO notice_offset (cp_id,release_date, stage, status) "
                               f"VALUES ('{cp_id}', {period_for_amendment[1]}, 'EV', 'active');").one()

        key_space_ocds.execute(
            f"INSERT INTO notice_compiled_release (cp_id,oc_id, json_data, publish_date, release_date, "
            f"release_id, stage, status) VALUES ('{cp_id}', '{ev_id}', '{json.dumps(json_notice_compiled_release_ev)}',"
            f"{period[2]},{period_for_amendment[1]}, '{ev_id + '-' + str(period_for_amendment[1])}','EV', "
            f"'active');").one()
        record = f"{instance_tender_url}{cp_id}"
        ms_release = f"{instance_tender_url}{cp_id}/{cp_id}"
        pn_release = f"{instance_tender_url}{cp_id}/{pn_id}"
        ev_release = f"{instance_tender_url}{cp_id}/{ev_id}"
        return cp_id, pn_id, pn_token, ev_id, record, ms_release, pn_release, ev_release, self.amendment_id, \
               self.amendment_token

    @allure.step('Insert CnOnPn: based on FS: own - full, based on EI: with items - full')
    def insert_cnonpn_full(self, first_lot_id, second_lot_id, first_item_id, second_item_id,
                           second_tender, second_enquiry):
        auth_provider = PlainTextAuthProvider(username=self.cassandra_username, password=self.cassandra_password)
        cluster = Cluster([self.cassandra_cluster], auth_provider=auth_provider)
        key_space_ocds = cluster.connect('ocds')
        key_space_access = cluster.connect('access')
        key_space_clarification = cluster.connect('clarification')
        key_space_submission = cluster.connect('submission')
        key_space_auctions = cluster.connect('auctions')
        owner = "445f6851-c908-407d-9b45-14b92f3e964b"
        ei_id = prepared_cp_id()
        fs_id = prepared_fs_oc_id(ei_id)
        cp_id = prepared_cp_id()
        pn_id = prepared_pn_oc_id(cp_id)
        pn_token = uuid4()
        ev_id = prepared_cn_oc_id(cp_id)
        period = get_period()
        auction_date = get_auction_date()
        contract_period = get_contract_period()
        enquiry_and_tender_period = create_enquiry_and_tender_period(
            second_enquiry=second_enquiry,
            second_tender=second_tender
        )

        operation_date = time_at_now()
        calculate_new_cpv_code = get_new_classification_id(
            self.first_item_cpv,
            self.second_item_cpv
        )
        get_value_by_new_cpv_code = get_value_from_classification_cpv_dictionary_xls(
            calculate_new_cpv_code,
            self.lang
        )
        get_value_by_first_item_cpv_code = get_value_from_classification_cpv_dictionary_xls(
            self.first_item_cpv,
            self.lang
        )
        get_value_by_second_item_cpv_code = get_value_from_classification_cpv_dictionary_xls(
            self.second_item_cpv,
            self.lang
        )
        get_value_by_first_item_cpvs_code = get_value_from_cpvs_dictionary_csv(
            self.first_item_additional_classifications,
            self.lang
        )
        get_value_by_second_item_cpvs_code = get_value_from_cpvs_dictionary_csv(
            self.second_item_additional_classifications,
            self.lang
        )
        get_value_by_first_item_unit_id = get_value_from_classification_unit_dictionary_csv(
            self.first_item_unit_id,
            self.lang
        )
        get_value_by_second_item_unit_id = get_value_from_classification_unit_dictionary_csv(
            self.second_item_unit_id,
            self.lang
        )

        mdm = MdmService(
            instance=self.instance
        )
        data_pn = mdm.process_tender_data(self.pmd).json()
        submission_method_details = data_pn["data"]["tender"]["submissionMethodDetails"]
        submission_method_rationale = data_pn["data"]["tender"]["submissionMethodRationale"]

        procurement_method_details_from_mdm = data_pn["data"]["tender"]["procurementMethodDetails"]
        eligibility_criteria_from_mdm = data_pn["data"]["tender"]["eligibilityCriteria"]
        instance_tender_url = None
        instance_budget_url = None
        instance_storage_url = None
        if self.instance == "dev":
            instance_tender_url = "http://dev.public.eprocurement.systems/tenders/"
            instance_budget_url = "http://dev.public.eprocurement.systems/budgets/"
            instance_storage_url = "https://dev.bpe.eprocurement.systems/api/v1/storage/get/"
        if self.instance == "sandbox":
            instance_tender_url = "http://public.eprocurement.systems/tenders/"
            instance_budget_url = "http://public.eprocurement.systems/budgets/"
            instance_storage_url = "http://storage.eprocurement.systems/get/"
        json_orchestrator_context = {
            "operationId": f"{uuid4()}",
            "requestId": f"{uuid1()}",
            "cpid": cp_id,
            "ocid": ev_id,
            "ocidCn": ev_id,
            "stage": "EV",
            "prevStage": "PN",
            "processType": "updateCN",
            "operationType": "createCNonPN",
            "phase": "clarification",
            "owner": owner,
            "country": self.country,
            "language": self.lang,
            "pmd": self.pmd,
            "token": f"{pn_token}",
            "startDate": period[0],
            "timeStamp": period[2],
            "isAuction": True
        }

        json_access_tender = {
            "ocid": cp_id,
            "planning": {
                "rationale": "create Pn: planning.rationale",
                "budget": {
                    "description": "create Pn: planning.budget.description",
                    "amount": {
                        "amount": 2000.00,
                        "currency": "EUR"
                    },
                    "isEuropeanUnionFunded": True,
                    "budgetBreakdown": [{
                        "id": fs_id,
                        "description": "create Fs: planning.budget.description",
                        "amount": {
                            "amount": 2000.00,
                            "currency": "EUR"
                        },
                        "period": {
                            "startDate": period[0],
                            "endDate": period[1]
                        },
                        "sourceParty": {
                            "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                            "name": self.funder_name,
                        },
                        "europeanUnionFunding": {
                            "projectIdentifier": "create Fs: planning.budget.europeanUnionFunding.projectIdentifier",
                            "projectName": "create Fs: planning.budget.europeanUnionFunding.projectName",
                            "uri": "create Fs: planning.budget.europeanUnionFunding.uri"
                        }
                    }]
                }
            },
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "status": "active",
                "statusDetails": "clarification",
                "title": "create Pn: tender.title",
                "description": "create Pn: tender.description",
                "classification": {
                    "scheme": "CPV",
                    "id": get_value_by_new_cpv_code[0],
                    "description": get_value_by_new_cpv_code[1]
                },
                "tenderPeriod": {
                    "startDate": enquiry_and_tender_period[2],
                    "endDate": enquiry_and_tender_period[3]
                },
                "enquiryPeriod": {
                    "startDate": enquiry_and_tender_period[0],
                    "endDate": enquiry_and_tender_period[1]
                },
                "acceleratedProcedure": {
                    "isAcceleratedProcedure": False
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
                "procedureOutsourcing": {
                    "procedureOutsourced": False
                },
                "framework": {
                    "isAFramework": False
                },
                "dynamicPurchasingSystem": {
                    "hasDynamicPurchasingSystem": False
                },
                "legalBasis": "DIRECTIVE_2014_25_EU",
                "procurementMethod": "open",
                "procurementMethodDetails": procurement_method_details_from_mdm,
                "procurementMethodRationale": "create CNonPN: tender.procurementMethodRationale",
                "procurementMethodAdditionalInfo": "create CNonPN: tender.procurementMethodAdditionalInfo",
                "mainProcurementCategory": "works",
                "eligibilityCriteria": eligibility_criteria_from_mdm,
                "contractPeriod": {
                    "startDate": contract_period[0],
                    "endDate": contract_period[1]
                },
                "procurementMethodModalities": ["electronicAuction"],
                "electronicAuctions": {
                    "details": [{
                        "id": "503d6861-62d9-47f3-8939-4e4729df0cde",
                        "relatedLot": first_lot_id,
                        "electronicAuctionModalities": [{
                            "eligibleMinimumDifference": {
                                "amount": 100.00,
                                "currency": "EUR"
                            }
                        }]
                    }, {
                        "id": "f1a36bc8-ee22-4660-8a76-5b1671d34b0d",
                        "relatedLot": second_lot_id,
                        "electronicAuctionModalities": [{
                            "eligibleMinimumDifference": {
                                "amount": 10.00,
                                "currency": "EUR"
                            }
                        }]
                    }]
                },
                "procuringEntity": {
                    "id": "MD-IDNO-4",
                    "name": "create Pn: tender.procuringEntity.name",
                    "identifier": {
                        "scheme": "MD-IDNO",
                        "id": "4",
                        "legalName": "create Pn: tender.procuringEntity.identifier.legalName",
                        "uri": "create Pn: tender.procuringEntity.identifier.uri"
                    },
                    "additionalIdentifiers": [{
                        "scheme": "create Pn: tender.procuringEntity.additionalIdentifiers[0].scheme",
                        "id": "create Pn: tender.procuringEntity.additionalIdentifiers[0].id",
                        "legalName": "create Pn: tender.procuringEntity.additionalIdentifiers[0].legalName",
                        "uri": "create Pn: tender.procuringEntity.additionalIdentifiers[0].uri"
                    }],
                    "address": {
                        "streetAddress": "create Pn: tender.procuringEntity.address.streetAddress",
                        "postalCode": "create Pn: tender.procuringEntity.address.postalCode",
                        "addressDetails": {
                            "country": {
                                "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "country"]['scheme'],
                                "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "country"]['id'],
                                "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                    "addressDetails"]["country"]['description'],
                                "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "country"]['uri']
                            },
                            "region": {
                                "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "region"]['scheme'],
                                "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "region"]['id'],
                                "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                    "addressDetails"]["region"]['description'],
                                "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "region"]['uri']
                            },
                            "locality": {
                                "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "locality"]['scheme'],
                                "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "locality"]['id'],
                                "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                    "addressDetails"]["locality"]['description'],
                                "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "locality"]['uri']

                            }
                        }
                    },
                    "contactPoint": {
                        "name": "create Pn: tender.procuringEntity.contactPoint.name",
                        "email": "create Pn: tender.procuringEntity.contactPoint.email",
                        "telephone": "create Pn: tender.procuringEntity.contactPoint.telephone",
                        "faxNumber": "create Pn: tender.procuringEntity.contactPoint.faxNumber",
                        "url": "create Pn: tender.procuringEntity.contactPoint.url"
                    },
                    "persones": [{
                        "id": "create CNonPN: procuringEntity.persones[0].identifier.id",
                        "title": "create CNonPN: procuringEntity.persones[0].title",
                        "name": "create CNonPN: procuringEntity.persones[0].name",
                        "identifier": {
                            "scheme": "MD-IDNO",
                            "id": "create CNonPN: procuringEntity.persones[0].identifier.id",
                            "uri": "create CNonPN: procuringEntity.persones[0].identifier.uri"
                        },
                        "businessFunctions": [{
                            "id": "create CNonPN: procuringEntity.persones[0].businessFunctions[0].id",
                            "type": "contactPoint",
                            "jobTitle": "create CNonPN: procuringEntity.persones[0].businessFunctions[0].jobTitle",
                            "period": {
                                "startDate": period[0]
                            },
                            "documents": [{
                                "id": self.document_three_was_uploaded,
                                "documentType": "regulatoryDocument",
                                "title": "create CNonPN: procuringEntity.persones[0].businessFunctions[0].title",
                                "description": "create CNonPN: procuringEntity.persones[0].businessFunctions[0]."
                                               "description"
                            }]
                        }]
                    }]
                },
                "value": {
                    "amount": 1650.00,
                    "currency": "EUR"
                },
                "lotGroups": [{
                    "optionToCombine": False
                }],
                "criteria": [{
                    "id": "db6d8e23-5dce-4688-9b82-2e323994e709",
                    "title": "create CNonPN: tender.criteria[0].title =Bankruptcy",
                    "classification": {
                        "id": "CRITERION.EXCLUSION.CONVICTIONS.PARTICIPATION_IN_CRIMINAL_ORGANISATION",
                        "scheme": "ESPD"
                    },
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[0].description =Is the economic operator bankrupt? "
                                   "This information needs not be given if exclusion of economic operators in this "
                                   "case has been made mandatory under the applicable national law without any "
                                   "possibility of derogation where the economic operator is nevertheless able to "
                                   "perform the contract.",
                    "requirementGroups": [{
                        "id": "83af7655-a283-42ad-8151-ac2ff549e23e",
                        "description": "create CNonPN: tender.criteria[0].requirementGroups[0].description =approve "
                                       "that Bankruptcy requirement group",
                        "requirements": [{
                            "id": "86c15b70-0622-41e7-b333-457d14c770b6",
                            "title": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements.title",
                            "dataType": "boolean",
                            "description": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements."
                                           "description",
                            "status": "active",
                            "datePublished": operation_date,
                            "expectedValue": False,
                            "eligibleEvidences": [{
                                "id": "1",
                                "title": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements[0]."
                                         "eligibleEvidences[0].title",
                                "description": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements"
                                               "[0].eligibleEvidences[0].description",
                                "type": "document",
                                "relatedDocument": {
                                    "id": self.document_three_was_uploaded
                                }
                            }, {
                                "id": "2",
                                "title": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements[0]."
                                         "eligibleEvidences[1].title",
                                "description": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements"
                                               "[0].eligibleEvidences[1].description",
                                "type": "document",
                                "relatedDocument": {
                                    "id": self.document_three_was_uploaded
                                }
                            }]
                        }]
                    }],
                    "relatesTo": "tender"
                }, {
                    "id": "5ad0aa1e-ec8c-48d6-be0c-99fa777eaca9",
                    "title": "create CNonPN: tender.criteria[1].title",
                    "classification": {
                        "id": "CRITERION.SELECTION.ECONOMIC_FINANCIAL_STANDING.TURNOVER.GENERAL_YEARLY",
                        "scheme": "ESPD"
                    },
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[1].description",
                    "requirementGroups": [{
                        "id": "c3878528-b856-4a2d-92f9-6138dad28b51",
                        "description": "create CNonPN: tender.criteria[1].requirementGroups[0].description",
                        "requirements": [{
                            "id": "268877db-bfb9-45dc-9b0b-4a932f75c6ed",
                            "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[0].title",
                            "dataType": "boolean",
                            "description": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements."
                                           "description",
                            "status": "active",
                            "datePublished": operation_date,
                            "expectedValue": True
                        }, {
                            "id": "2aadefb6-869e-4695-9b2f-663c9a4acb37",
                            "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[1]."
                                     "title =The number of years for proposed product warranty",
                            "dataType": "number",
                            "description": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[1]."
                                           "description",
                            "status": "active",
                            "datePublished": operation_date,
                            "period": {
                                "startDate": period[0],
                                "endDate": period[1]
                            },
                            "minValue": 1.000,
                            "maxValue": 3.000,
                            "eligibleEvidences": [{
                                "id": "3",
                                "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[1]."
                                         "eligibleEvidences[0].title",
                                "description": "create CNonPN: tender.criteria[1].requirementGroups[0]."
                                               "requirements[1].eligibleEvidences[0].description",
                                "type": "document",
                                "relatedDocument": {
                                    "id": self.document_three_was_uploaded
                                }
                            }]
                        }]
                    }],
                    "relatesTo": "lot",
                    "relatedItem": first_lot_id
                }, {
                    "id": "1a600e32-354f-436c-bede-e3238ca1998d",
                    "title": "create CNonPN: tender.criteria[2].title",
                    "classification": {
                        "id": "CRITERION.EXCLUSION.NATIONAL.OTHER",
                        "scheme": "ESPD"
                    },
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[2].description",
                    "requirementGroups": [{
                        "id": "a2fa62cc-4ec3-4944-a091-bd158cded7ab",
                        "description": "create CNonPN: tender.criteria[2].requirementGroups[0].description",
                        "requirements": [{
                            "id": "5ac98f2b-9e55-4167-aa82-2d4baa1d01cb",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[0].requirements[0]."
                                     "title =Product has to be manufactured in the EU",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "expectedValue": True
                        }, {
                            "id": "5bfd430b-a663-4657-972f-788b8c7bffc5",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[0]..requirements[1]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }, {
                        "id": "eac18bd3-6c02-4245-a6e2-f839f80361ee",
                        "description": "create CNonPN: tender.criteria[2].requirementGroups[1].description",
                        "requirements": [{
                            "id": "6853dee4-1359-4522-87a6-ee50c00cb390",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[1].requirements[0]."
                                     "title =Product has to be manufactured in the EU",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "expectedValue": True
                        }, {
                            "id": "a470ea41-0825-44e2-89be-495d63a54f06",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[1]..requirements[1]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }],
                    "relatesTo": "tenderer"
                }, {
                    "id": "13e1682a-23bb-491d-ad6d-a9cbdba6ac80",
                    "title": "create CNonPN: tender.criteria[3].title",
                    "classification": {
                        "id": "CRITERION.OTHER.EO_DATA.RELIES_ON_OTHER_CAPACITIES",
                        "scheme": "ESPD"
                    },
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[3].description =A minimum product warranty "
                                   "of 1 year is required for all bids 2",
                    "requirementGroups": [{
                        "id": "8378bc93-9c06-47ae-9982-0b091e326728",
                        "description": "create CNonPN: tender.criteria[3].requirementGroups[0].description",
                        "requirements": [{
                            "id": "e64eb9e1-47dd-488f-acbe-ff13b7e258d8",
                            "title": "create CNonPN: tender.criteria[3].requirementGroups[0].requirements[0]."
                                     "title = The number of years for proposed product warranty",
                            "dataType": "number",
                            "status": "active",
                            "datePublished": operation_date,
                            "period": {
                                "startDate": period[0],
                                "endDate": period[1]
                            },
                            "minValue": 1.000,
                            "maxValue": 3.000
                        }]
                    }],
                    "relatesTo": "item",
                    "relatedItem": first_item_id
                }, {
                    "id": "50d6061e-5913-4bc4-a18b-3ad3261a2c88",
                    "title": "create CNonPN: tender.criteria[4].title",
                    "classification": {
                        "id": "CRITERION.EXCLUSION.NATIONAL.OTHER",
                        "scheme": "ESPD"
                    },
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[4].description",
                    "requirementGroups": [{
                        "id": "da026d11-3769-43ce-ba83-f93832b18409",
                        "description": "create CNonPN: tender.criteria[4].requirementGroups[0].description",
                        "requirements": [{
                            "id": "794ece62-28a9-4843-8241-6955d7020cde",
                            "title": "create CNonPN: tender.criteria[4].requirementGroups[0].requirements[0]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }],
                    "relatesTo": "tender"
                }, {
                    "id": "55a02e2f-dc9c-43ad-ad47-af0932cf0b89",
                    "title": "create CNonPN: tender.criteria[4].title",
                    "classification": {
                        "id": "CRITERION.OTHER.EO_DATA.RELIES_ON_OTHER_CAPACITIES",
                        "scheme": "ESPD"
                    },
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[4].description",
                    "requirementGroups": [{
                        "id": "735a5c8b-6adf-4256-ac73-104470b7b189",
                        "description": "create CNonPN: tender.criteria[4].requirementGroups[0].description",
                        "requirements": [{
                            "id": "ba9194d1-37a6-45ac-896c-faacd250eb72",
                            "title": "create CNonPN: tender.criteria[4].requirementGroups[0].requirements[0]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }],
                    "relatesTo": "tender"
                }],
                "conversions": [{
                    "id": "9eab3068-bcce-4f8a-a829-0181830f0636",
                    "relatesTo": "requirement",
                    "relatedItem": "268877db-bfb9-45dc-9b0b-4a932f75c6ed",
                    "rationale": "create CNonPN: tender.conversions[1].rationale",
                    "description": "create CNonPN: tender.conversions[1].description",
                    "coefficients": [{
                        "id": "e896f9d4-3f61-4370-97d0-25fd6e26b27a",
                        "value": False,
                        "coefficient": 1
                    }]
                }, {
                    "id": "4937c4b4-a50d-48f8-8363-7b02c48a12d9",
                    "relatesTo": "requirement",
                    "relatedItem": "2aadefb6-869e-4695-9b2f-663c9a4acb37",
                    "rationale": "create CNonPN: tender.conversions[3].rationale",
                    "description": "create CNonPN: tender.conversions[3].description",
                    "coefficients": [{
                        "id": "f09bf118-92fd-4702-a5ac-2393e2234dbb",
                        "value": 1.000,
                        "coefficient": 1
                    }, {
                        "id": "9b69b215-e75a-4d5b-b51a-2046a7207562",
                        "value": 2.000,
                        "coefficient": 1
                    }, {
                        "id": "9c985738-1903-49df-829d-a574a5021d35",
                        "value": 3.000,
                        "coefficient": 0.93
                    }]
                }, {
                    "id": "678dcf2c-2e9f-4a72-8cb6-8ecf067fcf75",
                    "relatesTo": "requirement",
                    "relatedItem": "e64eb9e1-47dd-488f-acbe-ff13b7e258d8",
                    "rationale": "create CNonPN: tender.conversions[6].rationale",
                    "description": "create CNonPN: tender.conversions[6].description",
                    "coefficients": [{
                        "id": "f4ab1b51-21ee-46d2-8e78-2d65c30fa3e2",
                        "value": 1.000,
                        "coefficient": 1
                    }, {
                        "id": "c5eb8b92-a1b5-41a0-a7ed-267b2a79bc91",
                        "value": 2.000,
                        "coefficient": 1
                    }, {
                        "id": "ab5e3241-0afd-40b1-86ac-887366caef2b",
                        "value": 3.000,
                        "coefficient": 0.93
                    }]
                }, {
                    "id": "89ac8671-0640-41c9-ba4b-fdfcc7aa9131",
                    "relatesTo": "requirement",
                    "relatedItem": "ba9194d1-37a6-45ac-896c-faacd250eb72",
                    "rationale": "create CNonPN: tender.conversions[6].rationale",
                    "description": "create CNonPN: tender.conversions[6].description",
                    "coefficients": [{
                        "id": "0728cc52-3c85-4283-a1f6-b3ae94ca6eae",
                        "relatedOption": "option_1",
                        "value": "option_1",
                        "coefficient": 1
                    }, {
                        "id": "66e52e5a-49fd-420f-936a-0ef9aeafae21",
                        "relatedOption": "option_2",
                        "value": "option_2",
                        "coefficient": 1
                    }, {
                        "id": "6151abc7-56e1-424b-a0ee-f9bba4205abf",
                        "relatedOption": "option_3",
                        "value": "option_3",
                        "coefficient": 0.93
                    }]
                }],
                "lots": [{
                    "id": first_lot_id,
                    "internalId": "create Pn: tender.lots[0].internalId",
                    "title": "create Pn: tender.lots[0].title",
                    "description": "create Pn: tender.lots[0].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 1500.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[0].placeOfPerformance.address.streetAddress",
                            "postalCode": "create Pn: tender.lots[0].placeOfPerformance.address.postalCode",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        },
                        "description": "create Pn: tender.lots[0].placeOfPerformance.description"
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }, {
                    "id": second_lot_id,
                    "internalId": "create Pn: tender.lots[1].internalId",
                    "title": "create Pn: tender.lots[1].title",
                    "description": "create Pn: tender.lots[1].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 150.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[1].placeOfPerformance.address.streetAddress",
                            "postalCode": "create Pn: tender.lots[1].placeOfPerformance.address.postalCode",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        },
                        "description": "create Pn: tender.lots[1].placeOfPerformance.description"
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }],
                "items": [{
                    "id": first_item_id,
                    "internalId": "create Pn: tender.items[0].internalId",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_first_item_cpv_code[0],
                        "description": get_value_by_first_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_first_item_cpvs_code[0],
                        "description": get_value_by_first_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_first_item_unit_id[0],
                        "name": get_value_by_first_item_unit_id[1]
                    },
                    "description": "create Pn: tender.items[0].description",
                    "relatedLot": first_lot_id
                }, {
                    "id": second_item_id,
                    "internalId": "create Pn: tender.items[1].internalId",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_second_item_cpv_code[0],
                        "description": get_value_by_second_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_second_item_cpvs_code[0],
                        "description": get_value_by_second_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_second_item_unit_id[0],
                        "name": get_value_by_second_item_unit_id[1]
                    },
                    "description": "create Pn: tender.items[1].description",
                    "relatedLot": second_lot_id
                }],
                "awardCriteria": "ratedCriteria",
                "awardCriteriaDetails": "automated",
                "requiresElectronicCatalogue": False,
                "submissionMethod": ["electronicSubmission"],
                "submissionMethodRationale": submission_method_rationale,
                "submissionMethodDetails": submission_method_details,
                "documents": [
                    {
                        "id": self.document_one_was_uploaded,
                        "documentType": "billOfQuantity",
                        "title": "create Pn: tender.documents[0].title",
                        "description": "create Pn: tender.documents[0].description",
                        "relatedLots": [
                            first_lot_id]
                    },
                    {
                        "id": self.document_two_was_uploaded,
                        "documentType": "billOfQuantity",
                        "title": "create Pn: tender.documents[1].title",
                        "description": "create Pn: tender.documents[1].description",
                        "relatedLots": [
                            second_lot_id]
                    },
                    {
                        "id": self.document_three_was_uploaded,
                        "documentType": "evaluationCriteria",
                        "title": "create CNonPN: tender.documents[2].title",
                        "description": "create CNonPN: tender.documents[2].description",
                        "relatedLots": [first_lot_id]
                    }
                ]
            }
        }

        json_auction_auctions = {
            "version": "1.0.0",
            "tender": {
                "id": ev_id,
                "country": self.country,
                "status": 1,
                "startDate": auction_date
            },
            "slots": ["917ba5a5-d39e-4c24-a465-4b7f5726d5f3"],
            "auctions": [{
                "id": "503d6861-62d9-47f3-8939-4e4729df0cde",
                "lotId": first_lot_id,
                "auctionPeriod": {
                    "startDate": auction_date
                },
                "modalities": [{
                    "url": f"https://eauction.eprocurement.systems/auctions/{ev_id}/{first_lot_id}",
                    "eligibleMinimumDifference": {
                        "amount": 100.00,
                        "currency": "EUR"
                    }
                }]
            }, {
                "id": "516f0bd4-7706-4dc8-bd37-894d93cac809",
                "lotId": second_lot_id,
                "auctionPeriod": {
                    "startDate": auction_date
                },
                "modalities": [{
                    "url": f"https://eauction.eprocurement.systems/auctions/{ev_id}/{second_lot_id}",
                    "eligibleMinimumDifference": {
                        "amount": 10.00,
                        "currency": "EUR"
                    }
                }]
            }]
        }
        json_notice_release_ms = {
            "ocid": cp_id,
            "id": f"{cp_id}-{ev_id[32:45]}",
            "date": f"{get_human_date_in_utc_format(int(ev_id[32:45]))[0]}",
            "tag": ["compiled"],
            "language": self.lang,
            "initiationType": "tender",
            "planning": {
                "budget": {
                    "description": "create Pn: planning.budget.description",
                    "amount": {
                        "amount": 2000.00,
                        "currency": "EUR"
                    },
                    "isEuropeanUnionFunded": True,
                    "budgetBreakdown": [{
                        "id": fs_id,
                        "description": "create Fs: planning.budget.description",
                        "amount": {
                            "amount": 2000.00,
                            "currency": "EUR"
                        },
                        "period": {
                            "startDate": period[0],
                            "endDate": period[1]
                        },
                        "sourceParty": {
                            "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                            "name": self.funder_name,
                        },
                        "europeanUnionFunding": {
                            "projectIdentifier": "create Fs: planning.budget.europeanUnionFunding.projectIdentifier",
                            "projectName": "create Fs: planning.budget.europeanUnionFunding.projectName",
                            "uri": "create Fs: planning.budget.europeanUnionFunding.uri"
                        }
                    }]
                },
                "rationale": "create Pn: planning.rationale"
            },
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "title": "create Pn: tender.title",
                "description": "create Pn: tender.description",
                "status": "active",
                "statusDetails": "evaluation",
                "value": {
                    "amount": 1650.00,
                    "currency": "EUR"
                },
                "procurementMethod": "open",
                "procurementMethodDetails": procurement_method_details_from_mdm,
                "procurementMethodRationale": "create CNonPN: tender.procurementMethodRationale",
                "mainProcurementCategory": "works",
                "hasEnquiries": False,
                "eligibilityCriteria": eligibility_criteria_from_mdm,
                "contractPeriod": {
                    "startDate": contract_period[0],
                    "endDate": contract_period[1]
                },
                "procuringEntity": {
                    "id": "MD-IDNO-4",
                    "name": "create Pn: tender.procuringEntity.name"
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
                "legalBasis": "DIRECTIVE_2014_25_EU",
                "procedureOutsourcing": {
                    "procedureOutsourced": False
                },
                "procurementMethodAdditionalInfo": "create CNonPN: tender.procurementMethodAdditionalInfo",
                "dynamicPurchasingSystem": {
                    "hasDynamicPurchasingSystem": False
                },
                "framework": {
                    "isAFramework": False
                }
            },
            "parties": [{
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name,
                "identifier": {
                    "scheme": self.buyer_identifier_scheme,
                    "id": self.buyer_identifier_id,
                    "legalName": self.buyer_identifier_legal_name,
                    "uri": self.buyer_identifier_uri
                },
                "address": {
                    "streetAddress": self.buyer_address_street_address,
                    "postalCode": self.buyer_address_postal_code,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.buyer_address_address_details_country_id,
                            "description": "Moldova, Republica",
                            "uri": "https://www.iso.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": self.buyer_address_address_details_region_id,
                            "description": "Cahul",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": self.buyer_address_address_details_locality_scheme,
                            "id": self.buyer_address_address_details_locality_id,
                            "description": self.buyer_address_address_details_locality_description,
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "additionalIdentifiers": [
                    {
                        "scheme": "create Ei: buyer.additionalIdentifiers[0].scheme",
                        "id": "create Ei: buyer.additionalIdentifiers[0].id",
                        "legalName": "create Ei: buyer.additionalIdentifiers[0].legalName",
                        "uri": "create Ei: buyer.additionalIdentifiers[0].uri"
                    }],
                "contactPoint": {
                    "name": self.buyer_contact_point_name,
                    "email": self.buyer_contact_point_email,
                    "telephone": self.buyer_contact_point_telephone,
                    "faxNumber": self.buyer_contact_point_fax_number,
                    "url": self.buyer_contact_point_url
                },
                "details": {
                    "typeOfBuyer": "NATIONAL_AGENCY",
                    "mainGeneralActivity": "HEALTH",
                    "mainSectoralActivity": "WATER"
                },
                "roles": [
                    "buyer"]
            }, {
                "id": f"{self.payer_identifier_scheme}-{self.payer_identifier_id}",
                "name": self.payer_name,
                "identifier": {
                    "scheme": self.payer_identifier_scheme,
                    "id": self.payer_identifier_id,
                    "legalName": self.payer_identifier_legal_name,
                    "uri": self.payer_identifier_uri
                },
                "address": {
                    "streetAddress": self.payer_address_street,
                    "postalCode": self.payer_address_postal_code,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.payer_address_address_details_country_id,
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": self.payer_address_address_details_region_id,
                            "description": "Cahul",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": self.payer_address_address_details_locality_scheme,
                            "id": self.payer_address_address_details_locality_id,
                            "description": self.payer_address_address_details_locality_description,
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "additionalIdentifiers": [
                    {
                        "scheme": "create Fs: tender.procuringEntity.additionalIdentifiers[0].scheme",
                        "id": "create Fs: tender.procuringEntity.additionalIdentifiers[0].id",
                        "legalName": "create Fs: tender.procuringEntity.additionalIdentifiers[0].legalName",
                        "uri": "create Fs: tender.procuringEntity.additionalIdentifiers[0].uri"
                    }],
                "contactPoint": {
                    "name": self.payer_contact_point_name,
                    "email": self.payer_contact_point_email,
                    "telephone": self.payer_contact_point_telephone,
                    "faxNumber": self.payer_contact_point_fax_number,
                    "url": self.payer_contact_point_url
                },
                "roles": ["payer"]
            }, {
                "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                "name": self.funder_name,
                "identifier": {
                    "scheme": self.funder_identifier_scheme,
                    "id": self.funder_identifier_id,
                    "legalName": self.funder_identifier_legal_name,
                    "uri": self.funder_identifier_uri
                },
                "address": {
                    "streetAddress": self.funder_address_street,
                    "postalCode": self.funder_address_postal_code,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.funder_address_address_details_country_id,
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": self.funder_address_address_details_region_id,
                            "description": "Cahul",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": self.funder_address_address_details_locality_scheme,
                            "id": self.funder_address_address_details_locality_id,
                            "description": self.funder_address_address_details_locality_description,
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "additionalIdentifiers": [
                    {
                        "scheme": "create Fs: buyer.additionalIdentifiers[0].scheme",
                        "id": "create Fs: buyer.additionalIdentifiers[0].id",
                        "legalName": "create Fs: buyer.additionalIdentifiers[0].legalName",
                        "uri": "create Fs: buyer.additionalIdentifiers[0].uri"
                    }],
                "contactPoint": {
                    "name": self.funder_contact_point_name,
                    "email": self.funder_contact_point_email,
                    "telephone": self.funder_contact_point_telephone,
                    "faxNumber": self.funder_contact_point_fax,
                    "url": self.funder_contact_point_url
                },
                "roles": [
                    "funder"]
            }, {
                "id": "MD-IDNO-4",
                "name": "create Pn: tender.procuringEntity.name",
                "identifier": {
                    "scheme": "MD-IDNO",
                    "id": "4",
                    "legalName": "create Pn: tender.procuringEntity.identigfier.legalName",
                    "uri": "create Pn: tender.procuringEntity.identifier.uri"
                },
                "address": {
                    "streetAddress": "create Pn: tender.procuringEntity.address.streetAddress",
                    "postalCode": "create Pn: tender.procuringEntity.address.postalCode",
                    "addressDetails": {
                        "country": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["country"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['uri']
                        },
                        "region": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["region"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['uri']
                        },
                        "locality": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["locality"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['uri']

                        }
                    }
                },
                "additionalIdentifiers": [{
                    "scheme": "create Pn: tender.procuringEntity.additionalIdentifiers[0].scheme",
                    "id": "create Pn: tender.procuringEntity.additionalIdentifiers[0].id",
                    "legalName": "create Pn: tender.procuringEntity.additionalIdentifiers[0].legalName",
                    "uri": "create Pn: tender.procuringEntity.additionalIdentifiers[0].uri"
                }],
                "contactPoint": {
                    "name": "create Pn: tender.procuringEntity.contactPoint.name",
                    "email": "create Pn: tender.procuringEntity.contactPoint.email",
                    "telephone": "create Pn: tender.procuringEntity.contactPoint.telephone",
                    "faxNumber": "create Pn: tender.procuringEntity.contactPoint.faxNumber",
                    "url": "create Pn: tender.procuringEntity.contactPoint.url"
                },
                "persones": [{
                    "id": "MD-IDNO-create CNonPN: procuringEntity.persones[0].identifier.id",
                    "title": "create CNonPN: procuringEntity.persones[0].title",
                    "name": "create CNonPN: procuringEntity.persones[0].name",
                    "identifier": {
                        "scheme": "MD-IDNO",
                        "id": "create CNonPN: procuringEntity.persones[0].identifier.id",
                        "uri": "create CNonPN: procuringEntity.persones[0].identifier.uri"
                    },
                    "businessFunctions": [{
                        "id": "create CNonPN: procuringEntity.persones[0].businessFunctions[0].id",
                        "type": "procurementOfficer",
                        "jobTitle": "create CNonPN: procuringEntity.persones[0].businessFunctions[0].jobTitle",
                        "period": {
                            "startDate": period[0]
                        },
                        "documents": [{
                            "id": self.document_three_was_uploaded,
                            "documentType": "regulatoryDocument",
                            "title": "create CNonPN: procuringEntity.persones[0].businessFunctions[0].title",
                            "description": "create CNonPN: procuringEntity.persones[0].businessFunctions[0]."
                                           "description",
                            "url": f"{instance_storage_url}"
                                   f"{self.document_three_was_uploaded}",
                            "datePublished": operation_date
                        }]
                    }]
                }],
                "roles": ["procuringEntity"]
            }],
            "relatedProcesses": [{
                "id": "36b553f0-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["planning"],
                "scheme": "ocid",
                "identifier": pn_id,
                "uri": f"{instance_tender_url}{cp_id}/{pn_id}"
            }, {
                "id": "36b553f1-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["x_expenditureItem"],
                "scheme": "ocid",
                "identifier": ei_id,
                "uri": f"{instance_budget_url}{ei_id}/{ei_id}"
            }, {
                "id": "36b553f2-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["x_fundingSource"],
                "scheme": "ocid",
                "identifier": fs_id,
                "uri": f"{instance_budget_url}{ei_id}/{fs_id}"
            },
                {
                    "id": "164cf530-ceca-11eb-8aed-69d06bed4d57",
                    "relationship": ["x_evaluation"],
                    "scheme": "ocid",
                    "identifier": ev_id,
                    "uri": f"{instance_tender_url}{cp_id}/{ev_id}"
                }
            ]
        }
        json_notice_release_pn = {
            "ocid": pn_id,
            "id": f"{pn_id}-{ev_id[32:45]}",
            "date": f"{get_human_date_in_utc_format(int(ev_id[32:45]))[0]}",
            "tag": ["planningUpdate"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "title": "Planning Notice",
                "description": "Contracting process is planned",
                "status": "complete",
                "statusDetails": "empty",
                "items": [{
                    "id": first_item_id,
                    "internalId": "create Pn: tender.items[0].internalId",
                    "description": "create Pn: tender.items[0].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_first_item_cpv_code[0],
                        "description": get_value_by_first_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_first_item_cpvs_code[0],
                        "description": get_value_by_first_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_first_item_unit_id[0],
                        "name": get_value_by_first_item_unit_id[1]
                    },
                    "relatedLot": first_lot_id
                }, {
                    "id": second_item_id,
                    "internalId": "create Pn: tender.items[1].internalId",
                    "description": "create Pn: tender.items[1].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_second_item_cpv_code[0],
                        "description": get_value_by_second_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_second_item_cpvs_code[0],
                        "description": get_value_by_second_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_second_item_unit_id[0],
                        "name": get_value_by_second_item_unit_id[1]
                    },
                    "relatedLot": second_lot_id
                }],
                "lots": [{
                    "id": first_lot_id,
                    "internalId": "create Pn: tender.lots[0].internalId",
                    "title": "create Pn: tender.lots[0].title",
                    "description": "create Pn: tender.lots[0].internalId.description",
                    "status": "planning",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 1500.00,
                        "currency": "EUR"
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
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[0].placeOfPerformance.address.streetAddress",
                            "postalCode": "create Pn: tender.lots[0].placeOfPerformance.address.postalCode",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        },
                        "description": "create Pn: tender.lots[0].placeOfPerformance.description"
                    },
                    "options": [{
                        "hasOptions": False
                    }]
                }, {
                    "id": second_lot_id,
                    "internalId": "create Pn: tender.lots[1].internalId",
                    "title": "create Pn: tender.lots[1].title",
                    "description": "create Pn: tender.lots[1].internalId.description",
                    "status": "planning",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 150.00,
                        "currency": "EUR"
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
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[1].placeOfPerformance.address.streetAddress",
                            "postalCode": "create Pn: tender.lots[1].placeOfPerformance.address.postalCode",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        },
                        "description": "create Pn: tender.lots[1].placeOfPerformance.description"
                    },
                    "options": [{
                        "hasOptions": False
                    }]
                }],
                "lotGroups": [{
                    "optionToCombine": False
                }],
                "tenderPeriod": {
                    "startDate": period[3]
                },
                "hasEnquiries": False,
                "documents": [
                    {
                        "id": self.document_one_was_uploaded,
                        "documentType": "contractArrangements",
                        "title": "create Pn: tender.documents[0].title",
                        "description": "create Pn: tender.documents[0].description",
                        "url": f"{instance_storage_url}"
                               f"{self.document_one_was_uploaded}",
                        "datePublished": f"{get_human_date_in_utc_format(int(pn_id[32:45]))[0]}",
                        "relatedLots": [first_lot_id]
                    },
                    {
                        "id": self.document_two_was_uploaded,
                        "documentType": "contractArrangements",
                        "title": "create Pn: tender.documents[1].title",
                        "description": "create Pn: tender.documents[1].description",
                        "url": f"{instance_storage_url}"
                               f"{self.document_two_was_uploaded}",
                        "datePublished": f"{get_human_date_in_utc_format(int(pn_id[32:45]))[0]}",
                        "relatedLots": [second_lot_id]
                    }],
                "submissionMethod": ["electronicSubmission"],
                "submissionMethodDetails": submission_method_details,
                "submissionMethodRationale": submission_method_rationale,
                "requiresElectronicCatalogue": False,
                "procurementMethodRationale": "create Pn: tender.procurementMethodRationale",
                "classification": {
                    "scheme": "CPV",
                    "id": get_value_by_new_cpv_code[0],
                    "description": get_value_by_new_cpv_code[1]
                },
                "value": {
                    "amount": 1650.00,
                    "currency": "EUR"
                }
            },
            "hasPreviousNotice": False,
            "purposeOfNotice": {
                "isACallForCompetition": False
            },
            "relatedProcesses": [{
                "id": "36b553f3-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": cp_id,
                "uri": f"{instance_tender_url}{cp_id}/{cp_id}"
            }]
        }
        json_notice_release_ev = {
            "ocid": ev_id,
            "id": f"{ev_id}-{ev_id[32:45]}",
            "date": f"{get_human_date_in_utc_format(int(ev_id[32:45]))[0]}",
            "tag": ["tender"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "c36f9952-06d5-41ef-9fe6-36722f1da414",
                "title": "Planning Notice",
                "description": "Contracting process is planned",
                "status": "active",
                "statusDetails": "clarification",
                "criteria": [{
                    "id": "9b62d854-acd3-479f-b0a9-402fe8081480",
                    "title": "create CNonPN: tender.criteria[0].title =Bankruptcy",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[0].description =Is the economic operator bankrupt? "
                                   "This information needs not be given if exclusion of economic operators in this "
                                   "case has been made mandatory under the applicable national law without any "
                                   "possibility of derogation where the economic operator is nevertheless able to "
                                   "perform the contract.",
                    "requirementGroups": [{
                        "id": "f83633d5-6d4e-4b9f-9bc2-8770f8bfb9b6",
                        "description": "create CNonPN: tender.criteria[0].requirementGroups[0].description =approve "
                                       "that Bankruptcy requirement group",
                        "requirements": [{
                            "id": "d5366584-8e57-445f-b1f6-55063bb29ea2",
                            "title": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements.title",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "description": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements."
                                           "description",
                            "eligibleEvidences": [{
                                "id": "1",
                                "title": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements[0]."
                                         "eligibleEvidences[0].title",
                                "type": "document",
                                "description": "create CNonPN: tender.criteria[0].requirementGroups[0]."
                                               "requirements[0].eligibleEvidences[0].description",
                                "relatedDocument": {
                                    "id": self.document_three_was_uploaded
                                }
                            }, {
                                "id": "2",
                                "title": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements[0]."
                                         "eligibleEvidences[1].title",
                                "type": "document",
                                "description": "create CNonPN: tender.criteria[0].requirementGroups[0]."
                                               "requirements[0].eligibleEvidences[1].description",
                                "relatedDocument": {
                                    "id": self.document_three_was_uploaded
                                }
                            }],
                            "expectedValue": False
                        }]
                    }],
                    "relatesTo": "tender",
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.EXCLUSION.CONVICTIONS.PARTICIPATION_IN_CRIMINAL_ORGANISATION"
                    }
                }, {
                    "id": "0b607a5e-e432-4d60-bcff-40c4de9ee04b",
                    "title": "create CNonPN: tender.criteria[1].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[1].description",
                    "requirementGroups": [{
                        "id": "437c395a-7a92-48c3-94bd-fcd3fb238304",
                        "description": "create CNonPN: tender.criteria[1].requirementGroups[0].description",
                        "requirements": [{
                            "id": "7bcf3819-a328-4560-b256-24c89b70d436",
                            "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[0].title",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "description": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements."
                                           "description",
                            "expectedValue": True
                        }, {
                            "id": "5b761cae-5c26-4266-b81d-9178232e931e",
                            "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[1]."
                                     "title =The number of years for proposed product warranty",
                            "dataType": "number",
                            "status": "active",
                            "datePublished": operation_date,
                            "description": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[1]."
                                           "description",
                            "period": {
                                "startDate": period[0],
                                "endDate": period[1]
                            },
                            "eligibleEvidences": [{
                                "id": "3",
                                "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[1]."
                                         "eligibleEvidences[0].title",
                                "type": "document",
                                "description": "create CNonPN: tender.criteria[1].requirementGroups[0]."
                                               "requirements[1].eligibleEvidences[0].description",
                                "relatedDocument": {
                                    "id": self.document_three_was_uploaded
                                }
                            }],
                            "minValue": 1.000,
                            "maxValue": 3.000
                        }]
                    }],
                    "relatesTo": "lot",
                    "relatedItem": first_lot_id,
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.SELECTION.ECONOMIC_FINANCIAL_STANDING.TURNOVER.GENERAL_YEARLY"
                    }
                }, {
                    "id": "11a3595b-4327-4382-a72f-e663f937a206",
                    "title": "create CNonPN: tender.criteria[2].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[2].description",
                    "requirementGroups": [{
                        "id": "779894eb-41c2-4db0-825c-27d3dbd522a6",
                        "description": "create CNonPN: tender.criteria[2].requirementGroups[0].description",
                        "requirements": [{
                            "id": "e30b1213-f94d-4364-9a75-e9532d7c98ed",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[0].requirements[0]."
                                     "title =Product has to be manufactured in the EU",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "expectedValue": True
                        }, {
                            "id": "e95d0bce-acf6-4873-867f-7a26a6935146",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[0]..requirements[1]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }, {
                        "id": "c1021836-1fe1-49e1-8286-42badf1b62aa",
                        "description": "create CNonPN: tender.criteria[2].requirementGroups[1].description",
                        "requirements": [{
                            "id": "0cef779c-9039-4a87-838d-1f8775a14f57",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[1].requirements[0]."
                                     "title =Product has to be manufactured in the EU",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "expectedValue": True
                        }, {
                            "id": "53cade1e-112a-441e-a2d0-64c2bc547f43",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[1]..requirements[1]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }],
                    "relatesTo": "tenderer",
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.EXCLUSION.NATIONAL.OTHER"
                    }
                }, {
                    "id": "a8168d9a-34c8-44b7-8a59-d126d770ffa2",
                    "title": "create CNonPN: tender.criteria[3].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[3].description =A minimum product warranty "
                                   "of 1 year is required for all bids 2",
                    "requirementGroups": [{
                        "id": "1992b2ca-4ac2-43c2-b1ef-90d41860c718",
                        "description": "create CNonPN: tender.criteria[3].requirementGroups[0].description",
                        "requirements": [{
                            "id": "aaa2e373-2fee-4da4-a153-16c89127a633",
                            "title": "create CNonPN: tender.criteria[3].requirementGroups[0].requirements[0]."
                                     "title = The number of years for proposed product warranty",
                            "dataType": "number",
                            "status": "active",
                            "datePublished": operation_date,
                            "period": {
                                "startDate": period[0],
                                "endDate": period[1]
                            },
                            "minValue": 1.000,
                            "maxValue": 3.000
                        }]
                    }],
                    "relatesTo": "item",
                    "relatedItem": first_item_id,
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.OTHER.EO_DATA.RELIES_ON_OTHER_CAPACITIES"
                    }
                }, {
                    "id": "a5569789-616d-407b-844e-8974611db63d",
                    "title": "create CNonPN: tender.criteria[4].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[4].description",
                    "requirementGroups": [{
                        "id": "e2e4291b-7e9c-401c-b9a6-2ec6bee0c85c",
                        "description": "create CNonPN: tender.criteria[4].requirementGroups[0].description",
                        "requirements": [{
                            "id": "4d104276-47fc-4d93-a694-444457b825e4",
                            "title": "create CNonPN: tender.criteria[4].requirementGroups[0].requirements[0]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }],
                    "relatesTo": "tender",
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.EXCLUSION.NATIONAL.OTHER"
                    }
                }, {
                    "id": "dd056608-225f-4e1b-9e22-e8b927f50678",
                    "title": "create CNonPN: tender.criteria[4].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[4].description",
                    "requirementGroups": [{
                        "id": "c6f455a8-dcd3-40ae-8518-c07bc68603c0",
                        "description": "create CNonPN: tender.criteria[4].requirementGroups[0].description",
                        "requirements": [{
                            "id": "9529530c-bdeb-45db-b559-aa9f5fba7b05",
                            "title": "create CNonPN: tender.criteria[4].requirementGroups[0].requirements[0]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }],
                    "relatesTo": "tender",
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.OTHER.EO_DATA.RELIES_ON_OTHER_CAPACITIES"
                    }
                }],
                "conversions": [{
                    "id": "1e49348e-1a13-409e-95f8-371cb7430a6a",
                    "relatesTo": "requirement",
                    "relatedItem": "7bcf3819-a328-4560-b256-24c89b70d436",
                    "rationale": "create CNonPN: tender.conversions[1].rationale",
                    "description": "create CNonPN: tender.conversions[1].description",
                    "coefficients": [{
                        "id": "3344c418-c0cb-40f5-86bd-2e7aab5d5e19",
                        "value": False,
                        "coefficient": 1
                    }]
                }, {
                    "id": "b61c8d3f-54cb-48cf-94d3-6547db1b6584",
                    "relatesTo": "requirement",
                    "relatedItem": "5b761cae-5c26-4266-b81d-9178232e931e",
                    "rationale": "create CNonPN: tender.conversions[3].rationale",
                    "description": "create CNonPN: tender.conversions[3].description",
                    "coefficients": [{
                        "id": "8e1c5c9d-9fd5-4524-8ee7-1dc69c392e25",
                        "value": 1.000,
                        "coefficient": 1
                    }, {
                        "id": "eea59dc3-cf39-43e4-85ae-c25f4207c378",
                        "value": 2.000,
                        "coefficient": 1
                    }, {
                        "id": "2ef0e48a-5359-4c2b-b4a7-e2e209239173",
                        "value": 3.000,
                        "coefficient": 0.93
                    }]
                }, {
                    "id": "602f52cb-6257-479b-b637-85bd1b94a3cf",
                    "relatesTo": "requirement",
                    "relatedItem": "aaa2e373-2fee-4da4-a153-16c89127a633",
                    "rationale": "create CNonPN: tender.conversions[6].rationale",
                    "description": "create CNonPN: tender.conversions[6].description",
                    "coefficients": [{
                        "id": "0b1fd4bc-dcb9-460d-89fa-ce44387b76ef",
                        "value": 1.000,
                        "coefficient": 1
                    }, {
                        "id": "c9bcba0e-f235-40c4-9023-1c4e7813e7a0",
                        "value": 2.000,
                        "coefficient": 1
                    }, {
                        "id": "998f9ae4-86a0-4c80-8973-f7d7cdc78351",
                        "value": 3.000,
                        "coefficient": 0.93
                    }]
                }, {
                    "id": "df048f38-c201-4aae-a529-a721a7687430",
                    "relatesTo": "requirement",
                    "relatedItem": "9529530c-bdeb-45db-b559-aa9f5fba7b05",
                    "rationale": "create CNonPN: tender.conversions[6].rationale",
                    "description": "create CNonPN: tender.conversions[6].description",
                    "coefficients": [{
                        "id": "49f34ab3-c0ad-4509-b77f-ead756c50419",
                        "value": "option_1",
                        "coefficient": 1
                    }, {
                        "id": "39819b5c-2c5c-40db-af46-2e6b6b2f0dcb",
                        "value": "option_2",
                        "coefficient": 1
                    }, {
                        "id": "0cda7c91-e74d-4f57-91bd-cae195078dda",
                        "value": "option_3",
                        "coefficient": 0.93
                    }]
                }],
                "items": [{
                    "id": first_item_id,
                    "internalId": "create Pn: tender.items[0].internalId",
                    "description": "create Pn: tender.items[0].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_first_item_cpv_code[0],
                        "description": get_value_by_first_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_first_item_cpvs_code[0],
                        "description": get_value_by_first_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "name": get_value_by_first_item_unit_id[1],
                        "id": get_value_by_first_item_unit_id[0]
                    },
                    "relatedLot": first_lot_id
                }, {
                    "id": second_item_id,
                    "internalId": "create Pn: tender.items[1].internalId",
                    "description": "create Pn: tender.items[1].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_second_item_cpv_code[0],
                        "description": get_value_by_second_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_second_item_cpvs_code[0],
                        "description": get_value_by_second_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_first_item_unit_id[0],
                        "name": get_value_by_first_item_unit_id[1]
                    },
                    "relatedLot": second_lot_id
                }],
                "lots": [{
                    "id": first_lot_id,
                    "internalId": "create Pn: tender.lots[0].internalId",
                    "title": "create Pn: tender.lots[0].title",
                    "description": "create Pn: tender.lots[0].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 1500.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[0].placeOfPerformance.address.streetAddress",
                            "postalCode": "create Pn: tender.lots[0].placeOfPerformance.address.postalCode",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        },
                        "description": "create Pn: tender.lots[0].placeOfPerformance.description"
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }, {
                    "id": second_lot_id,
                    "internalId": "create Pn: tender.lots[1].internalId",
                    "title": "create Pn: tender.lots[1].title",
                    "description": "create Pn: tender.lots[1].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 150.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[1].placeOfPerformance.address.streetAddress",
                            "postalCode": "create Pn: tender.lots[1].placeOfPerformance.address.postalCode",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        },
                        "description": "create Pn: tender.lots[1].placeOfPerformance.description"
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }],
                "lotGroups": [{
                    "optionToCombine": False
                }],
                "tenderPeriod": {
                    "startDate": enquiry_and_tender_period[2],
                    "endDate": enquiry_and_tender_period[3]
                },
                "enquiryPeriod": {
                    "startDate": enquiry_and_tender_period[0],
                    "endDate": enquiry_and_tender_period[1]
                },
                "auctionPeriod": {
                    "startDate": auction_date
                },
                "hasEnquiries": False,
                "documents": [{
                    "id": self.document_one_was_uploaded,
                    "documentType": "contractArrangements",
                    "title": "create Pn: tender.documents[0].title",
                    "description": "create Pn: tender.documents[0].description",
                    "url": f"{instance_storage_url}{self.document_one_was_uploaded}",
                    "datePublished": operation_date,
                    "relatedLots": [first_lot_id]
                }, {
                    "id": self.document_two_was_uploaded,
                    "documentType": "contractArrangements",
                    "title": "create Pn: tender.documents[1].title",
                    "description": "create Pn: tender.documents[1].description",
                    "url": f"{instance_storage_url}{self.document_two_was_uploaded}",
                    "datePublished": operation_date,
                    "relatedLots": [second_lot_id]
                }, {
                    "id": self.document_three_was_uploaded,
                    "documentType": "illustration",
                    "title": "create CNonPN: tender.documents[2].title",
                    "description": "create CNonPN: tender.documents[2].description",
                    "url": f"{instance_storage_url}"
                           f"{self.document_three_was_uploaded}",
                    "datePublished": operation_date,
                    "relatedLots": [first_lot_id]
                }],
                "awardCriteria": "ratedCriteria",
                "awardCriteriaDetails": "automated",
                "submissionMethod": ["electronicSubmission"],
                "submissionMethodDetails": submission_method_details,
                "submissionMethodRationale": submission_method_rationale,
                "requiresElectronicCatalogue": False,
                "procurementMethodModalities": ["electronicAuction"],
                "electronicAuctions": {
                    "details": [{
                        "id": "2cbf1162-4e8b-48d7-b64b-680b5fa6b350",
                        "relatedLot": first_lot_id,
                        "auctionPeriod": {
                            "startDate": auction_date
                        },
                        "electronicAuctionModalities": [{
                            "url": f"https://eauction.eprocurement.systems/auctions/{ev_id}/{first_lot_id}",
                            "eligibleMinimumDifference": {
                                "amount": 100.00,
                                "currency": "EUR"
                            }
                        }]
                    }, {
                        "id": "c19b09d5-3dcb-43a8-a1fc-096948abb403",
                        "relatedLot": second_lot_id,
                        "auctionPeriod": {
                            "startDate": auction_date
                        },
                        "electronicAuctionModalities": [{
                            "url": f"https://eauction.eprocurement.systems/auctions/{ev_id}/{second_lot_id}",
                            "eligibleMinimumDifference": {
                                "amount": 10.00,
                                "currency": "EUR"
                            }
                        }]
                    }]
                },
                "procurementMethodRationale": "create CNonPN: tender.procurementMethodRationale"
            },
            "hasPreviousNotice": True,
            "purposeOfNotice": {
                "isACallForCompetition": True
            },
            "relatedProcesses": [{
                "id": "12a3ea63-ceca-11eb-8aed-69d06bed4d57",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": cp_id,
                "uri": f"{instance_tender_url}{cp_id}/{cp_id}"
            }, {
                "id": "164cf531-ceca-11eb-8aed-69d06bed4d57",
                "relationship": ["planning"],
                "scheme": "ocid",
                "identifier": pn_id,
                "uri": f"{instance_tender_url}{cp_id}/{pn_id}"
            }]
        }
        json_notice_compiled_release_ms = {
            "ocid": cp_id,
            "id": f"{cp_id}-{ev_id[32:45]}",
            "date": f"{get_human_date_in_utc_format(int(ev_id[32:45]))[0]}",
            "tag": ["compiled"],
            "language": self.lang,
            "initiationType": "tender",
            "planning": {
                "budget": {
                    "description": "create Pn: planning.budget.description",
                    "amount": {
                        "amount": 2000.00,
                        "currency": "EUR"
                    },
                    "isEuropeanUnionFunded": True,
                    "budgetBreakdown": [{
                        "id": fs_id,
                        "description": "create Fs: planning.budget.description",
                        "amount": {
                            "amount": 2000.00,
                            "currency": "EUR"
                        },
                        "period": {
                            "startDate": period[0],
                            "endDate": period[1]
                        },
                        "sourceParty": {
                            "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                            "name": self.funder_name,
                        },
                        "europeanUnionFunding": {
                            "projectIdentifier": "create Fs: planning.budget.europeanUnionFunding.projectIdentifier",
                            "projectName": "create Fs: planning.budget.europeanUnionFunding.projectName",
                            "uri": "create Fs: planning.budget.europeanUnionFunding.uri"
                        }
                    }]
                },
                "rationale": "create Pn: planning.rationale"
            },
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "title": "create Pn: tender.title",
                "description": "create Pn: tender.description",
                "status": "active",
                "statusDetails": "evaluation",
                "value": {
                    "amount": 1650.00,
                    "currency": "EUR"
                },
                "procurementMethod": "open",
                "procurementMethodDetails": procurement_method_details_from_mdm,
                "procurementMethodRationale": "create CNonPN: tender.procurementMethodRationale",
                "mainProcurementCategory": "works",
                "hasEnquiries": False,
                "eligibilityCriteria": eligibility_criteria_from_mdm,
                "contractPeriod": {
                    "startDate": contract_period[0],
                    "endDate": contract_period[1]
                },
                "procuringEntity": {
                    "id": "MD-IDNO-4",
                    "name": "create Pn: tender.procuringEntity.name"
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
                "legalBasis": "DIRECTIVE_2014_25_EU",
                "procedureOutsourcing": {
                    "procedureOutsourced": False
                },
                "procurementMethodAdditionalInfo": "create CNonPN: tender.procurementMethodAdditionalInfo",
                "dynamicPurchasingSystem": {
                    "hasDynamicPurchasingSystem": False
                },
                "framework": {
                    "isAFramework": False
                }
            },
            "parties": [{
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name,
                "identifier": {
                    "scheme": self.buyer_identifier_scheme,
                    "id": self.buyer_identifier_id,
                    "legalName": self.buyer_identifier_legal_name,
                    "uri": self.buyer_identifier_uri
                },
                "address": {
                    "streetAddress": self.buyer_address_street_address,
                    "postalCode": self.buyer_address_postal_code,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.buyer_address_address_details_country_id,
                            "description": "Moldova, Republica",
                            "uri": "https://www.iso.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": self.buyer_address_address_details_region_id,
                            "description": "mun.Chişinău",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": self.buyer_address_address_details_locality_scheme,
                            "id": self.buyer_address_address_details_locality_id,
                            "description": self.buyer_address_address_details_locality_description,
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "additionalIdentifiers": [{
                    "scheme": "create Ei: buyer.additionalIdentifiers[0].scheme",
                    "id": "create Ei: buyer.additionalIdentifiers[0].id",
                    "legalName": "create Ei: buyer.additionalIdentifiers[0].legalName",
                    "uri": "create Ei: buyer.additionalIdentifiers[0].uri"
                }],
                "contactPoint": {
                    "name": self.buyer_contact_point_name,
                    "email": self.buyer_contact_point_email,
                    "telephone": self.buyer_contact_point_telephone,
                    "faxNumber": self.buyer_contact_point_fax_number,
                    "url": self.buyer_contact_point_url
                },
                "details": {
                    "typeOfBuyer": "NATIONAL_AGENCY",
                    "mainGeneralActivity": "HEALTH",
                    "mainSectoralActivity": "WATER"
                },
                "roles": ["buyer"]
            }, {
                "id": f"{self.payer_identifier_scheme}-{self.payer_identifier_id}",
                "name": self.payer_name,
                "identifier": {
                    "scheme": self.payer_identifier_scheme,
                    "id": self.payer_identifier_id,
                    "legalName": self.payer_identifier_legal_name,
                    "uri": self.payer_identifier_uri
                },
                "address": {
                    "streetAddress": self.payer_address_street,
                    "postalCode": self.payer_address_postal_code,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.payer_address_postal_code,
                            "description": "Moldova, Republica",
                            "uri": "https://www.iso.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": self.payer_address_address_details_region_id,
                            "description": "Donduşeni",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": self.payer_address_address_details_locality_scheme,
                            "id": self.payer_address_address_details_locality_id,
                            "description": self.payer_address_address_details_locality_description,
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "additionalIdentifiers": [{
                    "scheme": "create Fs: tender.procuringEntity.additionalIdentifiers[0].scheme",
                    "id": "create Fs: tender.procuringEntity.additionalIdentifiers[0].id",
                    "legalName": "create Fs: tender.procuringEntity.additionalIdentifiers[0].legalName",
                    "uri": "create Fs: tender.procuringEntity.additionalIdentifiers[0].uri"
                }],
                "contactPoint": {
                    "name": self.payer_contact_point_name,
                    "email": self.payer_contact_point_email,
                    "telephone": self.payer_contact_point_telephone,
                    "faxNumber": self.payer_contact_point_fax_number,
                    "url": self.payer_contact_point_url
                },
                "roles": ["payer"]
            }, {
                "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                "name": self.funder_name,
                "identifier": {
                    "scheme": self.funder_identifier_scheme,
                    "id": self.funder_identifier_id,
                    "legalName": self.funder_identifier_legal_name,
                    "uri": self.funder_identifier_uri
                },
                "address": {
                    "streetAddress": self.funder_address_street,
                    "postalCode": self.funder_address_postal_code,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.funder_address_address_details_country_id,
                            "description": "Moldova, Republica",
                            "uri": "https://www.iso.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": self.funder_address_address_details_region_id,
                            "description": "Cahul",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": self.funder_address_address_details_locality_scheme,
                            "id": self.funder_address_address_details_locality_id,
                            "description": self.funder_address_address_details_locality_description,
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "additionalIdentifiers": [{
                    "scheme": "create Fs: buyer.additionalIdentifiers[0].scheme",
                    "id": "create Fs: buyer.additionalIdentifiers[0].id",
                    "legalName": "create Fs: buyer.additionalIdentifiers[0].legalName",
                    "uri": "create Fs: buyer.additionalIdentifiers[0].uri"
                }],
                "contactPoint": {
                    "name": self.funder_contact_point_name,
                    "email": self.funder_contact_point_email,
                    "telephone": self.funder_contact_point_telephone,
                    "faxNumber": self.funder_contact_point_fax,
                    "url": self.funder_contact_point_url
                },
                "roles": ["funder"]
            }, {
                "id": "MD-IDNO-4",
                "name": "create Pn: tender.procuringEntity.name",
                "identifier": {
                    "scheme": "MD-IDNO",
                    "id": "4",
                    "legalName": "create Pn: tender.procuringEntity.identigfier.legalName",
                    "uri": "create Pn: tender.procuringEntity.identifier.uri"
                },
                "address": {
                    "streetAddress": "street address",
                    "postalCode": "02232",
                    "addressDetails": {
                        "country": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["country"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['uri']
                        },
                        "region": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["region"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['uri']
                        },
                        "locality": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["locality"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['uri']
                        }
                    }
                },
                "additionalIdentifiers": [{
                    "scheme": "create Pn: tender.procuringEntity.additionalIdentifiers[0].scheme",
                    "id": "create Pn: tender.procuringEntity.additionalIdentifiers[0].id",
                    "legalName": "create Pn: tender.procuringEntity.additionalIdentifiers[0].legalName",
                    "uri": "create Pn: tender.procuringEntity.additionalIdentifiers[0].uri"
                }],
                "contactPoint": {
                    "name": "name",
                    "email": "email",
                    "telephone": "456-95-96",
                    "faxNumber": "fax-number",
                    "url": "url"
                },
                "persones": [{
                    "id": "MD-IDNO-create CNonPN: procuringEntity.persones[0].identifier.id",
                    "title": "create CNonPN: procuringEntity.persones[0].title",
                    "name": "create CNonPN: procuringEntity.persones[0].name",
                    "identifier": {
                        "scheme": "MD-IDNO",
                        "id": "create CNonPN: procuringEntity.persones[0].identifier.id",
                        "uri": "create CNonPN: procuringEntity.persones[0].identifier.uri"
                    },
                    "businessFunctions": [{
                        "id": "create CNonPN: procuringEntity.persones[0].businessFunctions[0].id",
                        "type": "procurementOfficer",
                        "jobTitle": "create CNonPN: procuringEntity.persones[0].businessFunctions[0].jobTitle",
                        "period": {
                            "startDate": period[0]
                        },
                        "documents": [{
                            "id": self.document_three_was_uploaded,
                            "documentType": "regulatoryDocument",
                            "title": "create CNonPN: procuringEntity.persones[0].businessFunctions[0].title",
                            "description": "create CNonPN: procuringEntity.persones[0].businessFunctions[0]."
                                           "description",
                            "url": f"{instance_storage_url}"
                                   f"{self.document_three_was_uploaded}",
                            "datePublished": operation_date
                        }]
                    }]
                }],
                "roles": ["procuringEntity"]
            }],
            "relatedProcesses": [{
                "id": "36b553f0-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["planning"],
                "scheme": "ocid",
                "identifier": pn_id,
                "uri": f"{instance_tender_url}{cp_id}/{pn_id}"
            }, {
                "id": "36b553f1-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["x_expenditureItem"],
                "scheme": "ocid",
                "identifier": ei_id,
                "uri": f"{instance_budget_url}{ei_id}/{ei_id}"
            }, {
                "id": "36b553f2-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["x_fundingSource"],
                "scheme": "ocid",
                "identifier": fs_id,
                "uri": f"{instance_budget_url}{ei_id}/{fs_id}"
            },
                {
                    "id": "ed0f7290-cee4-11eb-8aed-69d06bed4d57",
                    "relationship": ["x_evaluation"],
                    "scheme": "ocid",
                    "identifier": ev_id,
                    "uri": f"{instance_tender_url}{cp_id}/{ev_id}"
                }
            ]

        }
        json_notice_compiled_release_pn = {
            "ocid": pn_id,
            "id": f"{pn_id}-{ev_id[32:45]}",
            "date": f"{get_human_date_in_utc_format(int(ev_id[32:45]))[0]}",
            "tag": ["planningUpdate"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "title": "Planning Notice",
                "description": "Contracting process is planned",
                "status": "complete",
                "statusDetails": "empty",
                "items": [{
                    "id": first_item_id,
                    "internalId": "create Pn: tender.items[0].internalId",
                    "description": "create Pn: tender.items[0].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_first_item_cpv_code[0],
                        "description": get_value_by_first_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_first_item_cpvs_code[0],
                        "description": get_value_by_first_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_first_item_unit_id[0],
                        "name": get_value_by_first_item_unit_id[1]
                    },
                    "relatedLot": first_lot_id
                }, {
                    "id": second_item_id,
                    "internalId": "create Pn: tender.items[1].internalId",
                    "description": "create Pn: tender.items[1].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_second_item_cpv_code[0],
                        "description": get_value_by_second_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_second_item_cpvs_code[0],
                        "description": get_value_by_second_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_second_item_unit_id[0],
                        "name": get_value_by_second_item_unit_id[1]
                    },
                    "relatedLot": second_lot_id
                }],
                "lots": [{
                    "id": first_lot_id,
                    "internalId": "create Pn: tender.lots[0].internalId",
                    "title": "create Pn: tender.lots[0].title",
                    "description": "create Pn: tender.lots[0].internalId.description",
                    "status": "planning",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 1500.00,
                        "currency": "EUR"
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
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[0].placeOfPerformance.address.streetAddress",
                            "postalCode": "create Pn: tender.lots[0].placeOfPerformance.address.postalCode",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        },
                        "description": "create Pn: tender.lots[0].placeOfPerformance.description"
                    },
                    "options": [{
                        "hasOptions": False
                    }]
                }, {
                    "id": second_lot_id,
                    "internalId": "create Pn: tender.lots[1].internalId",
                    "title": "create Pn: tender.lots[1].title",
                    "description": "create Pn: tender.lots[1].internalId.description",
                    "status": "planning",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 150.00,
                        "currency": "EUR"
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
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[1].placeOfPerformance.address.streetAddress",
                            "postalCode": "create Pn: tender.lots[1].placeOfPerformance.address.postalCode",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        },
                        "description": "create Pn: tender.lots[1].placeOfPerformance.description"
                    },
                    "options": [{
                        "hasOptions": False
                    }]
                }],
                "lotGroups": [{
                    "optionToCombine": False
                }],
                "tenderPeriod": {
                    "startDate": period[3]
                },
                "hasEnquiries": False,
                "documents": [
                    {
                        "id": self.document_one_was_uploaded,
                        "documentType": "contractArrangements",
                        "title": "title of document",
                        "description": "descrition of document",
                        "url": f"{instance_storage_url}"
                               f"{self.document_one_was_uploaded}",
                        "datePublished": f"{get_human_date_in_utc_format(int(pn_id[32:45]))[0]}",
                        "relatedLots": [first_lot_id]
                    },
                    {
                        "id": self.document_two_was_uploaded,
                        "documentType": "contractArrangements",
                        "title": "title of document",
                        "description": "descrition of document",
                        "url": f"{instance_storage_url}"
                               f"{self.document_two_was_uploaded}",
                        "datePublished": f"{get_human_date_in_utc_format(int(pn_id[32:45]))[0]}",
                        "relatedLots": [second_lot_id]
                    }],
                "submissionMethod": ["electronicSubmission"],
                "submissionMethodDetails": submission_method_details,
                "submissionMethodRationale": submission_method_rationale,
                "requiresElectronicCatalogue": False,
                "procurementMethodRationale": "create Pn: tender.procurementMethodRationale",
                "classification": {
                    "scheme": "CPV",
                    "id": get_value_by_new_cpv_code[0],
                    "description": get_value_by_new_cpv_code[1]
                },
                "value": {
                    "amount": 1650.00,
                    "currency": "EUR"
                }
            },
            "hasPreviousNotice": False,
            "purposeOfNotice": {
                "isACallForCompetition": False
            },
            "relatedProcesses": [{
                "id": "36b553f3-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": cp_id,
                "uri": f"{instance_tender_url}{cp_id}/{cp_id}"
            }]
        }
        json_notice_compiled_release_ev = {
            "ocid": ev_id,
            "id": f"{ev_id}-{ev_id[32:45]}",
            "date": f"{get_human_date_in_utc_format(int(ev_id[32:45]))[0]}",
            "tag": ["tender"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "title": "Evaluation",
                "description": "Evaluation stage of contracting process",
                "status": "active",
                "statusDetails": "clarification",
                "criteria": [{
                    "id": "58b814dc-ada7-40f1-b34e-fcb360830c2c",
                    "title": "create CNonPN: tender.criteria[0].title =Bankruptcy",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[0].description =Is the economic operator "
                                   "bankrupt? This information needs not be given if exclusion of economic "
                                   "operators in this case has been made mandatory under the applicable national "
                                   "law without any possibility of derogation where the economic operator is "
                                   "nevertheless able to perform the contract.",
                    "requirementGroups": [{
                        "id": "2f16e84f-aca2-4970-8a9a-6f253d20f8b3",
                        "description": "create CNonPN: tender.criteria[0].requirementGroups[0].description "
                                       "=approve that Bankruptcy requirement group",
                        "requirements": [{
                            "id": "01fcb528-6de6-4c07-9383-57c698116f18",
                            "title": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements.title",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "description": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements."
                                           "description",
                            "eligibleEvidences": [{
                                "id": "1",
                                "title": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements[0]."
                                         "eligibleEvidences[0].title",
                                "type": "document",
                                "description": "create CNonPN: tender.criteria[0].requirementGroups[0]."
                                               "requirements[0].eligibleEvidences[0].description",
                                "relatedDocument": {
                                    "id": self.document_three_was_uploaded
                                }
                            }, {
                                "id": "2",
                                "title": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements[0]."
                                         "eligibleEvidences[1].title",
                                "type": "document",
                                "description": "create CNonPN: tender.criteria[0].requirementGroups[0]."
                                               "requirements[0].eligibleEvidences[1].description",
                                "relatedDocument": {
                                    "id": self.document_three_was_uploaded
                                }
                            }],
                            "expectedValue": False
                        }]
                    }],
                    "relatesTo": "tender",
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.EXCLUSION.CONVICTIONS.PARTICIPATION_IN_CRIMINAL_ORGANISATION"
                    }
                }, {
                    "id": "a662195e-ad48-4ffc-9b51-7b01a3c04be0",
                    "title": "create CNonPN: tender.criteria[1].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[1].description",
                    "requirementGroups": [{
                        "id": "9ebb3a38-7835-48e2-84d5-c1debb0a4739",
                        "description": "create CNonPN: tender.criteria[1].requirementGroups[0].description",
                        "requirements": [{
                            "id": "1a149ebc-5d0c-4dd6-92b3-85ed9672a675",
                            "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[0].title",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "description": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements."
                                           "description",
                            "expectedValue": True
                        }, {
                            "id": "a4b456bb-32a6-4946-adf7-2ddaeb282c0e",
                            "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[1]."
                                     "title =The number of years for proposed product warranty",
                            "dataType": "number",
                            "status": "active",
                            "datePublished": operation_date,
                            "description": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements"
                                           "[1].description",
                            "period": {
                                "startDate": period[0],
                                "endDate": period[1]
                            },
                            "eligibleEvidences": [{
                                "id": "3",
                                "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[1]."
                                         "eligibleEvidences[0].title",
                                "type": "document",
                                "description": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements"
                                               "[1].eligibleEvidences[0].description",
                                "relatedDocument": {
                                    "id": self.document_three_was_uploaded
                                }
                            }],
                            "minValue": 1.000,
                            "maxValue": 3.000
                        }]
                    }],
                    "relatesTo": "lot",
                    "relatedItem": first_lot_id,
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.SELECTION.ECONOMIC_FINANCIAL_STANDING.TURNOVER.GENERAL_YEARLY"
                    }
                }, {
                    "id": "8e250762-2508-4175-af7e-1a5ca085a1e7",
                    "title": "create CNonPN: tender.criteria[2].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[2].description",
                    "requirementGroups": [{
                        "id": "ff3545aa-47ec-4666-8c8a-93c6e06f85d8",
                        "description": "create CNonPN: tender.criteria[2].requirementGroups[0].description",
                        "requirements": [{
                            "id": "e3f5ecdb-985d-42a0-97ca-85920a819095",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[0].requirements[0]."
                                     "title =Product has to be manufactured in the EU",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "expectedValue": True
                        }, {
                            "id": "22b9bb1f-692d-425a-bd11-3f4569ae35f3",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[0]..requirements[1]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }, {
                        "id": "31359580-435e-40d5-9a17-a40d03686a17",
                        "description": "create CNonPN: tender.criteria[2].requirementGroups[1].description",
                        "requirements": [{
                            "id": "9daba23f-510d-4f7f-a449-af17a3416081",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[1].requirements[0]."
                                     "title =Product has to be manufactured in the EU",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "expectedValue": True
                        }, {
                            "id": "03fc9deb-f9ca-4dcf-a9f0-e1dff43c6e42",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[1]..requirements[1]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }],
                    "relatesTo": "tenderer",
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.EXCLUSION.NATIONAL.OTHER"
                    }
                }, {
                    "id": "43fe2c58-14eb-47aa-9854-cbf594b1110e",
                    "title": "create CNonPN: tender.criteria[3].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[3].description =A minimum product warranty "
                                   "of 1 year is required for all bids 2",
                    "requirementGroups": [{
                        "id": "f18230c4-04e9-41af-b900-1a6521011c20",
                        "description": "create CNonPN: tender.criteria[3].requirementGroups[0].description",
                        "requirements": [{
                            "id": "25fe2901-8393-4198-88fc-01625039c48f",
                            "title": "create CNonPN: tender.criteria[3].requirementGroups[0].requirements[0]."
                                     "title = The number of years for proposed product warranty",
                            "dataType": "number",
                            "status": "active",
                            "datePublished": operation_date,
                            "period": {
                                "startDate": period[0],
                                "endDate": period[1]
                            },
                            "minValue": 1.000,
                            "maxValue": 3.000
                        }]
                    }],
                    "relatesTo": "item",
                    "relatedItem": first_item_id,
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.OTHER.EO_DATA.RELIES_ON_OTHER_CAPACITIES"
                    }
                }, {
                    "id": "5c8c1ce9-937c-41c6-a717-42db617da57b",
                    "title": "create CNonPN: tender.criteria[4].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[4].description",
                    "requirementGroups": [{
                        "id": "05f1412a-8cef-4534-b02f-2ecb8b82a34d",
                        "description": "create CNonPN: tender.criteria[4].requirementGroups[0].description",
                        "requirements": [{
                            "id": "4fde10c0-306f-4170-bc90-9290935c8ae1",
                            "title": "create CNonPN: tender.criteria[4].requirementGroups[0].requirements[0]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }],
                    "relatesTo": "tender",
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.EXCLUSION.NATIONAL.OTHER"
                    }
                }, {
                    "id": "6af5e886-b24d-4fa0-9e02-62c44833e609",
                    "title": "create CNonPN: tender.criteria[4].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[4].description",
                    "requirementGroups": [{
                        "id": "37fbcb8c-3cb5-4447-9597-04f161590ecd",
                        "description": "create CNonPN: tender.criteria[4].requirementGroups[0].description",
                        "requirements": [{
                            "id": "fb28d72b-4136-4535-8d5b-c0fae7a3bfcf",
                            "title": "create CNonPN: tender.criteria[4].requirementGroups[0].requirements[0]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }],
                    "relatesTo": "tender",
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.OTHER.EO_DATA.RELIES_ON_OTHER_CAPACITIES"
                    }
                }],
                "conversions": [{
                    "id": "72b46408-c9d1-40ff-ba93-ee8fdfa2a0f1",
                    "relatesTo": "requirement",
                    "relatedItem": "1a149ebc-5d0c-4dd6-92b3-85ed9672a675",
                    "rationale": "create CNonPN: tender.conversions[1].rationale",
                    "description": "create CNonPN: tender.conversions[1].description",
                    "coefficients": [{
                        "id": "05690b92-24b7-4422-9816-17fe8e3ed13b",
                        "value": False,
                        "coefficient": 1
                    }]
                }, {
                    "id": "7a93bc3b-f061-4f3b-a95a-9950bd577dcf",
                    "relatesTo": "requirement",
                    "relatedItem": "a4b456bb-32a6-4946-adf7-2ddaeb282c0e",
                    "rationale": "create CNonPN: tender.conversions[3].rationale",
                    "description": "create CNonPN: tender.conversions[3].description",
                    "coefficients": [{
                        "id": "0c8079ec-3c0e-4563-85f1-992975f7e04b",
                        "value": 1.000,
                        "coefficient": 1
                    }, {
                        "id": "f6f95e95-59af-42c1-9bc8-ecefcef27e7b",
                        "value": 2.000,
                        "coefficient": 1
                    }, {
                        "id": "a95aebf9-2d2c-41fa-9b43-1535682b20e8",
                        "value": 3.000,
                        "coefficient": 0.93
                    }]
                }, {
                    "id": "1b994f29-3341-4d21-a63a-22d430d40a13",
                    "relatesTo": "requirement",
                    "relatedItem": "25fe2901-8393-4198-88fc-01625039c48f",
                    "rationale": "create CNonPN: tender.conversions[6].rationale",
                    "description": "create CNonPN: tender.conversions[6].description",
                    "coefficients": [{
                        "id": "f25d0cf9-4787-44d7-b4b8-93e8db5a35c2",
                        "value": 1.000,
                        "coefficient": 1
                    }, {
                        "id": "ee713dff-62cd-4a36-abe3-53b332ed163d",
                        "value": 2.000,
                        "coefficient": 1
                    }, {
                        "id": "e1b625e7-28f1-4114-bf97-a5d5a4b4aaae",
                        "value": 3.000,
                        "coefficient": 0.93
                    }]
                }, {
                    "id": "4735af2c-766a-4c9a-891c-f2a84b5cb1b2",
                    "relatesTo": "requirement",
                    "relatedItem": "fb28d72b-4136-4535-8d5b-c0fae7a3bfcf",
                    "rationale": "create CNonPN: tender.conversions[6].rationale",
                    "description": "create CNonPN: tender.conversions[6].description",
                    "coefficients": [{
                        "id": "16acc108-d7cb-4ea4-af1c-c8bad67bda86",
                        "value": "option_1",
                        "coefficient": 1
                    }, {
                        "id": "231b3997-4c5f-4886-ae1d-1bd458801d54",
                        "value": "option_2",
                        "coefficient": 1
                    }, {
                        "id": "d248589c-55a4-4f74-817b-ddc7f8291805",
                        "value": "option_3",
                        "coefficient": 0.93
                    }]
                }],
                "items": [{
                    "id": first_item_id,
                    "internalId": "create Pn: tender.items[0].internalId",
                    "description": "create Pn: tender.items[0].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_first_item_cpv_code[0],
                        "description": get_value_by_first_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_first_item_cpvs_code[0],
                        "description": get_value_by_first_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_first_item_unit_id[0],
                        "name": get_value_by_first_item_unit_id[1]
                    },
                    "relatedLot": first_lot_id
                }, {
                    "id": second_item_id,
                    "internalId": "create Pn: tender.items[1].internalId",
                    "description": "create Pn: tender.items[1].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_second_item_cpv_code[0],
                        "description": get_value_by_second_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_second_item_cpvs_code[0],
                        "description": get_value_by_second_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_second_item_unit_id[0],
                        "name": get_value_by_second_item_unit_id[1]
                    },
                    "relatedLot": second_lot_id
                }],
                "lots": [{
                    "id": first_lot_id,
                    "internalId": "create Pn: tender.lots[0].internalId",
                    "title": "create Pn: tender.lots[0].title",
                    "description": "create Pn: tender.lots[0].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 1500.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[0].placeOfPerformance.address.streetAddress",
                            "postalCode": "create Pn: tender.lots[0].placeOfPerformance.address.postalCode",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        },
                        "description": "create Pn: tender.lots[0].placeOfPerformance.description"
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }, {
                    "id": second_lot_id,
                    "internalId": "create Pn: tender.lots[1].internalId",
                    "title": "create Pn: tender.lots[1].title",
                    "description": "create Pn: tender.lots[1].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 150.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[1].placeOfPerformance.address.streetAddress",
                            "postalCode": "create Pn: tender.lots[1].placeOfPerformance.address.postalCode",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        },
                        "description": "create Pn: tender.lots[1].placeOfPerformance.description"
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }],
                "lotGroups": [{
                    "optionToCombine": False
                }],
                "tenderPeriod": {
                    "startDate": enquiry_and_tender_period[2],
                    "endDate": enquiry_and_tender_period[3]
                },
                "enquiryPeriod": {
                    "startDate": enquiry_and_tender_period[0],
                    "endDate": enquiry_and_tender_period[1]
                },
                "auctionPeriod": {
                    "startDate": auction_date
                },
                "hasEnquiries": False,
                "documents": [{
                    "id": self.document_one_was_uploaded,
                    "documentType": "contractArrangements",
                    "title": "create Pn: tender.documents[0].title",
                    "description": "create Pn: tender.documents[0].description",
                    "url": f"{instance_storage_url}{self.document_one_was_uploaded}",
                    "datePublished": operation_date,
                    "relatedLots": [first_lot_id]
                }, {
                    "id": self.document_two_was_uploaded,
                    "documentType": "contractArrangements",
                    "title": "create Pn: tender.documents[1].title",
                    "description": "create Pn: tender.documents[1].description",
                    "url": f"{instance_storage_url}{self.document_two_was_uploaded}",
                    "datePublished": operation_date,
                    "relatedLots": [second_lot_id]
                }, {
                    "id": self.document_three_was_uploaded,
                    "documentType": "illustration",
                    "title": "create CNonPN: tender.documents[2].title",
                    "description": "create CNonPN: tender.documents[2].description",
                    "url": f"{instance_storage_url}"
                           f"{self.document_three_was_uploaded}",
                    "datePublished": operation_date,
                    "relatedLots": [first_lot_id]
                }],
                "awardCriteria": "ratedCriteria",
                "awardCriteriaDetails": "automated",
                "submissionMethod": ["electronicSubmission"],
                "submissionMethodDetails": submission_method_details,
                "submissionMethodRationale": submission_method_rationale,
                "requiresElectronicCatalogue": False,
                "procurementMethodModalities": ["electronicAuction"],
                "electronicAuctions": {
                    "details": [{
                        "id": "9f8c8d7c-127a-42ab-b72d-d215e5cc6b40",
                        "relatedLot": first_lot_id,
                        "auctionPeriod": {
                            "startDate": auction_date
                        },
                        "electronicAuctionModalities": [{
                            "url": f"https://eauction.eprocurement.systems/auctions/{ev_id}/{first_lot_id}",
                            "eligibleMinimumDifference": {
                                "amount": 100.00,
                                "currency": "EUR"
                            }
                        }]
                    }, {
                        "id": "5f2caa86-b76b-410f-b181-8528b233f43c",
                        "relatedLot": second_lot_id,
                        "auctionPeriod": {
                            "startDate": auction_date
                        },
                        "electronicAuctionModalities": [{
                            "url": f"https://eauction.eprocurement.systems/auctions/{ev_id}/{second_lot_id}",
                            "eligibleMinimumDifference": {
                                "amount": 10.00,
                                "currency": "EUR"
                            }
                        }]
                    }]
                },
                "procurementMethodRationale": "create CNonPN: tender.procurementMethodRationale"
            },
            "hasPreviousNotice": True,
            "purposeOfNotice": {
                "isACallForCompetition": True
            },
            "relatedProcesses": [{
                "id": "e84a2253-cee4-11eb-8aed-69d06bed4d57",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": cp_id,
                "uri": f"{instance_tender_url}{cp_id}/{cp_id}"
            }, {
                "id": "ed0f7291-cee4-11eb-8aed-69d06bed4d57",
                "relationship": ["planning"],
                "scheme": "ocid",
                "identifier": pn_id,
                "uri": f"{instance_tender_url}{cp_id}/{pn_id}"
            }]
        }

        kafka = Kafka(instance=self.instance)
        kafka.connect_kafka_producer()
        kafka.publish_message_into_chronograph_in_clarification(
            cp_id=cp_id,
            ev_id=ev_id,
            enquiry_end=enquiry_and_tender_period[1]
        )
        kafka.publish_message_into_chronograph_in_submission(
            cp_id=cp_id,
            ev_id=ev_id,
            tender_end=enquiry_and_tender_period[3]
        )

        key_space_ocds.execute(f"INSERT INTO orchestrator_context (cp_id,context) VALUES ("
                               f"'{ev_id}','{json.dumps(json_orchestrator_context)}');").one()
        key_space_access.execute(f"INSERT INTO tenders (cpid, ocid, token_entity,created_date,json_data, owner) "
                                 f"VALUES ('{cp_id}', '{ev_id}', '{pn_token}', {ev_id[32:45]}, "
                                 f"'{json.dumps(json_access_tender)}','{owner}');").one()
        key_space_auctions.execute(
            f"INSERT INTO auctions (cpid, ocid, api_version, country, data, operation_id, row_version, status ) "
            f"VALUES ('{cp_id}', '{ev_id}', '1.0.0', '{self.country}', '{json.dumps(json_auction_auctions)}', "
            f"'{uuid.uuid1()}',{0}, {1});").one()
        key_space_clarification.execute(
            f"INSERT INTO periods (cpid, ocid, end_date, owner, start_date) "
            f"VALUES ('{cp_id}', '{ev_id}', {get_timestamp_from_human_date(enquiry_and_tender_period[1])}, '{owner}', "
            f"{ev_id[32:45]});").one()
        key_space_submission.execute(
            f"INSERT INTO periods (cpid, ocid, end_date, start_date) "
            f"VALUES ('{cp_id}', '{ev_id}', {get_timestamp_from_human_date(enquiry_and_tender_period[3])}, "
            f"{get_timestamp_from_human_date(enquiry_and_tender_period[1])});").one()
        key_space_ocds.execute(f"INSERT INTO notice_offset (cp_id,release_date, stage, status) "
                               f"VALUES ('{cp_id}', {ev_id[32:45]}, 'EV', 'active');").one()
        key_space_ocds.execute(
            f"INSERT INTO notice_release (cp_id,oc_id, release_id, json_data, release_date, stage) "
            f"VALUES ('{cp_id}', '{cp_id}', '{cp_id + '-' + ev_id[32:45]}' ,'{json.dumps(json_notice_release_ms)}',"
            f"{ev_id[32:45]},'');").one()
        key_space_ocds.execute(
            f"INSERT INTO notice_release (cp_id,oc_id, release_id, json_data, release_date, stage) "
            f"VALUES ('{cp_id}', '{pn_id}', '{pn_id + '-' + ev_id[32:45]}' ,'{json.dumps(json_notice_release_pn)}',"
            f"{ev_id[32:45]},'PN');").one()
        key_space_ocds.execute(
            f"INSERT INTO notice_release (cp_id,oc_id, release_id, json_data, release_date, stage) "
            f"VALUES ('{cp_id}', '{ev_id}', '{ev_id + '-' + ev_id[32:45]}','{json.dumps(json_notice_release_ev)}',"
            f"{ev_id[32:45]},'EV');").one()
        key_space_ocds.execute(
            f"INSERT INTO notice_compiled_release (cp_id,oc_id, json_data, publish_date, release_date, "
            f"release_id, stage, status) VALUES ('{cp_id}', '{cp_id}', '{json.dumps(json_notice_compiled_release_ms)}',"
            f"{ev_id[32:45]},{ev_id[32:45]}, '{cp_id + '-' + ev_id[32:45]}','', 'active');").one()
        key_space_ocds.execute(
            f"INSERT INTO notice_compiled_release (cp_id,oc_id, json_data, publish_date, release_date, "
            f"release_id, stage, status) VALUES ('{cp_id}', '{pn_id}', '{json.dumps(json_notice_compiled_release_pn)}',"
            f"{ev_id[32:45]},{ev_id[32:45]}, '{pn_id + '-' + ev_id[32:45]}','PN', 'active');").one()
        key_space_ocds.execute(
            f"INSERT INTO notice_compiled_release (cp_id,oc_id, json_data, publish_date, release_date, "
            f"release_id, stage, status) VALUES ('{cp_id}', '{ev_id}', '{json.dumps(json_notice_compiled_release_ev)}',"
            f"{ev_id[32:45]},{ev_id[32:45]}, '{ev_id + '-' + ev_id[32:45]}','EV', 'active');").one()
        record = f"{instance_tender_url}{cp_id}"
        ms_release = f"{instance_tender_url}{cp_id}/{cp_id}"
        pn_release = f"{instance_tender_url}{cp_id}/{pn_id}"
        ev_release = f"{instance_tender_url}{cp_id}/{ev_id}"
        return cp_id, pn_id, pn_token, ev_id, record, ms_release, pn_release, ev_release

    @allure.step('Insert CnOnPn: based on FS: treasury - obligatory, based on EI: without items - obligatory')
    def insert_cnonpn_obligatory(self, first_lot_id, second_lot_id, first_item_id, second_item_id,
                                 second_tender, second_enquiry):
        auth_provider = PlainTextAuthProvider(username=self.cassandra_username, password=self.cassandra_password)
        cluster = Cluster([self.cassandra_cluster], auth_provider=auth_provider)
        key_space_ocds = cluster.connect('ocds')
        key_space_access = cluster.connect('access')
        key_space_clarification = cluster.connect('clarification')
        key_space_submission = cluster.connect('submission')
        owner = "445f6851-c908-407d-9b45-14b92f3e964b"
        ei_id = prepared_cp_id()
        fs_id = prepared_fs_oc_id(ei_id)
        cp_id = prepared_cp_id()
        pn_id = prepared_pn_oc_id(cp_id)
        pn_token = uuid4()
        ev_id = prepared_cn_oc_id(cp_id)
        period = get_period()
        contract_period = get_contract_period()
        enquiry_and_tender_period = create_enquiry_and_tender_period(
            second_enquiry=second_enquiry,
            second_tender=second_tender
        )

        operation_date = time_at_now()
        calculate_new_cpv_code = get_new_classification_id(
            self.first_item_cpv,
            self.second_item_cpv
        )
        get_value_by_new_cpv_code = get_value_from_classification_cpv_dictionary_xls(
            calculate_new_cpv_code,
            self.lang
        )
        get_value_by_first_item_cpv_code = get_value_from_classification_cpv_dictionary_xls(
            self.first_item_cpv,
            self.lang
        )
        get_value_by_second_item_cpv_code = get_value_from_classification_cpv_dictionary_xls(
            self.second_item_cpv,
            self.lang
        )
        get_value_by_first_item_cpvs_code = get_value_from_cpvs_dictionary_csv(
            self.first_item_additional_classifications,
            self.lang
        )
        get_value_by_second_item_cpvs_code = get_value_from_cpvs_dictionary_csv(
            self.second_item_additional_classifications,
            self.lang
        )
        get_value_by_first_item_unit_id = get_value_from_classification_unit_dictionary_csv(
            self.first_item_unit_id,
            self.lang
        )
        get_value_by_second_item_unit_id = get_value_from_classification_unit_dictionary_csv(
            self.second_item_unit_id,
            self.lang
        )

        mdm = MdmService(
            instance=self.instance
        )
        data_pn = mdm.process_tender_data(self.pmd).json()
        submission_method_details = data_pn["data"]["tender"]["submissionMethodDetails"]
        submission_method_rationale = data_pn["data"]["tender"]["submissionMethodRationale"]

        procurement_method_details_from_mdm = data_pn["data"]["tender"]["procurementMethodDetails"]
        eligibility_criteria_from_mdm = data_pn["data"]["tender"]["eligibilityCriteria"]
        instance_tender_url = None
        instance_budget_url = None
        instance_storage_url = None
        if self.instance == "dev":
            instance_tender_url = "http://dev.public.eprocurement.systems/tenders/"
            instance_budget_url = "http://dev.public.eprocurement.systems/budgets/"
            instance_storage_url = "https://dev.bpe.eprocurement.systems/api/v1/storage/get/"
        if self.instance == "sandbox":
            instance_tender_url = "http://public.eprocurement.systems/tenders/"
            instance_budget_url = "http://public.eprocurement.systems/budgets/"
            instance_storage_url = "http://storage.eprocurement.systems/get/"
        json_orchestrator_context = {
            "operationId": f"{uuid4()}",
            "requestId": f"{uuid1()}",
            "cpid": cp_id,
            "ocid": ev_id,
            "ocidCn": ev_id,
            "stage": "EV",
            "prevStage": "PN",
            "processType": "updateCN",
            "operationType": "createCNonPN",
            "phase": "clarification",
            "owner": owner,
            "country": self.country,
            "language": self.lang,
            "pmd": self.pmd,
            "token": f"{pn_token}",
            "startDate": period[0],
            "timeStamp": period[2],
            "isAuction": False
        }

        json_access_tender = {
            "ocid": cp_id,
            "planning": {
                "budget": {
                    "amount": {
                        "amount": 2000.00,
                        "currency": "EUR"
                    },
                    "isEuropeanUnionFunded": False,
                    "budgetBreakdown": [{
                        "id": fs_id,
                        "amount": {
                            "amount": 2000.00,
                            "currency": "EUR"
                        },
                        "period": {
                            "startDate": period[0],
                            "endDate": period[1]
                        },
                        "sourceParty": {
                            "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                            "name": self.buyer_name,
                        }
                    }]
                }
            },
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "status": "active",
                "statusDetails": "clarification",
                "title": "create Pn: tender.title",
                "description": "create Pn: tender.description",
                "classification": {
                    "scheme": "CPV",
                    "id": get_value_by_new_cpv_code[0],
                    "description": get_value_by_new_cpv_code[1]
                },
                "tenderPeriod": {
                    "startDate": enquiry_and_tender_period[2],
                    "endDate": enquiry_and_tender_period[3]
                },
                "enquiryPeriod": {
                    "startDate": enquiry_and_tender_period[0],
                    "endDate": enquiry_and_tender_period[1]
                },
                "acceleratedProcedure": {
                    "isAcceleratedProcedure": False
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
                "procedureOutsourcing": {
                    "procedureOutsourced": False
                },
                "framework": {
                    "isAFramework": False
                },
                "dynamicPurchasingSystem": {
                    "hasDynamicPurchasingSystem": False
                },
                "legalBasis": "DIRECTIVE_2014_25_EU",
                "procurementMethod": "open",
                "procurementMethodDetails": procurement_method_details_from_mdm,
                "mainProcurementCategory": "works",
                "eligibilityCriteria": eligibility_criteria_from_mdm,
                "contractPeriod": {
                    "startDate": contract_period[0],
                    "endDate": contract_period[1]
                },
                "procuringEntity": {
                    "id": "MD-IDNO-4",
                    "name": "create Pn: tender.procuringEntity.name",
                    "identifier": {
                        "scheme": "MD-IDNO",
                        "id": "4",
                        "legalName": "create Pn: tender.procuringEntity.identifier.legalName"
                    },
                    "address": {
                        "streetAddress": "create Pn: tender.procuringEntity.address.streetAddress",
                        "addressDetails": {
                            "country": {
                                "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "country"]['scheme'],
                                "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "country"]['id'],
                                "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                    "addressDetails"]["country"]['description'],
                                "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "country"]['uri']
                            },
                            "region": {
                                "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "region"]['scheme'],
                                "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "region"]['id'],
                                "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                    "addressDetails"]["region"]['description'],
                                "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "region"]['uri']
                            },
                            "locality": {
                                "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "locality"]['scheme'],
                                "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "locality"]['id'],
                                "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                    "addressDetails"]["locality"]['description'],
                                "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "locality"]['uri']

                            }
                        }
                    },
                    "contactPoint": {
                        "name": "create Pn: tender.procuringEntity.contactPoint.name",
                        "email": "create Pn: tender.procuringEntity.contactPoint.email",
                        "telephone": "create Pn: tender.procuringEntity.contactPoint.telephone"
                    }
                },
                "value": {
                    "amount": 1650.00,
                    "currency": "EUR"
                },
                "lotGroups": [{
                    "optionToCombine": False
                }],
                "lots": [{
                    "id": first_lot_id,
                    "title": "create Pn: tender.lots[0].title",
                    "description": "create Pn: tender.lots[0].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 1500.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[0].placeOfPerformance.address.streetAddress",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        }
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }, {
                    "id": second_lot_id,
                    "title": "create Pn: tender.lots[1].title",
                    "description": "create Pn: tender.lots[1].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 150.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[1].placeOfPerformance.address.streetAddress",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        }
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }],
                "items": [{
                    "id": first_item_id,
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_first_item_cpv_code[0],
                        "description": get_value_by_first_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_first_item_cpvs_code[0],
                        "description": get_value_by_first_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_first_item_unit_id[0],
                        "name": get_value_by_first_item_unit_id[1]
                    },
                    "description": "create Pn: tender.items[0].description",
                    "relatedLot": first_lot_id
                }, {
                    "id": second_item_id,
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_second_item_cpv_code[0],
                        "description": get_value_by_second_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_second_item_cpvs_code[0],
                        "description": get_value_by_second_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_second_item_unit_id[0],
                        "name": get_value_by_second_item_unit_id[1]
                    },
                    "description": "create Pn: tender.items[1].description",
                    "relatedLot": second_lot_id
                }],
                "awardCriteria": "ratedCriteria",
                "awardCriteriaDetails": "automated",
                "requiresElectronicCatalogue": False,
                "submissionMethod": ["electronicSubmission"],
                "submissionMethodRationale": submission_method_rationale,
                "submissionMethodDetails": submission_method_details,
                "documents": [
                    {
                        "id": self.document_three_was_uploaded,
                        "documentType": "evaluationCriteria",
                        "title": "create CNonPN: tender.documents[2].title"
                    }
                ]
            }
        }

        json_notice_release_ms = {
            "ocid": cp_id,
            "id": f"{cp_id}-{ev_id[32:45]}",
            "date": f"{get_human_date_in_utc_format(int(ev_id[32:45]))[0]}",
            "tag": ["compiled"],
            "language": self.lang,
            "initiationType": "tender",
            "planning": {
                "budget": {
                    "amount": {
                        "amount": 2000.00,
                        "currency": "EUR"
                    },
                    "isEuropeanUnionFunded": False,
                    "budgetBreakdown": [{
                        "id": fs_id,
                        "amount": {
                            "amount": 2000.00,
                            "currency": "EUR"
                        },
                        "period": {
                            "startDate": period[0],
                            "endDate": period[1]
                        },
                        "sourceParty": {
                            "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                            "name": self.buyer_name,
                        }
                    }]
                }
            },
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "title": "create Pn: tender.title",
                "description": "create Pn: tender.description",
                "status": "active",
                "statusDetails": "evaluation",
                "value": {
                    "amount": 1650.00,
                    "currency": "EUR"
                },
                "procurementMethod": "open",
                "procurementMethodDetails": procurement_method_details_from_mdm,
                "mainProcurementCategory": "works",
                "hasEnquiries": False,
                "eligibilityCriteria": eligibility_criteria_from_mdm,
                "contractPeriod": {
                    "startDate": contract_period[0],
                    "endDate": contract_period[1]
                },
                "procuringEntity": {
                    "id": "MD-IDNO-4",
                    "name": "create Pn: tender.procuringEntity.name"
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
                "legalBasis": "DIRECTIVE_2014_25_EU",
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
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name,
                "identifier": {
                    "scheme": self.buyer_identifier_scheme,
                    "id": self.buyer_identifier_id,
                    "legalName": self.buyer_identifier_legal_name
                },
                "address": {
                    "streetAddress": self.buyer_address_street_address,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.buyer_address_address_details_country_id,
                            "description": "Moldova, Republica",
                            "uri": "https://www.iso.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": self.buyer_address_address_details_region_id,
                            "description": "Cahul",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": self.buyer_address_address_details_locality_scheme,
                            "id": self.buyer_address_address_details_locality_id,
                            "description": self.buyer_address_address_details_locality_description,
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "contactPoint": {
                    "name": self.buyer_contact_point_name,
                    "email": self.buyer_contact_point_email,
                    "telephone": self.buyer_contact_point_telephone
                },
                "roles": [
                    "buyer"]
            }, {
                "id": f"{self.payer_identifier_scheme}-{self.payer_identifier_id}",
                "name": self.payer_name,
                "identifier": {
                    "scheme": self.payer_identifier_scheme,
                    "id": self.payer_identifier_id,
                    "legalName": self.payer_identifier_legal_name
                },
                "address": {
                    "streetAddress": self.payer_address_street,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.payer_address_address_details_country_id,
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": self.payer_address_address_details_region_id,
                            "description": "Cahul",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": self.payer_address_address_details_locality_scheme,
                            "id": self.payer_address_address_details_locality_id,
                            "description": self.payer_address_address_details_locality_description,
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "contactPoint": {
                    "name": self.payer_contact_point_name,
                    "email": self.payer_contact_point_email,
                    "telephone": self.payer_contact_point_telephone
                },
                "roles": ["payer"]
            }, {
                "id": "MD-IDNO-4",
                "name": "create Pn: tender.procuringEntity.name",
                "identifier": {
                    "scheme": "MD-IDNO",
                    "id": "4",
                    "legalName": "create Pn: tender.procuringEntity.identigfier.legalName"
                },
                "address": {
                    "streetAddress": "create Pn: tender.procuringEntity.address.streetAddress",
                    "addressDetails": {
                        "country": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["country"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['uri']
                        },
                        "region": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["region"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['uri']
                        },
                        "locality": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["locality"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['uri']

                        }
                    }
                },
                "contactPoint": {
                    "name": "create Pn: tender.procuringEntity.contactPoint.name",
                    "email": "create Pn: tender.procuringEntity.contactPoint.email",
                    "telephone": "create Pn: tender.procuringEntity.contactPoint.telephone"
                },
                "roles": ["procuringEntity"]
            }],
            "relatedProcesses": [{
                "id": "36b553f0-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["planning"],
                "scheme": "ocid",
                "identifier": pn_id,
                "uri": f"{instance_tender_url}{cp_id}/{pn_id}"
            }, {
                "id": "36b553f1-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["x_expenditureItem"],
                "scheme": "ocid",
                "identifier": ei_id,
                "uri": f"{instance_budget_url}{ei_id}/{ei_id}"
            }, {
                "id": "36b553f2-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["x_fundingSource"],
                "scheme": "ocid",
                "identifier": fs_id,
                "uri": f"{instance_budget_url}{ei_id}/{fs_id}"
            },
                {
                    "id": "164cf530-ceca-11eb-8aed-69d06bed4d57",
                    "relationship": ["x_evaluation"],
                    "scheme": "ocid",
                    "identifier": ev_id,
                    "uri": f"{instance_tender_url}{cp_id}/{ev_id}"
                }
            ]
        }
        json_notice_release_pn = {
            "ocid": pn_id,
            "id": f"{pn_id}-{ev_id[32:45]}",
            "date": f"{get_human_date_in_utc_format(int(ev_id[32:45]))[0]}",
            "tag": ["planningUpdate"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "title": "Planning Notice",
                "description": "Contracting process is planned",
                "status": "complete",
                "statusDetails": "empty",
                "lotGroups": [{
                    "optionToCombine": False
                }],
                "tenderPeriod": {
                    "startDate": period[3]
                },
                "hasEnquiries": False,
                "submissionMethod": ["electronicSubmission"],
                "submissionMethodDetails": submission_method_details,
                "submissionMethodRationale": submission_method_rationale,
                "requiresElectronicCatalogue": False,
                "procurementMethodRationale": "create Pn: tender.procurementMethodRationale",
                "classification": {
                    "scheme": "CPV",
                    "id": get_value_by_new_cpv_code[0],
                    "description": get_value_by_new_cpv_code[1]
                },
                "value": {
                    "amount": 1650.00,
                    "currency": "EUR"
                }
            },
            "hasPreviousNotice": False,
            "purposeOfNotice": {
                "isACallForCompetition": False
            },
            "relatedProcesses": [{
                "id": "36b553f3-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": cp_id,
                "uri": f"{instance_tender_url}{cp_id}/{cp_id}"
            }]
        }
        json_notice_release_ev = {
            "ocid": ev_id,
            "id": f"{ev_id}-{ev_id[32:45]}",
            "date": f"{get_human_date_in_utc_format(int(ev_id[32:45]))[0]}",
            "tag": ["tender"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "c36f9952-06d5-41ef-9fe6-36722f1da414",
                "title": "Planning Notice",
                "description": "Contracting process is planned",
                "status": "active",
                "statusDetails": "clarification",
                "items": [{
                    "id": first_item_id,
                    "description": "create Pn: tender.items[0].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_first_item_cpv_code[0],
                        "description": get_value_by_first_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_first_item_cpvs_code[0],
                        "description": get_value_by_first_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "name": get_value_by_first_item_unit_id[1],
                        "id": get_value_by_first_item_unit_id[0]
                    },
                    "relatedLot": first_lot_id
                }, {
                    "id": second_item_id,
                    "description": "create Pn: tender.items[1].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_second_item_cpv_code[0],
                        "description": get_value_by_second_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_second_item_cpvs_code[0],
                        "description": get_value_by_second_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_second_item_unit_id[0],
                        "name": get_value_by_second_item_unit_id[1]
                    },
                    "relatedLot": second_lot_id
                }],
                "lots": [{
                    "id": first_lot_id,
                    "title": "create Pn: tender.lots[0].title",
                    "description": "create Pn: tender.lots[0].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 1500.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[0].placeOfPerformance.address.streetAddress",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        }
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }, {
                    "id": second_lot_id,
                    "title": "create Pn: tender.lots[1].title",
                    "description": "create Pn: tender.lots[1].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 150.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[1].placeOfPerformance.address.streetAddress",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        }
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }],
                "lotGroups": [{
                    "optionToCombine": False
                }],
                "tenderPeriod": {
                    "startDate": enquiry_and_tender_period[2],
                    "endDate": enquiry_and_tender_period[3]
                },
                "enquiryPeriod": {
                    "startDate": enquiry_and_tender_period[0],
                    "endDate": enquiry_and_tender_period[1]
                },
                "hasEnquiries": False,
                "documents": [{
                    "id": self.document_three_was_uploaded,
                    "documentType": "illustration",
                    "title": "create CNonPN: tender.documents[2].title",
                    "url": f"{instance_storage_url}"
                           f"{self.document_three_was_uploaded}",
                    "datePublished": operation_date
                }],
                "awardCriteria": "ratedCriteria",
                "awardCriteriaDetails": "automated",
                "submissionMethod": ["electronicSubmission"],
                "submissionMethodDetails": submission_method_details,
                "submissionMethodRationale": submission_method_rationale,
                "requiresElectronicCatalogue": False
            },
            "hasPreviousNotice": True,
            "purposeOfNotice": {
                "isACallForCompetition": True
            },
            "relatedProcesses": [{
                "id": "12a3ea63-ceca-11eb-8aed-69d06bed4d57",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": cp_id,
                "uri": f"{instance_tender_url}{cp_id}/{cp_id}"
            }, {
                "id": "164cf531-ceca-11eb-8aed-69d06bed4d57",
                "relationship": ["planning"],
                "scheme": "ocid",
                "identifier": pn_id,
                "uri": f"{instance_tender_url}{cp_id}/{pn_id}"
            }]
        }
        json_notice_compiled_release_ms = {
            "ocid": cp_id,
            "id": f"{cp_id}-{ev_id[32:45]}",
            "date": f"{get_human_date_in_utc_format(int(ev_id[32:45]))[0]}",
            "tag": ["compiled"],
            "language": self.lang,
            "initiationType": "tender",
            "planning": {
                "budget": {
                    "amount": {
                        "amount": 2000.00,
                        "currency": "EUR"
                    },
                    "isEuropeanUnionFunded": False,
                    "budgetBreakdown": [{
                        "id": fs_id,
                        "amount": {
                            "amount": 2000.00,
                            "currency": "EUR"
                        },
                        "period": {
                            "startDate": period[0],
                            "endDate": period[1]
                        },
                        "sourceParty": {
                            "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                            "name": self.buyer_name,
                        }
                    }]
                }
            },
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "title": "create Pn: tender.title",
                "description": "create Pn: tender.description",
                "status": "active",
                "statusDetails": "evaluation",
                "value": {
                    "amount": 1650.00,
                    "currency": "EUR"
                },
                "procurementMethod": "open",
                "procurementMethodDetails": procurement_method_details_from_mdm,
                "mainProcurementCategory": "works",
                "hasEnquiries": False,
                "eligibilityCriteria": eligibility_criteria_from_mdm,
                "contractPeriod": {
                    "startDate": contract_period[0],
                    "endDate": contract_period[1]
                },
                "procuringEntity": {
                    "id": "MD-IDNO-4",
                    "name": "create Pn: tender.procuringEntity.name"
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
                "legalBasis": "DIRECTIVE_2014_25_EU",
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
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name,
                "identifier": {
                    "scheme": self.buyer_identifier_scheme,
                    "id": self.buyer_identifier_id,
                    "legalName": self.buyer_identifier_legal_name
                },
                "address": {
                    "streetAddress": self.buyer_address_street_address,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.buyer_address_address_details_country_id,
                            "description": "Moldova, Republica",
                            "uri": "https://www.iso.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": self.buyer_address_address_details_region_id,
                            "description": "mun.Chişinău",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": self.buyer_address_address_details_locality_scheme,
                            "id": self.buyer_address_address_details_locality_id,
                            "description": self.buyer_address_address_details_locality_description,
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "contactPoint": {
                    "name": self.buyer_contact_point_name,
                    "email": self.buyer_contact_point_email,
                    "telephone": self.buyer_contact_point_telephone
                },
                "roles": ["buyer"]
            }, {
                "id": f"{self.payer_identifier_scheme}-{self.payer_identifier_id}",
                "name": self.payer_name,
                "identifier": {
                    "scheme": self.payer_identifier_scheme,
                    "id": self.payer_identifier_id,
                    "legalName": self.payer_identifier_legal_name
                },
                "address": {
                    "streetAddress": self.payer_address_street,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.payer_address_postal_code,
                            "description": "Moldova, Republica",
                            "uri": "https://www.iso.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": self.payer_address_address_details_region_id,
                            "description": "Donduşeni",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": self.payer_address_address_details_locality_scheme,
                            "id": self.payer_address_address_details_locality_id,
                            "description": self.payer_address_address_details_locality_description,
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "contactPoint": {
                    "name": self.payer_contact_point_name,
                    "email": self.payer_contact_point_email,
                    "telephone": self.payer_contact_point_telephone
                },
                "roles": ["payer"]
            }, {
                "id": "MD-IDNO-4",
                "name": "create Pn: tender.procuringEntity.name",
                "identifier": {
                    "scheme": "MD-IDNO",
                    "id": "4",
                    "legalName": "create Pn: tender.procuringEntity.identigfier.legalName"
                },
                "address": {
                    "streetAddress": "street address",
                    "addressDetails": {
                        "country": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["country"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['uri']
                        },
                        "region": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["region"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['uri']
                        },
                        "locality": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["locality"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['uri']
                        }
                    }
                },
                "contactPoint": {
                    "name": "name",
                    "email": "email",
                    "telephone": "456-95-96"
                },
                "roles": ["procuringEntity"]
            }],
            "relatedProcesses": [{
                "id": "36b553f0-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["planning"],
                "scheme": "ocid",
                "identifier": pn_id,
                "uri": f"{instance_tender_url}{cp_id}/{pn_id}"
            }, {
                "id": "36b553f1-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["x_expenditureItem"],
                "scheme": "ocid",
                "identifier": ei_id,
                "uri": f"{instance_budget_url}{ei_id}/{ei_id}"
            }, {
                "id": "36b553f2-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["x_fundingSource"],
                "scheme": "ocid",
                "identifier": fs_id,
                "uri": f"{instance_budget_url}{ei_id}/{fs_id}"
            },
                {
                    "id": "ed0f7290-cee4-11eb-8aed-69d06bed4d57",
                    "relationship": ["x_evaluation"],
                    "scheme": "ocid",
                    "identifier": ev_id,
                    "uri": f"{instance_tender_url}{cp_id}/{ev_id}"
                }
            ]

        }
        json_notice_compiled_release_pn = {
            "ocid": pn_id,
            "id": f"{pn_id}-{ev_id[32:45]}",
            "date": f"{get_human_date_in_utc_format(int(ev_id[32:45]))[0]}",
            "tag": ["planningUpdate"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "title": "Planning Notice",
                "description": "Contracting process is planned",
                "status": "complete",
                "statusDetails": "empty",
                "lotGroups": [{
                    "optionToCombine": False
                }],
                "tenderPeriod": {
                    "startDate": period[3]
                },
                "hasEnquiries": False,
                "submissionMethod": ["electronicSubmission"],
                "submissionMethodDetails": submission_method_details,
                "submissionMethodRationale": submission_method_rationale,
                "requiresElectronicCatalogue": False,
                "classification": {
                    "scheme": "CPV",
                    "id": get_value_by_new_cpv_code[0],
                    "description": get_value_by_new_cpv_code[1]
                },
                "value": {
                    "amount": 1650.00,
                    "currency": "EUR"
                }
            },
            "hasPreviousNotice": False,
            "purposeOfNotice": {
                "isACallForCompetition": False
            },
            "relatedProcesses": [{
                "id": "36b553f3-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": cp_id,
                "uri": f"{instance_tender_url}/{cp_id}/{cp_id}"
            }]
        }
        json_notice_compiled_release_ev = {
            "ocid": ev_id,
            "id": f"{ev_id}-{ev_id[32:45]}",
            "date": f"{get_human_date_in_utc_format(int(ev_id[32:45]))[0]}",
            "tag": ["tender"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "title": "Evaluation",
                "description": "Evaluation stage of contracting process",
                "status": "active",
                "statusDetails": "clarification",
                "items": [{
                    "id": first_item_id,
                    "description": "create Pn: tender.items[0].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_first_item_cpv_code[0],
                        "description": get_value_by_first_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_first_item_cpvs_code[0],
                        "description": get_value_by_first_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_first_item_unit_id[0],
                        "name": get_value_by_first_item_unit_id[1]
                    },
                    "relatedLot": first_lot_id
                }, {
                    "id": second_item_id,
                    "description": "create Pn: tender.items[1].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_second_item_cpv_code[0],
                        "description": get_value_by_second_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_second_item_cpvs_code[0],
                        "description": get_value_by_second_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_second_item_unit_id[0],
                        "name": get_value_by_second_item_unit_id[1]
                    },
                    "relatedLot": second_lot_id
                }],
                "lots": [{
                    "id": first_lot_id,
                    "title": "create Pn: tender.lots[0].title",
                    "description": "create Pn: tender.lots[0].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 1500.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[0].placeOfPerformance.address.streetAddress",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        }
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }, {
                    "id": second_lot_id,
                    "title": "create Pn: tender.lots[1].title",
                    "description": "create Pn: tender.lots[1].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 150.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[1].placeOfPerformance.address.streetAddress",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        }
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }],
                "lotGroups": [{
                    "optionToCombine": False
                }],
                "tenderPeriod": {
                    "startDate": enquiry_and_tender_period[2],
                    "endDate": enquiry_and_tender_period[3]
                },
                "enquiryPeriod": {
                    "startDate": enquiry_and_tender_period[0],
                    "endDate": enquiry_and_tender_period[1]
                },
                "hasEnquiries": False,
                "documents": [{
                    "id": self.document_three_was_uploaded,
                    "documentType": "illustration",
                    "title": "create CNonPN: tender.documents[2].title",
                    "url": f"{instance_storage_url}"
                           f"{self.document_three_was_uploaded}",
                    "datePublished": operation_date
                }],
                "awardCriteria": "ratedCriteria",
                "awardCriteriaDetails": "automated",
                "submissionMethod": ["electronicSubmission"],
                "submissionMethodDetails": submission_method_details,
                "submissionMethodRationale": submission_method_rationale,
                "requiresElectronicCatalogue": False
            },
            "hasPreviousNotice": True,
            "purposeOfNotice": {
                "isACallForCompetition": True
            },
            "relatedProcesses": [{
                "id": "e84a2253-cee4-11eb-8aed-69d06bed4d57",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": cp_id,
                "uri": f"{instance_tender_url}{cp_id}/{cp_id}"
            }, {
                "id": "ed0f7291-cee4-11eb-8aed-69d06bed4d57",
                "relationship": ["planning"],
                "scheme": "ocid",
                "identifier": pn_id,
                "uri": f"{instance_tender_url}{cp_id}/{pn_id}"
            }]
        }

        kafka = Kafka(instance=self.instance)
        kafka.connect_kafka_producer()
        kafka.publish_message_into_chronograph_in_clarification(
            cp_id=cp_id,
            ev_id=ev_id,
            enquiry_end=enquiry_and_tender_period[1]
        )
        kafka.publish_message_into_chronograph_in_submission(
            cp_id=cp_id,
            ev_id=ev_id,
            tender_end=enquiry_and_tender_period[3]
        )

        key_space_ocds.execute(f"INSERT INTO orchestrator_context (cp_id,context) VALUES ("
                               f"'{ev_id}','{json.dumps(json_orchestrator_context)}');").one()
        key_space_access.execute(f"INSERT INTO tenders (cpid, ocid, token_entity,created_date,json_data, owner) "
                                 f"VALUES ('{cp_id}', '{ev_id}', '{pn_token}', {ev_id[32:45]}, "
                                 f"'{json.dumps(json_access_tender)}','{owner}');").one()
        key_space_clarification.execute(
            f"INSERT INTO periods (cpid, ocid, end_date, owner, start_date) "
            f"VALUES ('{cp_id}', '{ev_id}', {get_timestamp_from_human_date(enquiry_and_tender_period[1])}, '{owner}', "
            f"{ev_id[32:45]});").one()
        key_space_submission.execute(
            f"INSERT INTO periods (cpid, ocid, end_date, start_date) "
            f"VALUES ('{cp_id}', '{ev_id}', {get_timestamp_from_human_date(enquiry_and_tender_period[3])}, "
            f"{get_timestamp_from_human_date(enquiry_and_tender_period[1])});").one()
        key_space_ocds.execute(f"INSERT INTO notice_offset (cp_id,release_date, stage, status) "
                               f"VALUES ('{cp_id}', {ev_id[32:45]}, 'EV', 'active');").one()
        key_space_ocds.execute(
            f"INSERT INTO notice_release (cp_id,oc_id, release_id, json_data, release_date, stage) "
            f"VALUES ('{cp_id}', '{cp_id}', '{cp_id + '-' + ev_id[32:45]}' ,'{json.dumps(json_notice_release_ms)}',"
            f"{ev_id[32:45]},'');").one()
        key_space_ocds.execute(
            f"INSERT INTO notice_release (cp_id,oc_id, release_id, json_data, release_date, stage) "
            f"VALUES ('{cp_id}', '{pn_id}', '{pn_id + '-' + ev_id[32:45]}' ,'{json.dumps(json_notice_release_pn)}',"
            f"{ev_id[32:45]},'PN');").one()
        key_space_ocds.execute(
            f"INSERT INTO notice_release (cp_id,oc_id, release_id, json_data, release_date, stage) "
            f"VALUES ('{cp_id}', '{ev_id}', '{ev_id + '-' + ev_id[32:45]}','{json.dumps(json_notice_release_ev)}',"
            f"{ev_id[32:45]},'EV');").one()
        key_space_ocds.execute(
            f"INSERT INTO notice_compiled_release (cp_id,oc_id, json_data, publish_date, release_date, "
            f"release_id, stage, status) VALUES ('{cp_id}', '{cp_id}', '{json.dumps(json_notice_compiled_release_ms)}',"
            f"{ev_id[32:45]},{ev_id[32:45]}, '{cp_id + '-' + ev_id[32:45]}','', 'active');").one()
        key_space_ocds.execute(
            f"INSERT INTO notice_compiled_release (cp_id,oc_id, json_data, publish_date, release_date, "
            f"release_id, stage, status) VALUES ('{cp_id}', '{pn_id}', '{json.dumps(json_notice_compiled_release_pn)}',"
            f"{ev_id[32:45]},{ev_id[32:45]}, '{pn_id + '-' + ev_id[32:45]}','PN', 'active');").one()
        key_space_ocds.execute(
            f"INSERT INTO notice_compiled_release (cp_id,oc_id, json_data, publish_date, release_date, "
            f"release_id, stage, status) VALUES ('{cp_id}', '{ev_id}', '{json.dumps(json_notice_compiled_release_ev)}',"
            f"{ev_id[32:45]},{ev_id[32:45]}, '{ev_id + '-' + ev_id[32:45]}','EV', 'active');").one()
        record = f"{instance_tender_url}{cp_id}"
        ms_release = f"{instance_tender_url}{cp_id}/{cp_id}"
        pn_release = f"{instance_tender_url}{cp_id}/{pn_id}"
        ev_release = f"{instance_tender_url}{cp_id}/{ev_id}"
        return cp_id, pn_id, pn_token, ev_id, record, ms_release, pn_release, ev_release

    @allure.step('Insert CnOnPn: based on FS: own - full, based on EI: with items - full')
    def insert_cancel_lot_full(self, first_lot_id, second_lot_id, first_item_id, second_item_id,
                               second_tender, second_enquiry, lot_id):
        auth_provider = PlainTextAuthProvider(username=self.cassandra_username, password=self.cassandra_password)
        cluster = Cluster([self.cassandra_cluster], auth_provider=auth_provider)
        key_space_ocds = cluster.connect('ocds')
        key_space_access = cluster.connect('access')
        key_space_clarification = cluster.connect('clarification')
        key_space_submission = cluster.connect('submission')
        key_space_auctions = cluster.connect('auctions')
        key_space_revision = cluster.connect('revision')
        owner = "445f6851-c908-407d-9b45-14b92f3e964b"
        ei_id = prepared_cp_id()
        fs_id = prepared_fs_oc_id(ei_id)
        cp_id = prepared_cp_id()
        pn_id = prepared_pn_oc_id(cp_id)
        pn_token = uuid4()
        ev_id = prepared_cn_oc_id(cp_id)
        period = get_period()
        period_for_amendment = get_period_for_amendment()
        auction_date = get_auction_date()
        contract_period = get_contract_period()
        enquiry_and_tender_period = create_enquiry_and_tender_period(
            second_enquiry=second_enquiry,
            second_tender=second_tender
        )

        operation_date = time_at_now()
        calculate_new_cpv_code = get_new_classification_id(
            self.first_item_cpv,
            self.second_item_cpv
        )
        get_value_by_new_cpv_code = get_value_from_classification_cpv_dictionary_xls(
            calculate_new_cpv_code,
            self.lang
        )
        get_value_by_first_item_cpv_code = get_value_from_classification_cpv_dictionary_xls(
            self.first_item_cpv,
            self.lang
        )
        get_value_by_second_item_cpv_code = get_value_from_classification_cpv_dictionary_xls(
            self.second_item_cpv,
            self.lang
        )
        get_value_by_first_item_cpvs_code = get_value_from_cpvs_dictionary_csv(
            self.first_item_additional_classifications,
            self.lang
        )
        get_value_by_second_item_cpvs_code = get_value_from_cpvs_dictionary_csv(
            self.second_item_additional_classifications,
            self.lang
        )
        get_value_by_first_item_unit_id = get_value_from_classification_unit_dictionary_csv(
            self.first_item_unit_id,
            self.lang
        )
        get_value_by_second_item_unit_id = get_value_from_classification_unit_dictionary_csv(
            self.second_item_unit_id,
            self.lang
        )

        mdm = MdmService(
            instance=self.instance
        )
        data_pn = mdm.process_tender_data(self.pmd).json()
        submission_method_details = data_pn["data"]["tender"]["submissionMethodDetails"]
        submission_method_rationale = data_pn["data"]["tender"]["submissionMethodRationale"]

        procurement_method_details_from_mdm = data_pn["data"]["tender"]["procurementMethodDetails"]
        eligibility_criteria_from_mdm = data_pn["data"]["tender"]["eligibilityCriteria"]
        instance_tender_url = None
        instance_budget_url = None
        instance_storage_url = None
        if self.instance == "dev":
            instance_tender_url = "http://dev.public.eprocurement.systems/tenders/"
            instance_budget_url = "http://dev.public.eprocurement.systems/budgets/"
            instance_storage_url = "https://dev.bpe.eprocurement.systems/api/v1/storage/get/"
        if self.instance == "sandbox":
            instance_tender_url = "http://public.eprocurement.systems/tenders/"
            instance_budget_url = "http://public.eprocurement.systems/budgets/"
            instance_storage_url = "http://storage.eprocurement.systems/get/"
        json_orchestrator_context = {
            "cpid": cp_id,
            "ocid": ev_id,
            "operationId": f"{uuid4()}",
            "requestId": f"{uuid4()}",
            "owner": owner,
            "stage": "EV",
            "prevStage": "EV",
            "phase": "clarification",
            "processType": "cancelLot",
            "operationType": "lotCancellation",
            "country": self.country,
            "language": self.lang,
            "pmd": self.pmd,
            "startDate": period_for_amendment[0],
            "timeStamp": period_for_amendment[1],
            "isAuction": True
        }

        json_access_tender = {
            "ocid": cp_id,
            "planning": {
                "rationale": "create Pn: planning.rationale",
                "budget": {
                    "description": "create Pn: planning.budget.description",
                    "amount": {
                        "amount": 2000.00,
                        "currency": "EUR"
                    },
                    "isEuropeanUnionFunded": True,
                    "budgetBreakdown": [{
                        "id": fs_id,
                        "description": "create Fs: planning.budget.description",
                        "amount": {
                            "amount": 2000.00,
                            "currency": "EUR"
                        },
                        "period": {
                            "startDate": period[0],
                            "endDate": period[1]
                        },
                        "sourceParty": {
                            "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                            "name": self.funder_name,
                        },
                        "europeanUnionFunding": {
                            "projectIdentifier": "create Fs: planning.budget.europeanUnionFunding.projectIdentifier",
                            "projectName": "create Fs: planning.budget.europeanUnionFunding.projectName",
                            "uri": "create Fs: planning.budget.europeanUnionFunding.uri"
                        }
                    }]
                }
            },
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "status": "active",
                "statusDetails": "clarification",
                "title": "create Pn: tender.title",
                "description": "create Pn: tender.description",
                "classification": {
                    "scheme": "CPV",
                    "id": get_value_by_new_cpv_code[0],
                    "description": get_value_by_new_cpv_code[1]
                },
                "tenderPeriod": {
                    "startDate": enquiry_and_tender_period[2],
                    "endDate": enquiry_and_tender_period[3]
                },
                "enquiryPeriod": {
                    "startDate": enquiry_and_tender_period[0],
                    "endDate": enquiry_and_tender_period[1]
                },
                "acceleratedProcedure": {
                    "isAcceleratedProcedure": False
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
                "procedureOutsourcing": {
                    "procedureOutsourced": False
                },
                "framework": {
                    "isAFramework": False
                },
                "dynamicPurchasingSystem": {
                    "hasDynamicPurchasingSystem": False
                },
                "legalBasis": "DIRECTIVE_2014_25_EU",
                "procurementMethod": "open",
                "procurementMethodDetails": procurement_method_details_from_mdm,
                "procurementMethodRationale": "create CNonPN: tender.procurementMethodRationale",
                "procurementMethodAdditionalInfo": "create CNonPN: tender.procurementMethodAdditionalInfo",
                "mainProcurementCategory": "works",
                "eligibilityCriteria": eligibility_criteria_from_mdm,
                "contractPeriod": {
                    "startDate": contract_period[0],
                    "endDate": contract_period[1]
                },
                "procurementMethodModalities": ["electronicAuction"],
                "electronicAuctions": {
                    "details": [{
                        "id": "503d6861-62d9-47f3-8939-4e4729df0cde",
                        "relatedLot": first_lot_id,
                        "electronicAuctionModalities": [{
                            "eligibleMinimumDifference": {
                                "amount": 100.00,
                                "currency": "EUR"
                            }
                        }]
                    }, {
                        "id": "f1a36bc8-ee22-4660-8a76-5b1671d34b0d",
                        "relatedLot": second_lot_id,
                        "electronicAuctionModalities": [{
                            "eligibleMinimumDifference": {
                                "amount": 10.00,
                                "currency": "EUR"
                            }
                        }]
                    }]
                },
                "procuringEntity": {
                    "id": "MD-IDNO-4",
                    "name": "create Pn: tender.procuringEntity.name",
                    "identifier": {
                        "scheme": "MD-IDNO",
                        "id": "4",
                        "legalName": "create Pn: tender.procuringEntity.identifier.legalName",
                        "uri": "create Pn: tender.procuringEntity.identifier.uri"
                    },
                    "additionalIdentifiers": [{
                        "scheme": "create Pn: tender.procuringEntity.additionalIdentifiers[0].scheme",
                        "id": "create Pn: tender.procuringEntity.additionalIdentifiers[0].id",
                        "legalName": "create Pn: tender.procuringEntity.additionalIdentifiers[0].legalName",
                        "uri": "create Pn: tender.procuringEntity.additionalIdentifiers[0].uri"
                    }],
                    "address": {
                        "streetAddress": "create Pn: tender.procuringEntity.address.streetAddress",
                        "postalCode": "create Pn: tender.procuringEntity.address.postalCode",
                        "addressDetails": {
                            "country": {
                                "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "country"]['scheme'],
                                "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "country"]['id'],
                                "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                    "addressDetails"]["country"]['description'],
                                "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "country"]['uri']
                            },
                            "region": {
                                "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "region"]['scheme'],
                                "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "region"]['id'],
                                "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                    "addressDetails"]["region"]['description'],
                                "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "region"]['uri']
                            },
                            "locality": {
                                "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "locality"]['scheme'],
                                "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "locality"]['id'],
                                "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                    "addressDetails"]["locality"]['description'],
                                "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "locality"]['uri']

                            }
                        }
                    },
                    "contactPoint": {
                        "name": "create Pn: tender.procuringEntity.contactPoint.name",
                        "email": "create Pn: tender.procuringEntity.contactPoint.email",
                        "telephone": "create Pn: tender.procuringEntity.contactPoint.telephone",
                        "faxNumber": "create Pn: tender.procuringEntity.contactPoint.faxNumber",
                        "url": "create Pn: tender.procuringEntity.contactPoint.url"
                    },
                    "persones": [{
                        "id": "create CNonPN: procuringEntity.persones[0].identifier.id",
                        "title": "create CNonPN: procuringEntity.persones[0].title",
                        "name": "create CNonPN: procuringEntity.persones[0].name",
                        "identifier": {
                            "scheme": "MD-IDNO",
                            "id": "create CNonPN: procuringEntity.persones[0].identifier.id",
                            "uri": "create CNonPN: procuringEntity.persones[0].identifier.uri"
                        },
                        "businessFunctions": [{
                            "id": "create CNonPN: procuringEntity.persones[0].businessFunctions[0].id",
                            "type": "contactPoint",
                            "jobTitle": "create CNonPN: procuringEntity.persones[0].businessFunctions[0].jobTitle",
                            "period": {
                                "startDate": period[0]
                            },
                            "documents": [{
                                "id": self.document_three_was_uploaded,
                                "documentType": "regulatoryDocument",
                                "title": "create CNonPN: procuringEntity.persones[0].businessFunctions[0].title",
                                "description": "create CNonPN: procuringEntity.persones[0].businessFunctions[0]."
                                               "description"
                            }]
                        }]
                    }]
                },
                "value": {
                    "amount": 1650.00,
                    "currency": "EUR"
                },
                "lotGroups": [{
                    "optionToCombine": False
                }],
                "criteria": [{
                    "id": "db6d8e23-5dce-4688-9b82-2e323994e709",
                    "title": "create CNonPN: tender.criteria[0].title =Bankruptcy",
                    "classification": {
                        "id": "CRITERION.EXCLUSION.CONVICTIONS.PARTICIPATION_IN_CRIMINAL_ORGANISATION",
                        "scheme": "ESPD"
                    },
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[0].description =Is the economic operator bankrupt? "
                                   "This information needs not be given if exclusion of economic operators in this "
                                   "case has been made mandatory under the applicable national law without any "
                                   "possibility of derogation where the economic operator is nevertheless able to "
                                   "perform the contract.",
                    "requirementGroups": [{
                        "id": "83af7655-a283-42ad-8151-ac2ff549e23e",
                        "description": "create CNonPN: tender.criteria[0].requirementGroups[0].description =approve "
                                       "that Bankruptcy requirement group",
                        "requirements": [{
                            "id": "86c15b70-0622-41e7-b333-457d14c770b6",
                            "title": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements.title",
                            "dataType": "boolean",
                            "description": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements."
                                           "description",
                            "status": "active",
                            "datePublished": operation_date,
                            "expectedValue": False,
                            "eligibleEvidences": [{
                                "id": "1",
                                "title": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements[0]."
                                         "eligibleEvidences[0].title",
                                "description": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements"
                                               "[0].eligibleEvidences[0].description",
                                "type": "document",
                                "relatedDocument": {
                                    "id": self.document_three_was_uploaded
                                }
                            }, {
                                "id": "2",
                                "title": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements[0]."
                                         "eligibleEvidences[1].title",
                                "description": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements"
                                               "[0].eligibleEvidences[1].description",
                                "type": "document",
                                "relatedDocument": {
                                    "id": self.document_three_was_uploaded
                                }
                            }]
                        }]
                    }],
                    "relatesTo": "tender"
                }, {
                    "id": "5ad0aa1e-ec8c-48d6-be0c-99fa777eaca9",
                    "title": "create CNonPN: tender.criteria[1].title",
                    "classification": {
                        "id": "CRITERION.SELECTION.ECONOMIC_FINANCIAL_STANDING.TURNOVER.GENERAL_YEARLY",
                        "scheme": "ESPD"
                    },
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[1].description",
                    "requirementGroups": [{
                        "id": "c3878528-b856-4a2d-92f9-6138dad28b51",
                        "description": "create CNonPN: tender.criteria[1].requirementGroups[0].description",
                        "requirements": [{
                            "id": "268877db-bfb9-45dc-9b0b-4a932f75c6ed",
                            "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[0].title",
                            "dataType": "boolean",
                            "description": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements."
                                           "description",
                            "status": "active",
                            "datePublished": operation_date,
                            "expectedValue": True
                        }, {
                            "id": "2aadefb6-869e-4695-9b2f-663c9a4acb37",
                            "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[1]."
                                     "title =The number of years for proposed product warranty",
                            "dataType": "number",
                            "description": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[1]."
                                           "description",
                            "status": "active",
                            "datePublished": operation_date,
                            "period": {
                                "startDate": period[0],
                                "endDate": period[1]
                            },
                            "minValue": 1.000,
                            "maxValue": 3.000,
                            "eligibleEvidences": [{
                                "id": "3",
                                "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[1]."
                                         "eligibleEvidences[0].title",
                                "description": "create CNonPN: tender.criteria[1].requirementGroups[0]."
                                               "requirements[1].eligibleEvidences[0].description",
                                "type": "document",
                                "relatedDocument": {
                                    "id": self.document_three_was_uploaded
                                }
                            }]
                        }]
                    }],
                    "relatesTo": "lot",
                    "relatedItem": first_lot_id
                }, {
                    "id": "1a600e32-354f-436c-bede-e3238ca1998d",
                    "title": "create CNonPN: tender.criteria[2].title",
                    "classification": {
                        "id": "CRITERION.EXCLUSION.NATIONAL.OTHER",
                        "scheme": "ESPD"
                    },
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[2].description",
                    "requirementGroups": [{
                        "id": "a2fa62cc-4ec3-4944-a091-bd158cded7ab",
                        "description": "create CNonPN: tender.criteria[2].requirementGroups[0].description",
                        "requirements": [{
                            "id": "5ac98f2b-9e55-4167-aa82-2d4baa1d01cb",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[0].requirements[0]."
                                     "title =Product has to be manufactured in the EU",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "expectedValue": True
                        }, {
                            "id": "5bfd430b-a663-4657-972f-788b8c7bffc5",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[0]..requirements[1]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }, {
                        "id": "eac18bd3-6c02-4245-a6e2-f839f80361ee",
                        "description": "create CNonPN: tender.criteria[2].requirementGroups[1].description",
                        "requirements": [{
                            "id": "6853dee4-1359-4522-87a6-ee50c00cb390",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[1].requirements[0]."
                                     "title =Product has to be manufactured in the EU",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "expectedValue": True
                        }, {
                            "id": "a470ea41-0825-44e2-89be-495d63a54f06",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[1]..requirements[1]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }],
                    "relatesTo": "tenderer"
                }, {
                    "id": "13e1682a-23bb-491d-ad6d-a9cbdba6ac80",
                    "title": "create CNonPN: tender.criteria[3].title",
                    "classification": {
                        "id": "CRITERION.OTHER.EO_DATA.RELIES_ON_OTHER_CAPACITIES",
                        "scheme": "ESPD"
                    },
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[3].description =A minimum product warranty "
                                   "of 1 year is required for all bids 2",
                    "requirementGroups": [{
                        "id": "8378bc93-9c06-47ae-9982-0b091e326728",
                        "description": "create CNonPN: tender.criteria[3].requirementGroups[0].description",
                        "requirements": [{
                            "id": "e64eb9e1-47dd-488f-acbe-ff13b7e258d8",
                            "title": "create CNonPN: tender.criteria[3].requirementGroups[0].requirements[0]."
                                     "title = The number of years for proposed product warranty",
                            "dataType": "number",
                            "status": "active",
                            "datePublished": operation_date,
                            "period": {
                                "startDate": period[0],
                                "endDate": period[1]
                            },
                            "minValue": 1.000,
                            "maxValue": 3.000
                        }]
                    }],
                    "relatesTo": "item",
                    "relatedItem": first_item_id
                }, {
                    "id": "50d6061e-5913-4bc4-a18b-3ad3261a2c88",
                    "title": "create CNonPN: tender.criteria[4].title",
                    "classification": {
                        "id": "CRITERION.EXCLUSION.NATIONAL.OTHER",
                        "scheme": "ESPD"
                    },
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[4].description",
                    "requirementGroups": [{
                        "id": "da026d11-3769-43ce-ba83-f93832b18409",
                        "description": "create CNonPN: tender.criteria[4].requirementGroups[0].description",
                        "requirements": [{
                            "id": "794ece62-28a9-4843-8241-6955d7020cde",
                            "title": "create CNonPN: tender.criteria[4].requirementGroups[0].requirements[0]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }],
                    "relatesTo": "tender"
                }, {
                    "id": "55a02e2f-dc9c-43ad-ad47-af0932cf0b89",
                    "title": "create CNonPN: tender.criteria[4].title",
                    "classification": {
                        "id": "CRITERION.OTHER.EO_DATA.RELIES_ON_OTHER_CAPACITIES",
                        "scheme": "ESPD"
                    },
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[4].description",
                    "requirementGroups": [{
                        "id": "735a5c8b-6adf-4256-ac73-104470b7b189",
                        "description": "create CNonPN: tender.criteria[4].requirementGroups[0].description",
                        "requirements": [{
                            "id": "ba9194d1-37a6-45ac-896c-faacd250eb72",
                            "title": "create CNonPN: tender.criteria[4].requirementGroups[0].requirements[0]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }],
                    "relatesTo": "tender"
                }],
                "conversions": [{
                    "id": "9eab3068-bcce-4f8a-a829-0181830f0636",
                    "relatesTo": "requirement",
                    "relatedItem": "268877db-bfb9-45dc-9b0b-4a932f75c6ed",
                    "rationale": "create CNonPN: tender.conversions[1].rationale",
                    "description": "create CNonPN: tender.conversions[1].description",
                    "coefficients": [{
                        "id": "e896f9d4-3f61-4370-97d0-25fd6e26b27a",
                        "value": False,
                        "coefficient": 1
                    }]
                }, {
                    "id": "4937c4b4-a50d-48f8-8363-7b02c48a12d9",
                    "relatesTo": "requirement",
                    "relatedItem": "2aadefb6-869e-4695-9b2f-663c9a4acb37",
                    "rationale": "create CNonPN: tender.conversions[3].rationale",
                    "description": "create CNonPN: tender.conversions[3].description",
                    "coefficients": [{
                        "id": "f09bf118-92fd-4702-a5ac-2393e2234dbb",
                        "value": 1.000,
                        "coefficient": 1
                    }, {
                        "id": "9b69b215-e75a-4d5b-b51a-2046a7207562",
                        "value": 2.000,
                        "coefficient": 1
                    }, {
                        "id": "9c985738-1903-49df-829d-a574a5021d35",
                        "value": 3.000,
                        "coefficient": 0.93
                    }]
                }, {
                    "id": "678dcf2c-2e9f-4a72-8cb6-8ecf067fcf75",
                    "relatesTo": "requirement",
                    "relatedItem": "e64eb9e1-47dd-488f-acbe-ff13b7e258d8",
                    "rationale": "create CNonPN: tender.conversions[6].rationale",
                    "description": "create CNonPN: tender.conversions[6].description",
                    "coefficients": [{
                        "id": "f4ab1b51-21ee-46d2-8e78-2d65c30fa3e2",
                        "value": 1.000,
                        "coefficient": 1
                    }, {
                        "id": "c5eb8b92-a1b5-41a0-a7ed-267b2a79bc91",
                        "value": 2.000,
                        "coefficient": 1
                    }, {
                        "id": "ab5e3241-0afd-40b1-86ac-887366caef2b",
                        "value": 3.000,
                        "coefficient": 0.93
                    }]
                }, {
                    "id": "89ac8671-0640-41c9-ba4b-fdfcc7aa9131",
                    "relatesTo": "requirement",
                    "relatedItem": "ba9194d1-37a6-45ac-896c-faacd250eb72",
                    "rationale": "create CNonPN: tender.conversions[6].rationale",
                    "description": "create CNonPN: tender.conversions[6].description",
                    "coefficients": [{
                        "id": "0728cc52-3c85-4283-a1f6-b3ae94ca6eae",
                        "relatedOption": "option_1",
                        "value": "option_1",
                        "coefficient": 1
                    }, {
                        "id": "66e52e5a-49fd-420f-936a-0ef9aeafae21",
                        "relatedOption": "option_2",
                        "value": "option_2",
                        "coefficient": 1
                    }, {
                        "id": "6151abc7-56e1-424b-a0ee-f9bba4205abf",
                        "relatedOption": "option_3",
                        "value": "option_3",
                        "coefficient": 0.93
                    }]
                }],
                "lots": [{
                    "id": first_lot_id,
                    "internalId": "create Pn: tender.lots[0].internalId",
                    "title": "create Pn: tender.lots[0].title",
                    "description": "create Pn: tender.lots[0].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 1500.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[0].placeOfPerformance.address.streetAddress",
                            "postalCode": "create Pn: tender.lots[0].placeOfPerformance.address.postalCode",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        },
                        "description": "create Pn: tender.lots[0].placeOfPerformance.description"
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }, {
                    "id": second_lot_id,
                    "internalId": "create Pn: tender.lots[1].internalId",
                    "title": "create Pn: tender.lots[1].title",
                    "description": "create Pn: tender.lots[1].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 150.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[1].placeOfPerformance.address.streetAddress",
                            "postalCode": "create Pn: tender.lots[1].placeOfPerformance.address.postalCode",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        },
                        "description": "create Pn: tender.lots[1].placeOfPerformance.description"
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }],
                "items": [{
                    "id": first_item_id,
                    "internalId": "create Pn: tender.items[0].internalId",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_first_item_cpv_code[0],
                        "description": get_value_by_first_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_first_item_cpvs_code[0],
                        "description": get_value_by_first_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_first_item_unit_id[0],
                        "name": get_value_by_first_item_unit_id[1]
                    },
                    "description": "create Pn: tender.items[0].description",
                    "relatedLot": first_lot_id
                }, {
                    "id": second_item_id,
                    "internalId": "create Pn: tender.items[1].internalId",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_second_item_cpv_code[0],
                        "description": get_value_by_second_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_second_item_cpvs_code[0],
                        "description": get_value_by_second_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_second_item_unit_id[0],
                        "name": get_value_by_second_item_unit_id[1]
                    },
                    "description": "create Pn: tender.items[1].description",
                    "relatedLot": second_lot_id
                }],
                "awardCriteria": "ratedCriteria",
                "awardCriteriaDetails": "automated",
                "requiresElectronicCatalogue": False,
                "submissionMethod": ["electronicSubmission"],
                "submissionMethodRationale": submission_method_rationale,
                "submissionMethodDetails": submission_method_details,
                "documents": [
                    {
                        "id": self.document_one_was_uploaded,
                        "documentType": "billOfQuantity",
                        "title": "create Pn: tender.documents[0].title",
                        "description": "create Pn: tender.documents[0].description",
                        "relatedLots": [
                            first_lot_id]
                    },
                    {
                        "id": self.document_two_was_uploaded,
                        "documentType": "billOfQuantity",
                        "title": "create Pn: tender.documents[1].title",
                        "description": "create Pn: tender.documents[1].description",
                        "relatedLots": [
                            second_lot_id]
                    },
                    {
                        "id": self.document_three_was_uploaded,
                        "documentType": "evaluationCriteria",
                        "title": "create CNonPN: tender.documents[2].title",
                        "description": "create CNonPN: tender.documents[2].description",
                        "relatedLots": [first_lot_id]
                    }
                ]
            }
        }

        json_auction_auctions = {
            "version": "1.0.0",
            "tender": {
                "id": ev_id,
                "country": self.country,
                "status": 1,
                "startDate": auction_date
            },
            "slots": ["917ba5a5-d39e-4c24-a465-4b7f5726d5f3"],
            "auctions": [{
                "id": "503d6861-62d9-47f3-8939-4e4729df0cde",
                "lotId": first_lot_id,
                "auctionPeriod": {
                    "startDate": auction_date
                },
                "modalities": [{
                    "url": f"https://eauction.eprocurement.systems/auctions/{ev_id}/{first_lot_id}",
                    "eligibleMinimumDifference": {
                        "amount": 100.00,
                        "currency": "EUR"
                    }
                }]
            }, {
                "id": "516f0bd4-7706-4dc8-bd37-894d93cac809",
                "lotId": second_lot_id,
                "auctionPeriod": {
                    "startDate": auction_date
                },
                "modalities": [{
                    "url": f"https://eauction.eprocurement.systems/auctions/{ev_id}/{second_lot_id}",
                    "eligibleMinimumDifference": {
                        "amount": 10.00,
                        "currency": "EUR"
                    }
                }]
            }]
        }
        json_amendments = {
            "id": self.amendment_id,
            "date": period_for_amendment[0],
            "rationale": "cancel_tender: amendments[0].rationale",
            "description": "cancel_tender: amendments[0].description",
            "status": "pending",
            "type": "cancellation",
            "relatesTo": "lot",
            "relatedItem": lot_id,
            "token": self.amendment_token,
            "owner": "445f6851-c908-407d-9b45-14b92f3e964b",
            "documents": [{
                "documentType": "cancellationDetails",
                "id": self.document_five_was_uploaded,
                "title": "cancel_tender: amendments[0].documents[0].title",
                "description": "cancel_tender: amendments[0].documents[0].description"
            }]
        }
        json_notice_release_ms = {
            "ocid": cp_id,
            "id": f"{cp_id}-{ev_id[32:45]}",
            "date": f"{get_human_date_in_utc_format(int(ev_id[32:45]))[0]}",
            "tag": ["compiled"],
            "language": self.lang,
            "initiationType": "tender",
            "planning": {
                "budget": {
                    "description": "create Pn: planning.budget.description",
                    "amount": {
                        "amount": 2000.00,
                        "currency": "EUR"
                    },
                    "isEuropeanUnionFunded": True,
                    "budgetBreakdown": [{
                        "id": fs_id,
                        "description": "create Fs: planning.budget.description",
                        "amount": {
                            "amount": 2000.00,
                            "currency": "EUR"
                        },
                        "period": {
                            "startDate": period[0],
                            "endDate": period[1]
                        },
                        "sourceParty": {
                            "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                            "name": self.funder_name,
                        },
                        "europeanUnionFunding": {
                            "projectIdentifier": "create Fs: planning.budget.europeanUnionFunding.projectIdentifier",
                            "projectName": "create Fs: planning.budget.europeanUnionFunding.projectName",
                            "uri": "create Fs: planning.budget.europeanUnionFunding.uri"
                        }
                    }]
                },
                "rationale": "create Pn: planning.rationale"
            },
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "title": "create Pn: tender.title",
                "description": "create Pn: tender.description",
                "status": "active",
                "statusDetails": "evaluation",
                "value": {
                    "amount": 1650.00,
                    "currency": "EUR"
                },
                "procurementMethod": "open",
                "procurementMethodDetails": procurement_method_details_from_mdm,
                "procurementMethodRationale": "create CNonPN: tender.procurementMethodRationale",
                "mainProcurementCategory": "works",
                "hasEnquiries": False,
                "eligibilityCriteria": eligibility_criteria_from_mdm,
                "contractPeriod": {
                    "startDate": contract_period[0],
                    "endDate": contract_period[1]
                },
                "procuringEntity": {
                    "id": "MD-IDNO-4",
                    "name": "create Pn: tender.procuringEntity.name"
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
                "legalBasis": "DIRECTIVE_2014_25_EU",
                "procedureOutsourcing": {
                    "procedureOutsourced": False
                },
                "procurementMethodAdditionalInfo": "create CNonPN: tender.procurementMethodAdditionalInfo",
                "dynamicPurchasingSystem": {
                    "hasDynamicPurchasingSystem": False
                },
                "framework": {
                    "isAFramework": False
                }
            },
            "parties": [{
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name,
                "identifier": {
                    "scheme": self.buyer_identifier_scheme,
                    "id": self.buyer_identifier_id,
                    "legalName": self.buyer_identifier_legal_name,
                    "uri": self.buyer_identifier_uri
                },
                "address": {
                    "streetAddress": self.buyer_address_street_address,
                    "postalCode": self.buyer_address_postal_code,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.buyer_address_address_details_country_id,
                            "description": "Moldova, Republica",
                            "uri": "https://www.iso.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": self.buyer_address_address_details_region_id,
                            "description": "Cahul",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": self.buyer_address_address_details_locality_scheme,
                            "id": self.buyer_address_address_details_locality_id,
                            "description": self.buyer_address_address_details_locality_description,
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "additionalIdentifiers": [
                    {
                        "scheme": "create Ei: buyer.additionalIdentifiers[0].scheme",
                        "id": "create Ei: buyer.additionalIdentifiers[0].id",
                        "legalName": "create Ei: buyer.additionalIdentifiers[0].legalName",
                        "uri": "create Ei: buyer.additionalIdentifiers[0].uri"
                    }],
                "contactPoint": {
                    "name": self.buyer_contact_point_name,
                    "email": self.buyer_contact_point_email,
                    "telephone": self.buyer_contact_point_telephone,
                    "faxNumber": self.buyer_contact_point_fax_number,
                    "url": self.buyer_contact_point_url
                },
                "details": {
                    "typeOfBuyer": "NATIONAL_AGENCY",
                    "mainGeneralActivity": "HEALTH",
                    "mainSectoralActivity": "WATER"
                },
                "roles": [
                    "buyer"]
            }, {
                "id": f"{self.payer_identifier_scheme}-{self.payer_identifier_id}",
                "name": self.payer_name,
                "identifier": {
                    "scheme": self.payer_identifier_scheme,
                    "id": self.payer_identifier_id,
                    "legalName": self.payer_identifier_legal_name,
                    "uri": self.payer_identifier_uri
                },
                "address": {
                    "streetAddress": self.payer_address_street,
                    "postalCode": self.payer_address_postal_code,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.payer_address_address_details_country_id,
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": self.payer_address_address_details_region_id,
                            "description": "Cahul",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": self.payer_address_address_details_locality_scheme,
                            "id": self.payer_address_address_details_locality_id,
                            "description": self.payer_address_address_details_locality_description,
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "additionalIdentifiers": [
                    {
                        "scheme": "create Fs: tender.procuringEntity.additionalIdentifiers[0].scheme",
                        "id": "create Fs: tender.procuringEntity.additionalIdentifiers[0].id",
                        "legalName": "create Fs: tender.procuringEntity.additionalIdentifiers[0].legalName",
                        "uri": "create Fs: tender.procuringEntity.additionalIdentifiers[0].uri"
                    }],
                "contactPoint": {
                    "name": self.payer_contact_point_name,
                    "email": self.payer_contact_point_email,
                    "telephone": self.payer_contact_point_telephone,
                    "faxNumber": self.payer_contact_point_fax_number,
                    "url": self.payer_contact_point_url
                },
                "roles": ["payer"]
            }, {
                "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                "name": self.funder_name,
                "identifier": {
                    "scheme": self.funder_identifier_scheme,
                    "id": self.funder_identifier_id,
                    "legalName": self.funder_identifier_legal_name,
                    "uri": self.funder_identifier_uri
                },
                "address": {
                    "streetAddress": self.funder_address_street,
                    "postalCode": self.funder_address_postal_code,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.funder_address_address_details_country_id,
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": self.funder_address_address_details_region_id,
                            "description": "Cahul",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": self.funder_address_address_details_locality_scheme,
                            "id": self.funder_address_address_details_locality_id,
                            "description": self.funder_address_address_details_locality_description,
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "additionalIdentifiers": [
                    {
                        "scheme": "create Fs: buyer.additionalIdentifiers[0].scheme",
                        "id": "create Fs: buyer.additionalIdentifiers[0].id",
                        "legalName": "create Fs: buyer.additionalIdentifiers[0].legalName",
                        "uri": "create Fs: buyer.additionalIdentifiers[0].uri"
                    }],
                "contactPoint": {
                    "name": self.funder_contact_point_name,
                    "email": self.funder_contact_point_email,
                    "telephone": self.funder_contact_point_telephone,
                    "faxNumber": self.funder_contact_point_fax,
                    "url": self.funder_contact_point_url
                },
                "roles": [
                    "funder"]
            }, {
                "id": "MD-IDNO-4",
                "name": "create Pn: tender.procuringEntity.name",
                "identifier": {
                    "scheme": "MD-IDNO",
                    "id": "4",
                    "legalName": "create Pn: tender.procuringEntity.identigfier.legalName",
                    "uri": "create Pn: tender.procuringEntity.identifier.uri"
                },
                "address": {
                    "streetAddress": "create Pn: tender.procuringEntity.address.streetAddress",
                    "postalCode": "create Pn: tender.procuringEntity.address.postalCode",
                    "addressDetails": {
                        "country": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["country"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['uri']
                        },
                        "region": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["region"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['uri']
                        },
                        "locality": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["locality"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['uri']

                        }
                    }
                },
                "additionalIdentifiers": [{
                    "scheme": "create Pn: tender.procuringEntity.additionalIdentifiers[0].scheme",
                    "id": "create Pn: tender.procuringEntity.additionalIdentifiers[0].id",
                    "legalName": "create Pn: tender.procuringEntity.additionalIdentifiers[0].legalName",
                    "uri": "create Pn: tender.procuringEntity.additionalIdentifiers[0].uri"
                }],
                "contactPoint": {
                    "name": "create Pn: tender.procuringEntity.contactPoint.name",
                    "email": "create Pn: tender.procuringEntity.contactPoint.email",
                    "telephone": "create Pn: tender.procuringEntity.contactPoint.telephone",
                    "faxNumber": "create Pn: tender.procuringEntity.contactPoint.faxNumber",
                    "url": "create Pn: tender.procuringEntity.contactPoint.url"
                },
                "persones": [{
                    "id": "MD-IDNO-create CNonPN: procuringEntity.persones[0].identifier.id",
                    "title": "create CNonPN: procuringEntity.persones[0].title",
                    "name": "create CNonPN: procuringEntity.persones[0].name",
                    "identifier": {
                        "scheme": "MD-IDNO",
                        "id": "create CNonPN: procuringEntity.persones[0].identifier.id",
                        "uri": "create CNonPN: procuringEntity.persones[0].identifier.uri"
                    },
                    "businessFunctions": [{
                        "id": "create CNonPN: procuringEntity.persones[0].businessFunctions[0].id",
                        "type": "procurementOfficer",
                        "jobTitle": "create CNonPN: procuringEntity.persones[0].businessFunctions[0].jobTitle",
                        "period": {
                            "startDate": period[0]
                        },
                        "documents": [{
                            "id": self.document_three_was_uploaded,
                            "documentType": "regulatoryDocument",
                            "title": "create CNonPN: procuringEntity.persones[0].businessFunctions[0].title",
                            "description": "create CNonPN: procuringEntity.persones[0].businessFunctions[0]."
                                           "description",
                            "url": f"{instance_storage_url}"
                                   f"{self.document_three_was_uploaded}",
                            "datePublished": operation_date
                        }]
                    }]
                }],
                "roles": ["procuringEntity"]
            }],
            "relatedProcesses": [{
                "id": "36b553f0-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["planning"],
                "scheme": "ocid",
                "identifier": pn_id,
                "uri": f"{instance_tender_url}{cp_id}/{pn_id}"
            }, {
                "id": "36b553f1-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["x_expenditureItem"],
                "scheme": "ocid",
                "identifier": ei_id,
                "uri": f"{instance_budget_url}{ei_id}/{ei_id}"
            }, {
                "id": "36b553f2-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["x_fundingSource"],
                "scheme": "ocid",
                "identifier": fs_id,
                "uri": f"{instance_budget_url}{ei_id}/{fs_id}"
            },
                {
                    "id": "164cf530-ceca-11eb-8aed-69d06bed4d57",
                    "relationship": ["x_evaluation"],
                    "scheme": "ocid",
                    "identifier": ev_id,
                    "uri": f"{instance_tender_url}{cp_id}/{ev_id}"
                }
            ]
        }
        json_notice_release_pn = {
            "ocid": pn_id,
            "id": f"{pn_id}-{ev_id[32:45]}",
            "date": f"{get_human_date_in_utc_format(int(ev_id[32:45]))[0]}",
            "tag": ["planningUpdate"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "title": "Planning Notice",
                "description": "Contracting process is planned",
                "status": "complete",
                "statusDetails": "empty",
                "items": [{
                    "id": first_item_id,
                    "internalId": "create Pn: tender.items[0].internalId",
                    "description": "create Pn: tender.items[0].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_first_item_cpv_code[0],
                        "description": get_value_by_first_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_first_item_cpvs_code[0],
                        "description": get_value_by_first_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_first_item_unit_id[0],
                        "name": get_value_by_first_item_unit_id[1]
                    },
                    "relatedLot": first_lot_id
                }, {
                    "id": second_item_id,
                    "internalId": "create Pn: tender.items[1].internalId",
                    "description": "create Pn: tender.items[1].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_second_item_cpv_code[0],
                        "description": get_value_by_second_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_second_item_cpvs_code[0],
                        "description": get_value_by_second_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_second_item_unit_id[0],
                        "name": get_value_by_second_item_unit_id[1]
                    },
                    "relatedLot": second_lot_id
                }],
                "lots": [{
                    "id": first_lot_id,
                    "internalId": "create Pn: tender.lots[0].internalId",
                    "title": "create Pn: tender.lots[0].title",
                    "description": "create Pn: tender.lots[0].internalId.description",
                    "status": "planning",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 1500.00,
                        "currency": "EUR"
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
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[0].placeOfPerformance.address.streetAddress",
                            "postalCode": "create Pn: tender.lots[0].placeOfPerformance.address.postalCode",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        },
                        "description": "create Pn: tender.lots[0].placeOfPerformance.description"
                    },
                    "options": [{
                        "hasOptions": False
                    }]
                }, {
                    "id": second_lot_id,
                    "internalId": "create Pn: tender.lots[1].internalId",
                    "title": "create Pn: tender.lots[1].title",
                    "description": "create Pn: tender.lots[1].internalId.description",
                    "status": "planning",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 150.00,
                        "currency": "EUR"
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
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[1].placeOfPerformance.address.streetAddress",
                            "postalCode": "create Pn: tender.lots[1].placeOfPerformance.address.postalCode",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        },
                        "description": "create Pn: tender.lots[1].placeOfPerformance.description"
                    },
                    "options": [{
                        "hasOptions": False
                    }]
                }],
                "lotGroups": [{
                    "optionToCombine": False
                }],
                "tenderPeriod": {
                    "startDate": period[3]
                },
                "hasEnquiries": False,
                "documents": [
                    {
                        "id": self.document_one_was_uploaded,
                        "documentType": "contractArrangements",
                        "title": "create Pn: tender.documents[0].title",
                        "description": "create Pn: tender.documents[0].description",
                        "url": f"{instance_storage_url}"
                               f"{self.document_one_was_uploaded}",
                        "datePublished": f"{get_human_date_in_utc_format(int(pn_id[32:45]))[0]}",
                        "relatedLots": [first_lot_id]
                    },
                    {
                        "id": self.document_two_was_uploaded,
                        "documentType": "contractArrangements",
                        "title": "create Pn: tender.documents[1].title",
                        "description": "create Pn: tender.documents[1].description",
                        "url": f"{instance_storage_url}"
                               f"{self.document_two_was_uploaded}",
                        "datePublished": f"{get_human_date_in_utc_format(int(pn_id[32:45]))[0]}",
                        "relatedLots": [second_lot_id]
                    }],
                "submissionMethod": ["electronicSubmission"],
                "submissionMethodDetails": submission_method_details,
                "submissionMethodRationale": submission_method_rationale,
                "requiresElectronicCatalogue": False,
                "procurementMethodRationale": "create Pn: tender.procurementMethodRationale",
                "classification": {
                    "scheme": "CPV",
                    "id": get_value_by_new_cpv_code[0],
                    "description": get_value_by_new_cpv_code[1]
                },
                "value": {
                    "amount": 1650.00,
                    "currency": "EUR"
                }
            },
            "hasPreviousNotice": False,
            "purposeOfNotice": {
                "isACallForCompetition": False
            },
            "relatedProcesses": [{
                "id": "36b553f3-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": cp_id,
                "uri": f"{instance_tender_url}{cp_id}/{cp_id}"
            }]
        }
        json_notice_release_ev = {
            "ocid": ev_id,
            "id": f"{ev_id}-{ev_id[32:45]}",
            "date": f"{get_human_date_in_utc_format(int(ev_id[32:45]))[0]}",
            "tag": ["tender"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "c36f9952-06d5-41ef-9fe6-36722f1da414",
                "title": "Planning Notice",
                "description": "Contracting process is planned",
                "status": "active",
                "statusDetails": "clarification",
                "criteria": [{
                    "id": "9b62d854-acd3-479f-b0a9-402fe8081480",
                    "title": "create CNonPN: tender.criteria[0].title =Bankruptcy",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[0].description =Is the economic operator bankrupt? "
                                   "This information needs not be given if exclusion of economic operators in this "
                                   "case has been made mandatory under the applicable national law without any "
                                   "possibility of derogation where the economic operator is nevertheless able to "
                                   "perform the contract.",
                    "requirementGroups": [{
                        "id": "f83633d5-6d4e-4b9f-9bc2-8770f8bfb9b6",
                        "description": "create CNonPN: tender.criteria[0].requirementGroups[0].description =approve "
                                       "that Bankruptcy requirement group",
                        "requirements": [{
                            "id": "d5366584-8e57-445f-b1f6-55063bb29ea2",
                            "title": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements.title",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "description": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements."
                                           "description",
                            "eligibleEvidences": [{
                                "id": "1",
                                "title": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements[0]."
                                         "eligibleEvidences[0].title",
                                "type": "document",
                                "description": "create CNonPN: tender.criteria[0].requirementGroups[0]."
                                               "requirements[0].eligibleEvidences[0].description",
                                "relatedDocument": {
                                    "id": self.document_three_was_uploaded
                                }
                            }, {
                                "id": "2",
                                "title": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements[0]."
                                         "eligibleEvidences[1].title",
                                "type": "document",
                                "description": "create CNonPN: tender.criteria[0].requirementGroups[0]."
                                               "requirements[0].eligibleEvidences[1].description",
                                "relatedDocument": {
                                    "id": self.document_three_was_uploaded
                                }
                            }],
                            "expectedValue": False
                        }]
                    }],
                    "relatesTo": "tender",
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.EXCLUSION.CONVICTIONS.PARTICIPATION_IN_CRIMINAL_ORGANISATION"
                    }
                }, {
                    "id": "0b607a5e-e432-4d60-bcff-40c4de9ee04b",
                    "title": "create CNonPN: tender.criteria[1].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[1].description",
                    "requirementGroups": [{
                        "id": "437c395a-7a92-48c3-94bd-fcd3fb238304",
                        "description": "create CNonPN: tender.criteria[1].requirementGroups[0].description",
                        "requirements": [{
                            "id": "7bcf3819-a328-4560-b256-24c89b70d436",
                            "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[0].title",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "description": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements."
                                           "description",
                            "expectedValue": True
                        }, {
                            "id": "5b761cae-5c26-4266-b81d-9178232e931e",
                            "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[1]."
                                     "title =The number of years for proposed product warranty",
                            "dataType": "number",
                            "status": "active",
                            "datePublished": operation_date,
                            "description": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[1]."
                                           "description",
                            "period": {
                                "startDate": period[0],
                                "endDate": period[1]
                            },
                            "eligibleEvidences": [{
                                "id": "3",
                                "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[1]."
                                         "eligibleEvidences[0].title",
                                "type": "document",
                                "description": "create CNonPN: tender.criteria[1].requirementGroups[0]."
                                               "requirements[1].eligibleEvidences[0].description",
                                "relatedDocument": {
                                    "id": self.document_three_was_uploaded
                                }
                            }],
                            "minValue": 1.000,
                            "maxValue": 3.000
                        }]
                    }],
                    "relatesTo": "lot",
                    "relatedItem": first_lot_id,
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.SELECTION.ECONOMIC_FINANCIAL_STANDING.TURNOVER.GENERAL_YEARLY"
                    }
                }, {
                    "id": "11a3595b-4327-4382-a72f-e663f937a206",
                    "title": "create CNonPN: tender.criteria[2].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[2].description",
                    "requirementGroups": [{
                        "id": "779894eb-41c2-4db0-825c-27d3dbd522a6",
                        "description": "create CNonPN: tender.criteria[2].requirementGroups[0].description",
                        "requirements": [{
                            "id": "e30b1213-f94d-4364-9a75-e9532d7c98ed",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[0].requirements[0]."
                                     "title =Product has to be manufactured in the EU",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "expectedValue": True
                        }, {
                            "id": "e95d0bce-acf6-4873-867f-7a26a6935146",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[0]..requirements[1]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }, {
                        "id": "c1021836-1fe1-49e1-8286-42badf1b62aa",
                        "description": "create CNonPN: tender.criteria[2].requirementGroups[1].description",
                        "requirements": [{
                            "id": "0cef779c-9039-4a87-838d-1f8775a14f57",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[1].requirements[0]."
                                     "title =Product has to be manufactured in the EU",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "expectedValue": True
                        }, {
                            "id": "53cade1e-112a-441e-a2d0-64c2bc547f43",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[1]..requirements[1]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }],
                    "relatesTo": "tenderer",
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.EXCLUSION.NATIONAL.OTHER"
                    }
                }, {
                    "id": "a8168d9a-34c8-44b7-8a59-d126d770ffa2",
                    "title": "create CNonPN: tender.criteria[3].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[3].description =A minimum product warranty "
                                   "of 1 year is required for all bids 2",
                    "requirementGroups": [{
                        "id": "1992b2ca-4ac2-43c2-b1ef-90d41860c718",
                        "description": "create CNonPN: tender.criteria[3].requirementGroups[0].description",
                        "requirements": [{
                            "id": "aaa2e373-2fee-4da4-a153-16c89127a633",
                            "title": "create CNonPN: tender.criteria[3].requirementGroups[0].requirements[0]."
                                     "title = The number of years for proposed product warranty",
                            "dataType": "number",
                            "status": "active",
                            "datePublished": operation_date,
                            "period": {
                                "startDate": period[0],
                                "endDate": period[1]
                            },
                            "minValue": 1.000,
                            "maxValue": 3.000
                        }]
                    }],
                    "relatesTo": "item",
                    "relatedItem": first_item_id,
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.OTHER.EO_DATA.RELIES_ON_OTHER_CAPACITIES"
                    }
                }, {
                    "id": "a5569789-616d-407b-844e-8974611db63d",
                    "title": "create CNonPN: tender.criteria[4].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[4].description",
                    "requirementGroups": [{
                        "id": "e2e4291b-7e9c-401c-b9a6-2ec6bee0c85c",
                        "description": "create CNonPN: tender.criteria[4].requirementGroups[0].description",
                        "requirements": [{
                            "id": "4d104276-47fc-4d93-a694-444457b825e4",
                            "title": "create CNonPN: tender.criteria[4].requirementGroups[0].requirements[0]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }],
                    "relatesTo": "tender",
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.EXCLUSION.NATIONAL.OTHER"
                    }
                }, {
                    "id": "dd056608-225f-4e1b-9e22-e8b927f50678",
                    "title": "create CNonPN: tender.criteria[4].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[4].description",
                    "requirementGroups": [{
                        "id": "c6f455a8-dcd3-40ae-8518-c07bc68603c0",
                        "description": "create CNonPN: tender.criteria[4].requirementGroups[0].description",
                        "requirements": [{
                            "id": "9529530c-bdeb-45db-b559-aa9f5fba7b05",
                            "title": "create CNonPN: tender.criteria[4].requirementGroups[0].requirements[0]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }],
                    "relatesTo": "tender",
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.OTHER.EO_DATA.RELIES_ON_OTHER_CAPACITIES"
                    }
                }],
                "conversions": [{
                    "id": "1e49348e-1a13-409e-95f8-371cb7430a6a",
                    "relatesTo": "requirement",
                    "relatedItem": "7bcf3819-a328-4560-b256-24c89b70d436",
                    "rationale": "create CNonPN: tender.conversions[1].rationale",
                    "description": "create CNonPN: tender.conversions[1].description",
                    "coefficients": [{
                        "id": "3344c418-c0cb-40f5-86bd-2e7aab5d5e19",
                        "value": False,
                        "coefficient": 1
                    }]
                }, {
                    "id": "b61c8d3f-54cb-48cf-94d3-6547db1b6584",
                    "relatesTo": "requirement",
                    "relatedItem": "5b761cae-5c26-4266-b81d-9178232e931e",
                    "rationale": "create CNonPN: tender.conversions[3].rationale",
                    "description": "create CNonPN: tender.conversions[3].description",
                    "coefficients": [{
                        "id": "8e1c5c9d-9fd5-4524-8ee7-1dc69c392e25",
                        "value": 1.000,
                        "coefficient": 1
                    }, {
                        "id": "eea59dc3-cf39-43e4-85ae-c25f4207c378",
                        "value": 2.000,
                        "coefficient": 1
                    }, {
                        "id": "2ef0e48a-5359-4c2b-b4a7-e2e209239173",
                        "value": 3.000,
                        "coefficient": 0.93
                    }]
                }, {
                    "id": "602f52cb-6257-479b-b637-85bd1b94a3cf",
                    "relatesTo": "requirement",
                    "relatedItem": "aaa2e373-2fee-4da4-a153-16c89127a633",
                    "rationale": "create CNonPN: tender.conversions[6].rationale",
                    "description": "create CNonPN: tender.conversions[6].description",
                    "coefficients": [{
                        "id": "0b1fd4bc-dcb9-460d-89fa-ce44387b76ef",
                        "value": 1.000,
                        "coefficient": 1
                    }, {
                        "id": "c9bcba0e-f235-40c4-9023-1c4e7813e7a0",
                        "value": 2.000,
                        "coefficient": 1
                    }, {
                        "id": "998f9ae4-86a0-4c80-8973-f7d7cdc78351",
                        "value": 3.000,
                        "coefficient": 0.93
                    }]
                }, {
                    "id": "df048f38-c201-4aae-a529-a721a7687430",
                    "relatesTo": "requirement",
                    "relatedItem": "9529530c-bdeb-45db-b559-aa9f5fba7b05",
                    "rationale": "create CNonPN: tender.conversions[6].rationale",
                    "description": "create CNonPN: tender.conversions[6].description",
                    "coefficients": [{
                        "id": "49f34ab3-c0ad-4509-b77f-ead756c50419",
                        "value": "option_1",
                        "coefficient": 1
                    }, {
                        "id": "39819b5c-2c5c-40db-af46-2e6b6b2f0dcb",
                        "value": "option_2",
                        "coefficient": 1
                    }, {
                        "id": "0cda7c91-e74d-4f57-91bd-cae195078dda",
                        "value": "option_3",
                        "coefficient": 0.93
                    }]
                }],
                "items": [{
                    "id": first_item_id,
                    "internalId": "create Pn: tender.items[0].internalId",
                    "description": "create Pn: tender.items[0].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_first_item_cpv_code[0],
                        "description": get_value_by_first_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_first_item_cpvs_code[0],
                        "description": get_value_by_first_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "name": get_value_by_first_item_unit_id[1],
                        "id": get_value_by_first_item_unit_id[0]
                    },
                    "relatedLot": first_lot_id
                }, {
                    "id": second_item_id,
                    "internalId": "create Pn: tender.items[1].internalId",
                    "description": "create Pn: tender.items[1].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_second_item_cpv_code[0],
                        "description": get_value_by_second_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_second_item_cpvs_code[0],
                        "description": get_value_by_second_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_first_item_unit_id[0],
                        "name": get_value_by_first_item_unit_id[1]
                    },
                    "relatedLot": second_lot_id
                }],
                "lots": [{
                    "id": first_lot_id,
                    "internalId": "create Pn: tender.lots[0].internalId",
                    "title": "create Pn: tender.lots[0].title",
                    "description": "create Pn: tender.lots[0].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 1500.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[0].placeOfPerformance.address.streetAddress",
                            "postalCode": "create Pn: tender.lots[0].placeOfPerformance.address.postalCode",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        },
                        "description": "create Pn: tender.lots[0].placeOfPerformance.description"
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }, {
                    "id": second_lot_id,
                    "internalId": "create Pn: tender.lots[1].internalId",
                    "title": "create Pn: tender.lots[1].title",
                    "description": "create Pn: tender.lots[1].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 150.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[1].placeOfPerformance.address.streetAddress",
                            "postalCode": "create Pn: tender.lots[1].placeOfPerformance.address.postalCode",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        },
                        "description": "create Pn: tender.lots[1].placeOfPerformance.description"
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }],
                "lotGroups": [{
                    "optionToCombine": False
                }],
                "tenderPeriod": {
                    "startDate": enquiry_and_tender_period[2],
                    "endDate": enquiry_and_tender_period[3]
                },
                "enquiryPeriod": {
                    "startDate": enquiry_and_tender_period[0],
                    "endDate": enquiry_and_tender_period[1]
                },
                "auctionPeriod": {
                    "startDate": auction_date
                },
                "hasEnquiries": False,
                "documents": [{
                    "id": self.document_one_was_uploaded,
                    "documentType": "contractArrangements",
                    "title": "create Pn: tender.documents[0].title",
                    "description": "create Pn: tender.documents[0].description",
                    "url": f"{instance_storage_url}{self.document_one_was_uploaded}",
                    "datePublished": operation_date,
                    "relatedLots": [first_lot_id]
                }, {
                    "id": self.document_two_was_uploaded,
                    "documentType": "contractArrangements",
                    "title": "create Pn: tender.documents[1].title",
                    "description": "create Pn: tender.documents[1].description",
                    "url": f"{instance_storage_url}{self.document_two_was_uploaded}",
                    "datePublished": operation_date,
                    "relatedLots": [second_lot_id]
                }, {
                    "id": self.document_three_was_uploaded,
                    "documentType": "illustration",
                    "title": "create CNonPN: tender.documents[2].title",
                    "description": "create CNonPN: tender.documents[2].description",
                    "url": f"{instance_storage_url}"
                           f"{self.document_three_was_uploaded}",
                    "datePublished": operation_date,
                    "relatedLots": [first_lot_id]
                }],
                "awardCriteria": "ratedCriteria",
                "awardCriteriaDetails": "automated",
                "submissionMethod": ["electronicSubmission"],
                "submissionMethodDetails": submission_method_details,
                "submissionMethodRationale": submission_method_rationale,
                "requiresElectronicCatalogue": False,
                "procurementMethodModalities": ["electronicAuction"],
                "electronicAuctions": {
                    "details": [{
                        "id": "2cbf1162-4e8b-48d7-b64b-680b5fa6b350",
                        "relatedLot": first_lot_id,
                        "auctionPeriod": {
                            "startDate": auction_date
                        },
                        "electronicAuctionModalities": [{
                            "url": f"https://eauction.eprocurement.systems/auctions/{ev_id}/{first_lot_id}",
                            "eligibleMinimumDifference": {
                                "amount": 100.00,
                                "currency": "EUR"
                            }
                        }]
                    }, {
                        "id": "c19b09d5-3dcb-43a8-a1fc-096948abb403",
                        "relatedLot": second_lot_id,
                        "auctionPeriod": {
                            "startDate": auction_date
                        },
                        "electronicAuctionModalities": [{
                            "url": f"https://eauction.eprocurement.systems/auctions/{ev_id}/{second_lot_id}",
                            "eligibleMinimumDifference": {
                                "amount": 10.00,
                                "currency": "EUR"
                            }
                        }]
                    }]
                },
                "procurementMethodRationale": "create CNonPN: tender.procurementMethodRationale"
            },
            "hasPreviousNotice": True,
            "purposeOfNotice": {
                "isACallForCompetition": True
            },
            "relatedProcesses": [{
                "id": "12a3ea63-ceca-11eb-8aed-69d06bed4d57",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": cp_id,
                "uri": f"{instance_tender_url}{cp_id}/{cp_id}"
            }, {
                "id": "164cf531-ceca-11eb-8aed-69d06bed4d57",
                "relationship": ["planning"],
                "scheme": "ocid",
                "identifier": pn_id,
                "uri": f"{instance_tender_url}{cp_id}/{pn_id}"
            }]
        }

        json_notice_release_ev_new = {
            "ocid": ev_id,
            "id": f"{ev_id}-{period_for_amendment[1]}",
            "date": period_for_amendment[0],
            "tag": ["tender"],
            "initiationType": "tender",
            "language": self.lang,
            "tender": {
                "id": "c36f9952-06d5-41ef-9fe6-36722f1da414",
                "title": "Evaluation",
                "description": "Evaluation stage of contracting process",
                "status": "active",
                "statusDetails": "clarification",
                "criteria": [{
                    "id": "9b62d854-acd3-479f-b0a9-402fe8081480",
                    "title": "create CNonPN: tender.criteria[0].title =Bankruptcy",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[0].description =Is the economic operator bankrupt? "
                                   "This information needs not be given if exclusion of economic operators in this "
                                   "case has been made mandatory under the applicable national law without any "
                                   "possibility of derogation where the economic operator is nevertheless able to "
                                   "perform the contract.",
                    "requirementGroups": [{
                        "id": "f83633d5-6d4e-4b9f-9bc2-8770f8bfb9b6",
                        "description": "create CNonPN: tender.criteria[0].requirementGroups[0].description =approve "
                                       "that Bankruptcy requirement group",
                        "requirements": [{
                            "id": "d5366584-8e57-445f-b1f6-55063bb29ea2",
                            "title": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements.title",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "description": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements."
                                           "description",
                            "eligibleEvidences": [{
                                "id": "1",
                                "title": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements[0]."
                                         "eligibleEvidences[0].title",
                                "type": "document",
                                "description": "create CNonPN: tender.criteria[0].requirementGroups[0]."
                                               "requirements[0].eligibleEvidences[0].description",
                                "relatedDocument": {
                                    "id": self.document_three_was_uploaded
                                }
                            }, {
                                "id": "2",
                                "title": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements[0]."
                                         "eligibleEvidences[1].title",
                                "type": "document",
                                "description": "create CNonPN: tender.criteria[0].requirementGroups[0]."
                                               "requirements[0].eligibleEvidences[1].description",
                                "relatedDocument": {
                                    "id": self.document_three_was_uploaded
                                }
                            }],
                            "expectedValue": False
                        }]
                    }],
                    "relatesTo": "tender",
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.EXCLUSION.CONVICTIONS.PARTICIPATION_IN_CRIMINAL_ORGANISATION"
                    }
                }, {
                    "id": "0b607a5e-e432-4d60-bcff-40c4de9ee04b",
                    "title": "create CNonPN: tender.criteria[1].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[1].description",
                    "requirementGroups": [{
                        "id": "437c395a-7a92-48c3-94bd-fcd3fb238304",
                        "description": "create CNonPN: tender.criteria[1].requirementGroups[0].description",
                        "requirements": [{
                            "id": "7bcf3819-a328-4560-b256-24c89b70d436",
                            "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[0].title",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "description": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements."
                                           "description",
                            "expectedValue": True
                        }, {
                            "id": "5b761cae-5c26-4266-b81d-9178232e931e",
                            "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[1]."
                                     "title =The number of years for proposed product warranty",
                            "dataType": "number",
                            "status": "active",
                            "datePublished": operation_date,
                            "description": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[1]."
                                           "description",
                            "period": {
                                "startDate": period[0],
                                "endDate": period[1]
                            },
                            "eligibleEvidences": [{
                                "id": "3",
                                "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[1]."
                                         "eligibleEvidences[0].title",
                                "type": "document",
                                "description": "create CNonPN: tender.criteria[1].requirementGroups[0]."
                                               "requirements[1].eligibleEvidences[0].description",
                                "relatedDocument": {
                                    "id": self.document_three_was_uploaded
                                }
                            }],
                            "minValue": 1.000,
                            "maxValue": 3.000
                        }]
                    }],
                    "relatesTo": "lot",
                    "relatedItem": first_lot_id,
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.SELECTION.ECONOMIC_FINANCIAL_STANDING.TURNOVER.GENERAL_YEARLY"
                    }
                }, {
                    "id": "11a3595b-4327-4382-a72f-e663f937a206",
                    "title": "create CNonPN: tender.criteria[2].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[2].description",
                    "requirementGroups": [{
                        "id": "779894eb-41c2-4db0-825c-27d3dbd522a6",
                        "description": "create CNonPN: tender.criteria[2].requirementGroups[0].description",
                        "requirements": [{
                            "id": "e30b1213-f94d-4364-9a75-e9532d7c98ed",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[0].requirements[0]."
                                     "title =Product has to be manufactured in the EU",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "expectedValue": True
                        }, {
                            "id": "e95d0bce-acf6-4873-867f-7a26a6935146",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[0]..requirements[1]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }, {
                        "id": "c1021836-1fe1-49e1-8286-42badf1b62aa",
                        "description": "create CNonPN: tender.criteria[2].requirementGroups[1].description",
                        "requirements": [{
                            "id": "0cef779c-9039-4a87-838d-1f8775a14f57",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[1].requirements[0]."
                                     "title =Product has to be manufactured in the EU",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "expectedValue": True
                        }, {
                            "id": "53cade1e-112a-441e-a2d0-64c2bc547f43",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[1]..requirements[1]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }],
                    "relatesTo": "tenderer",
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.EXCLUSION.NATIONAL.OTHER"
                    }
                }, {
                    "id": "a8168d9a-34c8-44b7-8a59-d126d770ffa2",
                    "title": "create CNonPN: tender.criteria[3].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[3].description =A minimum product warranty "
                                   "of 1 year is required for all bids 2",
                    "requirementGroups": [{
                        "id": "1992b2ca-4ac2-43c2-b1ef-90d41860c718",
                        "description": "create CNonPN: tender.criteria[3].requirementGroups[0].description",
                        "requirements": [{
                            "id": "aaa2e373-2fee-4da4-a153-16c89127a633",
                            "title": "create CNonPN: tender.criteria[3].requirementGroups[0].requirements[0]."
                                     "title = The number of years for proposed product warranty",
                            "dataType": "number",
                            "status": "active",
                            "datePublished": operation_date,
                            "period": {
                                "startDate": period[0],
                                "endDate": period[1]
                            },
                            "minValue": 1.000,
                            "maxValue": 3.000
                        }]
                    }],
                    "relatesTo": "item",
                    "relatedItem": first_item_id,
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.OTHER.EO_DATA.RELIES_ON_OTHER_CAPACITIES"
                    }
                }, {
                    "id": "a5569789-616d-407b-844e-8974611db63d",
                    "title": "create CNonPN: tender.criteria[4].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[4].description",
                    "requirementGroups": [{
                        "id": "e2e4291b-7e9c-401c-b9a6-2ec6bee0c85c",
                        "description": "create CNonPN: tender.criteria[4].requirementGroups[0].description",
                        "requirements": [{
                            "id": "4d104276-47fc-4d93-a694-444457b825e4",
                            "title": "create CNonPN: tender.criteria[4].requirementGroups[0].requirements[0]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }],
                    "relatesTo": "tender",
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.EXCLUSION.NATIONAL.OTHER"
                    }
                }, {
                    "id": "dd056608-225f-4e1b-9e22-e8b927f50678",
                    "title": "create CNonPN: tender.criteria[4].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[4].description",
                    "requirementGroups": [{
                        "id": "c6f455a8-dcd3-40ae-8518-c07bc68603c0",
                        "description": "create CNonPN: tender.criteria[4].requirementGroups[0].description",
                        "requirements": [{
                            "id": "9529530c-bdeb-45db-b559-aa9f5fba7b05",
                            "title": "create CNonPN: tender.criteria[4].requirementGroups[0].requirements[0]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }],
                    "relatesTo": "tender",
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.OTHER.EO_DATA.RELIES_ON_OTHER_CAPACITIES"
                    }
                }],
                "conversions": [{
                    "id": "1e49348e-1a13-409e-95f8-371cb7430a6a",
                    "relatesTo": "requirement",
                    "relatedItem": "7bcf3819-a328-4560-b256-24c89b70d436",
                    "rationale": "create CNonPN: tender.conversions[1].rationale",
                    "description": "create CNonPN: tender.conversions[1].description",
                    "coefficients": [{
                        "id": "3344c418-c0cb-40f5-86bd-2e7aab5d5e19",
                        "value": False,
                        "coefficient": 1
                    }]
                }, {
                    "id": "b61c8d3f-54cb-48cf-94d3-6547db1b6584",
                    "relatesTo": "requirement",
                    "relatedItem": "5b761cae-5c26-4266-b81d-9178232e931e",
                    "rationale": "create CNonPN: tender.conversions[3].rationale",
                    "description": "create CNonPN: tender.conversions[3].description",
                    "coefficients": [{
                        "id": "8e1c5c9d-9fd5-4524-8ee7-1dc69c392e25",
                        "value": 1.000,
                        "coefficient": 1
                    }, {
                        "id": "eea59dc3-cf39-43e4-85ae-c25f4207c378",
                        "value": 2.000,
                        "coefficient": 1
                    }, {
                        "id": "2ef0e48a-5359-4c2b-b4a7-e2e209239173",
                        "value": 3.000,
                        "coefficient": 0.93
                    }]
                }, {
                    "id": "602f52cb-6257-479b-b637-85bd1b94a3cf",
                    "relatesTo": "requirement",
                    "relatedItem": "aaa2e373-2fee-4da4-a153-16c89127a633",
                    "rationale": "create CNonPN: tender.conversions[6].rationale",
                    "description": "create CNonPN: tender.conversions[6].description",
                    "coefficients": [{
                        "id": "0b1fd4bc-dcb9-460d-89fa-ce44387b76ef",
                        "value": 1.000,
                        "coefficient": 1
                    }, {
                        "id": "c9bcba0e-f235-40c4-9023-1c4e7813e7a0",
                        "value": 2.000,
                        "coefficient": 1
                    }, {
                        "id": "998f9ae4-86a0-4c80-8973-f7d7cdc78351",
                        "value": 3.000,
                        "coefficient": 0.93
                    }]
                }, {
                    "id": "df048f38-c201-4aae-a529-a721a7687430",
                    "relatesTo": "requirement",
                    "relatedItem": "9529530c-bdeb-45db-b559-aa9f5fba7b05",
                    "rationale": "create CNonPN: tender.conversions[6].rationale",
                    "description": "create CNonPN: tender.conversions[6].description",
                    "coefficients": [{
                        "id": "49f34ab3-c0ad-4509-b77f-ead756c50419",
                        "value": "option_1",
                        "coefficient": 1
                    }, {
                        "id": "39819b5c-2c5c-40db-af46-2e6b6b2f0dcb",
                        "value": "option_2",
                        "coefficient": 1
                    }, {
                        "id": "0cda7c91-e74d-4f57-91bd-cae195078dda",
                        "value": "option_3",
                        "coefficient": 0.93
                    }]
                }],
                "items": [{
                    "id": first_item_id,
                    "internalId": "create Pn: tender.items[0].internalId",
                    "description": "create Pn: tender.items[0].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_first_item_cpv_code[0],
                        "description": get_value_by_first_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_first_item_cpvs_code[0],
                        "description": get_value_by_first_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "name": get_value_by_first_item_unit_id[1],
                        "id": get_value_by_first_item_unit_id[0]
                    },
                    "relatedLot": first_lot_id
                }, {
                    "id": second_item_id,
                    "internalId": "create Pn: tender.items[1].internalId",
                    "description": "create Pn: tender.items[1].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_second_item_cpv_code[0],
                        "description": get_value_by_second_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_second_item_cpvs_code[0],
                        "description": get_value_by_second_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_first_item_unit_id[0],
                        "name": get_value_by_first_item_unit_id[1]
                    },
                    "relatedLot": second_lot_id
                }],
                "lots": [{
                    "id": first_lot_id,
                    "internalId": "create Pn: tender.lots[0].internalId",
                    "title": "create Pn: tender.lots[0].title",
                    "description": "create Pn: tender.lots[0].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 1500.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[0].placeOfPerformance.address.streetAddress",
                            "postalCode": "create Pn: tender.lots[0].placeOfPerformance.address.postalCode",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        },
                        "description": "create Pn: tender.lots[0].placeOfPerformance.description"
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }, {
                    "id": second_lot_id,
                    "internalId": "create Pn: tender.lots[1].internalId",
                    "title": "create Pn: tender.lots[1].title",
                    "description": "create Pn: tender.lots[1].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 150.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[1].placeOfPerformance.address.streetAddress",
                            "postalCode": "create Pn: tender.lots[1].placeOfPerformance.address.postalCode",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        },
                        "description": "create Pn: tender.lots[1].placeOfPerformance.description"
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }],
                "lotGroups": [{
                    "optionToCombine": False
                }],
                "tenderPeriod": {
                    "startDate": enquiry_and_tender_period[2],
                    "endDate": enquiry_and_tender_period[3]
                },
                "enquiryPeriod": {
                    "startDate": enquiry_and_tender_period[0],
                    "endDate": enquiry_and_tender_period[1]
                },
                "auctionPeriod": {
                    "startDate": auction_date
                },
                "hasEnquiries": False,
                "amendments": [{
                    "id": self.amendment_id,
                    "type": "cancellation",
                    "status": "pending",
                    "relatesTo": "lot",
                    "relatedItem": lot_id,
                    "date": period_for_amendment[0],
                    "description": "cancel_tender: amendments[0].description",
                    "rationale": "cancel_tender: amendments[0].rationale",
                    "documents": [{
                        "documentType": "cancellationDetails",
                        "id": self.document_five_was_uploaded,
                        "title": "cancel_tender: amendments[0].documents[0].title",
                        "description": "cancel_tender: amendments[0].documents[0].description",
                        "url": f"{instance_storage_url}"
                               f"{self.document_five_was_uploaded}",
                        "datePublished": period[0]
                    }]
                }],
                "documents": [{
                    "id": self.document_one_was_uploaded,
                    "documentType": "contractArrangements",
                    "title": "create Pn: tender.documents[0].title",
                    "description": "create Pn: tender.documents[0].description",
                    "url": f"{instance_storage_url}{self.document_one_was_uploaded}",
                    "datePublished": operation_date,
                    "relatedLots": [first_lot_id]
                }, {
                    "id": self.document_two_was_uploaded,
                    "documentType": "contractArrangements",
                    "title": "create Pn: tender.documents[1].title",
                    "description": "create Pn: tender.documents[1].description",
                    "url": f"{instance_storage_url}"
                           f"{self.document_two_was_uploaded}",
                    "datePublished": operation_date,
                    "relatedLots": [second_lot_id]
                }, {
                    "id": self.document_three_was_uploaded,
                    "documentType": "illustration",
                    "title": "create CNonPN: tender.documents[2].title",
                    "description": "create CNonPN: tender.documents[2].description",
                    "url": f"{instance_storage_url}"
                           f"{self.document_three_was_uploaded}",
                    "datePublished": operation_date,
                    "relatedLots": [first_lot_id]
                }],
                "awardCriteria": "ratedCriteria",
                "awardCriteriaDetails": "automated",
                "submissionMethod": ["electronicSubmission"],
                "submissionMethodDetails": submission_method_details,
                "submissionMethodRationale": submission_method_rationale,
                "requiresElectronicCatalogue": False,
                "procurementMethodModalities": ["electronicAuction"],
                "electronicAuctions": {
                    "details": [{
                        "id": "2cbf1162-4e8b-48d7-b64b-680b5fa6b350",
                        "relatedLot": first_lot_id,
                        "auctionPeriod": {
                            "startDate": auction_date
                        },
                        "electronicAuctionModalities": [{
                            "url": f"https://eauction.eprocurement.systems/auctions/{ev_id}/{first_lot_id}",
                            "eligibleMinimumDifference": {
                                "amount": 100.00,
                                "currency": "EUR"
                            }
                        }]
                    }, {
                        "id": "c19b09d5-3dcb-43a8-a1fc-096948abb403",
                        "relatedLot": second_lot_id,
                        "auctionPeriod": {
                            "startDate": auction_date
                        },
                        "electronicAuctionModalities": [{
                            "url": f"https://eauction.eprocurement.systems/auctions/{ev_id}/{second_lot_id}",
                            "eligibleMinimumDifference": {
                                "amount": 10.00,
                                "currency": "EUR"
                            }
                        }]
                    }]
                },
                "procurementMethodRationale": "create CNonPN: tender.procurementMethodRationale"
            },
            "hasPreviousNotice": True,
            "purposeOfNotice": {
                "isACallForCompetition": True
            },
            "relatedProcesses": [{
                "id": "12a3ea63-ceca-11eb-8aed-69d06bed4d57",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": cp_id,
                "uri": f"{instance_tender_url}{cp_id}/{cp_id}"
            }, {
                "id": "164cf531-ceca-11eb-8aed-69d06bed4d57",
                "relationship": ["planning"],
                "scheme": "ocid",
                "identifier": pn_id,
                "uri": f"{instance_tender_url}{cp_id}/{pn_id}"
            }]
        }

        json_notice_compiled_release_ms = {
            "ocid": cp_id,
            "id": f"{cp_id}-{ev_id[32:45]}",
            "date": f"{get_human_date_in_utc_format(int(ev_id[32:45]))[0]}",
            "tag": ["compiled"],
            "language": self.lang,
            "initiationType": "tender",
            "planning": {
                "budget": {
                    "description": "create Pn: planning.budget.description",
                    "amount": {
                        "amount": 2000.00,
                        "currency": "EUR"
                    },
                    "isEuropeanUnionFunded": True,
                    "budgetBreakdown": [{
                        "id": fs_id,
                        "description": "create Fs: planning.budget.description",
                        "amount": {
                            "amount": 2000.00,
                            "currency": "EUR"
                        },
                        "period": {
                            "startDate": period[0],
                            "endDate": period[1]
                        },
                        "sourceParty": {
                            "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                            "name": self.funder_name,
                        },
                        "europeanUnionFunding": {
                            "projectIdentifier": "create Fs: planning.budget.europeanUnionFunding.projectIdentifier",
                            "projectName": "create Fs: planning.budget.europeanUnionFunding.projectName",
                            "uri": "create Fs: planning.budget.europeanUnionFunding.uri"
                        }
                    }]
                },
                "rationale": "create Pn: planning.rationale"
            },
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "title": "create Pn: tender.title",
                "description": "create Pn: tender.description",
                "status": "active",
                "statusDetails": "evaluation",
                "value": {
                    "amount": 1650.00,
                    "currency": "EUR"
                },
                "procurementMethod": "open",
                "procurementMethodDetails": procurement_method_details_from_mdm,
                "procurementMethodRationale": "create CNonPN: tender.procurementMethodRationale",
                "mainProcurementCategory": "works",
                "hasEnquiries": False,
                "eligibilityCriteria": eligibility_criteria_from_mdm,
                "contractPeriod": {
                    "startDate": contract_period[0],
                    "endDate": contract_period[1]
                },
                "procuringEntity": {
                    "id": "MD-IDNO-4",
                    "name": "create Pn: tender.procuringEntity.name"
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
                "legalBasis": "DIRECTIVE_2014_25_EU",
                "procedureOutsourcing": {
                    "procedureOutsourced": False
                },
                "procurementMethodAdditionalInfo": "create CNonPN: tender.procurementMethodAdditionalInfo",
                "dynamicPurchasingSystem": {
                    "hasDynamicPurchasingSystem": False
                },
                "framework": {
                    "isAFramework": False
                }
            },
            "parties": [{
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name,
                "identifier": {
                    "scheme": self.buyer_identifier_scheme,
                    "id": self.buyer_identifier_id,
                    "legalName": self.buyer_identifier_legal_name,
                    "uri": self.buyer_identifier_uri
                },
                "address": {
                    "streetAddress": self.buyer_address_street_address,
                    "postalCode": self.buyer_address_postal_code,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.buyer_address_address_details_country_id,
                            "description": "Moldova, Republica",
                            "uri": "https://www.iso.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": self.buyer_address_address_details_region_id,
                            "description": "mun.Chişinău",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": self.buyer_address_address_details_locality_scheme,
                            "id": self.buyer_address_address_details_locality_id,
                            "description": self.buyer_address_address_details_locality_description,
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "additionalIdentifiers": [{
                    "scheme": "create Ei: buyer.additionalIdentifiers[0].scheme",
                    "id": "create Ei: buyer.additionalIdentifiers[0].id",
                    "legalName": "create Ei: buyer.additionalIdentifiers[0].legalName",
                    "uri": "create Ei: buyer.additionalIdentifiers[0].uri"
                }],
                "contactPoint": {
                    "name": self.buyer_contact_point_name,
                    "email": self.buyer_contact_point_email,
                    "telephone": self.buyer_contact_point_telephone,
                    "faxNumber": self.buyer_contact_point_fax_number,
                    "url": self.buyer_contact_point_url
                },
                "details": {
                    "typeOfBuyer": "NATIONAL_AGENCY",
                    "mainGeneralActivity": "HEALTH",
                    "mainSectoralActivity": "WATER"
                },
                "roles": ["buyer"]
            }, {
                "id": f"{self.payer_identifier_scheme}-{self.payer_identifier_id}",
                "name": self.payer_name,
                "identifier": {
                    "scheme": self.payer_identifier_scheme,
                    "id": self.payer_identifier_id,
                    "legalName": self.payer_identifier_legal_name,
                    "uri": self.payer_identifier_uri
                },
                "address": {
                    "streetAddress": self.payer_address_street,
                    "postalCode": self.payer_address_postal_code,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.payer_address_postal_code,
                            "description": "Moldova, Republica",
                            "uri": "https://www.iso.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": self.payer_address_address_details_region_id,
                            "description": "Donduşeni",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": self.payer_address_address_details_locality_scheme,
                            "id": self.payer_address_address_details_locality_id,
                            "description": self.payer_address_address_details_locality_description,
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "additionalIdentifiers": [{
                    "scheme": "create Fs: tender.procuringEntity.additionalIdentifiers[0].scheme",
                    "id": "create Fs: tender.procuringEntity.additionalIdentifiers[0].id",
                    "legalName": "create Fs: tender.procuringEntity.additionalIdentifiers[0].legalName",
                    "uri": "create Fs: tender.procuringEntity.additionalIdentifiers[0].uri"
                }],
                "contactPoint": {
                    "name": self.payer_contact_point_name,
                    "email": self.payer_contact_point_email,
                    "telephone": self.payer_contact_point_telephone,
                    "faxNumber": self.payer_contact_point_fax_number,
                    "url": self.payer_contact_point_url
                },
                "roles": ["payer"]
            }, {
                "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                "name": self.funder_name,
                "identifier": {
                    "scheme": self.funder_identifier_scheme,
                    "id": self.funder_identifier_id,
                    "legalName": self.funder_identifier_legal_name,
                    "uri": self.funder_identifier_uri
                },
                "address": {
                    "streetAddress": self.funder_address_street,
                    "postalCode": self.funder_address_postal_code,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.funder_address_address_details_country_id,
                            "description": "Moldova, Republica",
                            "uri": "https://www.iso.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": self.funder_address_address_details_region_id,
                            "description": "Cahul",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": self.funder_address_address_details_locality_scheme,
                            "id": self.funder_address_address_details_locality_id,
                            "description": self.funder_address_address_details_locality_description,
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "additionalIdentifiers": [{
                    "scheme": "create Fs: buyer.additionalIdentifiers[0].scheme",
                    "id": "create Fs: buyer.additionalIdentifiers[0].id",
                    "legalName": "create Fs: buyer.additionalIdentifiers[0].legalName",
                    "uri": "create Fs: buyer.additionalIdentifiers[0].uri"
                }],
                "contactPoint": {
                    "name": self.funder_contact_point_name,
                    "email": self.funder_contact_point_email,
                    "telephone": self.funder_contact_point_telephone,
                    "faxNumber": self.funder_contact_point_fax,
                    "url": self.funder_contact_point_url
                },
                "roles": ["funder"]
            }, {
                "id": "MD-IDNO-4",
                "name": "create Pn: tender.procuringEntity.name",
                "identifier": {
                    "scheme": "MD-IDNO",
                    "id": "4",
                    "legalName": "create Pn: tender.procuringEntity.identigfier.legalName",
                    "uri": "create Pn: tender.procuringEntity.identifier.uri"
                },
                "address": {
                    "streetAddress": "street address",
                    "postalCode": "02232",
                    "addressDetails": {
                        "country": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["country"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['uri']
                        },
                        "region": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["region"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['uri']
                        },
                        "locality": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["locality"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['uri']
                        }
                    }
                },
                "additionalIdentifiers": [{
                    "scheme": "create Pn: tender.procuringEntity.additionalIdentifiers[0].scheme",
                    "id": "create Pn: tender.procuringEntity.additionalIdentifiers[0].id",
                    "legalName": "create Pn: tender.procuringEntity.additionalIdentifiers[0].legalName",
                    "uri": "create Pn: tender.procuringEntity.additionalIdentifiers[0].uri"
                }],
                "contactPoint": {
                    "name": "name",
                    "email": "email",
                    "telephone": "456-95-96",
                    "faxNumber": "fax-number",
                    "url": "url"
                },
                "persones": [{
                    "id": "MD-IDNO-create CNonPN: procuringEntity.persones[0].identifier.id",
                    "title": "create CNonPN: procuringEntity.persones[0].title",
                    "name": "create CNonPN: procuringEntity.persones[0].name",
                    "identifier": {
                        "scheme": "MD-IDNO",
                        "id": "create CNonPN: procuringEntity.persones[0].identifier.id",
                        "uri": "create CNonPN: procuringEntity.persones[0].identifier.uri"
                    },
                    "businessFunctions": [{
                        "id": "create CNonPN: procuringEntity.persones[0].businessFunctions[0].id",
                        "type": "procurementOfficer",
                        "jobTitle": "create CNonPN: procuringEntity.persones[0].businessFunctions[0].jobTitle",
                        "period": {
                            "startDate": period[0]
                        },
                        "documents": [{
                            "id": self.document_three_was_uploaded,
                            "documentType": "regulatoryDocument",
                            "title": "create CNonPN: procuringEntity.persones[0].businessFunctions[0].title",
                            "description": "create CNonPN: procuringEntity.persones[0].businessFunctions[0]."
                                           "description",
                            "url": f"{instance_storage_url}"
                                   f"{self.document_three_was_uploaded}",
                            "datePublished": operation_date
                        }]
                    }]
                }],
                "roles": ["procuringEntity"]
            }],
            "relatedProcesses": [{
                "id": "36b553f0-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["planning"],
                "scheme": "ocid",
                "identifier": pn_id,
                "uri": f"{instance_tender_url}{cp_id}/{pn_id}"
            }, {
                "id": "36b553f1-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["x_expenditureItem"],
                "scheme": "ocid",
                "identifier": ei_id,
                "uri": f"{instance_budget_url}{ei_id}/{ei_id}"
            }, {
                "id": "36b553f2-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["x_fundingSource"],
                "scheme": "ocid",
                "identifier": fs_id,
                "uri": f"{instance_budget_url}{ei_id}/{fs_id}"
            },
                {
                    "id": "ed0f7290-cee4-11eb-8aed-69d06bed4d57",
                    "relationship": ["x_evaluation"],
                    "scheme": "ocid",
                    "identifier": ev_id,
                    "uri": f"{instance_tender_url}{cp_id}/{ev_id}"
                }
            ]

        }
        json_notice_compiled_release_pn = {
            "ocid": pn_id,
            "id": f"{pn_id}-{ev_id[32:45]}",
            "date": f"{get_human_date_in_utc_format(int(ev_id[32:45]))[0]}",
            "tag": ["planningUpdate"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "title": "Planning Notice",
                "description": "Contracting process is planned",
                "status": "complete",
                "statusDetails": "empty",
                "items": [{
                    "id": first_item_id,
                    "internalId": "create Pn: tender.items[0].internalId",
                    "description": "create Pn: tender.items[0].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_first_item_cpv_code[0],
                        "description": get_value_by_first_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_first_item_cpvs_code[0],
                        "description": get_value_by_first_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_first_item_unit_id[0],
                        "name": get_value_by_first_item_unit_id[1]
                    },
                    "relatedLot": first_lot_id
                }, {
                    "id": second_item_id,
                    "internalId": "create Pn: tender.items[1].internalId",
                    "description": "create Pn: tender.items[1].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_second_item_cpv_code[0],
                        "description": get_value_by_second_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_second_item_cpvs_code[0],
                        "description": get_value_by_second_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_second_item_unit_id[0],
                        "name": get_value_by_second_item_unit_id[1]
                    },
                    "relatedLot": second_lot_id
                }],
                "lots": [{
                    "id": first_lot_id,
                    "internalId": "create Pn: tender.lots[0].internalId",
                    "title": "create Pn: tender.lots[0].title",
                    "description": "create Pn: tender.lots[0].internalId.description",
                    "status": "planning",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 1500.00,
                        "currency": "EUR"
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
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[0].placeOfPerformance.address.streetAddress",
                            "postalCode": "create Pn: tender.lots[0].placeOfPerformance.address.postalCode",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        },
                        "description": "create Pn: tender.lots[0].placeOfPerformance.description"
                    },
                    "options": [{
                        "hasOptions": False
                    }]
                }, {
                    "id": second_lot_id,
                    "internalId": "create Pn: tender.lots[1].internalId",
                    "title": "create Pn: tender.lots[1].title",
                    "description": "create Pn: tender.lots[1].internalId.description",
                    "status": "planning",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 150.00,
                        "currency": "EUR"
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
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[1].placeOfPerformance.address.streetAddress",
                            "postalCode": "create Pn: tender.lots[1].placeOfPerformance.address.postalCode",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        },
                        "description": "create Pn: tender.lots[1].placeOfPerformance.description"
                    },
                    "options": [{
                        "hasOptions": False
                    }]
                }],
                "lotGroups": [{
                    "optionToCombine": False
                }],
                "tenderPeriod": {
                    "startDate": period[3]
                },
                "hasEnquiries": False,
                "documents": [
                    {
                        "id": self.document_one_was_uploaded,
                        "documentType": "contractArrangements",
                        "title": "title of document",
                        "description": "descrition of document",
                        "url": f"{instance_storage_url}"
                               f"{self.document_one_was_uploaded}",
                        "datePublished": f"{get_human_date_in_utc_format(int(pn_id[32:45]))[0]}",
                        "relatedLots": [first_lot_id]
                    },
                    {
                        "id": self.document_two_was_uploaded,
                        "documentType": "contractArrangements",
                        "title": "title of document",
                        "description": "descrition of document",
                        "url": f"{instance_storage_url}"
                               f"{self.document_two_was_uploaded}",
                        "datePublished": f"{get_human_date_in_utc_format(int(pn_id[32:45]))[0]}",
                        "relatedLots": [second_lot_id]
                    }],
                "submissionMethod": ["electronicSubmission"],
                "submissionMethodDetails": submission_method_details,
                "submissionMethodRationale": submission_method_rationale,
                "requiresElectronicCatalogue": False,
                "procurementMethodRationale": "create Pn: tender.procurementMethodRationale",
                "classification": {
                    "scheme": "CPV",
                    "id": get_value_by_new_cpv_code[0],
                    "description": get_value_by_new_cpv_code[1]
                },
                "value": {
                    "amount": 1650.00,
                    "currency": "EUR"
                }
            },
            "hasPreviousNotice": False,
            "purposeOfNotice": {
                "isACallForCompetition": False
            },
            "relatedProcesses": [{
                "id": "36b553f3-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": cp_id,
                "uri": f"{instance_tender_url}{cp_id}/{cp_id}"
            }]
        }
        json_notice_compiled_release_ev = {
            "ocid": ev_id,
            "id": f"{ev_id}-{period_for_amendment[1]}",
            "date": period_for_amendment[0],
            "tag": ["tender"],
            "initiationType": "tender",
            "language": self.lang,
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "title": "Evaluation",
                "description": "Evaluation stage of contracting process",
                "status": "active",
                "statusDetails": "clarification",
                "criteria": [{
                    "id": "58b814dc-ada7-40f1-b34e-fcb360830c2c",
                    "title": "create CNonPN: tender.criteria[0].title =Bankruptcy",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[0].description =Is the economic operator "
                                   "bankrupt? This information needs not be given if exclusion of economic "
                                   "operators in this case has been made mandatory under the applicable national "
                                   "law without any possibility of derogation where the economic operator is "
                                   "nevertheless able to perform the contract.",
                    "requirementGroups": [{
                        "id": "2f16e84f-aca2-4970-8a9a-6f253d20f8b3",
                        "description": "create CNonPN: tender.criteria[0].requirementGroups[0].description "
                                       "=approve that Bankruptcy requirement group",
                        "requirements": [{
                            "id": "01fcb528-6de6-4c07-9383-57c698116f18",
                            "title": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements.title",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "description": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements."
                                           "description",
                            "eligibleEvidences": [{
                                "id": "1",
                                "title": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements[0]."
                                         "eligibleEvidences[0].title",
                                "type": "document",
                                "description": "create CNonPN: tender.criteria[0].requirementGroups[0]."
                                               "requirements[0].eligibleEvidences[0].description",
                                "relatedDocument": {
                                    "id": self.document_three_was_uploaded
                                }
                            }, {
                                "id": "2",
                                "title": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements[0]."
                                         "eligibleEvidences[1].title",
                                "type": "document",
                                "description": "create CNonPN: tender.criteria[0].requirementGroups[0]."
                                               "requirements[0].eligibleEvidences[1].description",
                                "relatedDocument": {
                                    "id": self.document_three_was_uploaded
                                }
                            }],
                            "expectedValue": False
                        }]
                    }],
                    "relatesTo": "tender",
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.EXCLUSION.CONVICTIONS.PARTICIPATION_IN_CRIMINAL_ORGANISATION"
                    }
                }, {
                    "id": "a662195e-ad48-4ffc-9b51-7b01a3c04be0",
                    "title": "create CNonPN: tender.criteria[1].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[1].description",
                    "requirementGroups": [{
                        "id": "9ebb3a38-7835-48e2-84d5-c1debb0a4739",
                        "description": "create CNonPN: tender.criteria[1].requirementGroups[0].description",
                        "requirements": [{
                            "id": "1a149ebc-5d0c-4dd6-92b3-85ed9672a675",
                            "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[0].title",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "description": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements."
                                           "description",
                            "expectedValue": True
                        }, {
                            "id": "a4b456bb-32a6-4946-adf7-2ddaeb282c0e",
                            "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[1]."
                                     "title =The number of years for proposed product warranty",
                            "dataType": "number",
                            "status": "active",
                            "datePublished": operation_date,
                            "description": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements"
                                           "[1].description",
                            "period": {
                                "startDate": period[0],
                                "endDate": period[1]
                            },
                            "eligibleEvidences": [{
                                "id": "3",
                                "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[1]."
                                         "eligibleEvidences[0].title",
                                "type": "document",
                                "description": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements"
                                               "[1].eligibleEvidences[0].description",
                                "relatedDocument": {
                                    "id": self.document_three_was_uploaded
                                }
                            }],
                            "minValue": 1.000,
                            "maxValue": 3.000
                        }]
                    }],
                    "relatesTo": "lot",
                    "relatedItem": first_lot_id,
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.SELECTION.ECONOMIC_FINANCIAL_STANDING.TURNOVER.GENERAL_YEARLY"
                    }
                }, {
                    "id": "8e250762-2508-4175-af7e-1a5ca085a1e7",
                    "title": "create CNonPN: tender.criteria[2].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[2].description",
                    "requirementGroups": [{
                        "id": "ff3545aa-47ec-4666-8c8a-93c6e06f85d8",
                        "description": "create CNonPN: tender.criteria[2].requirementGroups[0].description",
                        "requirements": [{
                            "id": "e3f5ecdb-985d-42a0-97ca-85920a819095",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[0].requirements[0]."
                                     "title =Product has to be manufactured in the EU",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "expectedValue": True
                        }, {
                            "id": "22b9bb1f-692d-425a-bd11-3f4569ae35f3",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[0]..requirements[1]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }, {
                        "id": "31359580-435e-40d5-9a17-a40d03686a17",
                        "description": "create CNonPN: tender.criteria[2].requirementGroups[1].description",
                        "requirements": [{
                            "id": "9daba23f-510d-4f7f-a449-af17a3416081",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[1].requirements[0]."
                                     "title =Product has to be manufactured in the EU",
                            "dataType": "boolean",
                            "status": "active",
                            "datePublished": operation_date,
                            "expectedValue": True
                        }, {
                            "id": "03fc9deb-f9ca-4dcf-a9f0-e1dff43c6e42",
                            "title": "create CNonPN: tender.criteria[2].requirementGroups[1]..requirements[1]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }],
                    "relatesTo": "tenderer",
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.EXCLUSION.NATIONAL.OTHER"
                    }
                }, {
                    "id": "43fe2c58-14eb-47aa-9854-cbf594b1110e",
                    "title": "create CNonPN: tender.criteria[3].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[3].description =A minimum product warranty "
                                   "of 1 year is required for all bids 2",
                    "requirementGroups": [{
                        "id": "f18230c4-04e9-41af-b900-1a6521011c20",
                        "description": "create CNonPN: tender.criteria[3].requirementGroups[0].description",
                        "requirements": [{
                            "id": "25fe2901-8393-4198-88fc-01625039c48f",
                            "title": "create CNonPN: tender.criteria[3].requirementGroups[0].requirements[0]."
                                     "title = The number of years for proposed product warranty",
                            "dataType": "number",
                            "status": "active",
                            "datePublished": operation_date,
                            "period": {
                                "startDate": period[0],
                                "endDate": period[1]
                            },
                            "minValue": 1.000,
                            "maxValue": 3.000
                        }]
                    }],
                    "relatesTo": "item",
                    "relatedItem": first_item_id,
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.OTHER.EO_DATA.RELIES_ON_OTHER_CAPACITIES"
                    }
                }, {
                    "id": "5c8c1ce9-937c-41c6-a717-42db617da57b",
                    "title": "create CNonPN: tender.criteria[4].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[4].description",
                    "requirementGroups": [{
                        "id": "05f1412a-8cef-4534-b02f-2ecb8b82a34d",
                        "description": "create CNonPN: tender.criteria[4].requirementGroups[0].description",
                        "requirements": [{
                            "id": "4fde10c0-306f-4170-bc90-9290935c8ae1",
                            "title": "create CNonPN: tender.criteria[4].requirementGroups[0].requirements[0]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }],
                    "relatesTo": "tender",
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.EXCLUSION.NATIONAL.OTHER"
                    }
                }, {
                    "id": "6af5e886-b24d-4fa0-9e02-62c44833e609",
                    "title": "create CNonPN: tender.criteria[4].title",
                    "source": "tenderer",
                    "description": "create CNonPN: tender.criteria[4].description",
                    "requirementGroups": [{
                        "id": "37fbcb8c-3cb5-4447-9597-04f161590ecd",
                        "description": "create CNonPN: tender.criteria[4].requirementGroups[0].description",
                        "requirements": [{
                            "id": "fb28d72b-4136-4535-8d5b-c0fae7a3bfcf",
                            "title": "create CNonPN: tender.criteria[4].requirementGroups[0].requirements[0]."
                                     "title =Country of origin",
                            "dataType": "string",
                            "status": "active",
                            "datePublished": operation_date
                        }]
                    }],
                    "relatesTo": "tender",
                    "classification": {
                        "scheme": "ESPD",
                        "id": "CRITERION.OTHER.EO_DATA.RELIES_ON_OTHER_CAPACITIES"
                    }
                }],
                "conversions": [{
                    "id": "72b46408-c9d1-40ff-ba93-ee8fdfa2a0f1",
                    "relatesTo": "requirement",
                    "relatedItem": "1a149ebc-5d0c-4dd6-92b3-85ed9672a675",
                    "rationale": "create CNonPN: tender.conversions[1].rationale",
                    "description": "create CNonPN: tender.conversions[1].description",
                    "coefficients": [{
                        "id": "05690b92-24b7-4422-9816-17fe8e3ed13b",
                        "value": False,
                        "coefficient": 1
                    }]
                }, {
                    "id": "7a93bc3b-f061-4f3b-a95a-9950bd577dcf",
                    "relatesTo": "requirement",
                    "relatedItem": "a4b456bb-32a6-4946-adf7-2ddaeb282c0e",
                    "rationale": "create CNonPN: tender.conversions[3].rationale",
                    "description": "create CNonPN: tender.conversions[3].description",
                    "coefficients": [{
                        "id": "0c8079ec-3c0e-4563-85f1-992975f7e04b",
                        "value": 1.000,
                        "coefficient": 1
                    }, {
                        "id": "f6f95e95-59af-42c1-9bc8-ecefcef27e7b",
                        "value": 2.000,
                        "coefficient": 1
                    }, {
                        "id": "a95aebf9-2d2c-41fa-9b43-1535682b20e8",
                        "value": 3.000,
                        "coefficient": 0.93
                    }]
                }, {
                    "id": "1b994f29-3341-4d21-a63a-22d430d40a13",
                    "relatesTo": "requirement",
                    "relatedItem": "25fe2901-8393-4198-88fc-01625039c48f",
                    "rationale": "create CNonPN: tender.conversions[6].rationale",
                    "description": "create CNonPN: tender.conversions[6].description",
                    "coefficients": [{
                        "id": "f25d0cf9-4787-44d7-b4b8-93e8db5a35c2",
                        "value": 1.000,
                        "coefficient": 1
                    }, {
                        "id": "ee713dff-62cd-4a36-abe3-53b332ed163d",
                        "value": 2.000,
                        "coefficient": 1
                    }, {
                        "id": "e1b625e7-28f1-4114-bf97-a5d5a4b4aaae",
                        "value": 3.000,
                        "coefficient": 0.93
                    }]
                }, {
                    "id": "4735af2c-766a-4c9a-891c-f2a84b5cb1b2",
                    "relatesTo": "requirement",
                    "relatedItem": "fb28d72b-4136-4535-8d5b-c0fae7a3bfcf",
                    "rationale": "create CNonPN: tender.conversions[6].rationale",
                    "description": "create CNonPN: tender.conversions[6].description",
                    "coefficients": [{
                        "id": "16acc108-d7cb-4ea4-af1c-c8bad67bda86",
                        "value": "option_1",
                        "coefficient": 1
                    }, {
                        "id": "231b3997-4c5f-4886-ae1d-1bd458801d54",
                        "value": "option_2",
                        "coefficient": 1
                    }, {
                        "id": "d248589c-55a4-4f74-817b-ddc7f8291805",
                        "value": "option_3",
                        "coefficient": 0.93
                    }]
                }],
                "items": [{
                    "id": first_item_id,
                    "internalId": "create Pn: tender.items[0].internalId",
                    "description": "create Pn: tender.items[0].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_first_item_cpv_code[0],
                        "description": get_value_by_first_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_first_item_cpvs_code[0],
                        "description": get_value_by_first_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_first_item_unit_id[0],
                        "name": get_value_by_first_item_unit_id[1]
                    },
                    "relatedLot": first_lot_id
                }, {
                    "id": second_item_id,
                    "internalId": "create Pn: tender.items[1].internalId",
                    "description": "create Pn: tender.items[1].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_second_item_cpv_code[0],
                        "description": get_value_by_second_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_second_item_cpvs_code[0],
                        "description": get_value_by_second_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_second_item_unit_id[0],
                        "name": get_value_by_second_item_unit_id[1]
                    },
                    "relatedLot": second_lot_id
                }],
                "lots": [{
                    "id": first_lot_id,
                    "internalId": "create Pn: tender.lots[0].internalId",
                    "title": "create Pn: tender.lots[0].title",
                    "description": "create Pn: tender.lots[0].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 1500.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[0].placeOfPerformance.address.streetAddress",
                            "postalCode": "create Pn: tender.lots[0].placeOfPerformance.address.postalCode",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        },
                        "description": "create Pn: tender.lots[0].placeOfPerformance.description"
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }, {
                    "id": second_lot_id,
                    "internalId": "create Pn: tender.lots[1].internalId",
                    "title": "create Pn: tender.lots[1].title",
                    "description": "create Pn: tender.lots[1].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 150.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[1].placeOfPerformance.address.streetAddress",
                            "postalCode": "create Pn: tender.lots[1].placeOfPerformance.address.postalCode",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        },
                        "description": "create Pn: tender.lots[1].placeOfPerformance.description"
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }],
                "lotGroups": [{
                    "optionToCombine": False
                }],
                "tenderPeriod": {
                    "startDate": enquiry_and_tender_period[2],
                    "endDate": enquiry_and_tender_period[3]
                },
                "enquiryPeriod": {
                    "startDate": enquiry_and_tender_period[0],
                    "endDate": enquiry_and_tender_period[1]
                },
                "auctionPeriod": {
                    "startDate": auction_date
                },
                "hasEnquiries": False,
                "amendments": [{
                    "id": self.amendment_id,
                    "type": "cancellation",
                    "status": "pending",
                    "relatesTo": "lot",
                    "relatedItem": lot_id,
                    "date": period_for_amendment[0],
                    "description": "cancel_tender: amendments[0].description",
                    "rationale": "cancel_tender: amendments[0].rationale",
                    "documents": [{
                        "documentType": "cancellationDetails",
                        "id": self.document_five_was_uploaded,
                        "title": "cancel_tender: amendments[0].documents[0].title",
                        "description": "cancel_tender: amendments[0].documents[0].description",
                        "url": f"{instance_storage_url}"
                               f"{self.document_five_was_uploaded}",
                        "datePublished": period[0]
                    }]
                }],
                "documents": [{
                    "id": self.document_one_was_uploaded,
                    "documentType": "contractArrangements",
                    "title": "create Pn: tender.documents[0].title",
                    "description": "create Pn: tender.documents[0].description",
                    "url": f"{instance_storage_url}{self.document_one_was_uploaded}",
                    "datePublished": operation_date,
                    "relatedLots": [first_lot_id]
                }, {
                    "id": self.document_two_was_uploaded,
                    "documentType": "contractArrangements",
                    "title": "create Pn: tender.documents[1].title",
                    "description": "create Pn: tender.documents[1].description",
                    "url": f"{instance_storage_url}"
                           f"{self.document_two_was_uploaded}",
                    "datePublished": operation_date,
                    "relatedLots": [second_lot_id]
                }, {
                    "id": self.document_three_was_uploaded,
                    "documentType": "illustration",
                    "title": "create CNonPN: tender.documents[2].title",
                    "description": "create CNonPN: tender.documents[2].description",
                    "url": f"{instance_storage_url}"
                           f"{self.document_three_was_uploaded}",
                    "datePublished": operation_date,
                    "relatedLots": [first_lot_id]
                }],
                "awardCriteria": "ratedCriteria",
                "awardCriteriaDetails": "automated",
                "submissionMethod": ["electronicSubmission"],
                "submissionMethodDetails": submission_method_details,
                "submissionMethodRationale": submission_method_rationale,
                "requiresElectronicCatalogue": False,
                "procurementMethodModalities": ["electronicAuction"],
                "electronicAuctions": {
                    "details": [{
                        "id": "9f8c8d7c-127a-42ab-b72d-d215e5cc6b40",
                        "relatedLot": first_lot_id,
                        "auctionPeriod": {
                            "startDate": auction_date
                        },
                        "electronicAuctionModalities": [{
                            "url": f"https://eauction.eprocurement.systems/auctions/{ev_id}/{first_lot_id}",
                            "eligibleMinimumDifference": {
                                "amount": 100.00,
                                "currency": "EUR"
                            }
                        }]
                    }, {
                        "id": "5f2caa86-b76b-410f-b181-8528b233f43c",
                        "relatedLot": second_lot_id,
                        "auctionPeriod": {
                            "startDate": auction_date
                        },
                        "electronicAuctionModalities": [{
                            "url": f"https://eauction.eprocurement.systems/auctions/{ev_id}/{second_lot_id}",
                            "eligibleMinimumDifference": {
                                "amount": 10.00,
                                "currency": "EUR"
                            }
                        }]
                    }]
                },
                "procurementMethodRationale": "create CNonPN: tender.procurementMethodRationale"
            },
            "hasPreviousNotice": True,
            "purposeOfNotice": {
                "isACallForCompetition": True
            },
            "relatedProcesses": [{
                "id": "e84a2253-cee4-11eb-8aed-69d06bed4d57",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": cp_id,
                "uri": f"{instance_tender_url}{cp_id}/{cp_id}"
            }, {
                "id": "ed0f7291-cee4-11eb-8aed-69d06bed4d57",
                "relationship": ["planning"],
                "scheme": "ocid",
                "identifier": pn_id,
                "uri": f"{instance_tender_url}/{cp_id}/{pn_id}"
            }]
        }

        kafka = Kafka(instance=self.instance)
        kafka.connect_kafka_producer()
        kafka.publish_message_into_chronograph_in_clarification(
            cp_id=cp_id,
            ev_id=ev_id,
            enquiry_end=enquiry_and_tender_period[1]
        )
        kafka.publish_message_into_chronograph_in_submission(
            cp_id=cp_id,
            ev_id=ev_id,
            tender_end=enquiry_and_tender_period[3]
        )

        key_space_ocds.execute(f"INSERT INTO orchestrator_context (cp_id,context) VALUES ("
                               f"'{ev_id}','{json.dumps(json_orchestrator_context)}');").one()
        key_space_access.execute(f"INSERT INTO tenders (cpid, ocid, token_entity,created_date,json_data, owner) "
                                 f"VALUES ('{cp_id}', '{ev_id}', '{pn_token}', {ev_id[32:45]}, "
                                 f"'{json.dumps(json_access_tender)}','{owner}');").one()
        key_space_auctions.execute(
            f"INSERT INTO auctions (cpid, ocid, api_version, country, data, operation_id, row_version, status ) "
            f"VALUES ('{cp_id}', '{ev_id}', '1.0.0', '{self.country}', '{json.dumps(json_auction_auctions)}', "
            f"'{uuid.uuid1()}',{0}, {1});").one()
        key_space_clarification.execute(
            f"INSERT INTO periods (cpid, ocid, end_date, owner, start_date) "
            f"VALUES ('{cp_id}', '{ev_id}', {get_timestamp_from_human_date(enquiry_and_tender_period[1])}, '{owner}', "
            f"{ev_id[32:45]});").one()
        key_space_submission.execute(
            f"INSERT INTO periods (cpid, ocid, end_date, start_date) "
            f"VALUES ('{cp_id}', '{ev_id}', {get_timestamp_from_human_date(enquiry_and_tender_period[3])}, "
            f"{get_timestamp_from_human_date(enquiry_and_tender_period[1])});").one()
        key_space_ocds.execute(f"INSERT INTO notice_offset (cp_id,release_date, stage, status) "
                               f"VALUES ('{cp_id}', {ev_id[32:45]}, 'EV', 'active');").one()
        key_space_ocds.execute(
            f"INSERT INTO notice_release (cp_id,oc_id, release_id, json_data, release_date, stage) "
            f"VALUES ('{cp_id}', '{cp_id}', '{cp_id + '-' + ev_id[32:45]}' ,'{json.dumps(json_notice_release_ms)}',"
            f"{ev_id[32:45]},'');").one()
        key_space_ocds.execute(
            f"INSERT INTO notice_release (cp_id,oc_id, release_id, json_data, release_date, stage) "
            f"VALUES ('{cp_id}', '{pn_id}', '{pn_id + '-' + ev_id[32:45]}' ,'{json.dumps(json_notice_release_pn)}',"
            f"{ev_id[32:45]},'PN');").one()
        key_space_ocds.execute(
            f"INSERT INTO notice_release (cp_id,oc_id, release_id, json_data, release_date, stage) "
            f"VALUES ('{cp_id}', '{ev_id}', '{ev_id + '-' + ev_id[32:45]}','{json.dumps(json_notice_release_ev)}',"
            f"{ev_id[32:45]},'EV');").one()
        key_space_ocds.execute(
            f"INSERT INTO notice_release (cp_id,oc_id, release_id, json_data, release_date, stage) "
            f"VALUES ('{cp_id}', '{ev_id}', '{ev_id + '-' + str(period_for_amendment[1])}',"
            f"'{json.dumps(json_notice_release_ev_new)}',"
            f"{period_for_amendment[1]},'EV');").one()

        key_space_ocds.execute(
            f"INSERT INTO notice_compiled_release (cp_id,oc_id, json_data, publish_date, release_date, "
            f"release_id, stage, status) VALUES ('{cp_id}', '{cp_id}', '{json.dumps(json_notice_compiled_release_ms)}',"
            f"{ev_id[32:45]},{ev_id[32:45]}, '{cp_id + '-' + ev_id[32:45]}','', 'active');").one()
        key_space_ocds.execute(
            f"INSERT INTO notice_compiled_release (cp_id,oc_id, json_data, publish_date, release_date, "
            f"release_id, stage, status) VALUES ('{cp_id}', '{pn_id}', '{json.dumps(json_notice_compiled_release_pn)}',"
            f"{ev_id[32:45]},{ev_id[32:45]}, '{pn_id + '-' + ev_id[32:45]}','PN', 'active');").one()
        key_space_revision.execute(f"INSERT INTO amendments (cpid, ocid, id, data) "
                                   f"VALUES ('{cp_id}', '{ev_id}', {self.amendment_id}, "
                                   f"'{json.dumps(json_amendments)}');").one()

        key_space_ocds.execute(f"INSERT INTO notice_offset (cp_id,release_date, stage, status) "
                               f"VALUES ('{cp_id}', {period_for_amendment[1]}, 'EV', 'active');").one()

        key_space_ocds.execute(
            f"INSERT INTO notice_compiled_release (cp_id,oc_id, json_data, publish_date, release_date, "
            f"release_id, stage, status) VALUES ('{cp_id}', '{ev_id}', '{json.dumps(json_notice_compiled_release_ev)}',"
            f"{period[2]},{period_for_amendment[1]}, '{ev_id + '-' + str(period_for_amendment[1])}','EV', "
            f"'active');").one()
        record = f"{instance_tender_url}{cp_id}"
        ms_release = f"{instance_tender_url}{cp_id}/{cp_id}"
        pn_release = f"{instance_tender_url}{cp_id}/{pn_id}"
        ev_release = f"{instance_tender_url}{cp_id}/{ev_id}"
        return cp_id, pn_id, pn_token, ev_id, record, ms_release, pn_release, ev_release, self.amendment_id, \
               self.amendment_token

    @allure.step('Insert CnOnPn: based on FS: treasury - obligatory, based on EI: without items - obligatory')
    def insert_cancel_lot_obligatory(self, first_lot_id, second_lot_id, first_item_id, second_item_id,
                                     second_tender, second_enquiry, lot_id):
        auth_provider = PlainTextAuthProvider(username=self.cassandra_username, password=self.cassandra_password)
        cluster = Cluster([self.cassandra_cluster], auth_provider=auth_provider)
        key_space_ocds = cluster.connect('ocds')
        key_space_access = cluster.connect('access')
        key_space_clarification = cluster.connect('clarification')
        key_space_submission = cluster.connect('submission')
        key_space_revision = cluster.connect('revision')
        owner = "445f6851-c908-407d-9b45-14b92f3e964b"
        ei_id = prepared_cp_id()
        fs_id = prepared_fs_oc_id(ei_id)
        cp_id = prepared_cp_id()
        pn_id = prepared_pn_oc_id(cp_id)
        pn_token = uuid4()
        ev_id = prepared_cn_oc_id(cp_id)
        period = get_period()
        period_for_amendment = get_period_for_amendment()
        contract_period = get_contract_period()
        enquiry_and_tender_period = create_enquiry_and_tender_period(
            second_enquiry=second_enquiry,
            second_tender=second_tender
        )

        operation_date = time_at_now()
        calculate_new_cpv_code = get_new_classification_id(
            self.first_item_cpv,
            self.second_item_cpv
        )
        get_value_by_new_cpv_code = get_value_from_classification_cpv_dictionary_xls(
            calculate_new_cpv_code,
            self.lang
        )
        get_value_by_first_item_cpv_code = get_value_from_classification_cpv_dictionary_xls(
            self.first_item_cpv,
            self.lang
        )
        get_value_by_second_item_cpv_code = get_value_from_classification_cpv_dictionary_xls(
            self.second_item_cpv,
            self.lang
        )
        get_value_by_first_item_cpvs_code = get_value_from_cpvs_dictionary_csv(
            self.first_item_additional_classifications,
            self.lang
        )
        get_value_by_second_item_cpvs_code = get_value_from_cpvs_dictionary_csv(
            self.second_item_additional_classifications,
            self.lang
        )
        get_value_by_first_item_unit_id = get_value_from_classification_unit_dictionary_csv(
            self.first_item_unit_id,
            self.lang
        )
        get_value_by_second_item_unit_id = get_value_from_classification_unit_dictionary_csv(
            self.second_item_unit_id,
            self.lang
        )

        mdm = MdmService(
            instance=self.instance
        )
        data_pn = mdm.process_tender_data(self.pmd).json()
        submission_method_details = data_pn["data"]["tender"]["submissionMethodDetails"]
        submission_method_rationale = data_pn["data"]["tender"]["submissionMethodRationale"]

        procurement_method_details_from_mdm = data_pn["data"]["tender"]["procurementMethodDetails"]
        eligibility_criteria_from_mdm = data_pn["data"]["tender"]["eligibilityCriteria"]
        instance_tender_url = None
        instance_budget_url = None
        instance_storage_url = None
        if self.instance == "dev":
            instance_tender_url = "http://dev.public.eprocurement.systems/tenders/"
            instance_budget_url = "http://dev.public.eprocurement.systems/budgets/"
            instance_storage_url = "https://dev.bpe.eprocurement.systems/api/v1/storage/get/"
        if self.instance == "sandbox":
            instance_tender_url = "http://public.eprocurement.systems/tenders/"
            instance_budget_url = "http://public.eprocurement.systems/budgets/"
            instance_storage_url = "http://storage.eprocurement.systems/get/"
        json_orchestrator_context = {
            "cpid": cp_id,
            "ocid": ev_id,
            "operationId": f"{uuid4()}",
            "requestId": f"{uuid4()}",
            "owner": owner,
            "stage": "EV",
            "prevStage": "EV",
            "phase": "clarification",
            "processType": "cancelLot",
            "operationType": "lotCancellation",
            "country": self.country,
            "language": self.lang,
            "pmd": self.pmd,
            "startDate": period_for_amendment[0],
            "timeStamp": period_for_amendment[1],
            "isAuction": False
        }

        json_access_tender = {
            "ocid": cp_id,
            "planning": {
                "budget": {
                    "amount": {
                        "amount": 2000.00,
                        "currency": "EUR"
                    },
                    "isEuropeanUnionFunded": False,
                    "budgetBreakdown": [{
                        "id": fs_id,
                        "amount": {
                            "amount": 2000.00,
                            "currency": "EUR"
                        },
                        "period": {
                            "startDate": period[0],
                            "endDate": period[1]
                        },
                        "sourceParty": {
                            "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                            "name": self.buyer_name,
                        }
                    }]
                }
            },
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "status": "active",
                "statusDetails": "clarification",
                "title": "create Pn: tender.title",
                "description": "create Pn: tender.description",
                "classification": {
                    "scheme": "CPV",
                    "id": get_value_by_new_cpv_code[0],
                    "description": get_value_by_new_cpv_code[1]
                },
                "tenderPeriod": {
                    "startDate": enquiry_and_tender_period[2],
                    "endDate": enquiry_and_tender_period[3]
                },
                "enquiryPeriod": {
                    "startDate": enquiry_and_tender_period[0],
                    "endDate": enquiry_and_tender_period[1]
                },
                "acceleratedProcedure": {
                    "isAcceleratedProcedure": False
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
                "procedureOutsourcing": {
                    "procedureOutsourced": False
                },
                "framework": {
                    "isAFramework": False
                },
                "dynamicPurchasingSystem": {
                    "hasDynamicPurchasingSystem": False
                },
                "legalBasis": "DIRECTIVE_2014_25_EU",
                "procurementMethod": "open",
                "procurementMethodDetails": procurement_method_details_from_mdm,
                "mainProcurementCategory": "works",
                "eligibilityCriteria": eligibility_criteria_from_mdm,
                "contractPeriod": {
                    "startDate": contract_period[0],
                    "endDate": contract_period[1]
                },
                "procuringEntity": {
                    "id": "MD-IDNO-4",
                    "name": "create Pn: tender.procuringEntity.name",
                    "identifier": {
                        "scheme": "MD-IDNO",
                        "id": "4",
                        "legalName": "create Pn: tender.procuringEntity.identifier.legalName"
                    },
                    "address": {
                        "streetAddress": "create Pn: tender.procuringEntity.address.streetAddress",
                        "addressDetails": {
                            "country": {
                                "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "country"]['scheme'],
                                "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "country"]['id'],
                                "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                    "addressDetails"]["country"]['description'],
                                "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "country"]['uri']
                            },
                            "region": {
                                "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "region"]['scheme'],
                                "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "region"]['id'],
                                "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                    "addressDetails"]["region"]['description'],
                                "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "region"]['uri']
                            },
                            "locality": {
                                "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "locality"]['scheme'],
                                "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "locality"]['id'],
                                "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                    "addressDetails"]["locality"]['description'],
                                "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                    "locality"]['uri']

                            }
                        }
                    },
                    "contactPoint": {
                        "name": "create Pn: tender.procuringEntity.contactPoint.name",
                        "email": "create Pn: tender.procuringEntity.contactPoint.email",
                        "telephone": "create Pn: tender.procuringEntity.contactPoint.telephone"
                    }
                },
                "value": {
                    "amount": 1650.00,
                    "currency": "EUR"
                },
                "lotGroups": [{
                    "optionToCombine": False
                }],
                "lots": [{
                    "id": first_lot_id,
                    "title": "create Pn: tender.lots[0].title",
                    "description": "create Pn: tender.lots[0].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 1500.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[0].placeOfPerformance.address.streetAddress",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][0]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        }
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }, {
                    "id": second_lot_id,
                    "title": "create Pn: tender.lots[1].title",
                    "description": "create Pn: tender.lots[1].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 150.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[1].placeOfPerformance.address.streetAddress",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        }
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }],
                "items": [{
                    "id": first_item_id,
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_first_item_cpv_code[0],
                        "description": get_value_by_first_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_first_item_cpvs_code[0],
                        "description": get_value_by_first_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_first_item_unit_id[0],
                        "name": get_value_by_first_item_unit_id[1]
                    },
                    "description": "create Pn: tender.items[0].description",
                    "relatedLot": first_lot_id
                }, {
                    "id": second_item_id,
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_second_item_cpv_code[0],
                        "description": get_value_by_second_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_second_item_cpvs_code[0],
                        "description": get_value_by_second_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_second_item_unit_id[0],
                        "name": get_value_by_second_item_unit_id[1]
                    },
                    "description": "create Pn: tender.items[1].description",
                    "relatedLot": second_lot_id
                }],
                "awardCriteria": "ratedCriteria",
                "awardCriteriaDetails": "automated",
                "requiresElectronicCatalogue": False,
                "submissionMethod": ["electronicSubmission"],
                "submissionMethodRationale": submission_method_rationale,
                "submissionMethodDetails": submission_method_details,
                "documents": [
                    {
                        "id": self.document_three_was_uploaded,
                        "documentType": "evaluationCriteria",
                        "title": "create CNonPN: tender.documents[2].title"
                    }
                ]
            }
        }
        json_amendments = {
            "id": self.amendment_id,
            "date": period_for_amendment[0],
            "rationale": "cancel_tender: amendments[0].rationale",
            "status": "pending",
            "type": "cancellation",
            "relatesTo": "lot",
            "relatedItem": lot_id,
            "token": self.amendment_token,
            "owner": "445f6851-c908-407d-9b45-14b92f3e964b"
        }
        json_notice_release_ms = {
            "ocid": cp_id,
            "id": f"{cp_id}-{ev_id[32:45]}",
            "date": f"{get_human_date_in_utc_format(int(ev_id[32:45]))[0]}",
            "tag": ["compiled"],
            "language": self.lang,
            "initiationType": "tender",
            "planning": {
                "budget": {
                    "amount": {
                        "amount": 2000.00,
                        "currency": "EUR"
                    },
                    "isEuropeanUnionFunded": False,
                    "budgetBreakdown": [{
                        "id": fs_id,
                        "amount": {
                            "amount": 2000.00,
                            "currency": "EUR"
                        },
                        "period": {
                            "startDate": period[0],
                            "endDate": period[1]
                        },
                        "sourceParty": {
                            "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                            "name": self.buyer_name,
                        }
                    }]
                }
            },
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "title": "create Pn: tender.title",
                "description": "create Pn: tender.description",
                "status": "active",
                "statusDetails": "evaluation",
                "value": {
                    "amount": 1650.00,
                    "currency": "EUR"
                },
                "procurementMethod": "open",
                "procurementMethodDetails": procurement_method_details_from_mdm,
                "mainProcurementCategory": "works",
                "hasEnquiries": False,
                "eligibilityCriteria": eligibility_criteria_from_mdm,
                "contractPeriod": {
                    "startDate": contract_period[0],
                    "endDate": contract_period[1]
                },
                "procuringEntity": {
                    "id": "MD-IDNO-4",
                    "name": "create Pn: tender.procuringEntity.name"
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
                "legalBasis": "DIRECTIVE_2014_25_EU",
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
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name,
                "identifier": {
                    "scheme": self.buyer_identifier_scheme,
                    "id": self.buyer_identifier_id,
                    "legalName": self.buyer_identifier_legal_name
                },
                "address": {
                    "streetAddress": self.buyer_address_street_address,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.buyer_address_address_details_country_id,
                            "description": "Moldova, Republica",
                            "uri": "https://www.iso.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": self.buyer_address_address_details_region_id,
                            "description": "Cahul",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": self.buyer_address_address_details_locality_scheme,
                            "id": self.buyer_address_address_details_locality_id,
                            "description": self.buyer_address_address_details_locality_description,
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "contactPoint": {
                    "name": self.buyer_contact_point_name,
                    "email": self.buyer_contact_point_email,
                    "telephone": self.buyer_contact_point_telephone
                },
                "roles": [
                    "buyer"]
            }, {
                "id": f"{self.payer_identifier_scheme}-{self.payer_identifier_id}",
                "name": self.payer_name,
                "identifier": {
                    "scheme": self.payer_identifier_scheme,
                    "id": self.payer_identifier_id,
                    "legalName": self.payer_identifier_legal_name
                },
                "address": {
                    "streetAddress": self.payer_address_street,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.payer_address_address_details_country_id,
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": self.payer_address_address_details_region_id,
                            "description": "Cahul",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": self.payer_address_address_details_locality_scheme,
                            "id": self.payer_address_address_details_locality_id,
                            "description": self.payer_address_address_details_locality_description,
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "contactPoint": {
                    "name": self.payer_contact_point_name,
                    "email": self.payer_contact_point_email,
                    "telephone": self.payer_contact_point_telephone
                },
                "roles": ["payer"]
            }, {
                "id": "MD-IDNO-4",
                "name": "create Pn: tender.procuringEntity.name",
                "identifier": {
                    "scheme": "MD-IDNO",
                    "id": "4",
                    "legalName": "create Pn: tender.procuringEntity.identigfier.legalName"
                },
                "address": {
                    "streetAddress": "create Pn: tender.procuringEntity.address.streetAddress",
                    "addressDetails": {
                        "country": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["country"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['uri']
                        },
                        "region": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["region"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['uri']
                        },
                        "locality": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["locality"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['uri']

                        }
                    }
                },
                "contactPoint": {
                    "name": "create Pn: tender.procuringEntity.contactPoint.name",
                    "email": "create Pn: tender.procuringEntity.contactPoint.email",
                    "telephone": "create Pn: tender.procuringEntity.contactPoint.telephone"
                },
                "roles": ["procuringEntity"]
            }],
            "relatedProcesses": [{
                "id": "36b553f0-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["planning"],
                "scheme": "ocid",
                "identifier": pn_id,
                "uri": f"{instance_tender_url}{cp_id}/{pn_id}"
            }, {
                "id": "36b553f1-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["x_expenditureItem"],
                "scheme": "ocid",
                "identifier": ei_id,
                "uri": f"{instance_budget_url}{ei_id}/{ei_id}"
            }, {
                "id": "36b553f2-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["x_fundingSource"],
                "scheme": "ocid",
                "identifier": fs_id,
                "uri": f"{instance_budget_url}{ei_id}/{fs_id}"
            },
                {
                    "id": "164cf530-ceca-11eb-8aed-69d06bed4d57",
                    "relationship": ["x_evaluation"],
                    "scheme": "ocid",
                    "identifier": ev_id,
                    "uri": f"{instance_tender_url}{cp_id}/{ev_id}"
                }
            ]
        }
        json_notice_release_pn = {
            "ocid": pn_id,
            "id": f"{pn_id}-{ev_id[32:45]}",
            "date": f"{get_human_date_in_utc_format(int(ev_id[32:45]))[0]}",
            "tag": ["planningUpdate"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "title": "Planning Notice",
                "description": "Contracting process is planned",
                "status": "complete",
                "statusDetails": "empty",
                "lotGroups": [{
                    "optionToCombine": False
                }],
                "tenderPeriod": {
                    "startDate": period[3]
                },
                "hasEnquiries": False,
                "submissionMethod": ["electronicSubmission"],
                "submissionMethodDetails": submission_method_details,
                "submissionMethodRationale": submission_method_rationale,
                "requiresElectronicCatalogue": False,
                "procurementMethodRationale": "create Pn: tender.procurementMethodRationale",
                "classification": {
                    "scheme": "CPV",
                    "id": get_value_by_new_cpv_code[0],
                    "description": get_value_by_new_cpv_code[1]
                },
                "value": {
                    "amount": 1650.00,
                    "currency": "EUR"
                }
            },
            "hasPreviousNotice": False,
            "purposeOfNotice": {
                "isACallForCompetition": False
            },
            "relatedProcesses": [{
                "id": "36b553f3-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": cp_id,
                "uri": f"{instance_tender_url}{cp_id}/{cp_id}"
            }]
        }
        json_notice_release_ev = {
            "ocid": ev_id,
            "id": f"{ev_id}-{ev_id[32:45]}",
            "date": f"{get_human_date_in_utc_format(int(ev_id[32:45]))[0]}",
            "tag": ["tender"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "c36f9952-06d5-41ef-9fe6-36722f1da414",
                "title": "Planning Notice",
                "description": "Contracting process is planned",
                "status": "active",
                "statusDetails": "clarification",
                "items": [{
                    "id": first_item_id,
                    "description": "create Pn: tender.items[0].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_first_item_cpv_code[0],
                        "description": get_value_by_first_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_first_item_cpvs_code[0],
                        "description": get_value_by_first_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "name": get_value_by_first_item_unit_id[1],
                        "id": get_value_by_first_item_unit_id[0]
                    },
                    "relatedLot": first_lot_id
                }, {
                    "id": second_item_id,
                    "description": "create Pn: tender.items[1].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_second_item_cpv_code[0],
                        "description": get_value_by_second_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_second_item_cpvs_code[0],
                        "description": get_value_by_second_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_second_item_unit_id[0],
                        "name": get_value_by_second_item_unit_id[1]
                    },
                    "relatedLot": second_lot_id
                }],
                "lots": [{
                    "id": first_lot_id,
                    "title": "create Pn: tender.lots[0].title",
                    "description": "create Pn: tender.lots[0].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 1500.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[0].placeOfPerformance.address.streetAddress",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        }
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }, {
                    "id": second_lot_id,
                    "title": "create Pn: tender.lots[1].title",
                    "description": "create Pn: tender.lots[1].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 150.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[1].placeOfPerformance.address.streetAddress",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        }
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }],
                "lotGroups": [{
                    "optionToCombine": False
                }],
                "tenderPeriod": {
                    "startDate": enquiry_and_tender_period[2],
                    "endDate": enquiry_and_tender_period[3]
                },
                "enquiryPeriod": {
                    "startDate": enquiry_and_tender_period[0],
                    "endDate": enquiry_and_tender_period[1]
                },
                "hasEnquiries": False,
                "documents": [{
                    "id": self.document_three_was_uploaded,
                    "documentType": "illustration",
                    "title": "create CNonPN: tender.documents[2].title",
                    "url": f"{instance_storage_url}"
                           f"{self.document_three_was_uploaded}",
                    "datePublished": operation_date
                }],
                "awardCriteria": "ratedCriteria",
                "awardCriteriaDetails": "automated",
                "submissionMethod": ["electronicSubmission"],
                "submissionMethodDetails": submission_method_details,
                "submissionMethodRationale": submission_method_rationale,
                "requiresElectronicCatalogue": False
            },
            "hasPreviousNotice": True,
            "purposeOfNotice": {
                "isACallForCompetition": True
            },
            "relatedProcesses": [{
                "id": "12a3ea63-ceca-11eb-8aed-69d06bed4d57",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": cp_id,
                "uri": f"{instance_tender_url}{cp_id}/{cp_id}"
            }, {
                "id": "164cf531-ceca-11eb-8aed-69d06bed4d57",
                "relationship": ["planning"],
                "scheme": "ocid",
                "identifier": pn_id,
                "uri": f"{instance_tender_url}{cp_id}/{pn_id}"
            }]
        }
        json_notice_release_ev_new = {
            "ocid": ev_id,
            "id": f"{ev_id}-{period_for_amendment[1]}",
            "date": period_for_amendment[0],
            "tag": ["tender"],
            "initiationType": "tender",
            "language": self.lang,
            "tender": {
                "id": "c36f9952-06d5-41ef-9fe6-36722f1da414",
                "title": "Evaluation",
                "description": "Evaluation stage of contracting process",
                "status": "active",
                "statusDetails": "clarification",
                "items": [{
                    "id": first_item_id,
                    "description": "create Pn: tender.items[0].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_first_item_cpv_code[0],
                        "description": get_value_by_first_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_first_item_cpvs_code[0],
                        "description": get_value_by_first_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "name": get_value_by_first_item_unit_id[1],
                        "id": get_value_by_first_item_unit_id[0]
                    },
                    "relatedLot": first_lot_id
                }, {
                    "id": second_item_id,
                    "internalId": "create Pn: tender.items[1].internalId",
                    "description": "create Pn: tender.items[1].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_second_item_cpv_code[0],
                        "description": get_value_by_second_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_second_item_cpvs_code[0],
                        "description": get_value_by_second_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_first_item_unit_id[0],
                        "name": get_value_by_first_item_unit_id[1]
                    },
                    "relatedLot": second_lot_id
                }],
                "lots": [{
                    "id": first_lot_id,
                    "title": "create Pn: tender.lots[0].title",
                    "description": "create Pn: tender.lots[0].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 1500.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[0].placeOfPerformance.address.streetAddress",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        }
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }, {
                    "id": second_lot_id,
                    "title": "create Pn: tender.lots[1].title",
                    "description": "create Pn: tender.lots[1].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 150.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[1].placeOfPerformance.address.streetAddress",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        }
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }],
                "lotGroups": [{
                    "optionToCombine": False
                }],
                "tenderPeriod": {
                    "startDate": enquiry_and_tender_period[2],
                    "endDate": enquiry_and_tender_period[3]
                },
                "enquiryPeriod": {
                    "startDate": enquiry_and_tender_period[0],
                    "endDate": enquiry_and_tender_period[1]
                },
                "hasEnquiries": False,
                "amendments": [{
                    "id": self.amendment_id,
                    "type": "cancellation",
                    "status": "pending",
                    "relatesTo": "lot",
                    "relatedItem": lot_id,
                    "date": period_for_amendment[0],
                    "rationale": "cancel_tender: amendments[0].rationale"
                }],
                "documents": [{
                    "id": self.document_one_was_uploaded,
                    "documentType": "contractArrangements",
                    "title": "create Pn: tender.documents[0].title",
                    "description": "create Pn: tender.documents[0].description",
                    "url": f"{instance_storage_url}{self.document_one_was_uploaded}",
                    "datePublished": operation_date,
                    "relatedLots": [first_lot_id]
                }],
                "awardCriteria": "ratedCriteria",
                "awardCriteriaDetails": "automated",
                "submissionMethod": ["electronicSubmission"],
                "submissionMethodDetails": submission_method_details,
                "submissionMethodRationale": submission_method_rationale,
                "requiresElectronicCatalogue": False
            },
            "hasPreviousNotice": True,
            "purposeOfNotice": {
                "isACallForCompetition": True
            },
            "relatedProcesses": [{
                "id": "12a3ea63-ceca-11eb-8aed-69d06bed4d57",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": cp_id,
                "uri": f"{instance_tender_url}{cp_id}/{cp_id}"
            }, {
                "id": "164cf531-ceca-11eb-8aed-69d06bed4d57",
                "relationship": ["planning"],
                "scheme": "ocid",
                "identifier": pn_id,
                "uri": f"{instance_tender_url}{cp_id}/{pn_id}"
            }]
        }
        json_notice_compiled_release_ms = {
            "ocid": cp_id,
            "id": f"{cp_id}-{ev_id[32:45]}",
            "date": f"{get_human_date_in_utc_format(int(ev_id[32:45]))[0]}",
            "tag": ["compiled"],
            "language": self.lang,
            "initiationType": "tender",
            "planning": {
                "budget": {
                    "amount": {
                        "amount": 2000.00,
                        "currency": "EUR"
                    },
                    "isEuropeanUnionFunded": False,
                    "budgetBreakdown": [{
                        "id": fs_id,
                        "amount": {
                            "amount": 2000.00,
                            "currency": "EUR"
                        },
                        "period": {
                            "startDate": period[0],
                            "endDate": period[1]
                        },
                        "sourceParty": {
                            "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                            "name": self.buyer_name,
                        }
                    }]
                }
            },
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "title": "create Pn: tender.title",
                "description": "create Pn: tender.description",
                "status": "active",
                "statusDetails": "evaluation",
                "value": {
                    "amount": 1650.00,
                    "currency": "EUR"
                },
                "procurementMethod": "open",
                "procurementMethodDetails": procurement_method_details_from_mdm,
                "mainProcurementCategory": "works",
                "hasEnquiries": False,
                "eligibilityCriteria": eligibility_criteria_from_mdm,
                "contractPeriod": {
                    "startDate": contract_period[0],
                    "endDate": contract_period[1]
                },
                "procuringEntity": {
                    "id": "MD-IDNO-4",
                    "name": "create Pn: tender.procuringEntity.name"
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
                "legalBasis": "DIRECTIVE_2014_25_EU",
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
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name,
                "identifier": {
                    "scheme": self.buyer_identifier_scheme,
                    "id": self.buyer_identifier_id,
                    "legalName": self.buyer_identifier_legal_name
                },
                "address": {
                    "streetAddress": self.buyer_address_street_address,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.buyer_address_address_details_country_id,
                            "description": "Moldova, Republica",
                            "uri": "https://www.iso.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": self.buyer_address_address_details_region_id,
                            "description": "mun.Chişinău",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": self.buyer_address_address_details_locality_scheme,
                            "id": self.buyer_address_address_details_locality_id,
                            "description": self.buyer_address_address_details_locality_description,
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "contactPoint": {
                    "name": self.buyer_contact_point_name,
                    "email": self.buyer_contact_point_email,
                    "telephone": self.buyer_contact_point_telephone
                },
                "roles": ["buyer"]
            }, {
                "id": f"{self.payer_identifier_scheme}-{self.payer_identifier_id}",
                "name": self.payer_name,
                "identifier": {
                    "scheme": self.payer_identifier_scheme,
                    "id": self.payer_identifier_id,
                    "legalName": self.payer_identifier_legal_name
                },
                "address": {
                    "streetAddress": self.payer_address_street,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.payer_address_postal_code,
                            "description": "Moldova, Republica",
                            "uri": "https://www.iso.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": self.payer_address_address_details_region_id,
                            "description": "Donduşeni",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": self.payer_address_address_details_locality_scheme,
                            "id": self.payer_address_address_details_locality_id,
                            "description": self.payer_address_address_details_locality_description,
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "contactPoint": {
                    "name": self.payer_contact_point_name,
                    "email": self.payer_contact_point_email,
                    "telephone": self.payer_contact_point_telephone
                },
                "roles": ["payer"]
            }, {
                "id": "MD-IDNO-4",
                "name": "create Pn: tender.procuringEntity.name",
                "identifier": {
                    "scheme": "MD-IDNO",
                    "id": "4",
                    "legalName": "create Pn: tender.procuringEntity.identigfier.legalName"
                },
                "address": {
                    "streetAddress": "street address",
                    "addressDetails": {
                        "country": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["country"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "country"]['uri']
                        },
                        "region": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["region"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "region"]['uri']
                        },
                        "locality": {
                            "scheme": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['scheme'],
                            "id": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['id'],
                            "description": data_pn["data"]["tender"]["procuringEntity"]["address"][
                                "addressDetails"]["locality"]['description'],
                            "uri": data_pn["data"]["tender"]["procuringEntity"]["address"]["addressDetails"][
                                "locality"]['uri']
                        }
                    }
                },
                "contactPoint": {
                    "name": "name",
                    "email": "email",
                    "telephone": "456-95-96"
                },
                "roles": ["procuringEntity"]
            }],
            "relatedProcesses": [{
                "id": "36b553f0-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["planning"],
                "scheme": "ocid",
                "identifier": pn_id,
                "uri": f"{instance_tender_url}{cp_id}/{pn_id}"
            }, {
                "id": "36b553f1-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["x_expenditureItem"],
                "scheme": "ocid",
                "identifier": ei_id,
                "uri": f"{instance_budget_url}{ei_id}/{ei_id}"
            }, {
                "id": "36b553f2-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["x_fundingSource"],
                "scheme": "ocid",
                "identifier": fs_id,
                "uri": f"{instance_budget_url}{ei_id}/{fs_id}"
            },
                {
                    "id": "ed0f7290-cee4-11eb-8aed-69d06bed4d57",
                    "relationship": ["x_evaluation"],
                    "scheme": "ocid",
                    "identifier": ev_id,
                    "uri": f"{instance_tender_url}{cp_id}/{ev_id}"
                }
            ]

        }
        json_notice_compiled_release_pn = {
            "ocid": pn_id,
            "id": f"{pn_id}-{ev_id[32:45]}",
            "date": f"{get_human_date_in_utc_format(int(ev_id[32:45]))[0]}",
            "tag": ["planningUpdate"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "title": "Planning Notice",
                "description": "Contracting process is planned",
                "status": "complete",
                "statusDetails": "empty",
                "lotGroups": [{
                    "optionToCombine": False
                }],
                "tenderPeriod": {
                    "startDate": period[3]
                },
                "hasEnquiries": False,
                "submissionMethod": ["electronicSubmission"],
                "submissionMethodDetails": submission_method_details,
                "submissionMethodRationale": submission_method_rationale,
                "requiresElectronicCatalogue": False,
                "classification": {
                    "scheme": "CPV",
                    "id": get_value_by_new_cpv_code[0],
                    "description": get_value_by_new_cpv_code[1]
                },
                "value": {
                    "amount": 1650.00,
                    "currency": "EUR"
                }
            },
            "hasPreviousNotice": False,
            "purposeOfNotice": {
                "isACallForCompetition": False
            },
            "relatedProcesses": [{
                "id": "36b553f3-c072-11eb-ab87-09e4e5e94b2a",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": cp_id,
                "uri": f"{instance_tender_url}{cp_id}/{cp_id}"
            }]
        }
        json_notice_compiled_release_ev = {
            "ocid": ev_id,
            "id": f"{ev_id}-{period_for_amendment[1]}",
            "date": period_for_amendment[0],
            "tag": ["tender"],
            "initiationType": "tender",
            "language": self.lang,
            "tender": {
                "id": "bf029021-aeb7-403d-b301-b8823855f42a",
                "title": "Evaluation",
                "description": "Evaluation stage of contracting process",
                "status": "active",
                "statusDetails": "clarification",
                "items": [{
                    "id": first_item_id,
                    "description": "create Pn: tender.items[0].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_first_item_cpv_code[0],
                        "description": get_value_by_first_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_first_item_cpvs_code[0],
                        "description": get_value_by_first_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_first_item_unit_id[0],
                        "name": get_value_by_first_item_unit_id[1]
                    },
                    "relatedLot": first_lot_id
                }, {
                    "id": second_item_id,
                    "description": "create Pn: tender.items[1].description",
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_second_item_cpv_code[0],
                        "description": get_value_by_second_item_cpv_code[1]
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": get_value_by_second_item_cpvs_code[0],
                        "description": get_value_by_second_item_cpvs_code[2]
                    }],
                    "quantity": 0.010,
                    "unit": {
                        "id": get_value_by_second_item_unit_id[0],
                        "name": get_value_by_second_item_unit_id[1]
                    },
                    "relatedLot": second_lot_id
                }],
                "lots": [{
                    "id": first_lot_id,
                    "title": "create Pn: tender.lots[0].title",
                    "description": "create Pn: tender.lots[0].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 1500.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[0].placeOfPerformance.address.streetAddress",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        }
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }, {
                    "id": second_lot_id,
                    "title": "create Pn: tender.lots[1].title",
                    "description": "create Pn: tender.lots[1].internalId.description",
                    "status": "active",
                    "statusDetails": "empty",
                    "value": {
                        "amount": 150.00,
                        "currency": "EUR"
                    },
                    "contractPeriod": {
                        "startDate": contract_period[0],
                        "endDate": contract_period[1]
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "create Pn: tender.lots[1].placeOfPerformance.address.streetAddress",
                            "addressDetails": {
                                "country": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["country"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["country"]['uri']
                                },
                                "region": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["region"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["region"]['uri']
                                },
                                "locality": {
                                    "scheme": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['scheme'],
                                    "id": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['id'],
                                    "description": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance'][
                                        "address"]["addressDetails"]["locality"]['description'],
                                    "uri": data_pn["data"]["tender"]["lots"][1]['placeOfPerformance']["address"][
                                        "addressDetails"]["locality"]['uri']
                                }
                            }
                        }
                    },
                    "hasOptions": False,
                    "hasRecurrence": False,
                    "hasRenewal": False
                }],
                "lotGroups": [{
                    "optionToCombine": False
                }],
                "tenderPeriod": {
                    "startDate": enquiry_and_tender_period[2],
                    "endDate": enquiry_and_tender_period[3]
                },
                "enquiryPeriod": {
                    "startDate": enquiry_and_tender_period[0],
                    "endDate": enquiry_and_tender_period[1]
                },
                "hasEnquiries": False,
                "amendments": [{
                    "id": self.amendment_id,
                    "type": "cancellation",
                    "status": "pending",
                    "relatesTo": "lot",
                    "relatedItem": lot_id,
                    "date": period_for_amendment[0],
                    "rationale": "cancel_tender: amendments[0].rationale"
                }],
                "documents": [{
                    "id": self.document_one_was_uploaded,
                    "documentType": "contractArrangements",
                    "title": "create Pn: tender.documents[0].title",
                    "url": f"{instance_storage_url}{self.document_one_was_uploaded}",
                    "datePublished": operation_date
                }],
                "awardCriteria": "ratedCriteria",
                "awardCriteriaDetails": "automated",
                "submissionMethod": ["electronicSubmission"],
                "submissionMethodDetails": submission_method_details,
                "submissionMethodRationale": submission_method_rationale,
                "requiresElectronicCatalogue": False
            },
            "hasPreviousNotice": True,
            "purposeOfNotice": {
                "isACallForCompetition": True
            },
            "relatedProcesses": [{
                "id": "e84a2253-cee4-11eb-8aed-69d06bed4d57",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": cp_id,
                "uri": f"{instance_tender_url}{cp_id}/{cp_id}"
            }, {
                "id": "ed0f7291-cee4-11eb-8aed-69d06bed4d57",
                "relationship": ["planning"],
                "scheme": "ocid",
                "identifier": pn_id,
                "uri": f"{instance_tender_url}{cp_id}/{pn_id}"
            }]
        }

        kafka = Kafka(instance=self.instance)
        kafka.connect_kafka_producer()
        kafka.publish_message_into_chronograph_in_clarification(
            cp_id=cp_id,
            ev_id=ev_id,
            enquiry_end=enquiry_and_tender_period[1]
        )
        kafka.publish_message_into_chronograph_in_submission(
            cp_id=cp_id,
            ev_id=ev_id,
            tender_end=enquiry_and_tender_period[3]
        )

        key_space_ocds.execute(f"INSERT INTO orchestrator_context (cp_id,context) VALUES ("
                               f"'{ev_id}','{json.dumps(json_orchestrator_context)}');").one()
        key_space_access.execute(f"INSERT INTO tenders (cpid, ocid, token_entity,created_date,json_data, owner) "
                                 f"VALUES ('{cp_id}', '{ev_id}', '{pn_token}', {ev_id[32:45]}, "
                                 f"'{json.dumps(json_access_tender)}','{owner}');").one()
        key_space_clarification.execute(
            f"INSERT INTO periods (cpid, ocid, end_date, owner, start_date) "
            f"VALUES ('{cp_id}', '{ev_id}', {get_timestamp_from_human_date(enquiry_and_tender_period[1])}, '{owner}', "
            f"{ev_id[32:45]});").one()
        key_space_submission.execute(
            f"INSERT INTO periods (cpid, ocid, end_date, start_date) "
            f"VALUES ('{cp_id}', '{ev_id}', {get_timestamp_from_human_date(enquiry_and_tender_period[3])}, "
            f"{get_timestamp_from_human_date(enquiry_and_tender_period[1])});").one()
        key_space_ocds.execute(f"INSERT INTO notice_offset (cp_id,release_date, stage, status) "
                               f"VALUES ('{cp_id}', {ev_id[32:45]}, 'EV', 'active');").one()
        key_space_ocds.execute(
            f"INSERT INTO notice_release (cp_id,oc_id, release_id, json_data, release_date, stage) "
            f"VALUES ('{cp_id}', '{cp_id}', '{cp_id + '-' + ev_id[32:45]}' ,'{json.dumps(json_notice_release_ms)}',"
            f"{ev_id[32:45]},'');").one()
        key_space_ocds.execute(
            f"INSERT INTO notice_release (cp_id,oc_id, release_id, json_data, release_date, stage) "
            f"VALUES ('{cp_id}', '{pn_id}', '{pn_id + '-' + ev_id[32:45]}' ,'{json.dumps(json_notice_release_pn)}',"
            f"{ev_id[32:45]},'PN');").one()
        key_space_ocds.execute(
            f"INSERT INTO notice_release (cp_id,oc_id, release_id, json_data, release_date, stage) "
            f"VALUES ('{cp_id}', '{ev_id}', '{ev_id + '-' + ev_id[32:45]}','{json.dumps(json_notice_release_ev)}',"
            f"{ev_id[32:45]},'EV');").one()
        key_space_ocds.execute(
            f"INSERT INTO notice_release (cp_id,oc_id, release_id, json_data, release_date, stage) "
            f"VALUES ('{cp_id}', '{ev_id}', '{ev_id + '-' + str(period_for_amendment[1])}',"
            f"'{json.dumps(json_notice_release_ev_new)}',"
            f"{period_for_amendment[1]},'EV');").one()

        key_space_ocds.execute(
            f"INSERT INTO notice_compiled_release (cp_id,oc_id, json_data, publish_date, release_date, "
            f"release_id, stage, status) VALUES ('{cp_id}', '{cp_id}', '{json.dumps(json_notice_compiled_release_ms)}',"
            f"{ev_id[32:45]},{ev_id[32:45]}, '{cp_id + '-' + ev_id[32:45]}','', 'active');").one()
        key_space_ocds.execute(
            f"INSERT INTO notice_compiled_release (cp_id,oc_id, json_data, publish_date, release_date, "
            f"release_id, stage, status) VALUES ('{cp_id}', '{pn_id}', '{json.dumps(json_notice_compiled_release_pn)}',"
            f"{ev_id[32:45]},{ev_id[32:45]}, '{pn_id + '-' + ev_id[32:45]}','PN', 'active');").one()
        key_space_revision.execute(f"INSERT INTO amendments (cpid, ocid, id, data) "
                                   f"VALUES ('{cp_id}', '{ev_id}', {self.amendment_id}, "
                                   f"'{json.dumps(json_amendments)}');").one()

        key_space_ocds.execute(f"INSERT INTO notice_offset (cp_id,release_date, stage, status) "
                               f"VALUES ('{cp_id}', {period_for_amendment[1]}, 'EV', 'active');").one()

        key_space_ocds.execute(
            f"INSERT INTO notice_compiled_release (cp_id,oc_id, json_data, publish_date, release_date, "
            f"release_id, stage, status) VALUES ('{cp_id}', '{ev_id}', '{json.dumps(json_notice_compiled_release_ev)}',"
            f"{period[2]},{period_for_amendment[1]}, '{ev_id + '-' + str(period_for_amendment[1])}','EV', "
            f"'active');").one()
        record = f"{instance_tender_url}{cp_id}"
        ms_release = f"{instance_tender_url}{cp_id}/{cp_id}"
        pn_release = f"{instance_tender_url}{cp_id}/{pn_id}"
        ev_release = f"{instance_tender_url}{cp_id}/{ev_id}"
        return cp_id, pn_id, pn_token, ev_id, record, ms_release, pn_release, ev_release, self.amendment_id, \
               self.amendment_token
