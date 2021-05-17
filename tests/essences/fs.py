import fnmatch
import json
import time
from uuid import uuid4
import allure
import requests
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from tests.authorization import get_access_token_for_platform_one, get_x_operation_id
from tests.kafka_messages import get_message_from_kafka
from useful_functions import is_it_uuid, get_period, get_access_token_for_platform_two, prepared_fs_oc_id


class FS:
    def __init__(self, payload, instance, cassandra_username, cassandra_password, country='MD',
                 lang='ro', tender_classification_id="45100000-8",
                 tender_item_classification_id="45100000-8", planning_budget_id="45100000-8",
                 platform="platform_one", amount=2000.0, currency="EUR",
                 tender_classification_scheme="CPV", planning_budget_period_start_date=get_period()[0],
                 tender_classification_description="Lucrări de pregătire a şantierului",
                 planning_budget_period_end_date=get_period()[1], buyer_name="LLC Petrusenko",
                 buyer_identifier_id="380632074071", buyer_identifier_scheme="MD-IDNO",
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
                 funder_address_address_details_region_id="1700000", payer_identifier_id="963",
                 funder_address_address_details_country_id="MD", funder_contact_point_telephone="123",
                 funder_contact_point_fax="147", funder_contact_point_url="www@11,io",
                 funder_contact_point_name="OKSANA", funder_contact_point_email="OKSANA@gmail.com",
                 payer_contact_point_email="papa@gmail.com", payer_contact_point_name="KOliya",
                 payer_contact_point_telephone="0446789877", payer_address_address_details_country_id="MD",
                 payer_address_address_details_region_id="1700000", payer_name="Slava",
                 payer_address_address_details_locality_scheme="CUATM", payer_identifier_legal_name="ZamGar",
                 payer_address_address_details_locality_id="1701000", payer_address_street="Grisuka",
                 payer_address_address_details_locality_description="mun.Cahul",
                 payer_address_postal_code="44444", funder_address_postal_code="44444"):
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
        self.payload = payload
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

    @allure.step('Create FS')
    def create_fs(self, cp_id):
        fs = requests.post(
            url=self.host_of_request + "/do/fs/" + cp_id,
            headers={
                'Authorization': 'Bearer ' + self.access_token,
                'X-OPERATION-ID': self.x_operation_id,
                'Content-Type': 'application/json'},
            json=self.payload)
        allure.attach(self.host_of_request + "/do/fs/" + cp_id, 'URL')
        allure.attach(json.dumps(self.payload), 'Prepared payload')
        return fs

    @allure.step('Update FS')
    def update_fs(self, cp_id, fs_id, fs_token, authorization_token="Bearer"):
        fs = requests.post(
            url=self.host_of_request + "/do/fs/" + cp_id + "/" + fs_id,
            headers={
                'Authorization': authorization_token + self.access_token,
                'X-OPERATION-ID': self.x_operation_id,
                'X-TOKEN': fs_token,
                'Content-Type': 'application/json'},
            json=self.payload)
        allure.attach(self.host_of_request + "/do/fs/" + cp_id + "/" + fs_id, 'URL')
        allure.attach(json.dumps(self.payload), 'Prepared payload')
        return fs

    @allure.step('Create FS with fake authorization token')
    def create_fs_with_fake_authorization_token(self, cp_id):
        fs = requests.post(
            url=self.host_of_request + "/do/fs/" + cp_id,
            headers={
                'Authorization': self.access_token,
                'X-OPERATION-ID': self.x_operation_id,
                'Content-Type': 'application/json'},
            json=self.payload)
        allure.attach(self.host_of_request + "/do/fs/" + cp_id, 'URL')
        allure.attach(json.dumps(self.payload), 'Prepared payload')
        return fs

    @allure.step('Insert EI')
    def insert_ei_full_data_model(self, cp_id, ei_token):
        auth_provider = PlainTextAuthProvider(username=self.cassandra_username, password=self.cassandra_password)
        cluster = Cluster([self.cassandra_cluster], auth_provider=auth_provider)
        session = cluster.connect('ocds')
        owner = "445f6851-c908-407d-9b45-14b92f3e964b"
        period = get_period()
        json_orchestrator_context = {
            "operationId": f"{uuid4()}",
            "requestId": f"{uuid4()}",
            "cpid": cp_id,
            "stage": "EI",
            "processType": "ei",
            "operationType": "createEI",
            "owner": owner,
            "country": self.country,
            "language": self.lang,
            "token": ei_token,
            "startDate": self.planning_budget_period_start_date,
            "timeStamp": period[2],
            "isAuction": False,
            "testMode": False
        }
        json_budget_ei = {
            "ocid": cp_id,
            "tender": {
                "id": "fbd943ca-aaad-433d-9189-96566e3648ea",
                "title": self.tender_title,
                "description": self.tender_description,
                "status": "planning",
                "statusDetails": "empty",
                "classification": {
                    "id": self.tender_classification_id,
                    "scheme": self.tender_classification_scheme,
                    "description": self.tender_classification_description
                },
                "mainProcurementCategory": "works",
                "items": [{
                    "id": self.tender_items_id,
                    "description": self.tender_items_description,
                    "classification": {
                        "id": self.tender_item_classification_id,
                        "description": "Lucrări de pregătire a şantierului",
                        "scheme": "CPV"
                    },
                    "additionalClassifications": [{
                        "id": self.tender_items_additional_classifications_id,
                        "description": "Oţel carbon",
                        "scheme": "CPVS"
                    }],
                    "deliveryAddress": {
                        "streetAddress": self.tender_items_delivery_street,
                        "postalCode": self.tender_items_delivery_postal,
                        "addressDetails": {
                            "country": {
                                "id": self.tender_items_delivery_details_country_id,
                                "description": self.tender_items_delivery_details_country_description,
                                "scheme": self.tender_items_delivery_details_country_scheme,
                                "uri": self.tender_items_delivery_details_country_uri
                            },
                            "region": {
                                "id": self.tender_items_delivery_details_region_id,
                                "description": self.tender_items_delivery_details_region_description,
                                "scheme": self.tender_items_delivery_details_region_scheme,
                                "uri": self.tender_items_delivery_details_region_uri
                            },
                            "locality": {
                                "id": self.tender_items_delivery_details_locality_id,
                                "description": self.tender_items_delivery_details_locality_description,
                                "scheme": self.tender_items_delivery_details_locality_scheme,
                                "uri": self.tender_items_delivery_details_locality_uri
                            }
                        }
                    },
                    "quantity": self.tender_items_quantity,
                    "unit": {
                        "id": self.tender_items_unit_id,
                        "name": self.tender_items_unit_name
                    }
                }]
            },
            "planning": {
                "budget": {
                    "id": self.planning_budget_id,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    }
                },
                "rationale": self.planning_rationale
            },
            "buyer": {
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name,
                "identifier": {
                    "id": self.buyer_identifier_id,
                    "scheme": self.buyer_identifier_scheme,
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
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
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
                    "telephone": self.buyer_contact_point_telephone,
                    "faxNumber": self.buyer_contact_point_fax_number,
                    "url": self.buyer_contact_point_url
                },
                "additionalIdentifiers": [{
                    "id": "string",
                    "scheme": "MD-IDNO",
                    "legalName": "380935103469",
                    "uri": "http://petrusenko.com/svetlana"
                }],
                "details": {
                    "typeOfBuyer": "NATIONAL_AGENCY",
                    "mainGeneralActivity": "HEALTH",
                    "mainSectoralActivity": "WATER"
                }
            }
        }

        json_notice_budget_release_ei = {
            "ocid": cp_id,
            "id": cp_id + '-' + f'{period[2]}',
            "date": self.planning_budget_period_start_date,
            "tag": ["compiled"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "fbd943ca-aaad-433d-9189-96566e3648ea",
                "title": self.tender_title,
                "description": self.tender_description,
                "status": "planning",
                "statusDetails": "empty",
                "items": [{
                    "id": self.tender_items_id,
                    "description": self.tender_items_description,
                    "classification": {
                        "scheme": "CPV",
                        "id": self.tender_item_classification_id,
                        "description": "Lucrări de pregătire a şantierului"
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": self.tender_items_additional_classifications_id,
                        "description": "Oţel carbon"
                    }],
                    "quantity": self.tender_items_quantity,
                    "unit": {
                        "id": self.tender_items_unit_id,
                        "name": self.tender_items_unit_name
                    },
                    "deliveryAddress": {
                        "streetAddress": self.tender_items_delivery_street,
                        "postalCode": self.tender_items_delivery_postal,
                        "addressDetails": {
                            "country": {
                                "id": self.tender_items_delivery_details_country_id,
                                "description": self.tender_items_delivery_details_country_description,
                                "scheme": self.tender_items_delivery_details_country_scheme,
                                "uri": self.tender_items_delivery_details_country_uri
                            },
                            "region": {
                                "id": self.tender_items_delivery_details_region_id,
                                "description": self.tender_items_delivery_details_region_description,
                                "scheme": self.tender_items_delivery_details_region_scheme,
                                "uri": self.tender_items_delivery_details_region_uri
                            },
                            "locality": {
                                "id": self.tender_items_delivery_details_locality_id,
                                "description": self.tender_items_delivery_details_locality_description,
                                "scheme": self.tender_items_delivery_details_locality_scheme,
                                "uri": self.tender_items_delivery_details_locality_uri
                            }
                        }
                    }
                }],
                "mainProcurementCategory": "works",
                "classification": {
                    "scheme": self.tender_classification_scheme,
                    "id": self.tender_classification_id,
                    "description": self.tender_classification_description
                }
            },
            "buyer": {
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name
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
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
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
                "additionalIdentifiers": [{
                    "scheme": "MD-IDNO",
                    "id": "string",
                    "legalName": "380935103469",
                    "uri": "http://petrusenko.com/svetlana"
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
            }],
            "planning": {
                "budget": {
                    "id": self.planning_budget_id,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    }
                },
                "rationale": self.planning_rationale
            }
        }

        json_notice_budget_compiled_release_ei = {
            "ocid": cp_id,
            "id": cp_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": ["compiled"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "fbd943ca-aaad-433d-9189-96566e3648ea",
                "title": self.tender_title,
                "description": self.tender_description,
                "status": "planning",
                "statusDetails": "empty",
                "items": [{
                    "id": self.tender_items_id,
                    "description": self.tender_items_description,
                    "classification": {
                        "scheme": "CPV",
                        "id": self.tender_item_classification_id,
                        "description": "Lucrări de pregătire a şantierului"
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": self.tender_items_additional_classifications_id,
                        "description": "Oţel carbon"
                    }],
                    "quantity": self.tender_items_quantity,
                    "unit": {
                        "id": self.tender_items_unit_id,
                        "name": self.tender_items_unit_name
                    },
                    "deliveryAddress": {
                        "streetAddress": self.tender_items_delivery_street,
                        "postalCode": self.tender_items_delivery_postal,
                        "addressDetails": {
                            "country": {
                                "id": self.tender_items_delivery_details_country_id,
                                "description": self.tender_items_delivery_details_country_description,
                                "scheme": self.tender_items_delivery_details_country_scheme,
                                "uri": self.tender_items_delivery_details_country_uri
                            },
                            "region": {
                                "id": self.tender_items_delivery_details_region_id,
                                "description": self.tender_items_delivery_details_region_description,
                                "scheme": self.tender_items_delivery_details_region_scheme,
                                "uri": self.tender_items_delivery_details_region_uri
                            },
                            "locality": {
                                "id": self.tender_items_delivery_details_locality_id,
                                "description": self.tender_items_delivery_details_locality_description,
                                "scheme": self.tender_items_delivery_details_locality_scheme,
                                "uri": self.tender_items_delivery_details_locality_uri
                            }
                        }
                    }
                }],
                "mainProcurementCategory": "works",
                "classification": {
                    "scheme": self.tender_classification_scheme,
                    "id": self.tender_classification_id,
                    "description": self.tender_classification_description
                }
            },
            "buyer": {
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name
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
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
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
                "additionalIdentifiers": [{
                    "scheme": "MD-IDNO",
                    "id": "string",
                    "legalName": "380935103469",
                    "uri": "http://petrusenko.com/svetlana"
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
            }],
            "planning": {
                "budget": {
                    "id": self.planning_budget_id,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    }
                },
                "rationale": self.planning_rationale
            }
        }
        session.execute(f"INSERT INTO orchestrator_context (cp_id,context) VALUES ("
                        f"'{cp_id}','{json.dumps(json_orchestrator_context)}');").one()

        session.execute(f"INSERT INTO budget_ei (cp_id,token_entity,created_date,json_data,owner) VALUES("
                        f"'{cp_id}',{ei_token},1609927348000,'{json.dumps(json_budget_ei)}','{owner}')"
                        f";").one()

        session.execute(f"INSERT INTO notice_budget_release ("
                        f"cp_id,oc_id,release_id,json_data,release_date,stage) VALUES("
                        f"'{cp_id}','{cp_id}','{cp_id + '1609927348000'}',"
                        f"'{json.dumps(json_notice_budget_release_ei)}',1609943491271,'EI');").one()

        session.execute(f"INSERT INTO notice_budget_offset (cp_id,release_date) VALUES("
                        f"'{cp_id}','1609927348000');").one()

        session.execute(f"INSERT INTO notice_budget_compiled_release ("
                        f"cp_id,oc_id,amount,json_data,publish_date,release_date,"
                        f"release_id,stage) VALUES('{cp_id}','{cp_id}', 0.0, "
                        f"'{json.dumps(json_notice_budget_compiled_release_ei)}',"
                        f"1609943491271,1609943491271,'{cp_id + '-' + f'{period[2]}'}',"
                        f"'EI');").one()
        allure.attach(owner, 'OWNER')
        allure.attach(cp_id, 'CPID')
        allure.attach(ei_token, 'X-TOKEN')
        allure.attach(f"http://dev.public.eprocurement.systems/budgets/{cp_id}", 'URL')
        return f"http://dev.public.eprocurement.systems/budgets/{cp_id}", ei_token, cp_id

    @allure.step('Insert EI')
    def insert_ei_obligatory_data_model(self, cp_id, ei_token):
        auth_provider = PlainTextAuthProvider(username=self.cassandra_username, password=self.cassandra_password)
        cluster = Cluster([self.cassandra_cluster], auth_provider=auth_provider)
        session = cluster.connect('ocds')
        owner = "445f6851-c908-407d-9b45-14b92f3e964b"
        period = get_period()
        json_orchestrator_context = {
            "operationId": f"{uuid4()}",
            "requestId": f"{uuid4()}",
            "cpid": cp_id,
            "stage": "EI",
            "processType": "ei",
            "operationType": "createEI",
            "owner": owner,
            "country": self.country,
            "language": self.lang,
            "token": ei_token,
            "startDate": self.planning_budget_period_start_date,
            "timeStamp": period[2],
            "isAuction": False,
            "testMode": False
        }
        json_budget_ei = {
            "ocid": cp_id,
            "tender": {
                "id": "fbd943ca-aaad-433d-9189-96566e3648ea",
                "title": self.tender_title,
                "status": "planning",
                "statusDetails": "empty",
                "classification": {
                    "id": self.tender_classification_id,
                    "scheme": self.tender_classification_scheme,
                    "description": self.tender_classification_description
                },
                "mainProcurementCategory": "works",
                "items": [{
                    "id": self.tender_items_id,
                    "description": self.tender_items_description,
                    "classification": {
                        "id": self.tender_item_classification_id,
                        "description": "Lucrări de pregătire a şantierului",
                        "scheme": "CPV"
                    },
                    "deliveryAddress": {
                        "addressDetails": {
                            "country": {
                                "id": self.tender_items_delivery_details_country_id,
                                "description": self.tender_items_delivery_details_country_description,
                                "scheme": self.tender_items_delivery_details_country_scheme,
                                "uri": self.tender_items_delivery_details_country_uri
                            },
                            "region": {
                                "id": self.tender_items_delivery_details_region_id,
                                "description": self.tender_items_delivery_details_region_description,
                                "scheme": self.tender_items_delivery_details_region_scheme,
                                "uri": self.tender_items_delivery_details_region_uri
                            }
                        }
                    },
                    "quantity": self.tender_items_quantity,
                    "unit": {
                        "id": self.tender_items_unit_id,
                        "name": self.tender_items_unit_name
                    }
                }]
            },
            "planning": {
                "budget": {
                    "id": self.planning_budget_id,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    }
                }
            },
            "buyer": {
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name,
                "identifier": {
                    "id": self.buyer_identifier_id,
                    "scheme": self.buyer_identifier_scheme,
                    "legalName": self.buyer_identifier_legal_name
                },
                "address": {
                    "streetAddress": self.buyer_address_street_address,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.buyer_address_address_details_country_id,
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
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
                }
            }
        }

        json_notice_budget_release_ei = {
            "ocid": cp_id,
            "id": cp_id + '-' + f'{period[2]}',
            "date": self.planning_budget_period_start_date,
            "tag": ["compiled"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "fbd943ca-aaad-433d-9189-96566e3648ea",
                "title": self.tender_title,
                "status": "planning",
                "statusDetails": "empty",
                "items": [{
                    "id": self.tender_items_id,
                    "description": self.tender_items_description,
                    "classification": {
                        "scheme": "CPV",
                        "id": self.tender_item_classification_id,
                        "description": "Lucrări de pregătire a şantierului"
                    },
                    "quantity": self.tender_items_quantity,
                    "unit": {
                        "id": self.tender_items_unit_id,
                        "name": self.tender_items_unit_name
                    },
                    "deliveryAddress": {
                        "addressDetails": {
                            "country": {
                                "id": self.tender_items_delivery_details_country_id,
                                "description": self.tender_items_delivery_details_country_description,
                                "scheme": self.tender_items_delivery_details_country_scheme,
                                "uri": self.tender_items_delivery_details_country_uri
                            },
                            "region": {
                                "id": self.tender_items_delivery_details_region_id,
                                "description": self.tender_items_delivery_details_region_description,
                                "scheme": self.tender_items_delivery_details_region_scheme,
                                "uri": self.tender_items_delivery_details_region_uri
                            }
                        }
                    }
                }],
                "mainProcurementCategory": "works",
                "classification": {
                    "scheme": self.tender_classification_scheme,
                    "id": self.tender_classification_id,
                    "description": "Lucrări de pregătire a şantierului"
                }
            },
            "buyer": {
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name
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
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
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
                "roles": ["buyer"]
            }],
            "planning": {
                "budget": {
                    "id": self.planning_budget_id,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    }
                }
            }
        }

        json_notice_budget_compiled_release_ei = {
            "ocid": cp_id,
            "id": cp_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": ["compiled"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "fbd943ca-aaad-433d-9189-96566e3648ea",
                "title": self.tender_title,
                "status": "planning",
                "statusDetails": "empty",
                "items": [{
                    "id": self.tender_items_id,
                    "description": self.tender_items_description,
                    "classification": {
                        "scheme": "CPV",
                        "id": self.tender_item_classification_id,
                        "description": "Lucrări de pregătire a şantierului"
                    },
                    "quantity": self.tender_items_quantity,
                    "unit": {
                        "id": self.tender_items_unit_id,
                        "name": self.tender_items_unit_name
                    },
                    "deliveryAddress": {
                        "addressDetails": {
                            "country": {
                                "id": self.tender_items_delivery_details_country_id,
                                "description": self.tender_items_delivery_details_country_description,
                                "scheme": self.tender_items_delivery_details_country_scheme,
                                "uri": self.tender_items_delivery_details_country_uri
                            },
                            "region": {
                                "id": self.tender_items_delivery_details_region_id,
                                "description": self.tender_items_delivery_details_region_description,
                                "scheme": self.tender_items_delivery_details_region_scheme,
                                "uri": self.tender_items_delivery_details_region_uri
                            }
                        }
                    }
                }],
                "mainProcurementCategory": "works",
                "classification": {
                    "scheme": self.tender_classification_scheme,
                    "id": self.tender_classification_id,
                    "description": self.tender_classification_description
                }
            },
            "buyer": {
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name
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
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
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
                "roles": ["buyer"]
            }],
            "planning": {
                "budget": {
                    "id": self.planning_budget_id,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    }
                }
            }
        }
        session.execute(f"INSERT INTO orchestrator_context (cp_id,context) VALUES ("
                        f"'{cp_id}','{json.dumps(json_orchestrator_context)}');").one()

        session.execute(f"INSERT INTO budget_ei (cp_id,token_entity,created_date,json_data,owner) VALUES("
                        f"'{cp_id}',{ei_token},1609927348000,'{json.dumps(json_budget_ei)}','{owner}')"
                        f";").one()

        session.execute(f"INSERT INTO notice_budget_release ("
                        f"cp_id,oc_id,release_id,json_data,release_date,stage) VALUES("
                        f"'{cp_id}','{cp_id}','{cp_id + '1609927348000'}',"
                        f"'{json.dumps(json_notice_budget_release_ei)}',1609943491271,'EI');").one()

        session.execute(f"INSERT INTO notice_budget_offset (cp_id,release_date) VALUES("
                        f"'{cp_id}','1609927348000');").one()

        session.execute(f"INSERT INTO notice_budget_compiled_release ("
                        f"cp_id,oc_id,amount,json_data,publish_date,release_date,"
                        f"release_id,stage) VALUES('{cp_id}','{cp_id}', 0.0, "
                        f"'{json.dumps(json_notice_budget_compiled_release_ei)}',"
                        f"1609943491271,1609943491271,'{cp_id + '-' + f'{period[2]}'}',"
                        f"'EI');").one()
        allure.attach(owner, 'OWNER')
        allure.attach(cp_id, 'CPID')
        allure.attach(ei_token, 'X-TOKEN')
        allure.attach(f"http://dev.public.eprocurement.systems/budgets/{cp_id}", 'URL')
        return f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{cp_id}", ei_token, cp_id

    @allure.step('Insert EI')
    def insert_ei_full_data_model_without_item(self, cp_id, ei_token):
        auth_provider = PlainTextAuthProvider(username=self.cassandra_username, password=self.cassandra_password)
        cluster = Cluster([self.cassandra_cluster], auth_provider=auth_provider)
        session = cluster.connect('ocds')
        owner = "445f6851-c908-407d-9b45-14b92f3e964b"
        period = get_period()
        json_orchestrator_context = {
            "operationId": f"{uuid4()}",
            "requestId": f"{uuid4()}",
            "cpid": cp_id,
            "stage": "EI",
            "processType": "ei",
            "operationType": "createEI",
            "owner": owner,
            "country": self.country,
            "language": self.lang,
            "token": ei_token,
            "startDate": self.planning_budget_period_start_date,
            "timeStamp": period[2],
            "isAuction": False,
            "testMode": False
        }
        json_budget_ei = {
            "ocid": cp_id,
            "tender": {
                "id": "fbd943ca-aaad-433d-9189-96566e3648ea",
                "title": self.tender_title,
                "description": self.tender_description,
                "status": "planning",
                "statusDetails": "empty",
                "classification": {
                    "id": self.tender_classification_id,
                    "scheme": self.tender_classification_scheme,
                    "description": self.tender_classification_description
                },
                "mainProcurementCategory": "works"
            },
            "planning": {
                "budget": {
                    "id": self.planning_budget_id,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    }
                },
                "rationale": self.planning_rationale
            },
            "buyer": {
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name,
                "identifier": {
                    "id": self.buyer_identifier_id,
                    "scheme": self.buyer_identifier_scheme,
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
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
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
                    "telephone": self.buyer_contact_point_telephone,
                    "faxNumber": self.buyer_contact_point_fax_number,
                    "url": self.buyer_contact_point_url
                },
                "additionalIdentifiers": [{
                    "id": "string",
                    "scheme": "MD-IDNO",
                    "legalName": "380935103469",
                    "uri": "http://petrusenko.com/svetlana"
                }],
                "details": {
                    "typeOfBuyer": "NATIONAL_AGENCY",
                    "mainGeneralActivity": "HEALTH",
                    "mainSectoralActivity": "WATER"
                }
            }
        }

        json_notice_budget_release_ei = {
            "ocid": cp_id,
            "id": cp_id + '-' + f'{period[2]}',
            "date": self.planning_budget_period_start_date,
            "tag": ["compiled"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "fbd943ca-aaad-433d-9189-96566e3648ea",
                "title": self.tender_title,
                "description": self.tender_description,
                "status": "planning",
                "statusDetails": "empty",
                "mainProcurementCategory": "works",
                "classification": {
                    "scheme": self.tender_classification_scheme,
                    "id": self.tender_classification_id,
                    "description": self.tender_classification_description
                }
            },
            "buyer": {
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name
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
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
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
                "additionalIdentifiers": [{
                    "scheme": "MD-IDNO",
                    "id": "string",
                    "legalName": "380935103469",
                    "uri": "http://petrusenko.com/svetlana"
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
            }],
            "planning": {
                "budget": {
                    "id": self.planning_budget_id,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    }
                },
                "rationale": self.planning_rationale
            }
        }

        json_notice_budget_compiled_release_ei = {
            "ocid": cp_id,
            "id": cp_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": ["compiled"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "fbd943ca-aaad-433d-9189-96566e3648ea",
                "title": self.tender_title,
                "description": self.tender_description,
                "status": "planning",
                "statusDetails": "empty",
                "mainProcurementCategory": "works",
                "classification": {
                    "scheme": self.tender_classification_scheme,
                    "id": self.tender_classification_id,
                    "description": self.tender_classification_description
                }
            },
            "buyer": {
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name
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
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
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
                "additionalIdentifiers": [{
                    "scheme": "MD-IDNO",
                    "id": "string",
                    "legalName": "380935103469",
                    "uri": "http://petrusenko.com/svetlana"
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
            }],
            "planning": {
                "budget": {
                    "id": self.planning_budget_id,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    }
                },
                "rationale": self.planning_rationale
            }
        }
        session.execute(f"INSERT INTO orchestrator_context (cp_id,context) VALUES ("
                        f"'{cp_id}','{json.dumps(json_orchestrator_context)}');").one()

        session.execute(f"INSERT INTO budget_ei (cp_id,token_entity,created_date,json_data,owner) VALUES("
                        f"'{cp_id}',{ei_token},1609927348000,'{json.dumps(json_budget_ei)}','{owner}')"
                        f";").one()

        session.execute(f"INSERT INTO notice_budget_release ("
                        f"cp_id,oc_id,release_id,json_data,release_date,stage) VALUES("
                        f"'{cp_id}','{cp_id}','{cp_id + '1609927348000'}',"
                        f"'{json.dumps(json_notice_budget_release_ei)}',1609943491271,'EI');").one()

        session.execute(f"INSERT INTO notice_budget_offset (cp_id,release_date) VALUES("
                        f"'{cp_id}','1609927348000');").one()

        session.execute(f"INSERT INTO notice_budget_compiled_release ("
                        f"cp_id,oc_id,amount,json_data,publish_date,release_date,"
                        f"release_id,stage) VALUES('{cp_id}','{cp_id}', 0.0, "
                        f"'{json.dumps(json_notice_budget_compiled_release_ei)}',"
                        f"1609943491271,1609943491271,'{cp_id + '-' + f'{period[2]}'}',"
                        f"'EI');").one()
        allure.attach(owner, 'OWNER')
        allure.attach(cp_id, 'CPID')
        allure.attach(ei_token, 'X-TOKEN')
        allure.attach(f"http://dev.public.eprocurement.systems/budgets/{cp_id}", 'URL')
        return f"http://dev.public.eprocurement.systems/budgets/{cp_id}", ei_token, cp_id

    @allure.step('Insert FS: Treasury - obligatory, based on EI: without items - obligatory')
    def insert_fs_treasury_obligatory_ei_obligatory_without_items(self, cp_id, ei_token):
        auth_provider = PlainTextAuthProvider(username=self.cassandra_username, password=self.cassandra_password)
        cluster = Cluster([self.cassandra_cluster], auth_provider=auth_provider)
        session = cluster.connect('ocds')
        owner = "445f6851-c908-407d-9b45-14b92f3e964b"
        fs_id = prepared_fs_oc_id(cp_id)
        fs_token = uuid4()
        period = get_period()
        json_orchestrator_context = {
            "operationId": f"{uuid4()}",
            "requestId": f"{uuid4()}",
            "cpid": cp_id,
            "ocid": fs_id,
            "stage": "FS",
            "processType": "fs",
            "operationType": "createFS",
            "owner": owner,
            "country": self.country,
            "language": self.lang,
            "token": f"{fs_token}",
            "startDate": self.planning_budget_period_start_date,
            "timeStamp": period[2],
            "isAuction": False
        }

        json_budget_ei = {
            "ocid": cp_id,
            "tender": {
                "id": "2cc5a0b7-b1b7-4ed3-9210-1ca6d0af3261",
                "title": "Cardurilor de acces pentru Bibliotecii Municipale B.P. Hasdeu ",
                "status": "planning",
                "statusDetails": "empty",
                "classification": {
                    "id": self.tender_classification_id,
                    "scheme": self.tender_classification_scheme,
                    "description": self.tender_classification_description
                },
                "mainProcurementCategory": "works"
            },
            "planning": {
                "budget": {
                    "id": self.planning_budget_id,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    }
                }
            },
            "buyer": {
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name,
                "identifier": {
                    "id": self.buyer_identifier_id,
                    "scheme": self.buyer_identifier_scheme,
                    "legalName": self.buyer_identifier_legal_name
                },
                "address": {
                    "streetAddress": self.buyer_address_street_address,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.buyer_address_address_details_country_id,
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
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
                }
            }
        }

        json_budget_fs = {
            "ocid": fs_id,
            "tender": {
                "id": "195cf37f-99cc-4729-8374-596f2fba1810",
                "status": "planning",
                "statusDetails": "empty"
            },
            "planning": {
                "budget": {
                    "id": None,
                    "description": None,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    },
                    "europeanUnionFunding": None,
                    "isEuropeanUnionFunded": False,
                    "verified": False,
                    "sourceEntity": {
                        "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                        "name": self.buyer_name,
                    },
                    "verificationDetails": None,
                    "project": None,
                    "projectID": None,
                    "uri": None
                }
            },
            "payer": {
                "id": f"{self.payer_identifier_scheme}-{self.payer_identifier_id}",
                "name": self.payer_name,
                "identifier": {
                    "id": self.payer_identifier_id,
                    "scheme": self.payer_identifier_scheme,
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
                }
            }
        }

        json_notice_budget_release_ei = {
            "ocid": cp_id,
            "id": cp_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": ["compiled"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "2cc5a0b7-b1b7-4ed3-9210-1ca6d0af3261",
                "title": "Cardurilor de acces pentru Bibliotecii Municipale B.P. Hasdeu ",
                "status": "planning",
                "statusDetails": "empty",
                "mainProcurementCategory": "works",
                "classification": {
                    "scheme": self.tender_classification_scheme,
                    "id": self.tender_classification_id,
                    "description": self.tender_classification_description
                }
            },
            "buyer": {
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name,
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
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
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
                "roles": ["buyer"]
            }],
            "planning": {
                "budget": {
                    "id": self.planning_budget_id,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    }
                }
            },
            "relatedProcesses": [{
                "id": "412ee2c0-b194-11eb-8505-35fcd4e9bc47",
                "relationship": ["x_fundingSource"],
                "scheme": "ocid",
                "identifier": f"{fs_id}",
                "uri": f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{fs_id}"
            }]
        }

        json_notice_budget_release_fs = {
            "ocid": fs_id,
            "id": fs_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": ["planning"],
            "initiationType": "tender",
            "tender": {
                "id": "195cf37f-99cc-4729-8374-596f2fba1810",
                "status": "planning",
                "statusDetails": "empty"
            },
            "parties": [{
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
            }],
            "planning": {
                "budget": {
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    },
                    "isEuropeanUnionFunded": False,
                    "verified": False,
                    "sourceEntity": {
                        "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                        "name": self.buyer_name
                    }
                }
            },
            "relatedProcesses": [{
                "id": "412d5c20-b194-11eb-8505-35fcd4e9bc47",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": cp_id,
                "uri": f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{cp_id}"
            }]
        }

        json_notice_budget_compiled_release_ei = {
            "ocid": cp_id,
            "id": cp_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": ["compiled"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "2cc5a0b7-b1b7-4ed3-9210-1ca6d0af3261",
                "title": "Cardurilor de acces pentru Bibliotecii Municipale B.P. Hasdeu ",
                "status": "planning",
                "statusDetails": "empty",
                "mainProcurementCategory": "works",
                "classification": {
                    "scheme": self.tender_classification_scheme,
                    "id": self.tender_classification_id,
                    "description": self.tender_classification_description
                }
            },
            "buyer": {
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name
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
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
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
                "roles": ["buyer"]
            }],
            "planning": {
                "budget": {
                    "id": self.tender_classification_id,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    }
                }
            },
            "relatedProcesses": [{
                "id": "412ee2c0-b194-11eb-8505-35fcd4e9bc47",
                "relationship": ["x_fundingSource"],
                "scheme": "ocid",
                "identifier": f"{fs_id}",
                "uri": f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{fs_id}"
            }]
        }

        json_notice_budget_compiled_release_fs = {
            "ocid": fs_id,
            "id": fs_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": ["planning"],
            "initiationType": "tender",
            "tender": {
                "id": "195cf37f-99cc-4729-8374-596f2fba1810",
                "status": "planning",
                "statusDetails": "empty"
            },
            "parties": [{
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
            }],
            "planning": {
                "budget": {
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    },
                    "isEuropeanUnionFunded": False,
                    "verified": False,
                    "sourceEntity": {
                        "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                        "name": self.buyer_name
                    }
                }
            },
            "relatedProcesses": [{
                "id": "412d5c20-b194-11eb-8505-35fcd4e9bc47",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": f"{cp_id}",
                "uri": f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{cp_id}"
            }]
        }

        session.execute(f"INSERT INTO orchestrator_context (cp_id,context) VALUES ("
                        f"'{cp_id}','{json.dumps(json_orchestrator_context)}');").one()
        session.execute(f"INSERT INTO budget_ei (cp_id,token_entity,created_date,json_data,owner) VALUES("
                        f"'{cp_id}',{ei_token},{period[2]},'{json.dumps(json_budget_ei)}','{owner}');").one()
        session.execute(
            f"INSERT INTO budget_fs (cp_id,token_entity,amount,amount_reserved,created_date,json_data,oc_id,owner) "
            f"VALUES ('{cp_id}',{fs_token},{self.amount},0,{period[2]},'{json.dumps(json_budget_fs)}',"
            f"'{fs_id}','{owner}');").one()
        session.execute(f"INSERT INTO notice_budget_release ("
                        f"cp_id,oc_id,release_id,json_data,release_date,stage) VALUES("
                        f"'{cp_id}','{cp_id}','{cp_id + str(period[2])}',"
                        f"'{json.dumps(json_notice_budget_release_ei)}',{period[2]},'EI');").one()
        session.execute(f"INSERT INTO notice_budget_compiled_release ("
                        f"cp_id,oc_id,amount,json_data,publish_date,release_date,"
                        f"release_id,stage) VALUES('{cp_id}','{cp_id}', 0.0, "
                        f"'{json.dumps(json_notice_budget_compiled_release_ei)}',"
                        f"{period[2]},{period[2]},'{cp_id + '-' + f'{period[2]}'}',"
                        f"'EI');").one()
        session.execute(
            f"INSERT INTO notice_budget_release (cp_id,oc_id,release_id,json_data,release_date,stage) "
            f"VALUES ('{cp_id}','{fs_id}','{fs_id + '-' + str(period[2])}',"
            f"'{json.dumps(json_notice_budget_release_fs)}',{period[2]},'FS');").one()
        session.execute(
            f"INSERT INTO notice_budget_compiled_release (cp_id,oc_id,amount,json_data,publish_date,release_date,"
            f"release_id,stage) VALUES ('{cp_id}','{fs_id}',{self.amount},"
            f"'{json.dumps(json_notice_budget_compiled_release_fs)}',{period[2]},{period[2]},"
            f"'{fs_id + '-' + str(period[2])}','FS');")
        session.execute(f"INSERT INTO notice_budget_offset (cp_id,release_date) "
                        f"VALUES ('{cp_id}',{period[2]});").one()
        return f"http://dev.public.eprocurement.systems/budgets/{cp_id}", fs_id, fs_token

    @allure.step('Insert FS: Treasury - full, based on EI: without items - obligatory')
    def insert_fs_treasury_full_ei_obligatory_without_items(self, cp_id, ei_token):
        auth_provider = PlainTextAuthProvider(username=self.cassandra_username, password=self.cassandra_password)
        cluster = Cluster([self.cassandra_cluster], auth_provider=auth_provider)
        session = cluster.connect('ocds')
        owner = "445f6851-c908-407d-9b45-14b92f3e964b"
        fs_id = prepared_fs_oc_id(cp_id)
        fs_token = uuid4()
        period = get_period()
        json_orchestrator_context = {
            "operationId": f"{uuid4()}",
            "requestId": f"{uuid4()}",
            "cpid": cp_id,
            "ocid": fs_id,
            "stage": "FS",
            "processType": "fs",
            "operationType": "createFS",
            "owner": owner,
            "country": self.country,
            "language": self.lang,
            "token": f"{fs_token}",
            "startDate": self.planning_budget_period_start_date,
            "timeStamp": period[2],
            "isAuction": False
        }

        json_budget_ei = {
            "ocid": cp_id,
            "tender": {
                "id": "2cc5a0b7-b1b7-4ed3-9210-1ca6d0af3261",
                "title": "Cardurilor de acces pentru Bibliotecii Municipale B.P. Hasdeu ",
                "status": "planning",
                "statusDetails": "empty",
                "classification": {
                    "id": self.tender_classification_id,
                    "scheme": self.tender_classification_scheme,
                    "description": self.tender_classification_description
                },
                "mainProcurementCategory": "works"
            },
            "planning": {
                "budget": {
                    "id": self.planning_budget_id,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    }
                }
            },
            "buyer": {
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name,
                "identifier": {
                    "id": self.buyer_identifier_id,
                    "scheme": self.buyer_identifier_scheme,
                    "legalName": self.buyer_identifier_legal_name,
                },
                "address": {
                    "streetAddress": self.buyer_address_street_address,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.buyer_address_address_details_country_id,
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
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
                }
            }
        }

        json_budget_fs = {
            "ocid": fs_id,
            "tender": {
                "id": "195cf37f-99cc-4729-8374-596f2fba1810",
                "status": "planning",
                "statusDetails": "empty"
            },
            "planning": {
                "budget": {
                    "id": self.tender_classification_id,
                    "description": "description",
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    },
                    "europeanUnionFunding": {
                        "projectName": "Name of this project",
                        "projectIdentifier": "projectIdentifier",
                        "uri": "http://uriuri.th"
                    },
                    "isEuropeanUnionFunded": True,
                    "verified": False,
                    "sourceEntity": {
                        "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                        "name": self.buyer_name,
                    },
                    "verificationDetails": None,
                    "project": "project",
                    "projectID": "projectID",
                    "uri": "http://uri.ur"
                },
                "rationale": "reason for the budget"
            },
            "payer": {
                "id": f"{self.payer_identifier_scheme}-{self.payer_identifier_id}",
                "name": self.payer_name,
                "identifier": {
                    "id": self.payer_identifier_id,
                    "scheme": self.payer_identifier_scheme,
                    "legalName": self.payer_identifier_legal_name,
                    "uri": "http://454.to"
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
                "additionalIdentifiers": [{
                    "id": "additional identifier",
                    "scheme": "MD-K",
                    "legalName": "legalname",
                    "uri": "http://k.to"
                }],
                "contactPoint": {
                    "name": self.payer_contact_point_name,
                    "email": self.payer_contact_point_email,
                    "telephone": self.payer_contact_point_telephone,
                    "faxNumber": self.payer_contact_point_fax_number,
                    "url": self.payer_contact_point_url
                }
            }
        }

        json_notice_budget_release_ei = {
            "ocid": cp_id,
            "id": cp_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": ["compiled"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "2cc5a0b7-b1b7-4ed3-9210-1ca6d0af3261",
                "title": "Cardurilor de acces pentru Bibliotecii Municipale B.P. Hasdeu ",
                "status": "planning",
                "statusDetails": "empty",
                "mainProcurementCategory": "works",
                "classification": {
                    "scheme": self.tender_classification_scheme,
                    "id": self.tender_classification_id,
                    "description": self.tender_classification_description
                }
            },
            "buyer": {
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name,
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
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
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
                "roles": ["buyer"]
            }],
            "planning": {
                "budget": {
                    "id": self.planning_budget_id,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    }
                }
            },
            "relatedProcesses": [{
                "id": "412ee2c0-b194-11eb-8505-35fcd4e9bc47",
                "relationship": ["x_fundingSource"],
                "scheme": "ocid",
                "identifier": f"{fs_id}",
                "uri": f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{fs_id}"
            }]
        }

        json_notice_budget_release_fs = {
            "ocid": fs_id,
            "id": fs_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": ["planning"],
            "initiationType": "tender",
            "tender": {
                "id": "195cf37f-99cc-4729-8374-596f2fba1810",
                "status": "planning",
                "statusDetails": "empty"
            },
            "parties": [{
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
                "additionalIdentifiers": [{
                    "scheme": "MD-K",
                    "id": "additional identifier",
                    "legalName": "legalname",
                    "uri": "http://k.to"
                }],
                "contactPoint": {
                    "name": self.payer_contact_point_name,
                    "email": self.payer_contact_point_email,
                    "telephone": self.payer_contact_point_telephone,
                    "faxNumber": self.payer_contact_point_fax_number,
                    "url": self.payer_contact_point_url
                },
                "roles": ["payer"]
            }],
            "planning": {
                "budget": {
                    "id": self.tender_classification_id,
                    "description": "description",
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    },
                    "europeanUnionFunding": {
                        "projectIdentifier": "projectIdentifier",
                        "projectName": "Name of this project",
                        "uri": "http://uriuri.th"
                    },
                    "isEuropeanUnionFunded": True,
                    "verified": False,
                    "sourceEntity": {
                        "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                        "name": self.buyer_name
                    },
                    "project": "project",
                    "projectID": "projectID",
                    "uri": "http://uri.ur"
                },
                "rationale": "reason for the budget"
            },
            "relatedProcesses": [{
                "id": "412d5c20-b194-11eb-8505-35fcd4e9bc47",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": cp_id,
                "uri": f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{cp_id}"
            }]
        }

        json_notice_budget_compiled_release_ei = {
            "ocid": cp_id,
            "id": cp_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": ["compiled"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "2cc5a0b7-b1b7-4ed3-9210-1ca6d0af3261",
                "title": "Cardurilor de acces pentru Bibliotecii Municipale B.P. Hasdeu ",
                "status": "planning",
                "statusDetails": "empty",
                "mainProcurementCategory": "works",
                "classification": {
                    "scheme": self.tender_classification_scheme,
                    "id": self.tender_classification_id,
                    "description": self.tender_classification_description
                }
            },
            "buyer": {
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name
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
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
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
                "roles": ["buyer"]
            }],
            "planning": {
                "budget": {
                    "id": self.tender_classification_id,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    }
                }
            },
            "relatedProcesses": [{
                "id": "412ee2c0-b194-11eb-8505-35fcd4e9bc47",
                "relationship": ["x_fundingSource"],
                "scheme": "ocid",
                "identifier": f"{fs_id}",
                "uri": f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{fs_id}"
            }]
        }

        json_notice_budget_compiled_release_fs = {
            "ocid": fs_id,
            "id": fs_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": ["planning"],
            "initiationType": "tender",
            "tender": {
                "id": "195cf37f-99cc-4729-8374-596f2fba1810",
                "status": "planning",
                "statusDetails": "empty"
            },
            "parties": [{
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
                "additionalIdentifiers": [{
                    "scheme": "MD-K",
                    "id": "additional identifier",
                    "legalName": "legalname",
                    "uri": "http://k.to"
                }],
                "contactPoint": {
                    "name": self.payer_contact_point_name,
                    "email": self.payer_contact_point_email,
                    "telephone": self.payer_contact_point_telephone,
                    "faxNumber": self.payer_contact_point_fax_number,
                    "url": self.payer_contact_point_url
                },
                "roles": ["payer"]
            }],
            "planning": {
                "budget": {
                    "id": self.tender_classification_id,
                    "description": "description",
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    },
                    "europeanUnionFunding": {
                        "projectIdentifier": "projectIdentifier",
                        "projectName": "Name of this project",
                        "uri": "http://uriuri.th"
                    },
                    "isEuropeanUnionFunded": True,
                    "verified": False,
                    "sourceEntity": {
                        "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                        "name": self.buyer_name
                    },
                    "project": "project",
                    "projectID": "projectID",
                    "uri": "http://uri.ur"
                },
                "rationale": "reason for the budget"
            },
            "relatedProcesses": [{
                "id": "412d5c20-b194-11eb-8505-35fcd4e9bc47",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": f"{cp_id}",
                "uri": f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{cp_id}"
            }]
        }

        session.execute(f"INSERT INTO orchestrator_context (cp_id,context) VALUES ("
                        f"'{cp_id}','{json.dumps(json_orchestrator_context)}');").one()
        session.execute(f"INSERT INTO budget_ei (cp_id,token_entity,created_date,json_data,owner) VALUES("
                        f"'{cp_id}',{ei_token},{period[2]},'{json.dumps(json_budget_ei)}','{owner}');").one()
        session.execute(
            f"INSERT INTO budget_fs (cp_id,token_entity,amount,amount_reserved,created_date,json_data,oc_id,owner) "
            f"VALUES ('{cp_id}',{fs_token},{self.amount},0,{period[2]},'{json.dumps(json_budget_fs)}',"
            f"'{fs_id}','{owner}');").one()
        session.execute(f"INSERT INTO notice_budget_release ("
                        f"cp_id,oc_id,release_id,json_data,release_date,stage) VALUES("
                        f"'{cp_id}','{cp_id}','{cp_id + str(period[2])}',"
                        f"'{json.dumps(json_notice_budget_release_ei)}',{period[2]},'EI');").one()
        session.execute(f"INSERT INTO notice_budget_compiled_release ("
                        f"cp_id,oc_id,amount,json_data,publish_date,release_date,"
                        f"release_id,stage) VALUES('{cp_id}','{cp_id}', 0.0, "
                        f"'{json.dumps(json_notice_budget_compiled_release_ei)}',"
                        f"{period[2]},{period[2]},'{cp_id + '-' + f'{period[2]}'}',"
                        f"'EI');").one()
        session.execute(
            f"INSERT INTO notice_budget_release (cp_id,oc_id,release_id,json_data,release_date,stage) "
            f"VALUES ('{cp_id}','{fs_id}','{fs_id + '-' + str(period[2])}',"
            f"'{json.dumps(json_notice_budget_release_fs)}',{period[2]},'FS');").one()
        session.execute(
            f"INSERT INTO notice_budget_compiled_release (cp_id,oc_id,amount,json_data,publish_date,release_date,"
            f"release_id,stage) VALUES ('{cp_id}','{fs_id}',{self.amount},"
            f"'{json.dumps(json_notice_budget_compiled_release_fs)}',{period[2]},{period[2]},"
            f"'{fs_id + '-' + str(period[2])}','FS');")
        session.execute(f"INSERT INTO notice_budget_offset (cp_id,release_date) "
                        f"VALUES ('{cp_id}',{period[2]});").one()
        return f"http://dev.public.eprocurement.systems/budgets/{cp_id}", fs_id, fs_token

    @allure.step('Insert FS: Treasury - obligatory, based on EI: without items - full')
    def insert_fs_treasury_obligatory_ei_full_without_items(self, cp_id, ei_token):
        auth_provider = PlainTextAuthProvider(username=self.cassandra_username, password=self.cassandra_password)
        cluster = Cluster([self.cassandra_cluster], auth_provider=auth_provider)
        session = cluster.connect('ocds')
        owner = "445f6851-c908-407d-9b45-14b92f3e964b"
        fs_id = prepared_fs_oc_id(cp_id)
        fs_token = uuid4()
        period = get_period()
        json_orchestrator_context = {
            "operationId": f"{uuid4()}",
            "requestId": f"{uuid4()}",
            "cpid": cp_id,
            "ocid": fs_id,
            "stage": "FS",
            "processType": "fs",
            "operationType": "createFS",
            "owner": owner,
            "country": self.country,
            "language": self.lang,
            "token": f"{fs_token}",
            "startDate": self.planning_budget_period_start_date,
            "timeStamp": period[2],
            "isAuction": False
        }

        json_budget_ei = {
            "ocid": cp_id,
            "tender": {
                "id": "2cc5a0b7-b1b7-4ed3-9210-1ca6d0af3261",
                "title": "Cardurilor de acces pentru Bibliotecii Municipale B.P. Hasdeu ",
                "description": self.tender_description,
                "status": "planning",
                "statusDetails": "empty",
                "classification": {
                    "id": self.tender_classification_id,
                    "scheme": self.tender_classification_scheme,
                    "description": self.tender_classification_description
                },
                "mainProcurementCategory": "works"
            },
            "planning": {
                "budget": {
                    "id": self.planning_budget_id,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    }
                },
                "rationale": "planning.rationale"
            },
            "buyer": {
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name,
                "identifier": {
                    "id": self.buyer_identifier_id,
                    "scheme": self.buyer_identifier_scheme,
                    "legalName": self.buyer_identifier_legal_name,
                    "uri": "http://petrusenko.com/fop"
                },
                "address": {
                    "streetAddress": self.buyer_address_street_address,
                    "postalCode": self.buyer_address_postal_code,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.buyer_address_address_details_country_id,
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
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
                    "telephone": self.buyer_contact_point_telephone,
                    "faxNumber": self.buyer_contact_point_fax_number,
                    "url": self.buyer_contact_point_url
                },
                "additionalIdentifiers": [{
                    "id": "string",
                    "scheme": "MD-IDNO",
                    "legalName": "380935103469",
                    "uri": "http://petrusenko.com/svetlana"
                }],
                "details": {
                    "typeOfBuyer": "NATIONAL_AGENCY",
                    "mainGeneralActivity": "HEALTH",
                    "mainSectoralActivity": "WATER"
                }
            }
        }

        json_budget_fs = {
            "ocid": fs_id,
            "tender": {
                "id": "195cf37f-99cc-4729-8374-596f2fba1810",
                "status": "planning",
                "statusDetails": "empty"
            },
            "planning": {
                "budget": {
                    "id": None,
                    "description": None,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    },
                    "europeanUnionFunding": None,
                    "isEuropeanUnionFunded": False,
                    "verified": False,
                    "sourceEntity": {
                        "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                        "name": self.buyer_name,
                    },
                    "verificationDetails": None,
                    "project": None,
                    "projectID": None,
                    "uri": None
                }
            },
            "payer": {
                "id": f"{self.payer_identifier_scheme}-{self.payer_identifier_id}",
                "name": self.payer_name,
                "identifier": {
                    "id": self.payer_identifier_id,
                    "scheme": self.payer_identifier_scheme,
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
                }
            }
        }

        json_notice_budget_release_ei = {
            "ocid": cp_id,
            "id": cp_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": ["compiled"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "2cc5a0b7-b1b7-4ed3-9210-1ca6d0af3261",
                "title": "Cardurilor de acces pentru Bibliotecii Municipale B.P. Hasdeu ",
                "description": "description of finansical sourse",
                "status": "planning",
                "statusDetails": "empty",
                "mainProcurementCategory": "works",
                "classification": {
                    "scheme": self.tender_classification_scheme,
                    "id": self.tender_classification_id,
                    "description": self.tender_classification_description
                }
            },
            "buyer": {
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name,
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
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
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
                "additionalIdentifiers": [{
                    "scheme": "MD-IDNO",
                    "id": "string",
                    "legalName": "380935103469",
                    "uri": "http://petrusenko.com/svetlana"
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
            }],
            "planning": {
                "budget": {
                    "id": self.planning_budget_id,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    }
                },
                "rationale": self.planning_rationale
            },
            "relatedProcesses": [{
                "id": "412ee2c0-b194-11eb-8505-35fcd4e9bc47",
                "relationship": ["x_fundingSource"],
                "scheme": "ocid",
                "identifier": f"{fs_id}",
                "uri": f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{fs_id}"
            }]
        }

        json_notice_budget_release_fs = {
            "ocid": fs_id,
            "id": fs_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": ["planning"],
            "initiationType": "tender",
            "tender": {
                "id": "195cf37f-99cc-4729-8374-596f2fba1810",
                "status": "planning",
                "statusDetails": "empty"
            },
            "parties": [{
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
            }],
            "planning": {
                "budget": {
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    },
                    "isEuropeanUnionFunded": False,
                    "verified": False,
                    "sourceEntity": {
                        "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                        "name": self.buyer_name
                    }
                }
            },
            "relatedProcesses": [{
                "id": "412d5c20-b194-11eb-8505-35fcd4e9bc47",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": cp_id,
                "uri": f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{cp_id}"
            }]
        }

        json_notice_budget_compiled_release_ei = {
            "ocid": cp_id,
            "id": cp_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": ["compiled"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "2cc5a0b7-b1b7-4ed3-9210-1ca6d0af3261",
                "title": "Cardurilor de acces pentru Bibliotecii Municipale B.P. Hasdeu ",
                "description": "description of finansical sourse",
                "status": "planning",
                "statusDetails": "empty",
                "mainProcurementCategory": "works",
                "classification": {
                    "scheme": self.tender_classification_scheme,
                    "id": self.tender_classification_id,
                    "description": self.tender_classification_description
                }
            },
            "buyer": {
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name
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
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
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
                "additionalIdentifiers": [{
                    "scheme": "MD-IDNO",
                    "id": "string",
                    "legalName": "380935103469",
                    "uri": "http://petrusenko.com/svetlana"
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
            }],
            "planning": {
                "budget": {
                    "id": self.tender_classification_id,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    }
                },
                "rationale": self.planning_rationale
            },
            "relatedProcesses": [{
                "id": "412ee2c0-b194-11eb-8505-35fcd4e9bc47",
                "relationship": ["x_fundingSource"],
                "scheme": "ocid",
                "identifier": f"{fs_id}",
                "uri": f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{fs_id}"
            }]
        }

        json_notice_budget_compiled_release_fs = {
            "ocid": fs_id,
            "id": fs_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": ["planning"],
            "initiationType": "tender",
            "tender": {
                "id": "195cf37f-99cc-4729-8374-596f2fba1810",
                "status": "planning",
                "statusDetails": "empty"
            },
            "parties": [{
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
            }],
            "planning": {
                "budget": {
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    },
                    "isEuropeanUnionFunded": False,
                    "verified": False,
                    "sourceEntity": {
                        "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                        "name": self.buyer_name
                    }
                }
            },
            "relatedProcesses": [{
                "id": "412d5c20-b194-11eb-8505-35fcd4e9bc47",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": f"{cp_id}",
                "uri": f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{cp_id}"
            }]
        }

        session.execute(f"INSERT INTO orchestrator_context (cp_id,context) VALUES ("
                        f"'{cp_id}','{json.dumps(json_orchestrator_context)}');").one()
        session.execute(f"INSERT INTO budget_ei (cp_id,token_entity,created_date,json_data,owner) VALUES("
                        f"'{cp_id}',{ei_token},{period[2]},'{json.dumps(json_budget_ei)}','{owner}');").one()
        session.execute(
            f"INSERT INTO budget_fs (cp_id,token_entity,amount,amount_reserved,created_date,json_data,oc_id,owner) "
            f"VALUES ('{cp_id}',{fs_token},{self.amount},0,{period[2]},'{json.dumps(json_budget_fs)}',"
            f"'{fs_id}','{owner}');").one()
        session.execute(f"INSERT INTO notice_budget_release ("
                        f"cp_id,oc_id,release_id,json_data,release_date,stage) VALUES("
                        f"'{cp_id}','{cp_id}','{cp_id + str(period[2])}',"
                        f"'{json.dumps(json_notice_budget_release_ei)}',{period[2]},'EI');").one()
        session.execute(f"INSERT INTO notice_budget_compiled_release ("
                        f"cp_id,oc_id,amount,json_data,publish_date,release_date,"
                        f"release_id,stage) VALUES('{cp_id}','{cp_id}', 0.0, "
                        f"'{json.dumps(json_notice_budget_compiled_release_ei)}',"
                        f"{period[2]},{period[2]},'{cp_id + '-' + f'{period[2]}'}',"
                        f"'EI');").one()
        session.execute(
            f"INSERT INTO notice_budget_release (cp_id,oc_id,release_id,json_data,release_date,stage) "
            f"VALUES ('{cp_id}','{fs_id}','{fs_id + '-' + str(period[2])}',"
            f"'{json.dumps(json_notice_budget_release_fs)}',{period[2]},'FS');").one()
        session.execute(
            f"INSERT INTO notice_budget_compiled_release (cp_id,oc_id,amount,json_data,publish_date,release_date,"
            f"release_id,stage) VALUES ('{cp_id}','{fs_id}',{self.amount},"
            f"'{json.dumps(json_notice_budget_compiled_release_fs)}',{period[2]},{period[2]},"
            f"'{fs_id + '-' + str(period[2])}','FS');")
        session.execute(f"INSERT INTO notice_budget_offset (cp_id,release_date) "
                        f"VALUES ('{cp_id}',{period[2]});").one()
        return f"http://dev.public.eprocurement.systems/budgets/{cp_id}", fs_id, fs_token

    @allure.step('Insert FS: Treasury - full, based on EI: with items - obligatory')
    def insert_fs_treasury_full_ei_obligatory_with_items(self, cp_id, ei_token):
        auth_provider = PlainTextAuthProvider(username=self.cassandra_username, password=self.cassandra_password)
        cluster = Cluster([self.cassandra_cluster], auth_provider=auth_provider)
        session = cluster.connect('ocds')
        owner = "445f6851-c908-407d-9b45-14b92f3e964b"
        fs_id = prepared_fs_oc_id(cp_id)
        fs_token = uuid4()
        period = get_period()
        json_orchestrator_context = {
            "operationId": f"{uuid4()}",
            "requestId": f"{uuid4()}",
            "cpid": cp_id,
            "ocid": fs_id,
            "stage": "FS",
            "processType": "fs",
            "operationType": "createFS",
            "owner": owner,
            "country": self.country,
            "language": self.lang,
            "token": f"{fs_token}",
            "startDate": self.planning_budget_period_start_date,
            "timeStamp": period[2],
            "isAuction": False
        }

        json_budget_ei = {
            "ocid": cp_id,
            "tender": {
                "id": "2cc5a0b7-b1b7-4ed3-9210-1ca6d0af3261",
                "title": "Cardurilor de acces pentru Bibliotecii Municipale B.P. Hasdeu ",
                "status": "planning",
                "statusDetails": "empty",
                "classification": {
                    "id": self.tender_classification_id,
                    "scheme": self.tender_classification_scheme,
                    "description": self.tender_classification_description
                },
                "mainProcurementCategory": "works",
                "items": [{
                    "id": self.tender_items_id,
                    "description": self.tender_items_description,
                    "classification": {
                        "id": self.tender_item_classification_id,
                        "description": "Lucrări de pregătire a şantierului",
                        "scheme": "CPV"
                    },
                    "deliveryAddress": {
                        "addressDetails": {
                            "country": {
                                "id": self.tender_items_delivery_details_country_id,
                                "description": self.tender_items_delivery_details_country_description,
                                "scheme": self.tender_items_delivery_details_country_scheme,
                                "uri": self.tender_items_delivery_details_country_uri
                            },
                            "region": {
                                "id": self.tender_items_delivery_details_region_id,
                                "description": self.tender_items_delivery_details_region_description,
                                "scheme": self.tender_items_delivery_details_region_scheme,
                                "uri": self.tender_items_delivery_details_region_uri
                            }
                        }
                    },
                    "quantity": self.tender_items_quantity,
                    "unit": {
                        "id": self.tender_items_unit_id,
                        "name": self.tender_items_unit_name
                    }
                }]
            },
            "planning": {
                "budget": {
                    "id": self.planning_budget_id,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    }
                }
            },
            "buyer": {
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name,
                "identifier": {
                    "id": self.buyer_identifier_id,
                    "scheme": self.buyer_identifier_scheme,
                    "legalName": self.buyer_identifier_legal_name,
                },
                "address": {
                    "streetAddress": self.buyer_address_street_address,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.buyer_address_address_details_country_id,
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
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
                }
            }
        }

        json_budget_fs = {
            "ocid": fs_id,
            "tender": {
                "id": "195cf37f-99cc-4729-8374-596f2fba1810",
                "status": "planning",
                "statusDetails": "empty"
            },
            "planning": {
                "budget": {
                    "id": self.tender_classification_id,
                    "description": "description",
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    },
                    "europeanUnionFunding": {
                        "projectName": "Name of this project",
                        "projectIdentifier": "projectIdentifier",
                        "uri": "http://uriuri.th"
                    },
                    "isEuropeanUnionFunded": True,
                    "verified": False,
                    "sourceEntity": {
                        "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                        "name": self.buyer_name,
                    },
                    "verificationDetails": None,
                    "project": "project",
                    "projectID": "projectID",
                    "uri": "http://uri.ur"
                },
                "rationale": "reason for the budget"
            },
            "payer": {
                "id": f"{self.payer_identifier_scheme}-{self.payer_identifier_id}",
                "name": self.payer_name,
                "identifier": {
                    "id": self.payer_identifier_id,
                    "scheme": self.payer_identifier_scheme,
                    "legalName": self.payer_identifier_legal_name,
                    "uri": "http://454.to"
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
                "additionalIdentifiers": [{
                    "id": "additional identifier",
                    "scheme": "MD-K",
                    "legalName": "legalname",
                    "uri": "http://k.to"
                }],
                "contactPoint": {
                    "name": self.payer_contact_point_name,
                    "email": self.payer_contact_point_email,
                    "telephone": self.payer_contact_point_telephone,
                    "faxNumber": self.payer_contact_point_fax_number,
                    "url": self.payer_contact_point_url
                }
            }
        }

        json_notice_budget_release_ei = {
            "ocid": cp_id,
            "id": cp_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": ["compiled"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "2cc5a0b7-b1b7-4ed3-9210-1ca6d0af3261",
                "title": "Cardurilor de acces pentru Bibliotecii Municipale B.P. Hasdeu ",
                "status": "planning",
                "statusDetails": "empty",
                "items": [{
                    "id": self.tender_items_id,
                    "description": self.tender_items_description,
                    "classification": {
                        "id": self.tender_item_classification_id,
                        "description": "Lucrări de pregătire a şantierului",
                        "scheme": "CPV"
                    },
                    "quantity": self.tender_items_quantity,
                    "unit": {
                        "name": self.tender_items_unit_name,
                        "id": self.tender_items_unit_id
                    },
                    "deliveryAddress": {
                        "addressDetails": {
                            "country": {
                                "id": self.tender_items_delivery_details_country_id,
                                "description": self.tender_items_delivery_details_country_description,
                                "scheme": self.tender_items_delivery_details_country_scheme,
                                "uri": self.tender_items_delivery_details_country_uri
                            },
                            "region": {
                                "id": self.tender_items_delivery_details_region_id,
                                "description": self.tender_items_delivery_details_region_description,
                                "scheme": self.tender_items_delivery_details_region_scheme,
                                "uri": self.tender_items_delivery_details_region_uri
                            }
                        }
                    }

                }],
                "mainProcurementCategory": "works",
                "classification": {
                    "scheme": self.tender_classification_scheme,
                    "id": self.tender_classification_id,
                    "description": self.tender_classification_description
                }
            },
            "buyer": {
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name,
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
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
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
                "roles": ["buyer"]
            }],
            "planning": {
                "budget": {
                    "id": self.planning_budget_id,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    }
                }
            },
            "relatedProcesses": [{
                "id": "412ee2c0-b194-11eb-8505-35fcd4e9bc47",
                "relationship": ["x_fundingSource"],
                "scheme": "ocid",
                "identifier": f"{fs_id}",
                "uri": f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{fs_id}"
            }]
        }

        json_notice_budget_release_fs = {
            "ocid": fs_id,
            "id": fs_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": ["planning"],
            "initiationType": "tender",
            "tender": {
                "id": "195cf37f-99cc-4729-8374-596f2fba1810",
                "status": "planning",
                "statusDetails": "empty"
            },
            "parties": [{
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
                "additionalIdentifiers": [{
                    "scheme": "MD-K",
                    "id": "additional identifier",
                    "legalName": "legalname",
                    "uri": "http://k.to"
                }],
                "contactPoint": {
                    "name": self.payer_contact_point_name,
                    "email": self.payer_contact_point_email,
                    "telephone": self.payer_contact_point_telephone,
                    "faxNumber": self.payer_contact_point_fax_number,
                    "url": self.payer_contact_point_url
                },
                "roles": ["payer"]
            }],
            "planning": {
                "budget": {
                    "id": self.tender_classification_id,
                    "description": "description",
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    },
                    "europeanUnionFunding": {
                        "projectIdentifier": "projectIdentifier",
                        "projectName": "Name of this project",
                        "uri": "http://uriuri.th"
                    },
                    "isEuropeanUnionFunded": True,
                    "verified": False,
                    "sourceEntity": {
                        "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                        "name": self.buyer_name
                    },
                    "project": "project",
                    "projectID": "projectID",
                    "uri": "http://uri.ur"
                },
                "rationale": "reason for the budget"
            },
            "relatedProcesses": [{
                "id": "412d5c20-b194-11eb-8505-35fcd4e9bc47",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": cp_id,
                "uri": f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{cp_id}"
            }]
        }

        json_notice_budget_compiled_release_ei = {
            "ocid": cp_id,
            "id": cp_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": ["compiled"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "2cc5a0b7-b1b7-4ed3-9210-1ca6d0af3261",
                "title": "Cardurilor de acces pentru Bibliotecii Municipale B.P. Hasdeu ",
                "status": "planning",
                "statusDetails": "empty",
                "items": [{
                    "id": self.tender_items_id,
                    "description": self.tender_items_description,
                    "classification": {
                        "id": self.tender_item_classification_id,
                        "description": "Lucrări de pregătire a şantierului",
                        "scheme": "CPV"
                    },
                    "quantity": self.tender_items_quantity,
                    "unit": {
                        "name": self.tender_items_unit_name,
                        "id": self.tender_items_unit_id
                    },
                    "deliveryAddress": {
                        "addressDetails": {
                            "country": {
                                "id": self.tender_items_delivery_details_country_id,
                                "description": self.tender_items_delivery_details_country_description,
                                "scheme": self.tender_items_delivery_details_country_scheme,
                                "uri": self.tender_items_delivery_details_country_uri
                            },
                            "region": {
                                "id": self.tender_items_delivery_details_region_id,
                                "description": self.tender_items_delivery_details_region_description,
                                "scheme": self.tender_items_delivery_details_region_scheme,
                                "uri": self.tender_items_delivery_details_region_uri
                            }
                        }
                    }

                }],
                "mainProcurementCategory": "works",
                "classification": {
                    "scheme": self.tender_classification_scheme,
                    "id": self.tender_classification_id,
                    "description": self.tender_classification_description
                }
            },
            "buyer": {
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name
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
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
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
                "roles": ["buyer"]
            }],
            "planning": {
                "budget": {
                    "id": self.tender_classification_id,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    }
                }
            },
            "relatedProcesses": [{
                "id": "412ee2c0-b194-11eb-8505-35fcd4e9bc47",
                "relationship": ["x_fundingSource"],
                "scheme": "ocid",
                "identifier": f"{fs_id}",
                "uri": f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{fs_id}"
            }]
        }

        json_notice_budget_compiled_release_fs = {
            "ocid": fs_id,
            "id": fs_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": ["planning"],
            "initiationType": "tender",
            "tender": {
                "id": "195cf37f-99cc-4729-8374-596f2fba1810",
                "status": "planning",
                "statusDetails": "empty"
            },
            "parties": [{
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
                "additionalIdentifiers": [{
                    "scheme": "MD-K",
                    "id": "additional identifier",
                    "legalName": "legalname",
                    "uri": "http://k.to"
                }],
                "contactPoint": {
                    "name": self.payer_contact_point_name,
                    "email": self.payer_contact_point_email,
                    "telephone": self.payer_contact_point_telephone,
                    "faxNumber": self.payer_contact_point_fax_number,
                    "url": self.payer_contact_point_url
                },
                "roles": ["payer"]
            }],
            "planning": {
                "budget": {
                    "id": self.tender_classification_id,
                    "description": "description",
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    },
                    "europeanUnionFunding": {
                        "projectIdentifier": "projectIdentifier",
                        "projectName": "Name of this project",
                        "uri": "http://uriuri.th"
                    },
                    "isEuropeanUnionFunded": True,
                    "verified": False,
                    "sourceEntity": {
                        "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                        "name": self.buyer_name
                    },
                    "project": "project",
                    "projectID": "projectID",
                    "uri": "http://uri.ur"
                },
                "rationale": "reason for the budget"
            },
            "relatedProcesses": [{
                "id": "412d5c20-b194-11eb-8505-35fcd4e9bc47",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": f"{cp_id}",
                "uri": f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{cp_id}"
            }]
        }

        session.execute(f"INSERT INTO orchestrator_context (cp_id,context) VALUES ("
                        f"'{cp_id}','{json.dumps(json_orchestrator_context)}');").one()
        session.execute(f"INSERT INTO budget_ei (cp_id,token_entity,created_date,json_data,owner) VALUES("
                        f"'{cp_id}',{ei_token},{period[2]},'{json.dumps(json_budget_ei)}','{owner}');").one()
        session.execute(
            f"INSERT INTO budget_fs (cp_id,token_entity,amount,amount_reserved,created_date,json_data,oc_id,owner) "
            f"VALUES ('{cp_id}',{fs_token},{self.amount},0,{period[2]},'{json.dumps(json_budget_fs)}',"
            f"'{fs_id}','{owner}');").one()
        session.execute(f"INSERT INTO notice_budget_release ("
                        f"cp_id,oc_id,release_id,json_data,release_date,stage) VALUES("
                        f"'{cp_id}','{cp_id}','{cp_id + str(period[2])}',"
                        f"'{json.dumps(json_notice_budget_release_ei)}',{period[2]},'EI');").one()
        session.execute(f"INSERT INTO notice_budget_compiled_release ("
                        f"cp_id,oc_id,amount,json_data,publish_date,release_date,"
                        f"release_id,stage) VALUES('{cp_id}','{cp_id}', 0.0, "
                        f"'{json.dumps(json_notice_budget_compiled_release_ei)}',"
                        f"{period[2]},{period[2]},'{cp_id + '-' + f'{period[2]}'}',"
                        f"'EI');").one()
        session.execute(
            f"INSERT INTO notice_budget_release (cp_id,oc_id,release_id,json_data,release_date,stage) "
            f"VALUES ('{cp_id}','{fs_id}','{fs_id + '-' + str(period[2])}',"
            f"'{json.dumps(json_notice_budget_release_fs)}',{period[2]},'FS');").one()
        session.execute(
            f"INSERT INTO notice_budget_compiled_release (cp_id,oc_id,amount,json_data,publish_date,release_date,"
            f"release_id,stage) VALUES ('{cp_id}','{fs_id}',{self.amount},"
            f"'{json.dumps(json_notice_budget_compiled_release_fs)}',{period[2]},{period[2]},"
            f"'{fs_id + '-' + str(period[2])}','FS');")
        session.execute(f"INSERT INTO notice_budget_offset (cp_id,release_date) "
                        f"VALUES ('{cp_id}',{period[2]});").one()
        return f"http://dev.public.eprocurement.systems/budgets/{cp_id}", fs_id, fs_token

    @allure.step('Insert FS: Own - obligatory, based on EI: without items - obligatory')
    def insert_fs_own_obligatory_ei_obligatory_without_items(self, cp_id, ei_token):
        auth_provider = PlainTextAuthProvider(username=self.cassandra_username, password=self.cassandra_password)
        cluster = Cluster([self.cassandra_cluster], auth_provider=auth_provider)
        session = cluster.connect('ocds')
        owner = "445f6851-c908-407d-9b45-14b92f3e964b"
        fs_id = prepared_fs_oc_id(cp_id)
        fs_token = uuid4()
        period = get_period()
        json_orchestrator_context = {
            "operationId": f"{uuid4()}",
            "requestId": f"{uuid4()}",
            "cpid": cp_id,
            "ocid": fs_id,
            "stage": "FS",
            "processType": "fs",
            "operationType": "createFS",
            "owner": owner,
            "country": self.country,
            "language": self.lang,
            "token": f"{fs_token}",
            "startDate": self.planning_budget_period_start_date,
            "timeStamp": period[2],
            "isAuction": False
        }

        json_budget_ei = {
            "ocid": cp_id,
            "tender": {
                "id": "2cc5a0b7-b1b7-4ed3-9210-1ca6d0af3261",
                "title": "Cardurilor de acces pentru Bibliotecii Municipale B.P. Hasdeu ",
                "status": "planning",
                "statusDetails": "empty",
                "classification": {
                    "id": self.tender_classification_id,
                    "scheme": self.tender_classification_scheme,
                    "description": self.tender_classification_description
                },
                "mainProcurementCategory": "works"
            },
            "planning": {
                "budget": {
                    "id": self.planning_budget_id,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    }
                }
            },
            "buyer": {
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name,
                "identifier": {
                    "id": self.buyer_identifier_id,
                    "scheme": self.buyer_identifier_scheme,
                    "legalName": self.buyer_identifier_legal_name
                },
                "address": {
                    "streetAddress": self.buyer_address_street_address,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.buyer_address_address_details_country_id,
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
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
                }
            }
        }

        json_budget_fs = {
            "ocid": fs_id,
            "tender": {
                "id": "195cf37f-99cc-4729-8374-596f2fba1810",
                "status": "active",
                "statusDetails": "empty"
            },
            "planning": {
                "budget": {
                    "id": None,
                    "description": None,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    },
                    "europeanUnionFunding": None,
                    "isEuropeanUnionFunded": False,
                    "verified": True,
                    "sourceEntity": {
                        "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                        "name": self.funder_name,
                    },
                    "verificationDetails": None,
                    "project": None,
                    "projectID": None,
                    "uri": None
                }
            },
            "funder": {
                "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                "name": self.funder_name,
                "identifier": {
                    "id": self.funder_identifier_id,
                    "scheme": self.funder_identifier_scheme,
                    "legalName": self.funder_identifier_legal_name
                },
                "address": {
                    "streetAddress": self.funder_address_street,
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
                "contactPoint": {
                    "name": self.funder_contact_point_name,
                    "email": self.funder_contact_point_email,
                    "telephone": self.funder_contact_point_telephone
                }
            },
            "payer": {
                "id": f"{self.payer_identifier_scheme}-{self.payer_identifier_id}",
                "name": self.payer_name,
                "identifier": {
                    "id": self.payer_identifier_id,
                    "scheme": self.payer_identifier_scheme,
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
                }
            }
        }

        json_notice_budget_release_ei = {
            "ocid": cp_id,
            "id": cp_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": ["compiled"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "2cc5a0b7-b1b7-4ed3-9210-1ca6d0af3261",
                "title": "Cardurilor de acces pentru Bibliotecii Municipale B.P. Hasdeu ",
                "description": "description of finansical sourse",
                "status": "planning",
                "statusDetails": "empty",
                "mainProcurementCategory": "works",
                "classification": {
                    "scheme": self.tender_classification_scheme,
                    "id": self.tender_classification_id,
                    "description": self.tender_classification_description
                }
            },
            "buyer": {
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name,
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
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
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
                "roles": ["buyer"]
            }],
            "planning": {
                "budget": {
                    "id": self.planning_budget_id,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    }
                },
                "rationale": self.planning_rationale
            },
            "relatedProcesses": [{
                "id": "412ee2c0-b194-11eb-8505-35fcd4e9bc47",
                "relationship": ["x_fundingSource"],
                "scheme": "ocid",
                "identifier": f"{fs_id}",
                "uri": f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{fs_id}"
            }]
        }

        json_notice_budget_release_fs = {
            "ocid": fs_id,
            "id": fs_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": ["planning"],
            "initiationType": "tender",
            "tender": {
                "id": "195cf37f-99cc-4729-8374-596f2fba1810",
                "status": "active",
                "statusDetails": "empty"
            },
            "parties": [{
                "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                "name": self.funder_name,
                "identifier": {
                    "scheme": self.funder_identifier_scheme,
                    "id": self.funder_identifier_id,
                    "legalName": self.funder_identifier_legal_name
                },
                "address": {
                    "streetAddress": self.funder_address_street,
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
                "contactPoint": {
                    "name": self.funder_contact_point_name,
                    "email": self.funder_contact_point_email,
                    "telephone": self.funder_contact_point_telephone
                },
                "roles": ["funder"]
            },
                {
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
                }],
            "planning": {
                "budget": {
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    },
                    "isEuropeanUnionFunded": False,
                    "verified": True,
                    "sourceEntity": {
                        "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                        "name": self.funder_name
                    }
                }
            },
            "relatedProcesses": [{
                "id": "412d5c20-b194-11eb-8505-35fcd4e9bc47",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": cp_id,
                "uri": f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{cp_id}"
            }]
        }

        json_notice_budget_compiled_release_ei = {
            "ocid": cp_id,
            "id": cp_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": ["compiled"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "2cc5a0b7-b1b7-4ed3-9210-1ca6d0af3261",
                "title": "Cardurilor de acces pentru Bibliotecii Municipale B.P. Hasdeu ",
                "status": "planning",
                "statusDetails": "empty",
                "mainProcurementCategory": "works",
                "classification": {
                    "scheme": self.tender_classification_scheme,
                    "id": self.tender_classification_id,
                    "description": self.tender_classification_description
                }
            },
            "buyer": {
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name
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
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
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
                "roles": ["buyer"]
            }],
            "planning": {
                "budget": {
                    "id": self.tender_classification_id,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    }
                }
            },
            "relatedProcesses": [{
                "id": "412ee2c0-b194-11eb-8505-35fcd4e9bc47",
                "relationship": ["x_fundingSource"],
                "scheme": "ocid",
                "identifier": f"{fs_id}",
                "uri": f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{fs_id}"
            }]
        }

        json_notice_budget_compiled_release_fs = {
            "ocid": fs_id,
            "id": fs_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": ["planning"],
            "initiationType": "tender",
            "tender": {
                "id": "195cf37f-99cc-4729-8374-596f2fba1810",
                "status": "active",
                "statusDetails": "empty"
            },
            "parties": [{
                "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                "name": self.funder_name,
                "identifier": {
                    "scheme": self.funder_identifier_scheme,
                    "id": self.funder_identifier_id,
                    "legalName": self.funder_identifier_legal_name
                },
                "address": {
                    "streetAddress": self.funder_address_street,
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
                "contactPoint": {
                    "name": self.funder_contact_point_name,
                    "email": self.funder_contact_point_email,
                    "telephone": self.funder_contact_point_telephone
                },
                "roles": ["funder"]
            },
                {
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
                }
            ],
            "planning": {
                "budget": {
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    },
                    "isEuropeanUnionFunded": False,
                    "verified": True,
                    "sourceEntity": {
                        "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                        "name": self.funder_name
                    }
                }
            },
            "relatedProcesses": [{
                "id": "412d5c20-b194-11eb-8505-35fcd4e9bc47",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": f"{cp_id}",
                "uri": f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{cp_id}"
            }]
        }

        session.execute(f"INSERT INTO orchestrator_context (cp_id,context) VALUES ("
                        f"'{cp_id}','{json.dumps(json_orchestrator_context)}');").one()
        session.execute(f"INSERT INTO budget_ei (cp_id,token_entity,created_date,json_data,owner) VALUES("
                        f"'{cp_id}',{ei_token},{period[2]},'{json.dumps(json_budget_ei)}','{owner}');").one()
        session.execute(
            f"INSERT INTO budget_fs (cp_id,token_entity,amount,amount_reserved,created_date,json_data,oc_id,owner) "
            f"VALUES ('{cp_id}',{fs_token},{self.amount},0,{period[2]},'{json.dumps(json_budget_fs)}',"
            f"'{fs_id}','{owner}');").one()
        session.execute(f"INSERT INTO notice_budget_release ("
                        f"cp_id,oc_id,release_id,json_data,release_date,stage) VALUES("
                        f"'{cp_id}','{cp_id}','{cp_id + str(period[2])}',"
                        f"'{json.dumps(json_notice_budget_release_ei)}',{period[2]},'EI');").one()
        session.execute(f"INSERT INTO notice_budget_compiled_release ("
                        f"cp_id,oc_id,amount,json_data,publish_date,release_date,"
                        f"release_id,stage) VALUES('{cp_id}','{cp_id}', 0.0, "
                        f"'{json.dumps(json_notice_budget_compiled_release_ei)}',"
                        f"{period[2]},{period[2]},'{cp_id + '-' + f'{period[2]}'}',"
                        f"'EI');").one()
        session.execute(
            f"INSERT INTO notice_budget_release (cp_id,oc_id,release_id,json_data,release_date,stage) "
            f"VALUES ('{cp_id}','{fs_id}','{fs_id + '-' + str(period[2])}',"
            f"'{json.dumps(json_notice_budget_release_fs)}',{period[2]},'FS');").one()
        session.execute(
            f"INSERT INTO notice_budget_compiled_release (cp_id,oc_id,amount,json_data,publish_date,release_date,"
            f"release_id,stage) VALUES ('{cp_id}','{fs_id}',{self.amount},"
            f"'{json.dumps(json_notice_budget_compiled_release_fs)}',{period[2]},{period[2]},"
            f"'{fs_id + '-' + str(period[2])}','FS');")
        session.execute(f"INSERT INTO notice_budget_offset (cp_id,release_date) "
                        f"VALUES ('{cp_id}',{period[2]});").one()
        return f"http://dev.public.eprocurement.systems/budgets/{cp_id}", fs_id, fs_token

    @allure.step('Insert FS: Own - full, based on EI: without items - obligatory')
    def insert_fs_own_full_ei_obligatory_without_items(self, cp_id, ei_token):
        auth_provider = PlainTextAuthProvider(username=self.cassandra_username, password=self.cassandra_password)
        cluster = Cluster([self.cassandra_cluster], auth_provider=auth_provider)
        session = cluster.connect('ocds')
        owner = "445f6851-c908-407d-9b45-14b92f3e964b"
        fs_id = prepared_fs_oc_id(cp_id)
        fs_token = uuid4()
        period = get_period()
        json_orchestrator_context = {
            "operationId": f"{uuid4()}",
            "requestId": f"{uuid4()}",
            "cpid": cp_id,
            "ocid": fs_id,
            "stage": "FS",
            "processType": "fs",
            "operationType": "createFS",
            "owner": owner,
            "country": self.country,
            "language": self.lang,
            "token": f"{fs_token}",
            "startDate": self.planning_budget_period_start_date,
            "timeStamp": period[2],
            "isAuction": False
        }

        json_budget_ei = {
            "ocid": cp_id,
            "tender": {
                "id": "2cc5a0b7-b1b7-4ed3-9210-1ca6d0af3261",
                "title": self.tender_title,
                "status": "planning",
                "statusDetails": "empty",
                "classification": {
                    "id": self.tender_classification_id,
                    "scheme": self.tender_classification_scheme,
                    "description": self.tender_classification_description
                },
                "mainProcurementCategory": "works",
            },
            "planning": {
                "budget": {
                    "id": self.planning_budget_id,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    }
                }
            },
            "buyer": {
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name,
                "identifier": {
                    "id": self.buyer_identifier_id,
                    "scheme": self.buyer_identifier_scheme,
                    "legalName": self.buyer_identifier_legal_name
                },
                "address": {
                    "streetAddress": self.buyer_address_street_address,
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": self.buyer_address_address_details_country_id,
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
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
                }
            }
        }

        json_budget_fs = {
            "ocid": fs_id,
            "tender": {
                "id": "195cf37f-99cc-4729-8374-596f2fba1810",
                "status": "active",
                "statusDetails": "empty"
            },
            "planning": {
                "budget": {
                    "id": self.planning_budget_id,
                    "description": "description",
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    },
                    "europeanUnionFunding": {
                        "projectName": "Name of this project",
                        "projectIdentifier": "projectIdentifier",
                        "uri": "http://uriuri.th"
                    },
                    "isEuropeanUnionFunded": True,
                    "verified": True,
                    "sourceEntity": {
                        "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                        "name": self.funder_name,
                    },
                    "verificationDetails": None,
                    "project": "project",
                    "projectID": "projectID",
                    "uri": "http://uri.ur"
                },
                "rationale": self.planning_rationale
            },
            "funder": {
                "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                "name": self.funder_name,
                "identifier": {
                    "id": self.funder_identifier_id,
                    "scheme": self.funder_identifier_scheme,
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
                        "id": "additional identifier",
                        "scheme": "scheme",
                        "legalName": "legal name",
                        "uri": "http://addtIdent.com"
                    }],
                "contactPoint": {
                    "name": self.funder_contact_point_name,
                    "email": self.funder_contact_point_email,
                    "telephone": self.funder_contact_point_telephone,
                    "faxNumber": self.funder_contact_point_fax,
                    "url": self.funder_contact_point_url
                }
            },
            "payer": {
                "id": f"{self.payer_identifier_scheme}-{self.payer_identifier_id}",
                "name": self.payer_name,
                "identifier": {
                    "id": self.payer_identifier_id,
                    "scheme": self.payer_identifier_scheme,
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
                        "id": "additional identifier",
                        "scheme": "MD-K",
                        "legalName": "legalname",
                        "uri": "http://k.to"
                    }],
                "contactPoint": {
                    "name": self.payer_contact_point_name,
                    "email": self.payer_contact_point_email,
                    "telephone": self.payer_contact_point_telephone,
                    "faxNumber": self.payer_contact_point_fax_number,
                    "url": self.payer_contact_point_url,
                }
            }
        }

        json_notice_budget_release_ei = {
            "ocid": cp_id,
            "id": cp_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": [
                "compiled"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "2cc5a0b7-b1b7-4ed3-9210-1ca6d0af3261",
                "title": self.tender_title,
                "status": "planning",
                "statusDetails": "empty",
                "mainProcurementCategory": "works",
                "classification": {
                    "scheme": self.tender_classification_scheme,
                    "id": self.tender_classification_id,
                    "description": self.tender_classification_description
                }
            },
            "buyer": {
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name,
            },
            "parties": [
                {
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
                                "description": "MOLDOVA",
                                "uri": "http://reference.iatistandard.org"
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
                }],
            "planning": {
                "budget": {
                    "id": self.planning_budget_id,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    }
                }
            },
            "relatedProcesses": [
                {
                    "id": "412ee2c0-b194-11eb-8505-35fcd4e9bc47",
                    "relationship": [
                        "x_fundingSource"],
                    "scheme": "ocid",
                    "identifier": f"{fs_id}",
                    "uri": f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{fs_id}"
                }]
        }

        json_notice_budget_release_fs = {
            "ocid": fs_id,
            "id": fs_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": [
                "planning"],
            "initiationType": "tender",
            "tender": {
                "id": "195cf37f-99cc-4729-8374-596f2fba1810",
                "status": "active",
                "statusDetails": "empty"
            },
            "parties": [
                {
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
                    "additionalIdentifiers": [
                        {
                            "scheme": "scheme",
                            "id": "additional identifier",
                            "legalName": "legal name",
                            "uri": "http://addtIdent.com"
                        }],
                    "contactPoint": {
                        "name": self.funder_contact_point_name,
                        "email": self.funder_contact_point_email,
                        "telephone": self.funder_contact_point_telephone,
                        "faxNumber": self.funder_contact_point_fax,
                        "url": self.funder_contact_point_url,
                    },
                    "roles": [
                        "funder"]
                },
                {
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
                            "scheme": "MD-K",
                            "id": "additional identifier",
                            "legalName": "legalname",
                            "uri": "http://k.to"
                        }],
                    "contactPoint": {
                        "name": self.payer_contact_point_name,
                        "email": self.payer_contact_point_email,
                        "telephone": self.payer_contact_point_telephone,
                        "faxNumber": self.payer_contact_point_fax_number,
                        "url": self.payer_contact_point_url
                    },
                    "roles": [
                        "payer"]
                }],
            "planning": {
                "budget": {
                    "id": self.planning_budget_id,
                    "description": "description",
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    },
                    "europeanUnionFunding": {
                        "projectIdentifier": "projectIdentifier",
                        "projectName": "Name of this project",
                        "uri": "http://uriuri.th"
                    },
                    "isEuropeanUnionFunded": True,
                    "verified": True,
                    "sourceEntity": {
                        "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                        "name": self.funder_name
                    },
                    "project": "project",
                    "projectID": "projectID",
                    "uri": "http://uri.ur"
                },
                "rationale": "reason for the budget"
            },
            "relatedProcesses": [
                {
                    "id": "412d5c20-b194-11eb-8505-35fcd4e9bc47",
                    "relationship": [
                        "parent"],
                    "scheme": "ocid",
                    "identifier": cp_id,
                    "uri": f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{cp_id}"
                }]
        }

        json_notice_budget_compiled_release_ei = {
            "ocid": cp_id,
            "id": cp_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": [
                "compiled"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "2cc5a0b7-b1b7-4ed3-9210-1ca6d0af3261",
                "title": self.tender_title,
                "status": "planning",
                "statusDetails": "empty",
                "mainProcurementCategory": "works",
                "classification": {
                    "scheme": self.tender_classification_scheme,
                    "id": self.tender_classification_id,
                    "description": self.tender_classification_description
                }
            },
            "buyer": {
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name
            },
            "parties": [
                {
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
                                "description": "MOLDOVA",
                                "uri": "http://reference.iatistandard.org"
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
                }],
            "planning": {
                "budget": {
                    "id": self.tender_classification_id,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    }
                }
            },
            "relatedProcesses": [
                {
                    "id": "412ee2c0-b194-11eb-8505-35fcd4e9bc47",
                    "relationship": [
                        "x_fundingSource"],
                    "scheme": "ocid",
                    "identifier": f"{fs_id}",
                    "uri": f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{fs_id}"
                }]
        }

        json_notice_budget_compiled_release_fs = {
            "ocid": fs_id,
            "id": fs_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": [
                "planning"],
            "initiationType": "tender",
            "tender": {
                "id": "195cf37f-99cc-4729-8374-596f2fba1810",
                "status": "active",
                "statusDetails": "empty"
            },
            "parties": [
                {
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
                            "scheme": "scheme",
                            "id": "additional identifier",
                            "legalName": "legal name",
                            "uri": "http://addtIdent.com"
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
                },
                {
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
                            "scheme": "MD-K",
                            "id": "additional identifier",
                            "legalName": "legalname",
                            "uri": "http://k.to"
                        }],
                    "contactPoint": {
                        "name": self.payer_contact_point_name,
                        "email": self.payer_contact_point_email,
                        "telephone": self.payer_contact_point_telephone,
                        "faxNumber": self.payer_contact_point_fax_number,
                        "url": self.payer_contact_point_url,
                    },
                    "roles": [
                        "payer"]
                }
            ],
            "planning": {
                "budget": {
                    "id": self.tender_classification_id,
                    "description": "description",
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    },
                    "europeanUnionFunding": {
                        "projectIdentifier": "projectIdentifier",
                        "projectName": "Name of this project",
                        "uri": "http://uriuri.th"
                    },
                    "isEuropeanUnionFunded": True,
                    "verified": True,
                    "sourceEntity": {
                        "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                        "name": self.funder_name
                    },
                    "project": "project",
                    "projectID": "projectID",
                    "uri": "http://uri.ur"
                },
                "rationale": "reason for the budget"
            },
            "relatedProcesses": [
                {
                    "id": "412d5c20-b194-11eb-8505-35fcd4e9bc47",
                    "relationship": [
                        "parent"],
                    "scheme": "ocid",
                    "identifier": f"{cp_id}",
                    "uri": f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{cp_id}"
                }]
        }

        session.execute(f"INSERT INTO orchestrator_context (cp_id,context) VALUES ("
                        f"'{cp_id}','{json.dumps(json_orchestrator_context)}');").one()
        session.execute(f"INSERT INTO budget_ei (cp_id,token_entity,created_date,json_data,owner) VALUES("
                        f"'{cp_id}',{ei_token},{period[2]},'{json.dumps(json_budget_ei)}','{owner}');").one()
        session.execute(

            f"INSERT INTO budget_fs (cp_id,token_entity,amount,amount_reserved,created_date,json_data,oc_id,owner) "
            f"VALUES ('{cp_id}',{fs_token},{self.amount},0,{period[2]},'{json.dumps(json_budget_fs)}',"
            f"'{fs_id}','{owner}');").one()

        session.execute(f"INSERT INTO notice_budget_release ("
                        f"cp_id,oc_id,release_id,json_data,release_date,stage) VALUES("
                        f"'{cp_id}','{cp_id}','{cp_id + str(period[2])}',"
                        f"'{json.dumps(json_notice_budget_release_ei)}',{period[2]},'EI');").one()
        session.execute(f"INSERT INTO notice_budget_compiled_release ("
                        f"cp_id,oc_id,amount,json_data,publish_date,release_date,"
                        f"release_id,stage) VALUES('{cp_id}','{cp_id}', 0.0, "
                        f"'{json.dumps(json_notice_budget_compiled_release_ei)}',"
                        f"{period[2]},{period[2]},'{cp_id + '-' + f'{period[2]}'}',"
                        f"'EI');").one()
        session.execute(
            f"INSERT INTO notice_budget_release (cp_id,oc_id,release_id,json_data,release_date,stage) "
            f"VALUES ('{cp_id}','{fs_id}','{fs_id + '-' + str(period[2])}',"
            f"'{json.dumps(json_notice_budget_release_fs)}',{period[2]},'FS');").one()
        session.execute(
            f"INSERT INTO notice_budget_compiled_release (cp_id,oc_id,amount,json_data,publish_date,release_date,"
            f"release_id,stage) VALUES ('{cp_id}','{fs_id}',{self.amount},"
            f"'{json.dumps(json_notice_budget_compiled_release_fs)}',{period[2]},{period[2]},"
            f"'{fs_id + '-' + str(period[2])}','FS');")
        session.execute(f"INSERT INTO notice_budget_offset (cp_id,release_date) "
                        f"VALUES ('{cp_id}',{period[2]});").one()
        return f"http://dev.public.eprocurement.systems/budgets/{cp_id}", fs_id, fs_token

    @allure.step('Insert FS: Own - obligatory, based on EI: with items - full')
    def insert_fs_own_obligatory_ei_full_with_items(self, cp_id, ei_token):
        auth_provider = PlainTextAuthProvider(username=self.cassandra_username, password=self.cassandra_password)
        cluster = Cluster([self.cassandra_cluster], auth_provider=auth_provider)
        session = cluster.connect('ocds')
        owner = "445f6851-c908-407d-9b45-14b92f3e964b"
        fs_id = prepared_fs_oc_id(cp_id)
        fs_token = uuid4()
        period = get_period()
        json_orchestrator_context = {
            "operationId": f"{uuid4()}",
            "requestId": f"{uuid4()}",
            "cpid": cp_id,
            "ocid": fs_id,
            "stage": "FS",
            "processType": "fs",
            "operationType": "createFS",
            "owner": owner,
            "country": self.country,
            "language": self.lang,
            "token": f"{fs_token}",
            "startDate": self.planning_budget_period_start_date,
            "timeStamp": period[2],
            "isAuction": False
        }

        json_budget_ei = {
            "ocid": cp_id,
            "tender": {
                "id": "2cc5a0b7-b1b7-4ed3-9210-1ca6d0af3261",
                "title": self.tender_title,
                "description": self.tender_description,
                "status": "planning",
                "statusDetails": "empty",
                "classification": {
                    "id": self.tender_classification_id,
                    "scheme": self.tender_classification_scheme,
                    "description": self.tender_classification_description
                },
                "mainProcurementCategory": "works",
                "items": [
                    {
                        "id": self.tender_items_id,
                        "description": self.tender_items_description,
                        "classification": {
                            "id": self.tender_item_classification_id,
                            "description": "Lucrări de pregătire a şantierului",
                            "scheme": "CPV"
                        },
                        "additionalClassifications": [
                            {
                                "id": "AA12-4",
                                "description": "Oţel carbon",
                                "scheme": "CPVS"
                            }],
                        "deliveryAddress": {
                            "streetAddress": "street",
                            "postalCode": "postal",
                            "addressDetails": {
                                "country": {
                                    "id": self.tender_items_delivery_details_country_id,
                                    "description": self.tender_items_delivery_details_country_description,
                                    "scheme": self.tender_items_delivery_details_country_scheme,
                                    "uri": self.tender_items_delivery_details_country_uri
                                },
                                "region": {
                                    "id": self.tender_items_delivery_details_region_id,
                                    "description": self.tender_items_delivery_details_region_description,
                                    "scheme": self.tender_items_delivery_details_region_scheme,
                                    "uri": self.tender_items_delivery_details_region_uri
                                },
                                "locality": {
                                    "id": self.tender_items_delivery_details_locality_id,
                                    "description": self.tender_items_delivery_details_locality_description,
                                    "scheme": self.tender_items_delivery_details_locality_scheme,
                                    "uri": self.tender_items_delivery_details_locality_uri
                                }
                            }
                        },
                        "quantity": self.tender_items_quantity,
                        "unit": {
                            "name": self.tender_items_unit_name,
                            "id": self.tender_items_unit_id
                        }
                    }],
            },
            "planning": {
                "budget": {
                    "id": self.planning_budget_id,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    }
                },
                "rationale": self.planning_rationale
            },
            "buyer": {
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name,
                "identifier": {
                    "id": self.buyer_identifier_id,
                    "scheme": self.buyer_identifier_scheme,
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
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
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
                    "telephone": self.buyer_contact_point_telephone,
                    "faxNumber": self.buyer_contact_point_fax_number,
                    "url": self.buyer_contact_point_url
                },
                "additionalIdentifiers": [
                    {
                        "id": "string",
                        "scheme": "MD-IDNO",
                        "legalName": "380935103469",
                        "uri": "http://petrusenko.com/svetlana"
                    }],
                "details": {
                    "typeOfBuyer": "NATIONAL_AGENCY",
                    "mainGeneralActivity": "HEALTH",
                    "mainSectoralActivity": "WATER"
                }
            }
        }

        json_budget_fs = {
            "ocid": fs_id,
            "tender": {
                "id": "195cf37f-99cc-4729-8374-596f2fba1810",
                "status": "active",
                "statusDetails": "empty"
            },
            "planning": {
                "budget": {
                    "id": None,
                    "description": None,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    },
                    "europeanUnionFunding": None,
                    "isEuropeanUnionFunded": False,
                    "verified": True,
                    "sourceEntity": {
                        "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                        "name": self.funder_name,
                    },
                    "verificationDetails": None,
                    "project": None,
                    "projectID": None,
                    "uri": None
                }
            },
            "funder": {
                "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                "name": self.funder_name,
                "identifier": {
                    "id": self.funder_identifier_id,
                    "scheme": self.funder_identifier_scheme,
                    "legalName": self.funder_identifier_legal_name
                },
                "address": {
                    "streetAddress": self.funder_address_street,
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
                "contactPoint": {
                    "name": self.funder_contact_point_name,
                    "email": self.funder_contact_point_email,
                    "telephone": self.funder_contact_point_telephone
                }
            },
            "payer": {
                "id": f"{self.payer_identifier_scheme}-{self.payer_identifier_id}",
                "name": self.payer_name,
                "identifier": {
                    "id": self.payer_identifier_id,
                    "scheme": self.payer_identifier_scheme,
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
                }
            }
        }

        json_notice_budget_release_ei = {
            "ocid": cp_id,
            "id": cp_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": [
                "compiled"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "2cc5a0b7-b1b7-4ed3-9210-1ca6d0af3261",
                "title": self.tender_title,
                "description": self.tender_description,
                "status": "planning",
                "statusDetails": "empty",
                "items": [
                    {
                        "id": "56db9b8d-0306-41d4-8fb1-a525b42720a6",
                        "description": self.tender_items_description,
                        "classification": {
                            "scheme": "CPV",
                            "id": self.tender_item_classification_id,
                            "description": "Servicii de reparare şi de întreţinere a vehiculelor şi a "
                                           "echipamentelor aferente şi servicii conexe"
                        },
                        "additionalClassifications": [
                            {
                                "scheme": "CPVS",
                                "id": "AA12-4",
                                "description": "Oţel carbon"
                            }],
                        "quantity": 1.000,
                        "unit": {
                            "name": "Parsec",
                            "id": "10"
                        },
                        "deliveryAddress": {
                            "streetAddress": "street",
                            "postalCode": "postal",
                            "addressDetails": {
                                "country": {
                                    "id": self.tender_items_delivery_details_country_id,
                                    "description": self.tender_items_delivery_details_country_description,
                                    "scheme": self.tender_items_delivery_details_country_scheme,
                                    "uri": self.tender_items_delivery_details_country_uri
                                },
                                "region": {
                                    "id": self.tender_items_delivery_details_region_id,
                                    "description": self.tender_items_delivery_details_region_description,
                                    "scheme": self.tender_items_delivery_details_region_scheme,
                                    "uri": self.tender_items_delivery_details_region_uri
                                },
                                "locality": {
                                    "scheme": self.tender_items_delivery_details_locality_scheme,
                                    "id": self.tender_items_delivery_details_locality_id,
                                    "description": self.tender_items_delivery_details_locality_description
                                }
                            }
                        }
                    }],
                "mainProcurementCategory": "works",
                "classification": {
                    "scheme": self.tender_classification_scheme,
                    "id": self.tender_classification_id,
                    "description": self.tender_classification_description
                }
            },
            "buyer": {
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name,
            },
            "parties": [
                {
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
                                "description": "MOLDOVA",
                                "uri": "http://reference.iatistandard.org"
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
                            "scheme": "MD-IDNO",
                            "id": "string",
                            "legalName": "380935103469",
                            "uri": "http://petrusenko.com/svetlana"
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
                }],
            "planning": {
                "budget": {
                    "id": self.planning_budget_id,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    }
                },
                "rationale": self.planning_rationale
            },
            "relatedProcesses": [
                {
                    "id": "412ee2c0-b194-11eb-8505-35fcd4e9bc47",
                    "relationship": [
                        "x_fundingSource"],
                    "scheme": "ocid",
                    "identifier": f"{fs_id}",
                    "uri": f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{fs_id}"
                }]
        }

        json_notice_budget_release_fs = {
            "ocid": fs_id,
            "id": fs_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": ["planning"],
            "initiationType": "tender",
            "tender": {
                "id": "195cf37f-99cc-4729-8374-596f2fba1810",
                "status": "active",
                "statusDetails": "empty"
            },
            "parties": [{
                "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                "name": self.funder_name,
                "identifier": {
                    "scheme": self.funder_identifier_scheme,
                    "id": self.funder_identifier_id,
                    "legalName": self.funder_identifier_legal_name

                },
                "address": {
                    "streetAddress": self.funder_address_street,
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
                "contactPoint": {
                    "name": self.funder_contact_point_name,
                    "email": self.funder_contact_point_email,
                    "telephone": self.funder_contact_point_telephone
                },
                "roles": ["funder"]
            },
                {
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
                }],
            "planning": {
                "budget": {
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    },
                    "isEuropeanUnionFunded": False,
                    "verified": True,
                    "sourceEntity": {
                        "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                        "name": self.funder_name
                    }
                }
            },
            "relatedProcesses": [{
                "id": "412d5c20-b194-11eb-8505-35fcd4e9bc47",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": cp_id,
                "uri": f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{cp_id}"
            }]
        }

        json_notice_budget_compiled_release_ei = {
            "ocid": cp_id,
            "id": cp_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": [
                "compiled"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "2cc5a0b7-b1b7-4ed3-9210-1ca6d0af3261",
                "title": self.tender_title,
                "description": self.tender_description,
                "status": "planning",
                "statusDetails": "empty",
                "items": [
                    {
                        "id": "56db9b8d-0306-41d4-8fb1-a525b42720a6",
                        "description": self.tender_items_description,
                        "classification": {
                            "scheme": "CPV",
                            "id": self.tender_item_classification_id,
                            "description": "Servicii de reparare şi de întreţinere a vehiculelor şi a "
                                           "echipamentelor aferente şi servicii conexe"
                        },
                        "additionalClassifications": [
                            {
                                "scheme": "CPVS",
                                "id": "AA12-4",
                                "description": "Oţel carbon"
                            }],
                        "quantity": 1.000,
                        "unit": {
                            "name": "Parsec",
                            "id": "10"
                        },
                        "deliveryAddress": {
                            "streetAddress": "street",
                            "postalCode": "postal",
                            "addressDetails": {
                                "country": {
                                    "id": self.tender_items_delivery_details_country_id,
                                    "description": self.tender_items_delivery_details_country_description,
                                    "scheme": self.tender_items_delivery_details_country_scheme,
                                    "uri": self.tender_items_delivery_details_country_uri
                                },
                                "region": {
                                    "id": self.tender_items_delivery_details_region_id,
                                    "description": self.tender_items_delivery_details_region_description,
                                    "scheme": self.tender_items_delivery_details_region_scheme,
                                    "uri": self.tender_items_delivery_details_region_uri
                                },
                                "locality": {
                                    "scheme": self.tender_items_delivery_details_locality_scheme,
                                    "id": self.tender_items_delivery_details_locality_id,
                                    "description": self.tender_items_delivery_details_locality_description
                                }
                            }
                        }
                    }],
                "mainProcurementCategory": "works",
                "classification": {
                    "scheme": self.tender_classification_scheme,
                    "id": self.tender_classification_id,
                    "description": self.tender_classification_description
                }
            },
            "buyer": {
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name
            },
            "parties": [
                {
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
                                "description": "MOLDOVA",
                                "uri": "http://reference.iatistandard.org"
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
                            "scheme": "MD-IDNO",
                            "id": "string",
                            "legalName": "380935103469",
                            "uri": "http://petrusenko.com/svetlana"
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
                }],
            "planning": {
                "budget": {
                    "id": self.tender_classification_id,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    }
                },
                "rationale": self.planning_rationale
            },
            "relatedProcesses": [
                {
                    "id": "412ee2c0-b194-11eb-8505-35fcd4e9bc47",
                    "relationship": [
                        "x_fundingSource"],
                    "scheme": "ocid",
                    "identifier": f"{fs_id}",
                    "uri": f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{fs_id}"
                }]
        }

        json_notice_budget_compiled_release_fs = {
            "ocid": fs_id,
            "id": fs_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": ["planning"],
            "initiationType": "tender",
            "tender": {
                "id": "195cf37f-99cc-4729-8374-596f2fba1810",
                "status": "active",
                "statusDetails": "empty"
            },
            "parties": [{
                "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                "name": self.funder_name,
                "identifier": {
                    "scheme": self.funder_identifier_scheme,
                    "id": self.funder_identifier_id,
                    "legalName": self.funder_identifier_legal_name
                },
                "address": {
                    "streetAddress": self.funder_address_street,
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
                "contactPoint": {
                    "name": self.funder_contact_point_name,
                    "email": self.funder_contact_point_email,
                    "telephone": self.funder_contact_point_telephone
                },
                "roles": ["funder"]
            },
                {
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
                }
            ],
            "planning": {
                "budget": {
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    },
                    "isEuropeanUnionFunded": False,
                    "verified": True,
                    "sourceEntity": {
                        "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                        "name": self.funder_name
                    }
                }
            },
            "relatedProcesses": [{
                "id": "412d5c20-b194-11eb-8505-35fcd4e9bc47",
                "relationship": ["parent"],
                "scheme": "ocid",
                "identifier": f"{cp_id}",
                "uri": f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{cp_id}"
            }]
        }

        session.execute(f"INSERT INTO orchestrator_context (cp_id,context) VALUES ("
                        f"'{cp_id}','{json.dumps(json_orchestrator_context)}');").one()
        session.execute(f"INSERT INTO budget_ei (cp_id,token_entity,created_date,json_data,owner) VALUES("
                        f"'{cp_id}',{ei_token},{period[2]},'{json.dumps(json_budget_ei)}','{owner}');").one()
        session.execute(
            f"INSERT INTO budget_fs (cp_id,token_entity,amount,amount_reserved,created_date,json_data,oc_id,owner) "
            f"VALUES ('{cp_id}',{fs_token},{self.amount},0,{period[2]},'{json.dumps(json_budget_fs)}',"
            f"'{fs_id}','{owner}');").one()
        session.execute(f"INSERT INTO notice_budget_release ("
                        f"cp_id,oc_id,release_id,json_data,release_date,stage) VALUES("
                        f"'{cp_id}','{cp_id}','{cp_id + str(period[2])}',"
                        f"'{json.dumps(json_notice_budget_release_ei)}',{period[2]},'EI');").one()
        session.execute(f"INSERT INTO notice_budget_compiled_release ("
                        f"cp_id,oc_id,amount,json_data,publish_date,release_date,"
                        f"release_id,stage) VALUES('{cp_id}','{cp_id}', 0.0, "
                        f"'{json.dumps(json_notice_budget_compiled_release_ei)}',"
                        f"{period[2]},{period[2]},'{cp_id + '-' + f'{period[2]}'}',"
                        f"'EI');").one()
        session.execute(
            f"INSERT INTO notice_budget_release (cp_id,oc_id,release_id,json_data,release_date,stage) "
            f"VALUES ('{cp_id}','{fs_id}','{fs_id + '-' + str(period[2])}',"
            f"'{json.dumps(json_notice_budget_release_fs)}',{period[2]},'FS');").one()
        session.execute(
            f"INSERT INTO notice_budget_compiled_release (cp_id,oc_id,amount,json_data,publish_date,release_date,"
            f"release_id,stage) VALUES ('{cp_id}','{fs_id}',{self.amount},"
            f"'{json.dumps(json_notice_budget_compiled_release_fs)}',{period[2]},{period[2]},"
            f"'{fs_id + '-' + str(period[2])}','FS');")
        session.execute(f"INSERT INTO notice_budget_offset (cp_id,release_date) "
                        f"VALUES ('{cp_id}',{period[2]});").one()
        return f"http://dev.public.eprocurement.systems/budgets/{cp_id}", fs_id, fs_token

    @allure.step('Insert FS: Own - full, based on EI: with items - full')
    def insert_fs_own_full_ei_full_with_items(self, cp_id, ei_token):
        auth_provider = PlainTextAuthProvider(username=self.cassandra_username, password=self.cassandra_password)
        cluster = Cluster([self.cassandra_cluster], auth_provider=auth_provider)
        session = cluster.connect('ocds')
        owner = "445f6851-c908-407d-9b45-14b92f3e964b"
        fs_id = prepared_fs_oc_id(cp_id)
        fs_token = uuid4()
        period = get_period()
        json_orchestrator_context = {
            "operationId": f"{uuid4()}",
            "requestId": f"{uuid4()}",
            "cpid": cp_id,
            "ocid": fs_id,
            "stage": "FS",
            "processType": "fs",
            "operationType": "createFS",
            "owner": owner,
            "country": self.country,
            "language": self.lang,
            "token": f"{fs_token}",
            "startDate": self.planning_budget_period_start_date,
            "timeStamp": period[2],
            "isAuction": False
        }

        json_budget_ei = {
            "ocid": cp_id,
            "tender": {
                "id": "2cc5a0b7-b1b7-4ed3-9210-1ca6d0af3261",
                "title": self.tender_title,
                "description": self.tender_description,
                "status": "planning",
                "statusDetails": "empty",
                "classification": {
                    "id": self.tender_classification_id,
                    "scheme": self.tender_classification_scheme,
                    "description": self.tender_classification_description
                },
                "mainProcurementCategory": "works",
                "items": [
                    {
                        "id": "56db9b8d-0306-41d4-8fb1-a525b42720a6",
                        "description": self.tender_items_description,
                        "classification": {
                            "scheme": "CPV",
                            "id": self.tender_item_classification_id,
                            "description": "Servicii de reparare şi de întreţinere a vehiculelor şi a echipamentelor "
                                           "aferente şi servicii conexe"
                        },
                        "additionalClassifications": [
                            {
                                "scheme": "CPVS",
                                "id": "AA12-4",
                                "description": "Oţel carbon"
                            }],
                        "deliveryAddress": {
                            "streetAddress": "street",
                            "postalCode": "postal",
                            "addressDetails": {
                                "country": {
                                    "id": self.tender_items_delivery_details_country_id,
                                    "description": self.tender_items_delivery_details_country_description,
                                    "scheme": self.tender_items_delivery_details_country_scheme,
                                    "uri": self.tender_items_delivery_details_country_uri
                                },
                                "region": {
                                    "id": self.tender_items_delivery_details_region_id,
                                    "description": self.tender_items_delivery_details_region_description,
                                    "scheme": self.tender_items_delivery_details_region_scheme,
                                    "uri": self.tender_items_delivery_details_region_uri
                                },
                                "locality": {
                                    "scheme": self.tender_items_delivery_details_locality_scheme,
                                    "id": self.tender_items_delivery_details_locality_id,
                                    "description": self.tender_items_delivery_details_locality_description
                                }
                            }
                        },
                        "quantity": 1.000,
                        "unit": {
                            "name": "Parsec",
                            "id": "10"
                        }
                    }],
            },
            "planning": {
                "budget": {
                    "id": self.planning_budget_id,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    }
                },
                "rationale": self.planning_rationale
            },
            "buyer": {
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name,
                "identifier": {
                    "id": self.buyer_identifier_id,
                    "scheme": self.buyer_identifier_scheme,
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
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
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
                    "telephone": self.buyer_contact_point_telephone,
                    "faxNumber": self.buyer_contact_point_fax_number,
                    "url": self.buyer_contact_point_url
                },
                "additionalIdentifiers": [
                    {
                        "id": "string",
                        "scheme": "MD-IDNO",
                        "legalName": "380935103469",
                        "uri": "http://petrusenko.com/svetlana"
                    }],
                "details": {
                    "typeOfBuyer": "NATIONAL_AGENCY",
                    "mainGeneralActivity": "HEALTH",
                    "mainSectoralActivity": "WATER"
                }
            }
        }

        json_budget_fs = {
            "ocid": fs_id,
            "tender": {
                "id": "195cf37f-99cc-4729-8374-596f2fba1810",
                "status": "active",
                "statusDetails": "empty"
            },
            "planning": {
                "budget": {
                    "id": self.planning_budget_id,
                    "description": "description",
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    },
                    "europeanUnionFunding": {
                        "projectName": "Name of this project",
                        "projectIdentifier": "projectIdentifier",
                        "uri": "http://uriuri.th"
                    },
                    "isEuropeanUnionFunded": True,
                    "verified": True,
                    "sourceEntity": {
                        "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                        "name": self.funder_name,
                    },
                    "verificationDetails": None,
                    "project": "project",
                    "projectID": "projectID",
                    "uri": "http://uri.ur"
                },
                "rationale": self.planning_rationale
            },
            "funder": {
                "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                "name": self.funder_name,
                "identifier": {
                    "id": self.funder_identifier_id,
                    "scheme": self.funder_identifier_scheme,
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
                        "id": "additional identifier",
                        "scheme": "scheme",
                        "legalName": "legal name",
                        "uri": "http://addtIdent.com"
                    }],
                "contactPoint": {
                    "name": self.funder_contact_point_name,
                    "email": self.funder_contact_point_email,
                    "telephone": self.funder_contact_point_telephone,
                    "faxNumber": self.funder_contact_point_fax,
                    "url": self.funder_contact_point_url
                }
            },
            "payer": {
                "id": f"{self.payer_identifier_scheme}-{self.payer_identifier_id}",
                "name": self.payer_name,
                "identifier": {
                    "id": self.payer_identifier_id,
                    "scheme": self.payer_identifier_scheme,
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
                        "id": "additional identifier",
                        "scheme": "MD-K",
                        "legalName": "legalname",
                        "uri": "http://k.to"
                    }],
                "contactPoint": {
                    "name": self.payer_contact_point_name,
                    "email": self.payer_contact_point_email,
                    "telephone": self.payer_contact_point_telephone,
                    "faxNumber": self.payer_contact_point_fax_number,
                    "url": self.payer_contact_point_url,
                }
            }
        }

        json_notice_budget_release_ei = {
            "ocid": cp_id,
            "id": cp_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": [
                "compiled"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "2cc5a0b7-b1b7-4ed3-9210-1ca6d0af3261",
                "title": self.tender_title,
                "description": self.tender_description,
                "status": "planning",
                "statusDetails": "empty",
                "items": [
                    {
                        "id": "56db9b8d-0306-41d4-8fb1-a525b42720a6",
                        "description": self.tender_items_description,
                        "classification": {
                            "scheme": "CPV",
                            "id": self.tender_item_classification_id,
                            "description": "Servicii de reparare şi de întreţinere a vehiculelor şi a echipamentelor "
                                           "aferente şi servicii conexe"
                        },
                        "additionalClassifications": [
                            {
                                "scheme": "CPVS",
                                "id": "AA12-4",
                                "description": "Oţel carbon"
                            }],
                        "quantity": 1.000,
                        "unit": {
                            "name": "Parsec",
                            "id": "10"
                        },
                        "deliveryAddress": {
                            "streetAddress": "street",
                            "postalCode": "postal",
                            "addressDetails": {
                                "country": {
                                    "id": self.tender_items_delivery_details_country_id,
                                    "description": self.tender_items_delivery_details_country_description,
                                    "scheme": self.tender_items_delivery_details_country_scheme,
                                    "uri": self.tender_items_delivery_details_country_uri
                                },
                                "region": {
                                    "id": self.tender_items_delivery_details_region_id,
                                    "description": self.tender_items_delivery_details_region_description,
                                    "scheme": self.tender_items_delivery_details_region_scheme,
                                    "uri": self.tender_items_delivery_details_region_uri
                                },
                                "locality": {
                                    "scheme": self.tender_items_delivery_details_locality_scheme,
                                    "id": self.tender_items_delivery_details_locality_id,
                                    "description": self.tender_items_delivery_details_locality_description
                                }
                            }
                        }
                    }],
                "mainProcurementCategory": "works",
                "classification": {
                    "scheme": self.tender_classification_scheme,
                    "id": self.tender_classification_id,
                    "description": self.tender_classification_description
                }
            },
            "buyer": {
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name,
            },
            "parties": [
                {
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
                                "description": "MOLDOVA",
                                "uri": "http://reference.iatistandard.org"
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
                            "scheme": "MD-IDNO",
                            "id": "string",
                            "legalName": "380935103469",
                            "uri": "http://petrusenko.com/svetlana"
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
                }],
            "planning": {
                "budget": {
                    "id": self.planning_budget_id,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    }
                },
                "rationale": self.planning_rationale
            },
            "relatedProcesses": [
                {
                    "id": "412ee2c0-b194-11eb-8505-35fcd4e9bc47",
                    "relationship": [
                        "x_fundingSource"],
                    "scheme": "ocid",
                    "identifier": f"{fs_id}",
                    "uri": f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{fs_id}"
                }]
        }

        json_notice_budget_release_fs = {
            "ocid": fs_id,
            "id": fs_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": [
                "planning"],
            "initiationType": "tender",
            "tender": {
                "id": "195cf37f-99cc-4729-8374-596f2fba1810",
                "status": "active",
                "statusDetails": "empty"
            },
            "parties": [
                {
                    "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                    "name": self.funder_name,
                    "identifier": {
                        "scheme": self.funder_identifier_scheme,
                        "id": self.funder_identifier_id,
                        "legalName": self.funder_identifier_legal_name
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
                    "additionalIdentifiers": [
                        {
                            "scheme": "scheme",
                            "id": "additional identifier",
                            "legalName": "legal name",
                            "uri": "http://addtIdent.com"
                        }],
                    "contactPoint": {
                        "name": self.funder_contact_point_name,
                        "email": self.funder_contact_point_email,
                        "telephone": self.funder_contact_point_telephone,
                        "faxNumber": self.funder_contact_point_fax,
                        "url": self.funder_contact_point_url,
                    },
                    "roles": [
                        "funder"]
                },
                {
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
                            "scheme": "MD-K",
                            "id": "additional identifier",
                            "legalName": "legalname",
                            "uri": "http://k.to"
                        }],
                    "contactPoint": {
                        "name": self.payer_contact_point_name,
                        "email": self.payer_contact_point_email,
                        "telephone": self.payer_contact_point_telephone,
                        "faxNumber": self.payer_contact_point_fax_number,
                        "url": self.payer_contact_point_url
                    },
                    "roles": ["payer"]
                }],
            "planning": {
                "budget": {
                    "id": self.planning_budget_id,
                    "description": "description",
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    },
                    "europeanUnionFunding": {
                        "projectIdentifier": "projectIdentifier",
                        "projectName": "Name of this project",
                        "uri": "http://uriuri.th"
                    },
                    "isEuropeanUnionFunded": True,
                    "verified": True,
                    "sourceEntity": {
                        "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                        "name": self.funder_name
                    },
                    "project": "project",
                    "projectID": "projectID",
                    "uri": "http://uri.ur"
                },
                "rationale": "reason for the budget"
            },
            "relatedProcesses": [
                {
                    "id": "412d5c20-b194-11eb-8505-35fcd4e9bc47",
                    "relationship": [
                        "parent"],
                    "scheme": "ocid",
                    "identifier": cp_id,
                    "uri": f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{cp_id}"
                }]
        }

        json_notice_budget_compiled_release_ei = {
            "ocid": cp_id,
            "id": cp_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": [
                "compiled"],
            "language": self.lang,
            "initiationType": "tender",
            "tender": {
                "id": "2cc5a0b7-b1b7-4ed3-9210-1ca6d0af3261",
                "title": self.tender_title,
                "description": self.tender_description,
                "status": "planning",
                "statusDetails": "empty",
                "items": [
                    {
                        "id": "56db9b8d-0306-41d4-8fb1-a525b42720a6",
                        "description": self.tender_items_description,
                        "classification": {
                            "scheme": "CPV",
                            "id": self.tender_item_classification_id,
                            "description": "Servicii de reparare şi de întreţinere a vehiculelor şi a "
                                           "echipamentelor aferente şi servicii conexe"
                        },
                        "additionalClassifications": [
                            {
                                "scheme": "CPVS",
                                "id": "AA12-4",
                                "description": "Oţel carbon"
                            }],
                        "quantity": 1.000,
                        "unit": {
                            "name": "Parsec",
                            "id": "10"
                        },
                        "deliveryAddress": {
                            "streetAddress": "street",
                            "postalCode": "postal",
                            "addressDetails": {
                                "country": {
                                    "id": self.tender_items_delivery_details_country_id,
                                    "description": self.tender_items_delivery_details_country_description,
                                    "scheme": self.tender_items_delivery_details_country_scheme,
                                    "uri": self.tender_items_delivery_details_country_uri
                                },
                                "region": {
                                    "id": self.tender_items_delivery_details_region_id,
                                    "description": self.tender_items_delivery_details_region_description,
                                    "scheme": self.tender_items_delivery_details_region_scheme,
                                    "uri": self.tender_items_delivery_details_region_uri
                                },
                                "locality": {
                                    "scheme": self.tender_items_delivery_details_locality_scheme,
                                    "id": self.tender_items_delivery_details_locality_id,
                                    "description": self.tender_items_delivery_details_locality_description
                                }
                            }
                        }
                    }],
                "mainProcurementCategory": "works",
                "classification": {
                    "scheme": self.tender_classification_scheme,
                    "id": self.tender_classification_id,
                    "description": self.tender_classification_description
                }
            },
            "buyer": {
                "id": f"{self.buyer_identifier_scheme}-{self.buyer_identifier_id}",
                "name": self.buyer_name
            },
            "parties": [
                {
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
                                "description": "MOLDOVA",
                                "uri": "http://reference.iatistandard.org"
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
                            "scheme": "MD-IDNO",
                            "id": "string",
                            "legalName": "380935103469",
                            "uri": "http://petrusenko.com/svetlana"
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
                }],
            "planning": {
                "budget": {
                    "id": self.tender_classification_id,
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    }
                },
                "rationale": self.planning_rationale
            },
            "relatedProcesses": [
                {
                    "id": "412ee2c0-b194-11eb-8505-35fcd4e9bc47",
                    "relationship": [
                        "x_fundingSource"],
                    "scheme": "ocid",
                    "identifier": f"{fs_id}",
                    "uri": f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{fs_id}"
                }]
        }

        json_notice_budget_compiled_release_fs = {
            "ocid": fs_id,
            "id": fs_id + "-" + f"{period[2]}",
            "date": self.planning_budget_period_start_date,
            "tag": [
                "planning"],
            "initiationType": "tender",
            "tender": {
                "id": "195cf37f-99cc-4729-8374-596f2fba1810",
                "status": "active",
                "statusDetails": "empty"
            },
            "parties": [
                {
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
                            "scheme": "scheme",
                            "id": "additional identifier",
                            "legalName": "legal name",
                            "uri": "http://addtIdent.com"
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
                },
                {
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
                            "scheme": "MD-K",
                            "id": "additional identifier",
                            "legalName": "legalname",
                            "uri": "http://k.to"
                        }],
                    "contactPoint": {
                        "name": self.payer_contact_point_name,
                        "email": self.payer_contact_point_email,
                        "telephone": self.payer_contact_point_telephone,
                        "faxNumber": self.payer_contact_point_fax_number,
                        "url": self.payer_contact_point_url,
                    },
                    "roles": ["payer"]
                }
            ],
            "planning": {
                "budget": {
                    "id": self.tender_classification_id,
                    "description": "description",
                    "period": {
                        "startDate": self.planning_budget_period_start_date,
                        "endDate": self.planning_budget_period_end_date
                    },
                    "amount": {
                        "amount": self.amount,
                        "currency": self.currency
                    },
                    "europeanUnionFunding": {
                        "projectIdentifier": "projectIdentifier",
                        "projectName": "Name of this project",
                        "uri": "http://uriuri.th"
                    },
                    "isEuropeanUnionFunded": True,
                    "verified": True,
                    "sourceEntity": {
                        "id": f"{self.funder_identifier_scheme}-{self.funder_identifier_id}",
                        "name": self.funder_name
                    },
                    "project": "project",
                    "projectID": "projectID",
                    "uri": "http://uri.ur"
                },
                "rationale": "reason for the budget"
            },
            "relatedProcesses": [
                {
                    "id": "412d5c20-b194-11eb-8505-35fcd4e9bc47",
                    "relationship": [
                        "parent"],
                    "scheme": "ocid",
                    "identifier": f"{cp_id}",
                    "uri": f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{cp_id}"
                }]
        }

        session.execute(f"INSERT INTO orchestrator_context (cp_id,context) VALUES ("
                        f"'{cp_id}','{json.dumps(json_orchestrator_context)}');").one()
        session.execute(f"INSERT INTO budget_ei (cp_id,token_entity,created_date,json_data,owner) VALUES("
                        f"'{cp_id}',{ei_token},{period[2]},'{json.dumps(json_budget_ei)}','{owner}');").one()
        session.execute(

            f"INSERT INTO budget_fs (cp_id,token_entity,amount,amount_reserved,created_date,json_data,oc_id,owner) "
            f"VALUES ('{cp_id}',{fs_token},{self.amount},0,{period[2]},'{json.dumps(json_budget_fs)}',"
            f"'{fs_id}','{owner}');").one()

        session.execute(f"INSERT INTO notice_budget_release ("
                        f"cp_id,oc_id,release_id,json_data,release_date,stage) VALUES("
                        f"'{cp_id}','{cp_id}','{cp_id + str(period[2])}',"
                        f"'{json.dumps(json_notice_budget_release_ei)}',{period[2]},'EI');").one()
        session.execute(f"INSERT INTO notice_budget_compiled_release ("
                        f"cp_id,oc_id,amount,json_data,publish_date,release_date,"
                        f"release_id,stage) VALUES('{cp_id}','{cp_id}', 0.0, "
                        f"'{json.dumps(json_notice_budget_compiled_release_ei)}',"
                        f"{period[2]},{period[2]},'{cp_id + '-' + f'{period[2]}'}',"
                        f"'EI');").one()
        session.execute(
            f"INSERT INTO notice_budget_release (cp_id,oc_id,release_id,json_data,release_date,stage) "
            f"VALUES ('{cp_id}','{fs_id}','{fs_id + '-' + str(period[2])}',"
            f"'{json.dumps(json_notice_budget_release_fs)}',{period[2]},'FS');").one()
        session.execute(
            f"INSERT INTO notice_budget_compiled_release (cp_id,oc_id,amount,json_data,publish_date,release_date,"
            f"release_id,stage) VALUES ('{cp_id}','{fs_id}',{self.amount},"
            f"'{json.dumps(json_notice_budget_compiled_release_fs)}',{period[2]},{period[2]},"
            f"'{fs_id + '-' + str(period[2])}','FS');")
        session.execute(f"INSERT INTO notice_budget_offset (cp_id,release_date) "
                        f"VALUES ('{cp_id}',{period[2]});").one()
        return f"http://dev.public.eprocurement.systems/budgets/{cp_id}", fs_id, fs_token

    @allure.step('Receive message in feed-point')
    def get_message_from_kafka(self):
        time.sleep(1.8)
        message_from_kafka = get_message_from_kafka(self.x_operation_id)
        allure.attach(json.dumps(message_from_kafka), 'Message in feed-point')
        return message_from_kafka

    def check_on_that_message_is_successfully_create_fs(self):
        message = get_message_from_kafka(self.x_operation_id)
        check_x_operation_id = is_it_uuid(message["X-OPERATION-ID"], 4)
        check_x_response_id = is_it_uuid(message["X-RESPONSE-ID"], 1)
        check_initiator = fnmatch.fnmatch(message["initiator"], "platform")
        check_oc_id = fnmatch.fnmatch(message["data"]["ocid"], "ocds-t1s2t3-MD-*")
        check_url = fnmatch.fnmatch(message["data"]["url"],
                                    f"http://dev.public.eprocurement.systems/budgets/{message['data']['ocid']}")
        check_operation_date = fnmatch.fnmatch(message["data"]["operationDate"], "202*-*-*T*:*:*Z")
        check_fs_id = fnmatch.fnmatch(message["data"]["outcomes"]["fs"][0]["id"], f"{message['data']['ocid']}-FS-*")
        check_fs_token = is_it_uuid(message["data"]["outcomes"]["fs"][0]["X-TOKEN"], 4)
        if check_x_operation_id is True and check_x_response_id is True and check_initiator is True and \
                check_oc_id is True and check_url is True and check_operation_date is True and check_fs_id is True and \
                check_fs_token is True:
            return True
        else:
            return False

    def check_on_that_message_is_successfully_update_fs(self, cp_id, fs_id):
        message = get_message_from_kafka(self.x_operation_id)
        check_x_operation_id = is_it_uuid(message["X-OPERATION-ID"], 4)
        check_x_response_id = is_it_uuid(message["X-RESPONSE-ID"], 1)
        check_initiator = fnmatch.fnmatch(message["initiator"], "platform")
        check_oc_id = fnmatch.fnmatch(message["data"]["ocid"], f"{fs_id}")
        check_url = fnmatch.fnmatch(message["data"]["url"],
                                    f"http://dev.public.eprocurement.systems/budgets/{cp_id}/{fs_id}")
        check_operation_date = fnmatch.fnmatch(message["data"]["operationDate"], "202*-*-*T*:*:*Z")
        if check_x_operation_id is True and check_x_response_id is True and check_initiator is True and \
                check_oc_id is True and check_url is True and check_operation_date is True:
            return True
        else:
            return False

# def delete_data_from_database(self):
#     cpid = self.cpid
#     auth_provider = PlainTextAuthProvider(username=self.cassandra_username, password=self.cassandra_password)
#     cluster = Cluster([self.cassandra_cluster], auth_provider=auth_provider)
#     session = cluster.connect('ocds')
#     del_orchestrator_context_from_database = session.execute(
#         f"DELETE FROM orchestrator_context WHERE cp_id='{cpid}';").one()
#     del_budget_ei_from_database = session.execute(f"DELETE FROM budget_ei WHERE cp_id='{cpid}';").one()
#     del_notice_budget_release_from_database = session.execute(
#         f"DELETE FROM notice_budget_release WHERE cp_id='{cpid}';").one()
#     del_notice_budget_offset_from_database = session.execute(
#         f"DELETE FROM notice_budget_offset WHERE cp_id='{cpid}';").one()
#     del_notice_budget_compiled_release_from_database = session.execute(
#         f"DELETE FROM notice_budget_compiled_release WHERE cp_id='{cpid}';").one()
#     return del_orchestrator_context_from_database, del_budget_ei_from_database, \
#            del_notice_budget_release_from_database, del_notice_budget_offset_from_database, \
#            del_notice_budget_compiled_release_from_database
