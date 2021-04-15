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
from tests.presets import set_instance_for_cassandra, set_instance_for_request, create_ei, update_ei
from useful_functions import is_it_uuid, prepared_cpid, get_period

password_dev = '6AH7vbrkMWnfK'
password_sandbox = 'brT4Kn27RQs'
cluster_dev = '10.0.20.104'
cluster_sandbox = '10.0.10.104'

instance = set_instance_for_cassandra()
username = instance[1]
password = instance[2]
host = instance[0]


class EI:
    def __init__(self, payload, country='MD', lang='ro', tender_classification_id="45100000-8",
                 tender_item_classification_id="45100000-8", planning_budget_id="45100000-8"):
        self.tender_classification_id = tender_classification_id
        self.tender_item_classification_id = tender_item_classification_id
        self.planning_budget_id = planning_budget_id
        self.payload = payload
        self.country = country
        self.lang = lang
        self.access_token = get_access_token_for_platform_one()
        self.x_operation_id = get_x_operation_id(self.access_token)

    @allure.step('Create EI')
    def create_ei(self):
        environment_host = set_instance_for_request()
        ei = requests.post(
            url=environment_host + create_ei,
            headers={
                'Authorization': 'Bearer ' + self.access_token,
                'X-OPERATION-ID': self.x_operation_id,
                'Content-Type': 'application/json'},
            params={
                'country': self.country,
                'lang': self.lang
            },
            json=self.payload)
        allure.attach(environment_host + create_ei, 'URL')
        allure.attach(json.dumps(self.payload), 'Prepared payload')
        return ei

    @allure.step('Insert EI')
    def insert_ei_full_data_model(self):
        auth_provider = PlainTextAuthProvider(username=username, password=password)
        cluster = Cluster([host], auth_provider=auth_provider)
        session = cluster.connect('ocds')
        self.ei_token = str(uuid4())
        owner = "445f6851-c908-407d-9b45-14b92f3e964b"
        self.cpid = prepared_cpid()
        period = get_period()
        json_orchestrator_context = {
            "operationId": f"{uuid4()}",
            "requestId": f"{uuid4()}",
            "cpid": self.cpid,
            "stage": "EI",
            "processType": "ei",
            "operationType": "createEI",
            "owner": owner,
            "country": "MD",
            "language": "ro",
            "token": self.ei_token,
            "startDate": period[0],
            "timeStamp": period[2],
            "isAuction": False,
            "testMode": False
        }
        json_budget_ei = {
            "ocid": self.cpid,
            "tender": {
                "id": "fbd943ca-aaad-433d-9189-96566e3648ea",
                "title": "EI_FULL_WORKS",
                "description": "description of finansical sourse",
                "status": "planning",
                "statusDetails": "empty",
                "classification": {
                    "id": self.tender_classification_id,
                    "scheme": "CPV",
                    "description": "Lucrări de pregătire a şantierului"
                },
                "mainProcurementCategory": "works",
                "items": [{
                    "id": "6a565c47-ff11-4e2d-8ea1-3f34c5d751f9",
                    "description": "item 1",
                    "classification": {
                        "id": self.tender_item_classification_id,
                        "description": "Lucrări de pregătire a şantierului",
                        "scheme": "CPV"
                    },
                    "additionalClassifications": [{
                        "id": "AA12-4",
                        "description": "Oţel carbon",
                        "scheme": "CPVS"
                    }],
                    "deliveryAddress": {
                        "streetAddress": "Khreshchatyk",
                        "postalCode": "01124",
                        "addressDetails": {
                            "country": {
                                "id": "MD",
                                "description": "MOLDOVA",
                                "scheme": "iso-alpha2",
                                "uri": "http://reference.iatistandard.org"
                            },
                            "region": {
                                "id": "0101000",
                                "description": "mun.Chişinău",
                                "scheme": "CUATM",
                                "uri": "http://statistica.md"
                            },
                            "locality": {
                                "id": "0101000",
                                "description": "mun.Chişinău",
                                "scheme": "CUATM",
                                "uri": "http://statistica.md"
                            }
                        }
                    },
                    "quantity": 10.00,
                    "unit": {
                        "id": "10",
                        "name": "Parsec"
                    }
                }]
            },
            "planning": {
                "budget": {
                    "id": self.planning_budget_id,
                    "period": {
                        "startDate": period[0],
                        "endDate": period[1]
                    }
                },
                "rationale": "planning.rationale"
            },
            "buyer": {
                "id": "MD-IDNO-380632074071",
                "name": "LLC Petrusenko",
                "identifier": {
                    "id": "380632074071",
                    "scheme": "MD-IDNO",
                    "legalName": "LLC Petrusenko",
                    "uri": "http://petrusenko.com/fop"
                },
                "address": {
                    "streetAddress": "Zakrevskogo",
                    "postalCode": "02217",
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": "MD",
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": "1700000",
                            "description": "Cahul",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": "CUATM",
                            "id": "1701000",
                            "description": "mun.Cahul",
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "contactPoint": {
                    "name": "Petrusenko Svitlana",
                    "email": "svetik@gmail.com",
                    "telephone": "888999666",
                    "faxNumber": "5552233",
                    "url": "http://petrusenko.com/svetlana"
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
            "date": period[0],
            "tag": ["compiled"],
            "initiationType": "tender",
            "tender": {
                "id": "fbd943ca-aaad-433d-9189-96566e3648ea",
                "title": "EI_FULL_WORKS",
                "description": "description of finansical sourse",
                "status": "planning",
                "statusDetails": "empty",
                "items": [{
                    "id": "6a565c47-ff11-4e2d-8ea1-3f34c5d751f9",
                    "description": "item 1",
                    "classification": {
                        "scheme": "CPV",
                        "id": self.tender_item_classification_id,
                        "description": "Lucrări de pregătire a şantierului"
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": "AA12-4",
                        "description": "Oţel carbon"
                    }],
                    "quantity": 10.000,
                    "unit": {
                        "name": "Parsec",
                        "id": "10"
                    },
                    "deliveryAddress": {
                        "streetAddress": "Khreshchatyk",
                        "postalCode": "01124",
                        "addressDetails": {
                            "country": {
                                "scheme": "iso-alpha2",
                                "id": "MD",
                                "description": "MOLDOVA",
                                "uri": "http://reference.iatistandard.org"
                            },
                            "region": {
                                "scheme": "CUATM",
                                "id": "0101000",
                                "description": "mun.Chişinău",
                                "uri": "http://statistica.md"
                            },
                            "locality": {
                                "scheme": "CUATM",
                                "id": "0101000",
                                "description": "mun.Chişinău",
                                "uri": "http://statistica.md"
                            }
                        }
                    }
                }],
                "mainProcurementCategory": "works",
                "classification": {
                    "scheme": "CPV",
                    "id": self.tender_classification_id,
                    "description": "Lucrări de pregătire a şantierului"
                }
            },
            "buyer": {
                "id": "MD-IDNO-380632074071",
                "name": "LLC Petrusenko"
            },
            "parties": [{
                "id": "MD-IDNO-380632074071",
                "name": "LLC Petrusenko",
                "identifier": {
                    "scheme": "MD-IDNO",
                    "id": "380632074071",
                    "legalName": "LLC Petrusenko",
                    "uri": "http://petrusenko.com/fop"
                },
                "address": {
                    "streetAddress": "Zakrevskogo",
                    "postalCode": "02217",
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": "MD",
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": "1700000",
                            "description": "Cahul",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": "CUATM",
                            "id": "1701000",
                            "description": "mun.Cahul",
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
                    "name": "Petrusenko Svitlana",
                    "email": "svetik@gmail.com",
                    "telephone": "888999666",
                    "faxNumber": "5552233",
                    "url": "http://petrusenko.com/svetlana"
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
                        "startDate": period[0],
                        "endDate": period[1]
                    }
                },
                "rationale": "planning.rationale"
            }
        }

        json_notice_budget_compiled_release_ei = {
            "ocid": self.cpid,
            "id": self.cpid + "-" + f"{period[2]}",
            "date": period[0],
            "tag": ["compiled"],
            "initiationType": "tender",
            "tender": {
                "id": "fbd943ca-aaad-433d-9189-96566e3648ea",
                "title": "EI_FULL_WORKS",
                "description": "description of finansical sourse",
                "status": "planning",
                "statusDetails": "empty",
                "items": [{
                    "id": "6a565c47-ff11-4e2d-8ea1-3f34c5d751f9",
                    "description": "item 1",
                    "classification": {
                        "scheme": "CPV",
                        "id": self.tender_item_classification_id,
                        "description": "Lucrări de pregătire a şantierului"
                    },
                    "additionalClassifications": [{
                        "scheme": "CPVS",
                        "id": "AA12-4",
                        "description": "Oţel carbon"
                    }],
                    "quantity": 10.000,
                    "unit": {
                        "name": "Parsec",
                        "id": "10"
                    },
                    "deliveryAddress": {
                        "streetAddress": "Khreshchatyk",
                        "postalCode": "01124",
                        "addressDetails": {
                            "country": {
                                "scheme": "iso-alpha2",
                                "id": "MD",
                                "description": "MOLDOVA",
                                "uri": "http://reference.iatistandard.org"
                            },
                            "region": {
                                "scheme": "CUATM",
                                "id": "0101000",
                                "description": "mun.Chişinău",
                                "uri": "http://statistica.md"
                            },
                            "locality": {
                                "scheme": "CUATM",
                                "id": "0101000",
                                "description": "mun.Chişinău",
                                "uri": "http://statistica.md"
                            }
                        }
                    }
                }],
                "mainProcurementCategory": "works",
                "classification": {
                    "scheme": "CPV",
                    "id": self.tender_classification_id,
                    "description": "Lucrări de pregătire a şantierului"
                }
            },
            "buyer": {
                "id": "MD-IDNO-380632074071",
                "name": "LLC Petrusenko"
            },
            "parties": [{
                "id": "MD-IDNO-380632074071",
                "name": "LLC Petrusenko",
                "identifier": {
                    "scheme": "MD-IDNO",
                    "id": "380632074071",
                    "legalName": "LLC Petrusenko",
                    "uri": "http://petrusenko.com/fop"
                },
                "address": {
                    "streetAddress": "Zakrevskogo",
                    "postalCode": "02217",
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": "MD",
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": "1700000",
                            "description": "Cahul",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": "CUATM",
                            "id": "1701000",
                            "description": "mun.Cahul",
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
                    "name": "Petrusenko Svitlana",
                    "email": "svetik@gmail.com",
                    "telephone": "888999666",
                    "faxNumber": "5552233",
                    "url": "http://petrusenko.com/svetlana"
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
                        "startDate": period[0],
                        "endDate": period[1]
                    }
                },
                "rationale": "planning.rationale"
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
        auth_provider = PlainTextAuthProvider(username=username, password=password)
        cluster = Cluster([host], auth_provider=auth_provider)
        session = cluster.connect('ocds')
        self.ei_token = str(uuid4())
        owner = "445f6851-c908-407d-9b45-14b92f3e964b"
        self.cpid = prepared_cpid()
        period = get_period()
        json_orchestrator_context = {
            "operationId": f"{uuid4()}",
            "requestId": f"{uuid4()}",
            "cpid": self.cpid,
            "stage": "EI",
            "processType": "ei",
            "operationType": "createEI",
            "owner": owner,
            "country": "MD",
            "language": "ro",
            "token": self.ei_token,
            "startDate": period[0],
            "timeStamp": period[2],
            "isAuction": False,
            "testMode": False
        }
        json_budget_ei = {
            "ocid": self.cpid,
            "tender": {
                "id": "fbd943ca-aaad-433d-9189-96566e3648ea",
                "title": "EI_FULL_WORKS",
                "status": "planning",
                "statusDetails": "empty",
                "classification": {
                    "id": self.tender_classification_id,
                    "scheme": "CPV",
                    "description": "Lucrări de pregătire a şantierului"
                },
                "mainProcurementCategory": "works",
                "items": [{
                    "id": "6a565c47-ff11-4e2d-8ea1-3f34c5d751f9",
                    "description": "item 1",
                    "classification": {
                        "id": self.tender_item_classification_id,
                        "description": "Lucrări de pregătire a şantierului",
                        "scheme": "CPV"
                    },
                    "deliveryAddress": {
                        "addressDetails": {
                            "country": {
                                "id": "MD",
                                "description": "MOLDOVA",
                                "scheme": "iso-alpha2",
                                "uri": "http://reference.iatistandard.org"
                            },
                            "region": {
                                "id": "0101000",
                                "description": "mun.Chişinău",
                                "scheme": "CUATM",
                                "uri": "http://statistica.md"
                            }
                        }
                    },
                    "quantity": 10.00,
                    "unit": {
                        "id": "10",
                        "name": "Parsec"
                    }
                }]
            },
            "planning": {
                "budget": {
                    "id": self.planning_budget_id,
                    "period": {
                        "startDate": period[0],
                        "endDate": period[1]
                    }
                }
            },
            "buyer": {
                "id": "MD-IDNO-380632074071",
                "name": "LLC Petrusenko",
                "identifier": {
                    "id": "380632074071",
                    "scheme": "MD-IDNO",
                    "legalName": "LLC Petrusenko"
                },
                "address": {
                    "streetAddress": "Zakrevskogo",
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": "MD",
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": "1700000",
                            "description": "Cahul",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": "CUATM",
                            "id": "1701000",
                            "description": "mun.Cahul",
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "contactPoint": {
                    "name": "Petrusenko Svitlana",
                    "email": "svetik@gmail.com",
                    "telephone": "888999666"
                }
            }
        }

        json_notice_budget_release_ei = {
            "ocid": self.cpid,
            "id": self.cpid + '-' + f'{period[2]}',
            "date": period[0],
            "tag": ["compiled"],
            "initiationType": "tender",
            "tender": {
                "id": "fbd943ca-aaad-433d-9189-96566e3648ea",
                "title": "EI_FULL_WORKS",
                "status": "planning",
                "statusDetails": "empty",
                "items": [{
                    "id": "6a565c47-ff11-4e2d-8ea1-3f34c5d751f9",
                    "description": "item 1",
                    "classification": {
                        "scheme": "CPV",
                        "id": self.tender_item_classification_id,
                        "description": "Lucrări de pregătire a şantierului"
                    },
                    "quantity": 10.000,
                    "unit": {
                        "name": "Parsec",
                        "id": "10"
                    },
                    "deliveryAddress": {
                        "addressDetails": {
                            "country": {
                                "scheme": "iso-alpha2",
                                "id": "MD",
                                "description": "MOLDOVA",
                                "uri": "http://reference.iatistandard.org"
                            },
                            "region": {
                                "scheme": "CUATM",
                                "id": "0101000",
                                "description": "mun.Chişinău",
                                "uri": "http://statistica.md"
                            }
                        }
                    }
                }],
                "mainProcurementCategory": "works",
                "classification": {
                    "scheme": "CPV",
                    "id": self.tender_classification_id,
                    "description": "Lucrări de pregătire a şantierului"
                }
            },
            "buyer": {
                "id": "MD-IDNO-380632074071",
                "name": "LLC Petrusenko"
            },
            "parties": [{
                "id": "MD-IDNO-380632074071",
                "name": "LLC Petrusenko",
                "identifier": {
                    "scheme": "MD-IDNO",
                    "id": "380632074071",
                    "legalName": "LLC Petrusenko"
                },
                "address": {
                    "streetAddress": "Zakrevskogo",
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": "MD",
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": "1700000",
                            "description": "Cahul",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": "CUATM",
                            "id": "1701000",
                            "description": "mun.Cahul",
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "contactPoint": {
                    "name": "Petrusenko Svitlana",
                    "email": "svetik@gmail.com",
                    "telephone": "888999666"
                },
                "roles": ["buyer"]
            }],
            "planning": {
                "budget": {
                    "id": self.planning_budget_id,
                    "period": {
                        "startDate": period[0],
                        "endDate": period[1]
                    }
                }
            }
        }

        json_notice_budget_compiled_release_ei = {
            "ocid": self.cpid,
            "id": self.cpid + "-" + f"{period[2]}",
            "date": period[0],
            "tag": ["compiled"],
            "language": "ro",
            "initiationType": "tender",
            "tender": {
                "id": "fbd943ca-aaad-433d-9189-96566e3648ea",
                "title": "EI_FULL_WORKS",
                "status": "planning",
                "statusDetails": "empty",
                "items": [{
                    "id": "6a565c47-ff11-4e2d-8ea1-3f34c5d751f9",
                    "description": "item 1",
                    "classification": {
                        "scheme": "CPV",
                        "id": self.tender_item_classification_id,
                        "description": "Lucrări de pregătire a şantierului"
                    },
                    "quantity": 10.000,
                    "unit": {
                        "name": "Parsec",
                        "id": "10"
                    },
                    "deliveryAddress": {
                        "addressDetails": {
                            "country": {
                                "scheme": "iso-alpha2",
                                "id": "MD",
                                "description": "MOLDOVA",
                                "uri": "http://reference.iatistandard.org"
                            },
                            "region": {
                                "scheme": "CUATM",
                                "id": "0101000",
                                "description": "mun.Chişinău",
                                "uri": "http://statistica.md"
                            }
                        }
                    }
                }],
                "mainProcurementCategory": "works",
                "classification": {
                    "scheme": "CPV",
                    "id": self.tender_classification_id,
                    "description": "Lucrări de pregătire a şantierului"
                }
            },
            "buyer": {
                "id": "MD-IDNO-380632074071",
                "name": "LLC Petrusenko"
            },
            "parties": [{
                "id": "MD-IDNO-380632074071",
                "name": "LLC Petrusenko",
                "identifier": {
                    "scheme": "MD-IDNO",
                    "id": "380632074071",
                    "legalName": "LLC Petrusenko"
                },
                "address": {
                    "streetAddress": "Zakrevskogo",
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": "MD",
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": "1700000",
                            "description": "Cahul",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": "CUATM",
                            "id": "1701000",
                            "description": "mun.Cahul",
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "contactPoint": {
                    "name": "Petrusenko Svitlana",
                    "email": "svetik@gmail.com",
                    "telephone": "888999666"
                },
                "roles": ["buyer"]
            }],
            "planning": {
                "budget": {
                    "id": self.planning_budget_id,
                    "period": {
                        "startDate": period[0],
                        "endDate": period[1]
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

    @allure.step('Update EI')
    def update_ei(self):
        environment_host = set_instance_for_request()
        ei = requests.post(
            url=environment_host + update_ei + self.cpid,
            headers={
                'Authorization': 'Bearer ' + self.access_token,
                'X-OPERATION-ID': self.x_operation_id,
                'X-TOKEN': self.ei_token,
                'Content-Type': 'application/json'},
            json=self.payload)
        allure.attach(environment_host + update_ei + self.cpid, 'URL')
        allure.attach(json.dumps(self.payload), 'Prepared payload')
        return ei

    @allure.step('Receive message in feed-point')
    def get_message_from_kafka(self):
        time.sleep(1.8)
        message_from_kafka = get_message_from_kafka(self.x_operation_id)
        allure.attach(json.dumps(message_from_kafka), 'Message in feed-point')
        return message_from_kafka

    def delete_data_from_database(self):
        cpid = get_message_from_kafka(self.x_operation_id)['data']['outcomes']['ei'][0]['id']
        auth_provider = PlainTextAuthProvider(username=username, password=password)
        cluster = Cluster([host], auth_provider=auth_provider)
        session = cluster.connect('ocds')
        del_orchestrator_context_from_database = session.execute(
            f"DELETE FROM orchestrator_context WHERE cp_id='{cpid}';").one()
        del_budget_ei_from_database = session.execute(f"DELETE FROM budget_ei WHERE cp_id='{cpid}';").one()
        del_notice_budget_release_from_database = session.execute(
            f"DELETE FROM notice_budget_release WHERE cp_id='{cpid}';").one()
        del_notice_budget_offset_from_database = session.execute(
            f"DELETE FROM notice_budget_offset WHERE cp_id='{cpid}';").one()
        del_notice_budget_compiled_release_from_database = session.execute(
            f"DELETE FROM notice_budget_compiled_release WHERE cp_id='{cpid}';").one()
        return del_orchestrator_context_from_database, del_budget_ei_from_database, \
               del_notice_budget_release_from_database, del_notice_budget_offset_from_database, \
               del_notice_budget_compiled_release_from_database

    def check_on_that_message_is_successfull_create_ei(self):
        message = get_message_from_kafka(self.x_operation_id)
        check_x_operartion_id = is_it_uuid(message["X-OPERATION-ID"], 4)
        check_x_response_id = is_it_uuid(message["X-RESPONSE-ID"], 1)
        check_initiator = fnmatch.fnmatch(message["initiator"], "platform")
        check_ocid = fnmatch.fnmatch(message["data"]["ocid"], "ocds-t1s2t3-MD-*")
        check_url = fnmatch.fnmatch(message["data"]["url"],
                                    f"http://dev.public.eprocurement.systems/budgets/{message['data']['ocid']}")
        check_operation_date = fnmatch.fnmatch(message["data"]["operationDate"], "202*-*-*T*:*:*Z")
        check_ei_id = fnmatch.fnmatch(message["data"]["outcomes"]["ei"][0]["id"], "ocds-t1s2t3-MD-*")
        check_ei_token = is_it_uuid(message["data"]["outcomes"]["ei"][0]["X-TOKEN"], 4)
        if check_x_operartion_id == True and check_x_response_id == True and check_initiator == True and \
                check_ocid == True and check_url == True and check_operation_date == True and check_ei_id == True and \
                check_ei_token == True:
            return True
        else:
            return False

    def check_on_that_message_is_successfull_update_ei(self):
        message = get_message_from_kafka(self.x_operation_id)
        check_x_operartion_id = is_it_uuid(message["X-OPERATION-ID"], 4)
        check_x_response_id = is_it_uuid(message["X-RESPONSE-ID"], 1)
        check_initiator = fnmatch.fnmatch(message["initiator"], "platform")
        check_ocid = fnmatch.fnmatch(message["data"]["ocid"], "ocds-t1s2t3-MD-*")
        check_url = fnmatch.fnmatch(message["data"]["url"],
                                    f"http://dev.public.eprocurement.systems/budgets/{message['data']['ocid']}/"
                                    f"{message['data']['ocid']}")
        check_operation_date = fnmatch.fnmatch(message["data"]["operationDate"], "202*-*-*T*:*:*Z")
        if check_x_operartion_id == True and check_x_response_id == True and check_initiator == True and \
                check_ocid == True and check_url == True and check_operation_date == True:
            return True
        else:
            return False
