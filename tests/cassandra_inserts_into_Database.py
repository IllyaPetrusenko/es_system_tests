import json
from uuid import uuid4

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

from tests.presets_choose_instance import instance

password_dev = '6AH7vbrkMWnfK'
password_sandbox = 'brT4Kn27RQs'
cluster_dev = '10.0.20.104'
cluster_sandbox = '10.0.10.104'

username = instance[1]
password = instance[2]
host = instance[0]


def insert_into_db_create_ei(cpid):
    auth_provider = PlainTextAuthProvider(username=username, password=password)
    cluster = Cluster([host], auth_provider=auth_provider)
    session = cluster.connect('ocds')
    ei_token = uuid4()
    owner = "445f6851-c908-407d-9b45-14b92f3e964b"

    json_orchestrator_context = {
        "operationId": f"{uuid4()}",
        "requestId": f"{uuid4()}",
        "cpid": f"{cpid}",
        "stage": "EI",
        "processType": "ei",
        "operationType": "createEI",
        "owner": owner,
        "country": "MD",
        "language": "ro",
        "token": f"{ei_token}",
        "startDate": "2021-01-06T14:31:31Z",
        "timeStamp": 1609943491271,
        "isAuction": False,
        "testMode": False
    }
    json_budget_ei = {
        "ocid": f"{cpid}",
        "tender": {
            "id": "fbd943ca-aaad-433d-9189-96566e3648ea",
            "title": "EI_FULL_WORKS",
            "description": "description of finansical sourse",
            "status": "planning",
            "statusDetails": "empty",
            "classification": {
                "id": "45100000-8",
                "scheme": "CPV",
                "description": "Lucrări de pregătire a şantierului"
            },
            "mainProcurementCategory": "works",
            "items": [{
                "id": "6a565c47-ff11-4e2d-8ea1-3f34c5d751f9",
                "description": "item 1",
                "classification": {
                    "id": "45100000-8",
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
                "id": "45100000-8",
                "period": {
                    "startDate": "2021-01-01T00:00:00Z",
                    "endDate": "2021-12-31T00:00:00Z"
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

    json_notice_budget_release = {
        "ocid": f"{cpid}",
        "id": f"{cpid + '1609927348000'}",
        "date": "2021-01-06T10:02:28Z",
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
                    "id": "45100000-8",
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
                "id": "45100000-8",
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
                "id": "45100000-8",
                "period": {
                    "startDate": "2021-01-01T00:00:00Z",
                    "endDate": "2021-12-31T00:00:00Z"
                }
            },
            "rationale": "planning.rationale"
        }
    }

    json_notice_budget_compiled_release = {
        "ocid": f"{cpid}",
        "id": f"{cpid + '1609927348000'}",
        "date": "2021-01-06T10:02:28Z",
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
                    "id": "45100000-8",
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
                "id": "45100000-8",
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
                "id": "45100000-8",
                "period": {
                    "startDate": "2021-01-01T00:00:00Z",
                    "endDate": "2021-12-31T00:00:00Z"
                }
            },
            "rationale": "planning.rationale"
        }
    }
    orchestrator_context = session.execute(f"INSERT INTO orchestrator_context (cp_id,context) VALUES ("
                                           f"'{cpid}','{json.dumps(json_orchestrator_context)}');").one()

    budget_ei = session.execute(f"INSERT INTO budget_ei (cp_id,token_entity,created_date,json_data,owner) VALUES("
                                f"'{cpid}',{ei_token},1609927348000,'{json.dumps(json_budget_ei)}','{owner}');").one()

    notice_budget_release = session.execute(f"INSERT INTO notice_budget_release ("
                                            f"cp_id,oc_id,release_id,json_data,release_date,stage) VALUES("
                                            f"'{cpid}','{cpid}','{cpid + '1609927348000'}',"
                                            f"'{json.dumps(json_notice_budget_release)}',1609943491271,'EI');").one()

    notice_budget_release = session.execute(f"INSERT INTO notice_budget_offset (cp_id,release_date) VALUES("
                                            f"'{cpid}','1609927348000');").one()

    notice_budget_compiled_release = session.execute(f"INSERT INTO notice_budget_compiled_release ("
                                                     f"cp_id,oc_id,amount,json_data,publish_date,release_date,"
                                                     f"release_id,stage) VALUES('{cpid}','{cpid}', 0.0, "
                                                     f"'{json.dumps(json_notice_budget_compiled_release)}',"
                                                     f"1609943491271,1609943491271,'{cpid + '1609927348000'}',"
                                                     f"'EI');").one()
    # json_data = json.loads(rows.json_data)
    # print(json_data)
    # return json_data

    print(ei_token, owner)


cpid = 'ocds-t1s2t3-MD-1609943491360'

test = insert_into_db_create_ei(cpid)

