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
from useful_functions import is_it_uuid, prepared_cp_id, get_period, get_access_token_for_platform_two


class EI:
    def __init__(self, payload, instance, cassandra_username, cassandra_password, country='MD',
                 cpid=prepared_cp_id(), ei_token=str(uuid4()), ei_token_update_ei=None,
                 lang='ro', tender_classification_id="45100000-8",
                 tender_item_classification_id="45100000-8", planning_budget_id="45100000-8",
                 platform="platform_one",
                 tender_classification_scheme="CPV", planning_budget_period_start_date=get_period()[0],
                 tender_classification_description="Lucrări de pregătire a şantierului",
                 planning_budget_period_end_date=get_period()[1], buyer_name="LLC Petrusenko",
                 buyer_identifier_id="380632074071", buyer_identifier_scheme="MD-IDNO",
                 buyer_identifier_legal_name="LLC Petrusenko", buyer_identifier_uri="http://petrusenko.com/fop",
                 buyer_address_street_address="Zakrevskogo", buyer_address_address_details_country_id="MD",
                 buyer_address_address_details_region_id="1700000", buyer_address_address_details_locality_id="1701000",
                 buyer_address_address_details_locality_scheme="CUATM", buyer_contact_point_email="svetik@gmail.com",
                 buyer_address_address_details_locality_description="mun.Cahul", buyer_contact_point_telephone="",
                 buyer_contact_point_name="Petrusenko Svitlana", buyer_contact_point_fax_number="5552233",
                 buyer_contact_point_url="http://petrusenko.com/svetlana", buyer_address_postal_code="02217",
                 tender_description="description of finansical sourse", tender_title="EI_FULL_WORKS",
                 planning_rationale="planning.rationale", tender_items_description="item 1",
                 tender_items_additional_classifications_id="AA12-4",
                 tender_items_delivery_details_country_id="MD",
                 tender_items_delivery_details_country_scheme="iso-alpha2",
                 tender_items_delivery_details_country_description="Moldova, Republica",
                 tender_items_delivery_details_country_uri="https://www.iso.org",
                 tender_items_delivery_details_region_id="0101000",
                 tender_items_delivery_details_region_scheme="CUATM",
                 tender_items_delivery_details_region_description="mun.Chişinău",
                 tender_items_delivery_details_region_uri="http://statistica.md",
                 tender_items_delivery_details_locality_id="0101000",
                 tender_items_delivery_details_locality_scheme="CUATM",
                 tender_items_delivery_details_locality_description="mun.Chişinău",
                 tender_items_delivery_details_locality_uri="http://statistica.md",
                 tender_items_delivery_street="Khreshchatyk", tender_items_delivery_postal="01124",
                 tender_items_unit_name="Parsec", tender_items_unit_id="10", tender_items_quantity=10.00,
                 tender_items_id="6a565c47-ff11-4e2d-8ea1-3f34c5d751f9"):
        if ei_token_update_ei is None:
            self.ei_token_update_ei = self.ei_token
        self.payload = payload
        self.cpid = cpid
        self.ei_token = ei_token
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

    @allure.step('Create EI')
    def create_ei(self):
        ei = requests.post(
            url=self.host_of_request + "/do/ei",
            headers={
                'Authorization': 'Bearer ' + self.access_token,
                'X-OPERATION-ID': self.x_operation_id,
                'Content-Type': 'application/json'},
            params={
                'country': self.country,
                'lang': self.lang
            },
            json=self.payload)
        allure.attach(self.host_of_request + "/do/ei", 'URL')
        allure.attach(json.dumps(self.payload), 'Prepared payload')
        return ei

    @allure.step('Update EI')
    def update_ei(self):
        ei = requests.post(
            url=self.host_of_request + "/do/ei",
            headers={
                'Authorization': 'Bearer ' + self.access_token,
                'X-OPERATION-ID': self.x_operation_id,
                'X-TOKEN': self.ei_token_update_ei,
                'Content-Type': 'application/json'},
            json=self.payload)
        allure.attach(self.host_of_request + "/do/ei", 'URL')
        allure.attach(json.dumps(self.payload), 'Prepared payload')
        return ei

    @allure.step('Insert EI')
    def insert_ei_full_data_model(self):
        auth_provider = PlainTextAuthProvider(username=self.cassandra_username, password=self.cassandra_password)
        cluster = Cluster([self.cassandra_cluster], auth_provider=auth_provider)
        session = cluster.connect('ocds')
        owner = "445f6851-c908-407d-9b45-14b92f3e964b"
        period = get_period()
        json_orchestrator_context = {
            "operationId": f"{uuid4()}",
            "requestId": f"{uuid4()}",
            "cpid": self.cpid,
            "stage": "EI",
            "processType": "ei",
            "operationType": "createEI",
            "owner": owner,
            "country": self.country,
            "language": self.lang,
            "token": self.ei_token,
            "startDate": self.planning_budget_period_start_date,
            "timeStamp": period[2],
            "isAuction": False,
            "testMode": False
        }
        json_budget_ei = {
            "ocid": self.cpid,
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
            "ocid": self.cpid,
            "id": self.cpid + '-' + f'{period[2]}',
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
            "ocid": self.cpid,
            "id": self.cpid + "-" + f"{period[2]}",
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
                        f"'{self.cpid}','{json.dumps(json_orchestrator_context)}');").one()

        session.execute(f"INSERT INTO budget_ei (cp_id,token_entity,created_date,json_data,owner) VALUES("
                        f"'{self.cpid}',{self.ei_token},1609927348000,'{json.dumps(json_budget_ei)}','{owner}');").one()

        session.execute(f"INSERT INTO notice_budget_release ("
                        f"cp_id,oc_id,release_id,json_data,release_date,stage) VALUES("
                        f"'{self.cpid}','{self.cpid}','{self.cpid + '1609927348000'}',"
                        f"'{json.dumps(json_notice_budget_release_ei)}',1609943491271,'EI');").one()

        session.execute(f"INSERT INTO notice_budget_offset (cp_id,release_date) VALUES("
                        f"'{self.cpid}','1609927348000');").one()

        session.execute(f"INSERT INTO notice_budget_compiled_release ("
                        f"cp_id,oc_id,amount,json_data,publish_date,release_date,"
                        f"release_id,stage) VALUES('{self.cpid}','{self.cpid}', 0.0, "
                        f"'{json.dumps(json_notice_budget_compiled_release_ei)}',"
                        f"1609943491271,1609943491271,'{self.cpid + '-' + f'{period[2]}'}',"
                        f"'EI');").one()
        allure.attach(owner, 'OWNER')
        allure.attach(self.cpid, 'CPID')
        allure.attach(self.ei_token, 'X-TOKEN')
        allure.attach(f"http://dev.public.eprocurement.systems/budgets/{self.cpid}", 'URL')
        return f"http://dev.public.eprocurement.systems/budgets/{self.cpid}", self.ei_token, self.cpid

    @allure.step('Insert EI')
    def insert_ei_obligatory_data_model(self):
        auth_provider = PlainTextAuthProvider(username=self.cassandra_username, password=self.cassandra_password)
        cluster = Cluster([self.cassandra_cluster], auth_provider=auth_provider)
        session = cluster.connect('ocds')
        owner = "445f6851-c908-407d-9b45-14b92f3e964b"
        period = get_period()
        json_orchestrator_context = {
            "operationId": f"{uuid4()}",
            "requestId": f"{uuid4()}",
            "cpid": self.cpid,
            "stage": "EI",
            "processType": "ei",
            "operationType": "createEI",
            "owner": owner,
            "country": self.country,
            "language": self.lang,
            "token": self.ei_token,
            "startDate": self.planning_budget_period_start_date,
            "timeStamp": period[2],
            "isAuction": False,
            "testMode": False
        }
        json_budget_ei = {
            "ocid": self.cpid,
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
            "ocid": self.cpid,
            "id": self.cpid + '-' + f'{period[2]}',
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
            "ocid": self.cpid,
            "id": self.cpid + "-" + f"{period[2]}",
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
                        f"'{self.cpid}','{json.dumps(json_orchestrator_context)}');").one()

        session.execute(f"INSERT INTO budget_ei (cp_id,token_entity,created_date,json_data,owner) VALUES("
                        f"'{self.cpid}',{self.ei_token},1609927348000,'{json.dumps(json_budget_ei)}','{owner}');").one()

        session.execute(f"INSERT INTO notice_budget_release ("
                        f"cp_id,oc_id,release_id,json_data,release_date,stage) VALUES("
                        f"'{self.cpid}','{self.cpid}','{self.cpid + '1609927348000'}',"
                        f"'{json.dumps(json_notice_budget_release_ei)}',1609943491271,'EI');").one()

        session.execute(f"INSERT INTO notice_budget_offset (cp_id,release_date) VALUES("
                        f"'{self.cpid}','1609927348000');").one()

        session.execute(f"INSERT INTO notice_budget_compiled_release ("
                        f"cp_id,oc_id,amount,json_data,publish_date,release_date,"
                        f"release_id,stage) VALUES('{self.cpid}','{self.cpid}', 0.0, "
                        f"'{json.dumps(json_notice_budget_compiled_release_ei)}',"
                        f"1609943491271,1609943491271,'{self.cpid + '-' + f'{period[2]}'}',"
                        f"'EI');").one()
        allure.attach(owner, 'OWNER')
        allure.attach(self.cpid, 'CPID')
        allure.attach(self.ei_token, 'X-TOKEN')
        allure.attach(f"http://dev.public.eprocurement.systems/budgets/{self.cpid}", 'URL')
        return f"http://dev.public.eprocurement.systems/budgets/{self.cpid}/{self.cpid}", self.ei_token, self.cpid

    @allure.step('Insert EI')
    def insert_ei_full_data_model_without_item(self):
        auth_provider = PlainTextAuthProvider(username=self.cassandra_username, password=self.cassandra_password)
        cluster = Cluster([self.cassandra_cluster], auth_provider=auth_provider)
        session = cluster.connect('ocds')
        owner = "445f6851-c908-407d-9b45-14b92f3e964b"
        period = get_period()
        json_orchestrator_context = {
            "operationId": f"{uuid4()}",
            "requestId": f"{uuid4()}",
            "cpid": self.cpid,
            "stage": "EI",
            "processType": "ei",
            "operationType": "createEI",
            "owner": owner,
            "country": self.country,
            "language": self.lang,
            "token": self.ei_token,
            "startDate": self.planning_budget_period_start_date,
            "timeStamp": period[2],
            "isAuction": False,
            "testMode": False
        }
        json_budget_ei = {
            "ocid": self.cpid,
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
            "ocid": self.cpid,
            "id": self.cpid + '-' + f'{period[2]}',
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
            "ocid": self.cpid,
            "id": self.cpid + "-" + f"{period[2]}",
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
                        f"'{self.cpid}','{json.dumps(json_orchestrator_context)}');").one()

        session.execute(f"INSERT INTO budget_ei (cp_id,token_entity,created_date,json_data,owner) VALUES("
                        f"'{self.cpid}',{self.ei_token},1609927348000,'{json.dumps(json_budget_ei)}','{owner}');").one()

        session.execute(f"INSERT INTO notice_budget_release ("
                        f"cp_id,oc_id,release_id,json_data,release_date,stage) VALUES("
                        f"'{self.cpid}','{self.cpid}','{self.cpid + '1609927348000'}',"
                        f"'{json.dumps(json_notice_budget_release_ei)}',1609943491271,'EI');").one()

        session.execute(f"INSERT INTO notice_budget_offset (cp_id,release_date) VALUES("
                        f"'{self.cpid}','1609927348000');").one()

        session.execute(f"INSERT INTO notice_budget_compiled_release ("
                        f"cp_id,oc_id,amount,json_data,publish_date,release_date,"
                        f"release_id,stage) VALUES('{self.cpid}','{self.cpid}', 0.0, "
                        f"'{json.dumps(json_notice_budget_compiled_release_ei)}',"
                        f"1609943491271,1609943491271,'{self.cpid + '-' + f'{period[2]}'}',"
                        f"'EI');").one()
        allure.attach(owner, 'OWNER')
        allure.attach(self.cpid, 'CPID')
        allure.attach(self.ei_token, 'X-TOKEN')
        allure.attach(f"http://dev.public.eprocurement.systems/budgets/{self.cpid}", 'URL')
        return f"http://dev.public.eprocurement.systems/budgets/{self.cpid}", self.ei_token, self.cpid

    @allure.step('Receive message in feed-point')
    def get_message_from_kafka(self):
        time.sleep(1.8)
        message_from_kafka = get_message_from_kafka(self.x_operation_id)
        allure.attach(json.dumps(message_from_kafka), 'Message in feed-point')
        return message_from_kafka

    def check_on_that_message_is_successfull_create_ei(self):
        message = get_message_from_kafka(self.x_operation_id)
        check_x_operation_id = is_it_uuid(message["X-OPERATION-ID"], 4)
        check_x_response_id = is_it_uuid(message["X-RESPONSE-ID"], 1)
        check_initiator = fnmatch.fnmatch(message["initiator"], "platform")
        check_oc_id = fnmatch.fnmatch(message["data"]["ocid"], "ocds-t1s2t3-MD-*")
        check_url = fnmatch.fnmatch(message["data"]["url"],
                                    f"http://dev.public.eprocurement.systems/budgets/{message['data']['ocid']}")
        check_operation_date = fnmatch.fnmatch(message["data"]["operationDate"], "202*-*-*T*:*:*Z")
        check_ei_id = fnmatch.fnmatch(message["data"]["outcomes"]["ei"][0]["id"], "ocds-t1s2t3-MD-*")
        check_ei_token = is_it_uuid(message["data"]["outcomes"]["ei"][0]["X-TOKEN"], 4)
        if check_x_operation_id is True and check_x_response_id is True and check_initiator is True and \
                check_oc_id is True and check_url is True and check_operation_date is True and check_ei_id is True and \
                check_ei_token is True:
            return True
        else:
            return False

    def check_on_that_message_is_successfully_update_ei(self):
        message = get_message_from_kafka(self.x_operation_id)
        check_x_operation_id = is_it_uuid(message["X-OPERATION-ID"], 4)
        check_x_response_id = is_it_uuid(message["X-RESPONSE-ID"], 1)
        check_initiator = fnmatch.fnmatch(message["initiator"], "platform")
        check_oc_id = fnmatch.fnmatch(message["data"]["ocid"], "ocds-t1s2t3-MD-*")
        check_url = fnmatch.fnmatch(message["data"]["url"],
                                    f"http://dev.public.eprocurement.systems/budgets/{message['data']['ocid']}/"
                                    f"{message['data']['ocid']}")
        check_operation_date = fnmatch.fnmatch(message["data"]["operationDate"], "202*-*-*T*:*:*Z")
        if check_x_operation_id is True and check_x_response_id is True and check_initiator is True and \
                check_oc_id is True and check_url is True and check_operation_date is True:
            return True
        else:
            return False

    # def delete_data_from_database(self):
    #     cpid = get_message_from_kafka(self.x_operation_id)['data']['outcomes']['ei'][0]['id']
    #     auth_provider = PlainTextAuthProvider(username=username, password=password)
    #     cluster = Cluster([host], auth_provider=auth_provider)
    #     session = cluster.connect('ocds')
    #     del_orchestrator_context_from_db = session.execute(
    #         f"DELETE FROM orchestrator_context WHERE cp_id='{cpid}';").one()
    #     del_budget_ei_from_db = session.execute(f"DELETE FROM budget_ei WHERE cp_id='{cpid}';").one()
    #     del_notice_budget_release_from_db = session.execute(
    #         f"DELETE FROM notice_budget_release WHERE cp_id='{cpid}';").one()
    #     del_notice_budget_offset_from_db = session.execute(
    #         f"DELETE FROM notice_budget_offset WHERE cp_id='{cpid}';").one()
    #     del_notice_budget_compiled_release_from_db = session.execute(
    #         f"DELETE FROM notice_budget_compiled_release WHERE cp_id='{cpid}';").one()
    #     return del_orchestrator_context_from_db, del_budget_ei_from_db, del_notice_budget_release_from_db, \
    #            del_notice_budget_offset_from_db, del_notice_budget_compiled_release_from_db
