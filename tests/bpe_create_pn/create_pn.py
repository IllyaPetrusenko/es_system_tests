import time

import requests

from tests.authorization import get_access_token_for_platform_one, get_x_operation_id

from tests.cassandra_inserts_into_Database import insert_into_db_create_fs
from tests.kafka_messages import get_message_from_kafka
from tests.presets import set_instance_for_request, create_pn
from useful_functions import get_period, get_timestamp_from_human_date


def bpe_create_pn_one_fs(cpid, pn_create_payload, pmd, status="active", statusDetails="empty", amount=2000.00,
                         currency="EUR", start_date=get_period()[0],
                         end_date=get_period()[1], timestamp=get_timestamp_from_human_date(get_period()[0]),
                         test_mode=False, buyer_id="1", payer_id="2", funder_id="3"):
    access_token = get_access_token_for_platform_one()
    x_operation_id = get_x_operation_id(access_token)
    time.sleep(2)
    test_create_fs = insert_into_db_create_fs(cpid, status=status, statusDetails=statusDetails, amount=amount,
                                              currency=currency, start_date=start_date,
                                              end_date=end_date, timestamp=timestamp, buyer_id=buyer_id,
                                              payer_id=payer_id, funder_id=funder_id)
    if "planning" in pn_create_payload.keys() and "budget" in pn_create_payload[
        "planning"].keys() and "budgetBreakdown" in pn_create_payload["planning"][
        "budget"].keys() and "id" in pn_create_payload["planning"]["budget"]["budgetBreakdown"][0].keys():
        pn_create_payload["planning"]["budget"]["budgetBreakdown"][0]["id"] = test_create_fs[2]
        host = set_instance_for_request()
        request_to_create_pn = requests.post(
            url=host + create_pn,
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'Content-Type': 'application/json'},
            params={"country": "MD", "pmd": pmd, "testMode": test_mode},
            json=pn_create_payload)
        time.sleep(2)
        message_from_kafka = get_message_from_kafka(x_operation_id)
    else:
        host = set_instance_for_request()
        request_to_create_pn = requests.post(
            url=host + create_pn,
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'Content-Type': 'application/json'},
            params={"country": "MD", "pmd": pmd, "testMode": test_mode},
            json=pn_create_payload)
        time.sleep(2)
        message_from_kafka = get_message_from_kafka(x_operation_id)
    return request_to_create_pn, message_from_kafka, x_operation_id, test_create_fs[2], test_create_fs[3], \
           test_create_fs[4], test_create_fs[5]


def bpe_create_pn_two_fs(cpid_1, cpid_2, pn_create_payload, buyer_1="1", payer_1="2", funder_1="3", buyer_2="11",
                         payer_2="22", funder_2="33",
                         classification_id_1="45100000-8", classification_id_2="45100000-8", currency_1="EUR",
                         currency_2="EUR", planning_rationale="plan",
                         country_id="MD",
                         country_scheme="iso-alpha2", country_description="Moldova, Republica", region_scheme="CUATM",
                         region_id="3400000", region_description="Donduşeni", locality_scheme="CUATM",
                         locality_id="3401000",
                         locality_description="or.Donduşeni (r-l Donduşeni)", contact_point_name="Petrusenko Svitlana",
                         contact_point_email="svetik@gmail.com",
                         contact_point_telephone="888999666", contact_point_fax="5552233",
                         contact_point_url="http://petrusenko.com/svetlana",
                         buyer_name="LLC Dmitro", funder_name="LLC Petro", payer_name="LLC Milola",
                         budget_id="test id for budget",
                         budget_description="test description", project_name=" test project name",
                         project_id="test project id",
                         project_uri="test project uri", amount_1=1000.00, amount_2=1000.00, is_european_funding_1=True,
                         is_european_funding_2=True,
                         european_project_name="test eropean name",
                         european_project_id="test european id",
                         european_project_uri="european uri",
                         buyer_identifier_scheme="MD-IDNO",
                         funder_identifier_scheme="MD-IDNO", payer_identifier_scheme="MD-IDNO",
                         payer_identifier_legal_name="legal",
                         payer_identifier_legal_uri="uri", payer_address_street="street",
                         payer_address_postal="postalCode", payer_additional_id="id of additional",
                         payer_additional_scheme="scheme of additional", payer_additional_uri="uri of additional",
                         payer_additional_legal="legal of additional",
                         funder_identifier_legal_name="legal", funder_identifier_legal_uri="uri",
                         funder_address_street="street", funder_address_postal="02223",
                         funder_additional_id="id of additional", funder_additional_scheme="scheme of additional",
                         funder_additional_legal="legal of additional",
                         funder_additional_uri="uri of additional", buyer_identifier_legal_name="legal",
                         buyer_identifier_uri="uri", buyer_address_street="street", buyer_address_postal="35365",
                         buyer_additional_id="id of additional", buyer_additional_scheme="scheme of additional",
                         buyer_additional_legal="legal of additional", buyer_additional_uri="uri of additional",
                         buyer_details_type="NATIONAL_AGENCY", buyer_details_general_activity="HEALTH",
                         buyer_details_sectoral_activity="WATER", pmd="OT", seconds=0):
    access_token = get_access_token_for_platform_one()
    x_operation_id = get_x_operation_id(access_token)
    time.sleep(2)
    test_create_fs_1 = insert_into_db_create_fs(cpid=cpid_1, buyer_id=buyer_1, payer_id=payer_1,
                                                funder_id=funder_1,
                                                status="active", statusDetails="empty",
                                                classification_id=classification_id_1, currency=currency_1,
                                                planning_rationale=planning_rationale, country_id=country_id,
                                                country_scheme=country_scheme, country_description=country_description,
                                                region_scheme=region_scheme,
                                                region_id=region_id, region_description=region_description,
                                                locality_scheme=locality_scheme, locality_id=locality_id,
                                                locality_description=locality_description,
                                                contact_point_name=contact_point_name,
                                                contact_point_email=contact_point_email,
                                                contact_point_telephone=contact_point_telephone,
                                                contact_point_fax=contact_point_fax,
                                                contact_point_url=contact_point_url,
                                                buyer_name=buyer_name,
                                                funder_name=funder_name, payer_name=payer_name,
                                                budget_id=budget_id, budget_description=budget_description,
                                                project_name=project_name, project_id=project_id,
                                                project_uri=project_uri, amount=amount_1,
                                                is_european_funding=is_european_funding_1,
                                                european_project_name=european_project_name,
                                                european_project_id=european_project_id,
                                                european_project_uri=european_project_uri,
                                                buyer_identifier_scheme=buyer_identifier_scheme,
                                                funder_identifier_scheme=funder_identifier_scheme,
                                                payer_identifier_scheme=payer_identifier_scheme,
                                                payer_identifier_legal_name=payer_identifier_legal_name,
                                                payer_identifier_legal_uri=payer_identifier_legal_uri,
                                                payer_address_street=payer_address_street,
                                                payer_address_postal=payer_address_postal,
                                                payer_additional_id=payer_additional_id,
                                                payer_additional_scheme=payer_additional_scheme,
                                                payer_additional_uri=payer_additional_uri,
                                                payer_additional_legal=payer_additional_legal,
                                                funder_identifier_legal_name=funder_identifier_legal_name,
                                                funder_identifier_legal_uri=funder_identifier_legal_uri,
                                                funder_address_street=funder_address_street,
                                                funder_address_postal=funder_address_postal,
                                                funder_additional_id=funder_additional_id,
                                                funder_additional_scheme=funder_additional_scheme,
                                                funder_additional_legal=funder_additional_legal,
                                                funder_additional_uri=funder_additional_uri,
                                                buyer_identifier_legal_name=buyer_identifier_legal_name,
                                                buyer_identifier_uri=buyer_identifier_uri,
                                                buyer_address_street=buyer_address_street,
                                                buyer_address_postal=buyer_address_postal,
                                                buyer_additional_id=buyer_additional_id,
                                                buyer_additional_scheme=buyer_additional_scheme,
                                                buyer_additional_legal=buyer_additional_legal,
                                                buyer_additional_uri=buyer_additional_uri,
                                                buyer_details_type=buyer_details_type,
                                                buyer_details_general_activity=buyer_details_general_activity,
                                                buyer_details_sectoral_activity=buyer_details_sectoral_activity
                                                )

    time.sleep(seconds)
    test_create_fs_2 = insert_into_db_create_fs(cpid=cpid_2, buyer_id=buyer_2, payer_id=payer_2,
                                                funder_id=funder_2,
                                                status="active", statusDetails="empty",
                                                classification_id=classification_id_2, currency=currency_2,
                                                planning_rationale=planning_rationale, country_id=country_id,
                                                country_scheme=country_scheme, country_description=country_description,
                                                region_scheme=region_scheme,
                                                region_id=region_id, region_description=region_description,
                                                locality_scheme=locality_scheme, locality_id=locality_id,
                                                locality_description=locality_description,
                                                contact_point_name=contact_point_name,
                                                contact_point_email=contact_point_email,
                                                contact_point_telephone=contact_point_telephone,
                                                contact_point_fax=contact_point_fax,
                                                contact_point_url=contact_point_url,
                                                buyer_name=buyer_name,
                                                funder_name=funder_name, payer_name=payer_name,
                                                budget_id=budget_id, budget_description=budget_description,
                                                project_name=project_name, project_id=project_id,
                                                project_uri=project_uri, amount=amount_2,
                                                is_european_funding=is_european_funding_2,
                                                european_project_name=european_project_name,
                                                european_project_id=european_project_id,
                                                european_project_uri=european_project_uri,
                                                buyer_identifier_scheme=buyer_identifier_scheme,
                                                funder_identifier_scheme=funder_identifier_scheme,
                                                payer_identifier_scheme=payer_identifier_scheme,
                                                payer_identifier_legal_name=payer_identifier_legal_name,
                                                payer_identifier_legal_uri=payer_identifier_legal_uri,
                                                payer_address_street=payer_address_street,
                                                payer_address_postal=payer_address_postal,
                                                payer_additional_id=payer_additional_id,
                                                payer_additional_scheme=payer_additional_scheme,
                                                payer_additional_uri=payer_additional_uri,
                                                payer_additional_legal=payer_additional_legal,
                                                funder_identifier_legal_name=funder_identifier_legal_name,
                                                funder_identifier_legal_uri=funder_identifier_legal_uri,
                                                funder_address_street=funder_address_street,
                                                funder_address_postal=funder_address_postal,
                                                funder_additional_id=funder_additional_id,
                                                funder_additional_scheme=funder_additional_scheme,
                                                funder_additional_legal=funder_additional_legal,
                                                funder_additional_uri=funder_additional_uri,
                                                buyer_identifier_legal_name=buyer_identifier_legal_name,
                                                buyer_identifier_uri=buyer_identifier_uri,
                                                buyer_address_street=buyer_address_street,
                                                buyer_address_postal=buyer_address_postal,
                                                buyer_additional_id=buyer_additional_id,
                                                buyer_additional_scheme=buyer_additional_scheme,
                                                buyer_additional_legal=buyer_additional_legal,
                                                buyer_additional_uri=buyer_additional_uri,
                                                buyer_details_type=buyer_details_type,
                                                buyer_details_general_activity=buyer_details_general_activity,
                                                buyer_details_sectoral_activity=buyer_details_sectoral_activity
                                                )
    if "planning" in pn_create_payload.keys() and "budget" in pn_create_payload[
        "planning"].keys() and "budgetBreakdown" in pn_create_payload["planning"][
        "budget"].keys() and "id" in pn_create_payload["planning"]["budget"]["budgetBreakdown"][0].keys() and "id" in \
            pn_create_payload["planning"]["budget"]["budgetBreakdown"][1].keys():

        pn_create_payload["planning"]["budget"]["budgetBreakdown"][0]["id"] = test_create_fs_1[2]

        pn_create_payload["planning"]["budget"]["budgetBreakdown"][1]["id"] = test_create_fs_2[2]
        host = set_instance_for_request()
        request_to_create_pn = requests.post(
            url=host + create_pn,
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'Content-Type': 'application/json'},
            params={"country": "MD", "pmd": pmd},
            json=pn_create_payload)
        time.sleep(2)
        message_from_kafka = get_message_from_kafka(x_operation_id)
    else:
        host = set_instance_for_request()
        request_to_create_pn = requests.post(
            url=host + create_pn,
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'Content-Type': 'application/json'},
            params={"country": "MD", "pmd": pmd},
            json=pn_create_payload)
        time.sleep(2)
        message_from_kafka = get_message_from_kafka(x_operation_id)
    return request_to_create_pn, message_from_kafka, x_operation_id, test_create_fs_1[2], test_create_fs_2[2]
