import json
import time
import datetime

from uuid import uuid4

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

from tests.iStorage import correct_document_uploading
from tests.presets import set_instance_for_cassandra
from useful_functions import prepared_fs_ocid, get_period, get_timestamp_from_human_date, time_at_now, \
    get_contract_period, prepared_pn_ocid

# password_dev = '6AH7vbrkMWnfK'
# password_sandbox = 'brT4Kn27RQs'
# cluster_dev = '10.0.20.104'
# cluster_sandbox = '10.0.10.104'

instance = set_instance_for_cassandra()
username = instance[1]
password = instance[2]
host = instance[0]

document_1 = correct_document_uploading()
document_2 = correct_document_uploading()


def insert_into_db_create_ei(cpid):
    auth_provider = PlainTextAuthProvider(username=username, password=password)
    cluster = Cluster([host], auth_provider=auth_provider)
    session = cluster.connect('ocds')
    ei_token = uuid4()
    owner = "445f6851-c908-407d-9b45-14b92f3e964b"

    period = get_period()
    # date = datetime.datetime.now()
    # time_at_now = date.strftime('%Y-%m-%dT%H:%M:%SZ')
    # time_at_now_miliseconds = date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    # timestamp = int(
    #     time.mktime(datetime.datetime.strptime(time_at_now_miliseconds, "%Y-%m-%dT%H:%M:%S.%fZ").timetuple())) * 1000

    json_orchestrator_context = {
        "operationId": f"{uuid4()}",
        "requestId": f"{uuid4()}",
        "cpid": cpid,
        "stage": "EI",
        "processType": "ei",
        "operationType": "createEI",
        "owner": owner,
        "country": "MD",
        "language": "ro",
        "token": f"{ei_token}",
        "startDate": period[0],
        "timeStamp": period[2],
        "isAuction": False,
        "testMode": False
    }
    json_budget_ei = {
        "ocid": cpid,
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
        "ocid": cpid,
        "id": cpid + '-' + f'{period[2]}',
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
                    "startDate": period[0],
                    "endDate": period[1]
                }
            },
            "rationale": "planning.rationale"
        }
    }

    json_notice_budget_compiled_release_ei = {
        "ocid": cpid,
        "id": cpid + "-" + f"{period[2]}",
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
                    "startDate": period[0],
                    "endDate": period[1]
                }
            },
            "rationale": "planning.rationale"
        }
    }
    session.execute(f"INSERT INTO orchestrator_context (cp_id,context) VALUES ("
                    f"'{cpid}','{json.dumps(json_orchestrator_context)}');").one()

    session.execute(f"INSERT INTO budget_ei (cp_id,token_entity,created_date,json_data,owner) VALUES("
                    f"'{cpid}',{ei_token},1609927348000,'{json.dumps(json_budget_ei)}','{owner}');").one()

    session.execute(f"INSERT INTO notice_budget_release ("
                    f"cp_id,oc_id,release_id,json_data,release_date,stage) VALUES("
                    f"'{cpid}','{cpid}','{cpid + '1609927348000'}',"
                    f"'{json.dumps(json_notice_budget_release_ei)}',1609943491271,'EI');").one()

    session.execute(f"INSERT INTO notice_budget_offset (cp_id,release_date) VALUES("
                    f"'{cpid}','1609927348000');").one()

    session.execute(f"INSERT INTO notice_budget_compiled_release ("
                    f"cp_id,oc_id,amount,json_data,publish_date,release_date,"
                    f"release_id,stage) VALUES('{cpid}','{cpid}', 0.0, "
                    f"'{json.dumps(json_notice_budget_compiled_release_ei)}',"
                    f"1609943491271,1609943491271,'{cpid + '-' + f'{period[2]}'}',"
                    f"'EI');").one()

    return f"http://dev.public.eprocurement.systems/budgets/{cpid}/{cpid}", ei_token


def insert_into_db_update_ei(cpid):
    auth_provider = PlainTextAuthProvider(username=username, password=password)
    cluster = Cluster([host], auth_provider=auth_provider)
    session = cluster.connect('ocds')
    ei_token = uuid4()
    owner = "445f6851-c908-407d-9b45-14b92f3e964b"

    period = get_period()
    # date = datetime.datetime.now()
    # time_at_now = date.strftime('%Y-%m-%dT%H:%M:%SZ')
    # time_at_now_miliseconds = date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    # timestamp = int(
    #     time.mktime(datetime.datetime.strptime(time_at_now_miliseconds, "%Y-%m-%dT%H:%M:%S.%fZ").timetuple())) * 1000

    json_orchestrator_context = {
        "operationId": f"{uuid4()}",
        "requestId": f"{uuid4()}",
        "cpid": cpid,
        "stage": "EI",
        "processType": "updateEI",
        "operationType": "createEI",
        "owner": owner,
        "country": "MD",
        "language": "ro",
        "token": f"{ei_token}",
        "startDate": period[0],
        "timeStamp": period[2],
        "isAuction": False,
        "testMode": False
    }
    json_budget_ei = {
        "ocid": cpid,
        "tender": {
            "id": "fbd943ca-aaad-433d-9189-96566e3648ea",
            "title": "for EI updating from 2021 year",
            "description": "for EI updating from 2021 year",
            "status": "planning",
            "statusDetails": "empty",
            "classification": {
                "id": "45100000-8",
                "scheme": "CPV",
                "description": "Lucrări de pregătire a şantierului"
            },
            "mainProcurementCategory": "works",
            "items": [{
                "id": "e646d563-5b22-448c-b344-f2cb6eb7969d",
                "description": "for EI updating from 2021 year",
                "classification": {
                    "id": "45112350-3",
                    "description": "Lucrări de valorificare a terenurilor virane",
                    "scheme": "CPV"
                },
                "additionalClassifications": [{
                    "id": "AA05-3",
                    "description": "Fier",
                    "scheme": "CPVS"
                }],
                "deliveryAddress": {
                    "streetAddress": "for EI updating from 2021 year",
                    "postalCode": "for EI updating from 2021 year",
                    "addressDetails": {
                        "country": {
                            "id": "MD",
                            "description": "Moldova, Republica",
                            "scheme": "iso-alpha2",
                            "uri": "https://www.iso.org"
                        },
                        "region": {
                            "id": "1700000",
                            "description": "Cahul",
                            "scheme": "CUATM",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "id": "for EI updating from 2021 year",
                            "description": "for EI updating from 2021 year",
                            "scheme": "for EI updating from 2021 year"
                        }
                    }
                },
                "quantity": 999.99,
                "unit": {
                    "id": "120",
                    "name": "Milion decalitri"
                }
            }]
        },
        "planning": {
            "budget": {
                "id": "45100000-8",
                "period": {
                    "startDate": period[0],
                    "endDate": period[1]
                }
            },
            "rationale": "for EI updating from 2021 year"
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
        "ocid": cpid,
        "id": cpid + "-" + f"{period[2]}",
        "date": period[0],
        "tag": ["compiled"],
        "initiationType": "tender",
        "tender": {
            "id": "fbd943ca-aaad-433d-9189-96566e3648ea",
            "title": "for EI updating from 2021 year",
            "description": "for EI updating from 2021 year",
            "status": "planning",
            "statusDetails": "empty",
            "items": [{
                "id": "e646d563-5b22-448c-b344-f2cb6eb7969d",
                "description": "for EI updating from 2021 year",
                "classification": {
                    "scheme": "CPV",
                    "id": "45112350-3",
                    "description": "Lucrări de valorificare a terenurilor virane"
                },
                "additionalClassifications": [{
                    "scheme": "CPVS",
                    "id": "AA05-3",
                    "description": "Fier"
                }],
                "quantity": 999.990,
                "unit": {
                    "name": "Milion decalitri",
                    "id": "120"
                },
                "deliveryAddress": {
                    "streetAddress": "for EI updating from 2021 year",
                    "postalCode": "for EI updating from 2021 year",
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": "MD",
                            "description": "Moldova, Republica",
                            "uri": "https://www.iso.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": "1700000",
                            "description": "Cahul",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": "for EI updating from 2021 year",
                            "id": "for EI updating from 2021 year",
                            "description": "for EI updating from 2021 year"
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
                    "startDate": period[0],
                    "endDate": period[1]
                }
            },
            "rationale": "for EI updating from 2021 year"
        }
    }

    json_notice_budget_compiled_release_ei = {
        "ocid": cpid,
        "id": cpid + "-" + f"{period[2]}",
        "date": period[0],
        "tag": ["compiled"],
        "initiationType": "tender",
        "tender": {
            "id": "fbd943ca-aaad-433d-9189-96566e3648ea",
            "title": "for EI updating from 2021 year",
            "description": "for EI updating from 2021 year",
            "status": "planning",
            "statusDetails": "empty",
            "items": [{
                "id": "e646d563-5b22-448c-b344-f2cb6eb7969d",
                "description": "for EI updating from 2021 year",
                "classification": {
                    "scheme": "CPV",
                    "id": "45112350-3",
                    "description": "Lucrări de valorificare a terenurilor virane"
                },
                "additionalClassifications": [{
                    "scheme": "CPVS",
                    "id": "AA05-3",
                    "description": "Fier"
                }],
                "quantity": 999.990,
                "unit": {
                    "name": "Milion decalitri",
                    "id": "120"
                },
                "deliveryAddress": {
                    "streetAddress": "for EI updating from 2021 year",
                    "postalCode": "for EI updating from 2021 year",
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": "MD",
                            "description": "Moldova, Republica",
                            "uri": "https://www.iso.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": "1700000",
                            "description": "Cahul",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": "for EI updating from 2021 year",
                            "id": "for EI updating from 2021 year",
                            "description": "for EI updating from 2021 year"
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
                    "startDate": period[0],
                    "endDate": period[1]
                }
            },
            "rationale": "for EI updating from 2021 year"
        }
    }
    session.execute(f"INSERT INTO orchestrator_context (cp_id,context) VALUES ("
                    f"'{cpid}','{json.dumps(json_orchestrator_context)}');").one()

    session.execute(f"INSERT INTO budget_ei (cp_id,token_entity,created_date,json_data,owner) VALUES("
                    f"'{cpid}',{ei_token},1609927348000,'{json.dumps(json_budget_ei)}','{owner}');").one()

    session.execute(f"INSERT INTO notice_budget_release ("
                    f"cp_id,oc_id,release_id,json_data,release_date,stage) VALUES("
                    f"'{cpid}','{cpid}','{cpid + '1609927348000'}',"
                    f"'{json.dumps(json_notice_budget_release_ei)}',1609943491271,'EI');").one()

    session.execute(f"INSERT INTO notice_budget_offset (cp_id,release_date) VALUES("
                    f"'{cpid}','1609927348000');").one()

    session.execute(f"INSERT INTO notice_budget_compiled_release ("
                    f"cp_id,oc_id,amount,json_data,publish_date,release_date,"
                    f"release_id,stage) VALUES('{cpid}','{cpid}', 0.0, "
                    f"'{json.dumps(json_notice_budget_compiled_release_ei)}',"
                    f"1609943491271,1609943491271,'{cpid + '-' + f'{period[2]}'}',"
                    f"'EI');").one()

    return f"http://dev.public.eprocurement.systems/budgets/{cpid}/{cpid}", ei_token


def insert_into_db_create_fs(cpid, status="active", statusDetails="empty", buyer_id="1", payer_id="2", funder_id="3",
                             classification_id="45100000-8", currency="EUR", planning_rationale="plan", country_id="MD",
                             country_scheme="iso-alpha2", region_scheme="CUATM", region_id="3400000",
                             region_description="Donduşeni",
                             locality_scheme="CUATM", locality_id="3401000",
                             locality_description="or.Donduşeni (r-l Donduşeni)",
                             contact_point_name="Petrusenko Svitlana", contact_point_email="svetik@gmail.com",
                             contact_point_telephone="888999666", contact_point_fax="5552233",
                             contact_point_url="http://petrusenko.com/svetlana", buyer_name="LLC Dmitro",
                             funder_name="LLC Petro", payer_name="LLC Milola", country_description="Moldova, Republica",
                             budget_id="test id for budget", budget_description="test description",
                             project_name=" test project name", project_id="test project id",
                             project_uri="test project uri", amount=2000.00, is_european_funding=True,
                             european_project_name="test eropean name",
                             european_project_id="test european id",
                             european_project_uri="european uri",
                             buyer_identifier_scheme="MD-IDNO", funder_identifier_scheme="MD-IDNO",
                             payer_identifier_scheme="MD-IDNO", payer_identifier_legal_name="legal",
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
                             buyer_details_sectoral_activity="WATER", start_date=get_period()[0],
                             end_date=get_period()[1], timestamp=get_timestamp_from_human_date(get_period()[0])):
    auth_provider = PlainTextAuthProvider(username=username, password=password)
    cluster = Cluster([host], auth_provider=auth_provider)
    session = cluster.connect('ocds')
    fs_token = uuid4()
    ei_token = uuid4()
    owner = "445f6851-c908-407d-9b45-14b92f3e964b"

    # period = get_period()

    fs_ocid = prepared_fs_ocid(cpid)

    json_orchestrator_context = {
        "operationId": f"{uuid4()}",
        "requestId": f"{uuid4()}",
        "cpid": cpid,
        "ocid": fs_ocid,
        "stage": "FS",
        "processType": "fs",
        "operationType": "createFS",
        "owner": "445f6851-c908-407d-9b45-14b92f3e964b",
        "country": "MD",
        "language": "ro",
        "token": f"{fs_token}",
        "startDate": start_date,
        "timeStamp": timestamp,
        "isAuction": False
    }

    json_budget_ei = {
        "ocid": cpid,
        "tender": {
            "id": "b3f31996-60e4-4871-893d-b4e985573c8c",
            "title": "EI_FULL_WORKS",
            "description": "description of finansical sourse",
            "status": "planning",
            "statusDetails": "empty",
            "classification": {
                "id": classification_id,
                "scheme": "CPV",
                "description": "Lucrări de pregătire a şantierului"
            },
            "mainProcurementCategory": "works"
        },
        "planning": {
            "budget": {
                "id": classification_id,
                "period": {
                    "startDate": start_date,
                    "endDate": end_date
                },
                "amount": {
                    "amount": amount,
                    "currency": currency
                }
            },
            "rationale": planning_rationale
        },
        "buyer": {
            "id": f"{buyer_identifier_scheme}-{buyer_id}",
            "name": buyer_name,
            "identifier": {
                "id": buyer_id,
                "scheme": buyer_identifier_scheme,
                "legalName": buyer_identifier_legal_name,
                "uri": buyer_identifier_uri
            },
            "address": {
                "streetAddress": buyer_address_street,
                "postalCode": buyer_address_postal,
                "addressDetails": {
                    "country": {
                        "scheme": country_scheme,
                        "id": country_id,
                        "description": country_description,
                        "uri": "https://www.iso.org"
                    },
                    "region": {
                        "scheme": region_scheme,
                        "id": region_id,
                        "description": region_description,
                        "uri": "http://statistica.md"
                    },
                    "locality": {
                        "scheme": locality_scheme,
                        "id": locality_id,
                        "description": locality_description,
                        "uri": "http://statistica.md"
                    }
                }
            },
            "contactPoint": {
                "name": contact_point_name,
                "email": contact_point_email,
                "telephone": contact_point_telephone,
                "faxNumber": contact_point_fax,
                "url": contact_point_url
            },
            "additionalIdentifiers": [{
                "id": buyer_additional_id,
                "scheme": buyer_additional_scheme,
                "legalName": buyer_additional_legal,
                "uri": buyer_additional_uri
            }],
            "details": {
                "typeOfBuyer": buyer_details_type,
                "mainGeneralActivity": buyer_details_general_activity,
                "mainSectoralActivity": buyer_details_sectoral_activity
            }
        }
    }

    json_notice_budget_release_ei = {
        "ocid": cpid,
        "id": cpid + "-" + f"{timestamp}",
        "date": start_date,
        "tag": ["compiled"],
        "initiationType": "tender",
        "tender": {
            "id": "b3f31996-60e4-4871-893d-b4e985573c8c",
            "title": "EI_FULL_WORKS",
            "description": "description of finansical sourse",
            "status": "planning",
            "statusDetails": "empty",
            "mainProcurementCategory": "works",
            "classification": {
                "scheme": "CPV",
                "id": classification_id,
                "description": "Lucrări de pregătire a şantierului"
            }
        },
        "buyer": {
            "id": f"{buyer_identifier_scheme}-{buyer_id}",
            "name": buyer_name
        },
        "parties": [{
            "id": f"{buyer_identifier_scheme}-{buyer_id}",
            "name": buyer_name,
            "identifier": {
                "scheme": buyer_identifier_scheme,
                "id": buyer_id,
                "legalName": buyer_identifier_legal_name,
                "uri": buyer_identifier_uri
            },
            "address": {
                "streetAddress": buyer_address_street,
                "postalCode": buyer_address_postal,
                "addressDetails": {
                    "country": {
                        "scheme": country_scheme,
                        "id": country_id,
                        "description": country_description,
                        "uri": "https://www.iso.org"
                    },
                    "region": {
                        "scheme": region_scheme,
                        "id": region_id,
                        "description": region_description,
                        "uri": "http://statistica.md"
                    },
                    "locality": {
                        "scheme": locality_scheme,
                        "id": locality_id,
                        "description": locality_description,
                        "uri": "http://statistica.md"
                    }
                }
            },
            "additionalIdentifiers": [{
                "scheme": buyer_additional_scheme,
                "id": buyer_additional_id,
                "legalName": buyer_additional_legal,
                "uri": buyer_additional_uri
            }],
            "contactPoint": {
                "name": contact_point_name,
                "email": contact_point_email,
                "telephone": contact_point_telephone,
                "faxNumber": contact_point_fax,
                "url": contact_point_url
            },
            "details": {
                "typeOfBuyer": buyer_details_type,
                "mainGeneralActivity": buyer_details_general_activity,
                "mainSectoralActivity": buyer_details_sectoral_activity
            },
            "roles": ["buyer"]
        }],
        "planning": {
            "budget": {
                "id": classification_id,
                "id": classification_id,
                "period": {
                    "startDate": start_date,
                    "endDate": end_date
                },
                "amount": {
                    "amount": amount,
                    "currency": currency
                }
            },
            "rationale": planning_rationale
        },
        "relatedProcesses": [{
            "id": "a3e8d470-557d-11eb-a1bb-b300e52ae89e",
            "relationship": ["x_fundingSource"],
            "scheme": "ocid",
            "identifier": fs_ocid,
            "uri": f"http://dev.public.eprocurement.systems/budgets/{cpid}/{fs_ocid}"
        }]
    }

    json_notice_budget_compiled_release_ei = {
        "ocid": cpid,
        "id": cpid + "-" + f"{timestamp}",
        "date": start_date,
        "tag": ["compiled"],
        "initiationType": "tender",
        "tender": {
            "id": "b3f31996-60e4-4871-893d-b4e985573c8c",
            "title": "EI_FULL_WORKS",
            "description": "description of finansical sourse",
            "status": "planning",
            "statusDetails": "empty",
            "mainProcurementCategory": "works",
            "classification": {
                "scheme": "CPV",
                "id": classification_id,
                "description": "Lucrări de pregătire a şantierului"
            }
        },
        "buyer": {
            "id": f"{buyer_identifier_scheme}-{buyer_id}",
            "name": buyer_name
        },
        "parties": [{
            "id": f"{buyer_identifier_scheme}-{buyer_id}",
            "name": buyer_name,
            "identifier": {
                "scheme": buyer_identifier_scheme,
                "id": buyer_id,
                "legalName": buyer_identifier_legal_name,
                "uri": buyer_identifier_uri
            },
            "address": {
                "streetAddress": buyer_address_street,
                "postalCode": buyer_address_postal,
                "addressDetails": {
                    "country": {
                        "scheme": country_scheme,
                        "id": country_id,
                        "description": country_description,
                        "uri": "https://www.iso.org"
                    },
                    "region": {
                        "scheme": region_scheme,
                        "id": region_id,
                        "description": region_description,
                        "uri": "http://statistica.md"
                    },
                    "locality": {
                        "scheme": locality_scheme,
                        "id": locality_id,
                        "description": locality_description,
                        "uri": "http://statistica.md"
                    }
                }
            },
            "additionalIdentifiers": [{
                "scheme": buyer_additional_scheme,
                "id": buyer_additional_id,
                "legalName": buyer_additional_legal,
                "uri": buyer_additional_uri
            }],
            "contactPoint": {
                "name": contact_point_name,
                "email": contact_point_email,
                "telephone": contact_point_telephone,
                "faxNumber": contact_point_fax,
                "url": contact_point_url
            },
            "details": {
                "typeOfBuyer": buyer_details_type,
                "mainGeneralActivity": buyer_details_general_activity,
                "mainSectoralActivity": buyer_details_sectoral_activity
            },
            "roles": ["buyer"]
        }],
        "planning": {
            "budget": {
                "id": classification_id,
                "period": {
                    "startDate": start_date,
                    "endDate": end_date
                },
                "amount": {
                    "amount": amount,
                    "currency": currency
                }
            },
            "rationale": planning_rationale
        },
        "relatedProcesses": [{
            "id": "a3e8d470-557d-11eb-a1bb-b300e52ae89e",
            "relationship": ["x_fundingSource"],
            "scheme": "ocid",
            "identifier": fs_ocid,
            "uri": f"http://dev.public.eprocurement.systems/budgets/{cpid}/{fs_ocid}"
        }]
    }

    json_budget_fs = {
        "ocid": fs_ocid,
        "tender": {
            "id": "3c12101f-2059-4240-a805-0f129ed9f6e9",
            "status": status,
            "statusDetails": statusDetails
        },
        "planning": {
            "budget": {
                "id": budget_id,
                "description": budget_description,
                "period": {
                    "startDate": start_date,
                    "endDate": end_date
                },
                "amount": {
                    "amount": amount,
                    "currency": currency
                },
                "europeanUnionFunding": {
                    "projectName": european_project_name,
                    "projectIdentifier": european_project_id,
                    "uri": european_project_uri
                },
                "isEuropeanUnionFunded": is_european_funding,
                "verified": True,
                "sourceEntity": {
                    "id": f"{buyer_identifier_scheme}-{buyer_id}",
                    "name": buyer_name
                },
                "verificationDetails": None,
                "project": project_name,
                "projectID": project_id,
                "uri": project_uri
            },
            "rationale": planning_rationale
        },
        "funder": {
            "id": f"{funder_identifier_scheme}-{funder_id}",
            "name": funder_name,
            "identifier": {
                "id": funder_id,
                "scheme": funder_identifier_scheme,
                "legalName": funder_identifier_legal_name,
                "uri": funder_identifier_legal_uri
            },
            "address": {
                "streetAddress": funder_address_street,
                "postalCode": funder_address_postal,
                "addressDetails": {
                    "country": {
                        "scheme": country_scheme,
                        "id": country_id,
                        "description": country_description,
                        "uri": "https://www.iso.org"
                    },
                    "region": {
                        "scheme": region_scheme,
                        "id": region_id,
                        "description": region_description,
                        "uri": "http://statistica.md"
                    },
                    "locality": {
                        "scheme": locality_scheme,
                        "id": locality_id,
                        "description": locality_description,
                        "uri": "http://statistica.md"
                    }
                }
            },
            "additionalIdentifiers": [{
                "id": funder_additional_id,
                "scheme": funder_additional_scheme,
                "legalName": funder_additional_legal,
                "uri": funder_additional_uri
            }],
            "contactPoint": {
                "name": contact_point_name,
                "email": contact_point_email,
                "telephone": contact_point_telephone,
                "faxNumber": contact_point_fax,
                "url": contact_point_url
            }
        },
        "payer": {
            "id": f"{payer_identifier_scheme}-{payer_id}",
            "name": payer_name,
            "identifier": {
                "id": payer_id,
                "scheme": payer_identifier_scheme,
                "legalName": payer_identifier_legal_name,
                "uri": payer_identifier_legal_uri
            },
            "address": {
                "streetAddress": payer_address_street,
                "postalCode": payer_address_postal,
                "addressDetails": {
                    "country": {
                        "scheme": country_scheme,
                        "id": country_id,
                        "description": country_description,
                        "uri": "https://www.iso.org"
                    },
                    "region": {
                        "scheme": region_scheme,
                        "id": region_id,
                        "description": region_description,
                        "uri": "http://statistica.md"
                    },
                    "locality": {
                        "scheme": locality_scheme,
                        "id": locality_id,
                        "description": locality_description,
                        "uri": "http://statistica.md"
                    }
                }
            },
            "additionalIdentifiers": [{
                "id": payer_additional_id,
                "scheme": payer_additional_scheme,
                "legalName": payer_additional_legal,
                "uri": payer_additional_uri
            }],
            "contactPoint": {
                "name": contact_point_name,
                "email": contact_point_email,
                "telephone": contact_point_telephone,
                "faxNumber": contact_point_fax,
                "url": contact_point_url
            }
        }
    }
    if is_european_funding == False:
        del json_budget_fs["planning"]["budget"]["europeanUnionFunding"]

    json_notice_budget_release_fs = {
        "ocid": fs_ocid,
        "id": fs_ocid + "-" + f"{timestamp}",
        "date": start_date,
        "tag": ["planning"],
        "initiationType": "tender",
        "tender": {
            "id": "3c12101f-2059-4240-a805-0f129ed9f6e9",
            "status": status,
            "statusDetails": statusDetails
        },
        "parties": [{
            "id": f"{funder_identifier_scheme}-{funder_id}",
            "name": funder_name,
            "identifier": {
                "scheme": funder_identifier_scheme,
                "id": funder_id,
                "legalName": funder_identifier_legal_name,
                "uri": funder_identifier_legal_uri
            },
            "address": {
                "streetAddress": funder_address_street,
                "postalCode": funder_address_postal,
                "addressDetails": {
                    "country": {
                        "scheme": country_scheme,
                        "id": country_id,
                        "description": country_description,
                        "uri": "https://www.iso.org"
                    },
                    "region": {
                        "scheme": region_scheme,
                        "id": region_id,
                        "description": region_description,
                        "uri": "http://statistica.md"
                    },
                    "locality": {
                        "scheme": locality_scheme,
                        "id": locality_id,
                        "description": locality_description,
                        "uri": "http://statistica.md"
                    }
                }
            },
            "additionalIdentifiers": [{
                "id": funder_additional_id,
                "scheme": funder_additional_scheme,
                "legalName": funder_additional_legal,
                "uri": funder_additional_uri
            }],
            "contactPoint": {
                "name": contact_point_name,
                "email": contact_point_email,
                "telephone": contact_point_telephone,
                "faxNumber": contact_point_fax,
                "url": contact_point_url
            },
            "roles": ["funder"]
        }, {
            "id": f"{payer_identifier_scheme}-{payer_id}",
            "name": payer_name,
            "identifier": {
                "scheme": payer_identifier_scheme,
                "id": payer_id,
                "legalName": payer_identifier_legal_name,
                "uri": payer_identifier_legal_uri
            },
            "address": {
                "streetAddress": payer_address_street,
                "postalCode": payer_address_postal,
                "addressDetails": {
                    "country": {
                        "scheme": country_scheme,
                        "id": country_id,
                        "description": country_description,
                        "uri": "https://www.iso.org"
                    },
                    "region": {
                        "scheme": region_scheme,
                        "id": region_id,
                        "description": region_description,
                        "uri": "http://statistica.md"
                    },
                    "locality": {
                        "scheme": locality_scheme,
                        "id": locality_id,
                        "description": locality_description,
                        "uri": "http://statistica.md"
                    }
                }
            },
            "additionalIdentifiers": [{
                "id": payer_additional_id,
                "scheme": payer_additional_scheme,
                "legalName": payer_additional_legal,
                "uri": payer_additional_uri
            }],
            "contactPoint": {
                "name": contact_point_name,
                "email": contact_point_email,
                "telephone": contact_point_telephone,
                "faxNumber": contact_point_fax,
                "url": contact_point_url
            },
            "roles": ["payer"]
        }],
        "planning": {
            "budget": {
                "id": "IBAN - 102030",
                "description": budget_description,
                "period": {
                    "startDate": start_date,
                    "endDate": end_date
                },
                "amount": {
                    "amount": amount,
                    "currency": currency
                },
                "europeanUnionFunding": {
                    "projectName": european_project_name,
                    "projectIdentifier": european_project_id,
                    "uri": european_project_uri
                },
                "isEuropeanUnionFunded": is_european_funding,
                "verified": True,
                "sourceEntity": {
                    "id": f"{buyer_identifier_scheme}-{buyer_id}",
                    "name": buyer_name
                },
                "project": project_name,
                "projectID": project_id,
                "uri": project_uri
            },
            "rationale": planning_rationale
        },
        "relatedProcesses": [{
            "id": "a3e85f40-557d-11eb-a1bb-b300e52ae89e",
            "relationship": ["parent"],
            "scheme": "ocid",
            "identifier": cpid,
            "uri": f"http://dev.public.eprocurement.systems/budgets/{cpid}/{cpid}"
        }]
    }
    if is_european_funding == False:
        del json_notice_budget_release_fs["planning"]["budget"]["europeanUnionFunding"]

    json_budget_compiled_release_fs = {
        "ocid": fs_ocid,
        "id": fs_ocid + "-" + f"{timestamp}",
        "date": start_date,
        "tag": ["planning"],
        "initiationType": "tender",
        "tender": {
            "id": "3c12101f-2059-4240-a805-0f129ed9f6e9",
            "status": status,
            "statusDetails": statusDetails
        },
        "parties": [{
            "id": f"{funder_identifier_scheme}-{funder_id}",
            "name": funder_name,
            "identifier": {
                "scheme": funder_identifier_scheme,
                "id": funder_id,
                "legalName": funder_identifier_legal_name,
                "uri": funder_identifier_legal_uri
            },
            "address": {
                "streetAddress": funder_address_street,
                "postalCode": funder_address_postal,
                "addressDetails": {
                    "country": {
                        "scheme": country_scheme,
                        "id": country_id,
                        "description": country_description,
                        "uri": "https://www.iso.org"
                    },
                    "region": {
                        "scheme": region_scheme,
                        "id": region_id,
                        "description": region_description,
                        "uri": "http://statistica.md"
                    },
                    "locality": {
                        "scheme": locality_scheme,
                        "id": locality_id,
                        "description": locality_description,
                        "uri": "http://statistica.md"
                    }
                }
            },
            "additionalIdentifiers": [{
                "id": funder_additional_id,
                "scheme": funder_additional_scheme,
                "legalName": funder_additional_legal,
                "uri": funder_additional_uri
            }],
            "contactPoint": {
                "name": contact_point_name,
                "email": contact_point_email,
                "telephone": contact_point_telephone,
                "faxNumber": contact_point_fax,
                "url": contact_point_url
            },
            "roles": ["funder"]
        }, {
            "id": f"{payer_identifier_scheme}-{payer_id}",
            "name": payer_name,
            "identifier": {
                "scheme": payer_identifier_scheme,
                "id": payer_id,
                "legalName": payer_identifier_legal_name,
                "uri": payer_identifier_legal_uri
            },
            "address": {
                "streetAddress": payer_address_street,
                "postalCode": payer_address_postal,
                "addressDetails": {
                    "country": {
                        "scheme": country_scheme,
                        "id": country_id,
                        "description": country_description,
                        "uri": "https://www.iso.org"
                    },
                    "region": {
                        "scheme": region_scheme,
                        "id": region_id,
                        "description": region_description,
                        "uri": "http://statistica.md"
                    },
                    "locality": {
                        "scheme": locality_scheme,
                        "id": locality_id,
                        "description": locality_description,
                        "uri": "http://statistica.md"
                    }
                }
            },
            "additionalIdentifiers": [{
                "id": payer_additional_id,
                "scheme": payer_additional_scheme,
                "legalName": payer_additional_legal,
                "uri": payer_additional_uri
            }],
            "contactPoint": {
                "name": contact_point_name,
                "email": contact_point_email,
                "telephone": contact_point_telephone,
                "faxNumber": contact_point_fax,
                "url": contact_point_url
            },
            "roles": ["payer"]
        }],
        "planning": {
            "budget": {
                "id": "IBAN - 102030",
                "description": budget_description,
                "period": {
                    "startDate": start_date,
                    "endDate": end_date
                },
                "amount": {
                    "amount": amount,
                    "currency": currency
                },
                "europeanUnionFunding": {
                    "projectName": european_project_name,
                    "projectIdentifier": european_project_id,
                    "uri": european_project_uri
                },
                "isEuropeanUnionFunded": is_european_funding,
                "verified": True,
                "sourceEntity": {
                    "id": f"{buyer_identifier_scheme}-{buyer_id}",
                    "name": buyer_name
                },
                "project": project_name,
                "projectID": project_id,
                "uri": project_uri
            },
            "rationale": planning_rationale
        },
        "relatedProcesses": [{
            "id": "a3e85f40-557d-11eb-a1bb-b300e52ae89e",
            "relationship": ["parent"],
            "scheme": "ocid",
            "identifier": cpid,
            "uri": f"http://dev.public.eprocurement.systems/budgets/{cpid}/{cpid}"
        }]
    }
    if is_european_funding == False:
        del json_budget_compiled_release_fs["planning"]["budget"]["europeanUnionFunding"]
    session.execute(f"INSERT INTO notice_budget_release ("
                    f"cp_id,oc_id,release_id,json_data,release_date,stage) VALUES("
                    f"'{cpid}','{cpid}','{cpid + '1609927348000'}',"
                    f"'{json.dumps(json_notice_budget_release_ei)}',1609943491271,'EI');").one()

    session.execute(f"INSERT INTO notice_budget_compiled_release ("
                    f"cp_id,oc_id,amount,json_data,publish_date,release_date,"
                    f"release_id,stage) VALUES('{cpid}','{cpid}', 0.0, "
                    f"'{json.dumps(json_notice_budget_compiled_release_ei)}',"
                    f"1609943491271,1609943491271,'{cpid + '-' + f'{timestamp}'}',"
                    f"'EI');").one()

    session.execute(f"INSERT INTO budget_ei (cp_id,token_entity,created_date,json_data,owner) VALUES("
                    f"'{cpid}',{ei_token},1609927348000,'{json.dumps(json_budget_ei)}','{owner}');").one()

    session.execute(f"INSERT INTO orchestrator_context (cp_id,context) VALUES ("
                    f"'{cpid}','{json.dumps(json_orchestrator_context)}');").one()

    session.execute(
        f"INSERT INTO budget_fs (cp_id,token_entity,amount,amount_reserved,created_date,json_data,oc_id,owner) VALUES ("
        f"'{cpid}',{fs_token},2000.00,0,{timestamp},'{json.dumps(json_budget_fs)}','{fs_ocid}','{owner}');").one()

    session.execute(f"INSERT INTO notice_budget_offset (cp_id,release_date) "
                    f"VALUES ('{cpid}',{timestamp});").one()

    session.execute(
        f"INSERT INTO notice_budget_release (cp_id,oc_id,release_id,json_data,release_date,stage) "
        f"VALUES ('{cpid}','{fs_ocid}','{fs_ocid + '-' + str(timestamp)}','{json.dumps(json_notice_budget_release_fs)}',"
        f"1610212505151,'FS');").one()

    session.execute(
        f"INSERT INTO notice_budget_compiled_release (cp_id,oc_id,amount,json_data,publish_date,release_date,"
        f"release_id,stage) VALUES ('{cpid}','{fs_ocid}',8000.00,'{json.dumps(json_budget_compiled_release_fs)}',"
        f"{timestamp},"
        f"{timestamp},'{fs_ocid + '-' + str(timestamp)}','FS');")

    return f"http://dev.public.eprocurement.systems/budgets/{cpid}/{fs_ocid}", fs_token, fs_ocid, start_date, \
           end_date, timestamp


def insert_into_db_update_fs(cpid):
    auth_provider = PlainTextAuthProvider(username=username, password=password)
    cluster = Cluster([host], auth_provider=auth_provider)
    session = cluster.connect('ocds')
    fs_token = uuid4()
    ei_token = uuid4()
    owner = "445f6851-c908-407d-9b45-14b92f3e964b"

    period = get_period()
    date = datetime.datetime.now()
    # time_at_now = date.strftime('%Y-%m-%dT%H:%M:%SZ')
    # time_at_now_miliseconds = date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    # timestamp = int(
    #     time.mktime(datetime.datetime.strptime(time_at_now_miliseconds, "%Y-%m-%dT%H:%M:%S.%fZ").timetuple())) * 1000
    fs_ocid = prepared_fs_ocid(cpid)

    json_orchestrator_context = {
        "operationId": f"{uuid4()}",
        "requestId": f"{uuid4()}",
        "cpid": cpid,
        "ocid": fs_ocid,
        "stage": "FS",
        "processType": "fs",
        "operationType": "updateFS",
        "owner": "445f6851-c908-407d-9b45-14b92f3e964b",
        "country": "MD",
        "language": "ro",
        "token": f"{fs_token}",
        "startDate": period[0],
        "timeStamp": period[2],
        "isAuction": False
    }

    json_budget_ei = {
        "ocid": cpid,
        "tender": {
            "id": "72695c4a-9026-4ad9-a191-eb75f0698333",
            "title": "EI_FULL_WORKS",
            "description": "description of finansical sourse",
            "status": "planning",
            "statusDetails": "empty",
            "classification": {
                "id": "45100000-8",
                "scheme": "CPV",
                "description": "Lucrări de pregătire a şantierului"
            },
            "mainProcurementCategory": "works"
        },
        "planning": {
            "budget": {
                "id": "45100000-8",
                "period": {
                    "startDate": period[0],
                    "endDate": period[1]
                },
                "amount": {
                    "amount": 24.00,
                    "currency": "EUR"
                }
            },
            "rationale": "planning.rationale"
        },
        "buyer": {
            "id": "MD-IDNO-1",
            "name": "LLC Petrusenko",
            "identifier": {
                "id": "1",
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
                        "description": "Moldova, Republica",
                        "uri": "https://www.iso.org"
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
        "ocid": cpid,
        "id": cpid + "-" + f"{period[2]}",
        "date": period[0],
        "tag": ["compiled"],
        "initiationType": "tender",
        "tender": {
            "id": "72695c4a-9026-4ad9-a191-eb75f0698333",
            "title": "EI_FULL_WORKS",
            "description": "description of finansical sourse",
            "status": "planning",
            "statusDetails": "empty",
            "mainProcurementCategory": "works",
            "classification": {
                "scheme": "CPV",
                "id": "45100000-8",
                "description": "Lucrări de pregătire a şantierului"
            }
        },
        "buyer": {
            "id": "MD-IDNO-1",
            "name": "LLC Petrusenko"
        },
        "parties": [{
            "id": "MD-IDNO-1",
            "name": "LLC Petrusenko",
            "identifier": {
                "scheme": "MD-IDNO",
                "id": "1",
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
                        "description": "Moldova, Republica",
                        "uri": "https://www.iso.org"
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
                    "startDate": period[0],
                    "endDate": period[1]
                },
                "amount": {
                    "amount": 24.00,
                    "currency": "EUR"
                }
            },
            "rationale": "planning.rationale"
        },
        "relatedProcesses": [{
            "id": "d0d7c580-5592-11eb-a1bb-b300e52ae89e",
            "relationship": ["x_fundingSource"],
            "scheme": "ocid",
            "identifier": fs_ocid,
            "uri": f"http://dev.public.eprocurement.systems/budgets/{cpid}/{fs_ocid}"
        }]
    }

    json_notice_budget_compiled_release_ei = {
        "ocid": cpid,
        "id": cpid + "-" + f"{period[2]}",
        "date": period[0],
        "tag": ["compiled"],
        "initiationType": "tender",
        "tender": {
            "id": "72695c4a-9026-4ad9-a191-eb75f0698333",
            "title": "EI_FULL_WORKS",
            "description": "description of finansical sourse",
            "status": "planning",
            "statusDetails": "empty",
            "mainProcurementCategory": "works",
            "classification": {
                "scheme": "CPV",
                "id": "45100000-8",
                "description": "Lucrări de pregătire a şantierului"
            }
        },
        "buyer": {
            "id": "MD-IDNO-1",
            "name": "LLC Petrusenko"
        },
        "parties": [{
            "id": "MD-IDNO-1",
            "name": "LLC Petrusenko",
            "identifier": {
                "scheme": "MD-IDNO",
                "id": "1",
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
                        "description": "Moldova, Republica",
                        "uri": "https://www.iso.org"
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
                    "startDate": period[0],
                    "endDate": period[1]
                },
                "amount": {
                    "amount": 24.00,
                    "currency": "EUR"
                }
            },
            "rationale": "planning.rationale"
        },
        "relatedProcesses": [{
            "id": "d0d7c580-5592-11eb-a1bb-b300e52ae89e",
            "relationship": ["x_fundingSource"],
            "scheme": "ocid",
            "identifier": fs_ocid,
            "uri": f"http://dev.public.eprocurement.systems/budgets/{cpid}/{fs_ocid}"
        }]
    }

    json_budget_fs = {
        "ocid": fs_ocid,
        "tender": {
            "id": "4e1db367-c823-4f2c-89b1-207acedcd8f3",
            "status": "active",
            "statusDetails": "empty"
        },
        "planning": {
            "budget": {
                "id": "IBAN - 102030",
                "description": "updated value",
                "period": {
                    "startDate": period[0],
                    "endDate": period[1]
                },
                "amount": {
                    "amount": 24.00,
                    "currency": "EUR"
                },
                "europeanUnionFunding": {
                    "projectName": "updated valuet",
                    "projectIdentifier": "updated value",
                    "uri": "updated value"
                },
                "isEuropeanUnionFunded": True,
                "verified": True,
                "sourceEntity": {
                    "id": "MD-IDNO-3",
                    "name": "buyer name"
                },
                "verificationDetails": None,
                "project": "updated value",
                "projectID": "updated value",
                "uri": "updated value"
            },
            "rationale": "updated value"
        },
        "funder": {
            "id": "MD-IDNO-3",
            "name": "buyer name",
            "identifier": {
                "id": "3",
                "scheme": "MD-IDNO",
                "legalName": "legal Name",
                "uri": "http://buyer.com"
            },
            "address": {
                "streetAddress": "street address of buyer",
                "postalCode": "02054",
                "addressDetails": {
                    "country": {
                        "scheme": "iso-alpha2",
                        "id": "MD",
                        "description": "Moldova, Republica",
                        "uri": "https://www.iso.org"
                    },
                    "region": {
                        "scheme": "CUATM",
                        "id": "3400000",
                        "description": "Donduşeni",
                        "uri": "http://statistica.md"
                    },
                    "locality": {
                        "scheme": "CUATM",
                        "id": "3401000",
                        "description": "or.Donduşeni (r-l Donduşeni)",
                        "uri": "http://statistica.md"
                    }
                }
            },
            "additionalIdentifiers": [{
                "id": "additional identifier",
                "scheme": "scheme",
                "legalName": "legal name",
                "uri": "http://addtIdent.com"
            }],
            "contactPoint": {
                "name": "contact point of buyer",
                "email": "email.com",
                "telephone": "32-22-23",
                "faxNumber": "12-22-21",
                "url": "http://url.com"
            }
        },
        "payer": {
            "id": "MD-IDNO-2",
            "name": "Procuring Entity Name",
            "identifier": {
                "id": "2",
                "scheme": "MD-IDNO",
                "legalName": "Legal Name",
                "uri": "http://454.to"
            },
            "address": {
                "streetAddress": "street",
                "postalCode": "785412",
                "addressDetails": {
                    "country": {
                        "scheme": "iso-alpha2",
                        "id": "MD",
                        "description": "Moldova, Republica",
                        "uri": "https://www.iso.org"
                    },
                    "region": {
                        "scheme": "CUATM",
                        "id": "3400000",
                        "description": "Donduşeni",
                        "uri": "http://statistica.md"
                    },
                    "locality": {
                        "scheme": "CUATM",
                        "id": "3401000",
                        "description": "or.Donduşeni (r-l Donduşeni)",
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
                "name": "contact person",
                "email": "string@mail.ccc",
                "telephone": "98-79-87",
                "faxNumber": "78-56-55",
                "url": "http://url.com"
            }
        }
    }

    json_notice_budget_release_fs = {
        "ocid": fs_ocid,
        "id": fs_ocid + "-" + f"{period[2]}",
        "date": period[0],
        "tag": ["planning"],
        "initiationType": "tender",
        "tender": {
            "id": "4e1db367-c823-4f2c-89b1-207acedcd8f3",
            "status": "active",
            "statusDetails": "empty"
        },
        "parties": [{
            "id": "MD-IDNO-3",
            "name": "buyer name",
            "identifier": {
                "scheme": "MD-IDNO",
                "id": "3",
                "legalName": "legal Name",
                "uri": "http://buyer.com"
            },
            "address": {
                "streetAddress": "street address of buyer",
                "postalCode": "02054",
                "addressDetails": {
                    "country": {
                        "scheme": "iso-alpha2",
                        "id": "MD",
                        "description": "Moldova, Republica",
                        "uri": "https://www.iso.org"
                    },
                    "region": {
                        "scheme": "CUATM",
                        "id": "3400000",
                        "description": "Donduşeni",
                        "uri": "http://statistica.md"
                    },
                    "locality": {
                        "scheme": "CUATM",
                        "id": "3401000",
                        "description": "or.Donduşeni (r-l Donduşeni)",
                        "uri": "http://statistica.md"
                    }
                }
            },
            "additionalIdentifiers": [{
                "scheme": "scheme",
                "id": "additional identifier",
                "legalName": "legal name",
                "uri": "http://addtIdent.com"
            }],
            "contactPoint": {
                "name": "contact point of buyer",
                "email": "email.com",
                "telephone": "32-22-23",
                "faxNumber": "12-22-21",
                "url": "http://url.com"
            },
            "roles": ["funder"]
        }, {
            "id": "MD-IDNO-2",
            "name": "Procuring Entity Name",
            "identifier": {
                "scheme": "MD-IDNO",
                "id": "2",
                "legalName": "Legal Name",
                "uri": "http://454.to"
            },
            "address": {
                "streetAddress": "street",
                "postalCode": "785412",
                "addressDetails": {
                    "country": {
                        "scheme": "iso-alpha2",
                        "id": "MD",
                        "description": "Moldova, Republica",
                        "uri": "https://www.iso.org"
                    },
                    "region": {
                        "scheme": "CUATM",
                        "id": "3400000",
                        "description": "Donduşeni",
                        "uri": "http://statistica.md"
                    },
                    "locality": {
                        "scheme": "CUATM",
                        "id": "3401000",
                        "description": "or.Donduşeni (r-l Donduşeni)",
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
                "name": "contact person",
                "email": "string@mail.ccc",
                "telephone": "98-79-87",
                "faxNumber": "78-56-55",
                "url": "http://url.com"
            },
            "roles": ["payer"]
        }],
        "planning": {
            "budget": {
                "id": "IBAN - 102030",
                "description": "updated value",
                "period": {
                    "startDate": period[1],
                    "endDate": period[1]
                },
                "amount": {
                    "amount": 24.00,
                    "currency": "EUR"
                },
                "europeanUnionFunding": {
                    "projectIdentifier": "updated value",
                    "projectName": "updated valuet",
                    "uri": "updated value"
                },
                "isEuropeanUnionFunded": True,
                "verified": True,
                "sourceEntity": {
                    "id": "MD-IDNO-3",
                    "name": "buyer name"
                },
                "project": "updated value",
                "projectID": "updated value",
                "uri": "updated value"
            },
            "rationale": "updated value"
        },
        "relatedProcesses": [{
            "id": "d0d77760-5592-11eb-a1bb-b300e52ae89e",
            "relationship": ["parent"],
            "scheme": "ocid",
            "identifier": cpid,
            "uri": f"http://dev.public.eprocurement.systems/budgets/{cpid}/{cpid}"
        }]
    }

    json_budget_compiled_release_fs = {
        "ocid": fs_ocid,
        "id": fs_ocid + "-" + f"{period[2]}",
        "date": period[0],
        "tag": ["planning"],
        "initiationType": "tender",
        "tender": {
            "id": "4e1db367-c823-4f2c-89b1-207acedcd8f3",
            "status": "active",
            "statusDetails": "empty"
        },
        "parties": [{
            "id": "MD-IDNO-3",
            "name": "buyer name",
            "identifier": {
                "scheme": "MD-IDNO",
                "id": "3",
                "legalName": "legal Name",
                "uri": "http://buyer.com"
            },
            "address": {
                "streetAddress": "street address of buyer",
                "postalCode": "02054",
                "addressDetails": {
                    "country": {
                        "scheme": "iso-alpha2",
                        "id": "MD",
                        "description": "Moldova, Republica",
                        "uri": "https://www.iso.org"
                    },
                    "region": {
                        "scheme": "CUATM",
                        "id": "3400000",
                        "description": "Donduşeni",
                        "uri": "http://statistica.md"
                    },
                    "locality": {
                        "scheme": "CUATM",
                        "id": "3401000",
                        "description": "or.Donduşeni (r-l Donduşeni)",
                        "uri": "http://statistica.md"
                    }
                }
            },
            "additionalIdentifiers": [{
                "scheme": "scheme",
                "id": "additional identifier",
                "legalName": "legal name",
                "uri": "http://addtIdent.com"
            }],
            "contactPoint": {
                "name": "contact point of buyer",
                "email": "email.com",
                "telephone": "32-22-23",
                "faxNumber": "12-22-21",
                "url": "http://url.com"
            },
            "roles": ["funder"]
        }, {
            "id": "MD-IDNO-2",
            "name": "Procuring Entity Name",
            "identifier": {
                "scheme": "MD-IDNO",
                "id": "2",
                "legalName": "Legal Name",
                "uri": "http://454.to"
            },
            "address": {
                "streetAddress": "street",
                "postalCode": "785412",
                "addressDetails": {
                    "country": {
                        "scheme": "iso-alpha2",
                        "id": "MD",
                        "description": "Moldova, Republica",
                        "uri": "https://www.iso.org"
                    },
                    "region": {
                        "scheme": "CUATM",
                        "id": "3400000",
                        "description": "Donduşeni",
                        "uri": "http://statistica.md"
                    },
                    "locality": {
                        "scheme": "CUATM",
                        "id": "3401000",
                        "description": "or.Donduşeni (r-l Donduşeni)",
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
                "name": "contact person",
                "email": "string@mail.ccc",
                "telephone": "98-79-87",
                "faxNumber": "78-56-55",
                "url": "http://url.com"
            },
            "roles": ["payer"]
        }],
        "planning": {
            "budget": {
                "id": "IBAN - 102030",
                "description": "updated value",
                "period": {
                    "startDate": period[0],
                    "endDate": period[1]
                },
                "amount": {
                    "amount": 24.00,
                    "currency": "EUR"
                },
                "europeanUnionFunding": {
                    "projectIdentifier": "updated value",
                    "projectName": "updated valuet",
                    "uri": "updated value"
                },
                "isEuropeanUnionFunded": True,
                "verified": True,
                "sourceEntity": {
                    "id": "MD-IDNO-3",
                    "name": "buyer name"
                },
                "project": "updated value",
                "projectID": "updated value",
                "uri": "updated value"
            },
            "rationale": "updated value"
        },
        "relatedProcesses": [{
            "id": "d0d77760-5592-11eb-a1bb-b300e52ae89e",
            "relationship": ["parent"],
            "scheme": "ocid",
            "identifier": cpid,
            "uri": f"http://dev.public.eprocurement.systems/budgets/{cpid}/{cpid}"
        }]
    }

    session.execute(f"INSERT INTO notice_budget_release ("
                    f"cp_id,oc_id,release_id,json_data,release_date,stage) VALUES("
                    f"'{cpid}','{cpid}','{cpid + '1609927348000'}',"
                    f"'{json.dumps(json_notice_budget_release_ei)}',1609943491271,'EI');").one()

    session.execute(f"INSERT INTO notice_budget_compiled_release ("
                    f"cp_id,oc_id,amount,json_data,publish_date,release_date,"
                    f"release_id,stage) VALUES('{cpid}','{cpid}', 0.0, "
                    f"'{json.dumps(json_notice_budget_compiled_release_ei)}',"
                    f"1609943491271,1609943491271,'{cpid + '-' + f'{period[2]}'}',"
                    f"'EI');").one()

    session.execute(f"INSERT INTO budget_ei (cp_id,token_entity,created_date,json_data,owner) VALUES("
                    f"'{cpid}',{ei_token},1609927348000,'{json.dumps(json_budget_ei)}','{owner}');").one()

    session.execute(f"INSERT INTO orchestrator_context (cp_id,context) VALUES ("
                    f"'{cpid}','{json.dumps(json_orchestrator_context)}');").one()

    session.execute(
        f"INSERT INTO budget_fs (cp_id,token_entity,amount,amount_reserved,created_date,json_data,oc_id,owner) "
        f"VALUES ('{cpid}',{fs_token},8000.00,0,{period[2]},'{json.dumps(json_budget_fs)}','{fs_ocid}',"
        f"'{owner}');").one()

    session.execute(f"INSERT INTO notice_budget_offset (cp_id,release_date) "
                    f"VALUES ('{cpid}',{period[2]});").one()

    session.execute(
        f"INSERT INTO notice_budget_release (cp_id,oc_id,release_id,json_data,release_date,stage) "
        f"VALUES ('{cpid}','{fs_ocid}','{fs_ocid + '-' + str(period[2])}',"
        f"'{json.dumps(json_notice_budget_release_fs)}',"
        f"1610212505151,'FS');").one()

    session.execute(
        f"INSERT INTO notice_budget_compiled_release (cp_id,oc_id,amount,json_data,publish_date,release_date,"
        f"release_id,stage) VALUES ('{cpid}','{fs_ocid}',8000.00,'{json.dumps(json_budget_compiled_release_fs)}',"
        f"{period[2]},"
        f"{period[2]},'{fs_ocid + '-' + str(period[2])}','FS');")

    return f"http://dev.public.eprocurement.systems/budgets/{cpid}/{fs_ocid}", fs_token, fs_ocid


def insert_into_db_create_pn_full_data_model(cpid, ei_id, additional_value, start_date=get_period()[0],
                                             end_date=get_period()[1], tender_period=get_contract_period()[2],
                                             contract_start=get_contract_period()[0],
                                             contract_end=get_contract_period()[1],
                                             timestamp=get_timestamp_from_human_date(get_period()[0]), language="ro",
                                             country="MD", is_european_funding=True,
                                             european_project_name="test eropean name",
                                             european_project_id="test european id",
                                             european_project_uri="european uri", amount=2000.00, currency="EUR",
                                             lot_1_amount=1500.00, lot_2_amount=150.00,
                                             classification_id="45100000-8", main_procurement_category="works",
                                             buyer_identifier_scheme="MD-IDNO", buyer_id="1",
                                             payer_identifier_scheme="MD-IDNO", buyer_name="LLC Dmitro",
                                             procuring_entity_identifier_scheme="MD-IDNO", procuring_entity_id="2",
                                             procuring_entity_name="LLC Petrovich",
                                             procuring_entity_additional_id="id of additional",
                                             procuring_entity_additional_scheme="scheme of additional",
                                             procuring_entity_additional_legal="legal of additional",
                                             procuring_entity_additional_uri="uri of additional",
                                             procuring_entity_address_street="street",
                                             procuring_entity_address_postal="35365", country_id="MD",
                                             country_scheme="iso-alpha2", region_scheme="CUATM", region_id="3400000",
                                             region_description="Donduşeni", locality_scheme="CUATM",
                                             locality_id="3401000", locality_description="or.Donduşeni (r-l Donduşeni)",
                                             country_description="Moldova, Republica",
                                             country_uri="https://www.iso.org",
                                             region_uri="http://statistica.md", locality_uri="http://statistica.md",
                                             contact_point_name="Petrusenko Svitlana",
                                             contact_point_email="svetik@gmail.com",
                                             contact_point_telephone="888999666", contact_point_fax="5552233",
                                             contact_point_url="http://petrusenko.com/svetlana",
                                             lot_1_status="planning", lot_1_status_details="empty",
                                             lot_2_status="planning", lot_2_status_details="empty",
                                             lot_1_place_performance_address_street="Timoshenko",
                                             lot_1_place_performance_address_postal="02232",
                                             lot_1_place_performance_country_scheme="iso-alpha2",
                                             lot_1_place_performance_country_id="MD",
                                             lot_1_place_performance_country_description="Moldova, Republica",
                                             lot_1_place_performance_country_uri="https://www.iso.org",
                                             lot_1_place_performance_region_scheme="CUATM",
                                             lot_1_place_performance_region_id="3400000",
                                             lot_1_place_performance_region_description="Donduşeni",
                                             lot_1_place_performance_region_uri="http://statistica.md",
                                             lot_1_place_performance_locality_scheme="CUATM",
                                             lot_1_place_performance_locality_id="3401000",
                                             lot_1_place_performance_locality_description="or.Donduşeni (r-l Donduşeni)",
                                             lot_1_place_performance_locality_uri="http://statistica.md",
                                             lot_2_place_performance_address_street="Timoshenko",
                                             lot_2_place_performance_address_postal="02232",
                                             lot_2_place_performance_country_scheme="iso-alpha2",
                                             lot_2_place_performance_country_id="MD",
                                             lot_2_place_performance_country_description="Moldova, Republica",
                                             lot_2_place_performance_country_uri="https://www.iso.org",
                                             lot_2_place_performance_region_scheme="CUATM",
                                             lot_2_place_performance_region_id="3400000",
                                             lot_2_place_performance_region_description="Donduşeni",
                                             lot_2_place_performance_region_uri="http://statistica.md",
                                             lot_2_place_performance_locality_scheme="CUATM",
                                             lot_2_place_performance_locality_id="3401000",
                                             lot_2_place_performance_locality_description="or.Donduşeni (r-l Donduşeni)",
                                             lot_2_place_performance_locality_uri="http://statistica.md",
                                             item_1_classification_id="45112350-3",
                                             item_2_classification_id="45112360-6", payer_id="2",
                                             funder_id="3", funder_identifier_scheme="MD-IDNO",
                                             tender_status="planning", tender_status_details_pn="planning",
                                             tender_status_details_ms="planning notice"):
    auth_provider = PlainTextAuthProvider(username=username, password=password)
    cluster = Cluster([host], auth_provider=auth_provider)
    session = cluster.connect('ocds')
    pn_token = uuid4()
    owner = "445f6851-c908-407d-9b45-14b92f3e964b"
    pn_ocid = prepared_pn_ocid(cpid)
    lot_1 = f"{uuid4()}"
    lot_2 = f"{uuid4()}"
    item_1 = f"{uuid4()}"
    item_2 = f"{uuid4()}"
    fs_ocid = prepared_fs_ocid(ei_id)
    period = get_period()

    json_orchestrator_context = {
        "operationId": f"{uuid4()}",
        "requestId": f"{uuid4()}",
        "cpid": cpid,
        "ocid": pn_ocid,
        "stage": "PN",
        "processType": "createPN",
        "operationType": "createPN",
        "phase": "planning",
        "owner": owner,
        "country": country,
        "language": language,
        "pmd": additional_value,
        "token": f"{pn_token}",
        "startDate": start_date,
        "timeStamp": timestamp,
        "isAuction": False,
        "testMode": False
    }

    session.execute(f"INSERT INTO orchestrator_context (cp_id,context) VALUES ("
                    f"'{cpid}','{json.dumps(json_orchestrator_context)}');").one()

    json_access_tender = {
        "ocid": cpid,
        "planning": {
            "rationale": "reason for budget",
            "budget": {
                "description": "description of budget",
                "amount": {
                    "amount": amount,
                    "currency": currency
                },
                "isEuropeanUnionFunded": is_european_funding,
                "budgetBreakdown": [{
                    "id": fs_ocid,
                    "amount": {
                        "amount": amount,
                        "currency": currency
                    },
                    "period": {
                        "startDate": start_date,
                        "endDate": end_date
                    },
                    "sourceParty": {
                        "id": f"{buyer_identifier_scheme}-{buyer_id}",
                        "name": buyer_name
                    },
                    "europeanUnionFunding": {
                        "projectName": european_project_name,
                        "projectIdentifier": european_project_id,
                        "uri": european_project_uri
                    }
                }]
            }
        },
        "tender": {
            "id": "d4419c10-de2f-4a81-9e30-424eb3611b25",
            "status": tender_status,
            "statusDetails": tender_status_details_pn,
            "title": "title of tender",
            "description": "desription of tender",
            "classification": {
                "scheme": "CPV",
                "id": classification_id,
                "description": "Lucrări de rambleiere şi de asanare a terenului"
            },
            "mainProcurementCategory": main_procurement_category,
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
            "legalBasis": "REGULATION_966_2012",
            "procurementMethod": "open",
            "procurementMethodDetails": "testOpenTender",
            "procurementMethodRationale": "procurementMethodRationale",
            "procurementMethodAdditionalInfo": "procurementMethodAdditionalInfo",
            "eligibilityCriteria": "Regulile generale privind naționalitatea și originea, precum și alte criterii de "
                                   "eligibilitate sunt enumerate în Ghidul practic privind procedurile de contractare "
                                   "a acțiunilor externe ale UE (PRAG)",
            "tenderPeriod": {
                "startDate": tender_period
            },
            "contractPeriod": {
                "startDate": contract_start,
                "endDate": contract_end
            },
            "procuringEntity": {
                "id": f"{procuring_entity_identifier_scheme}-{procuring_entity_id}",
                "name": procuring_entity_name,
                "identifier": {
                    "scheme": procuring_entity_identifier_scheme,
                    "id": procuring_entity_id,
                    "legalName": procuring_entity_name,
                    "uri": "uri"
                },
                "additionalIdentifiers": [{
                    "scheme": procuring_entity_additional_scheme,
                    "id": procuring_entity_additional_id,
                    "legalName": procuring_entity_additional_legal,
                    "uri": procuring_entity_additional_uri
                }],
                "address": {
                    "streetAddress": procuring_entity_address_street,
                    "postalCode": procuring_entity_address_postal,
                    "addressDetails": {
                        "country": {
                            "scheme": country_scheme,
                            "id": country_id,
                            "description": country_description,
                            "uri": country_uri
                        },
                        "region": {
                            "scheme": region_scheme,
                            "id": region_id,
                            "description": region_description,
                            "uri": region_uri
                        },
                        "locality": {
                            "scheme": locality_scheme,
                            "id": locality_id,
                            "description": locality_description,
                            "uri": locality_uri
                        }
                    }
                },
                "contactPoint": {
                    "name": contact_point_name,
                    "email": contact_point_email,
                    "telephone": contact_point_telephone,
                    "faxNumber": contact_point_fax,
                    "url": contact_point_url
                }
            },
            "value": {
                "amount": lot_1_amount + lot_2_amount,
                "currency": currency
            },
            "lotGroups": [{
                "optionToCombine": False
            }],
            "lots": [{
                "id": lot_1,
                "internalId": "lot 1",
                "title": "title",
                "description": "description",
                "status": lot_1_status,
                "statusDetails": lot_1_status_details,
                "value": {
                    "amount": lot_1_amount,
                    "currency": currency
                },
                "options": [{
                    "hasOptions": False
                }],
                "variants": [{
                    "hasVariants": False
                }],
                "renewals": [{
                    "hasRenewals": False
                }],
                "recurrentProcurement": [{
                    "isRecurrent": False
                }],
                "contractPeriod": {
                    "startDate": contract_start,
                    "endDate": contract_end
                },
                "placeOfPerformance": {
                    "address": {
                        "streetAddress": lot_1_place_performance_address_street,
                        "postalCode": lot_1_place_performance_address_postal,
                        "addressDetails": {
                            "country": {
                                "scheme": lot_1_place_performance_country_scheme,
                                "id": lot_1_place_performance_country_id,
                                "description": lot_1_place_performance_country_description,
                                "uri": lot_1_place_performance_country_uri
                            },
                            "region": {
                                "scheme": lot_1_place_performance_region_scheme,
                                "id": lot_1_place_performance_region_id,
                                "description": lot_1_place_performance_region_description,
                                "uri": lot_1_place_performance_region_uri
                            },
                            "locality": {
                                "scheme": lot_1_place_performance_locality_scheme,
                                "id": lot_1_place_performance_locality_id,
                                "description": lot_1_place_performance_locality_description,
                                "uri": lot_1_place_performance_locality_uri
                            }
                        }
                    },
                    "description": "description of lot"
                }
            }, {
                "id": lot_2,
                "internalId": "lot 2",
                "title": "title",
                "description": "description",
                "status": lot_2_status,
                "statusDetails": lot_2_status_details,
                "value": {
                    "amount": lot_2_amount,
                    "currency": currency
                },
                "options": [{
                    "hasOptions": False
                }],
                "variants": [{
                    "hasVariants": False
                }],
                "renewals": [{
                    "hasRenewals": False
                }],
                "recurrentProcurement": [{
                    "isRecurrent": False
                }],
                "contractPeriod": {
                    "startDate": contract_start,
                    "endDate": contract_end
                },
                "placeOfPerformance": {
                    "address": {
                        "streetAddress": lot_2_place_performance_address_street,
                        "postalCode": lot_2_place_performance_address_postal,
                        "addressDetails": {
                            "country": {
                                "scheme": lot_2_place_performance_country_scheme,
                                "id": lot_2_place_performance_country_id,
                                "description": lot_2_place_performance_country_description,
                                "uri": lot_2_place_performance_country_uri
                            },
                            "region": {
                                "scheme": lot_2_place_performance_region_scheme,
                                "id": lot_2_place_performance_region_id,
                                "description": lot_2_place_performance_region_description,
                                "uri": lot_2_place_performance_region_uri
                            },
                            "locality": {
                                "scheme": lot_2_place_performance_locality_scheme,
                                "id": lot_2_place_performance_locality_id,
                                "description": lot_2_place_performance_locality_description,
                                "uri": lot_2_place_performance_locality_uri
                            }
                        }
                    },
                    "description": "description of lot"
                }
            }],
            "items": [{
                "id": item_1,
                "internalId": "item 1",
                "classification": {
                    "scheme": "CPV",
                    "id": item_1_classification_id,
                    "description": "Lucrări de valorificare a terenurilor virane"
                },
                "additionalClassifications": [{
                    "scheme": "CPVS",
                    "id": "AA12-4",
                    "description": "Oţel carbon"
                }],
                "quantity": 0.010,
                "unit": {
                    "id": "10",
                    "name": "Parsec"
                },
                "description": "description",
                "relatedLot": lot_1
            }, {
                "id": item_2,
                "internalId": "item 2",
                "classification": {
                    "scheme": "CPV",
                    "id": item_2_classification_id,
                    "description": "Lucrări de reabilitare a terenului"
                },
                "additionalClassifications": [{
                    "scheme": "CPVS",
                    "id": "AA12-4",
                    "description": "Oţel carbon"
                }],
                "quantity": 0.010,
                "unit": {
                    "id": "10",
                    "name": "Parsec"
                },
                "description": "description",
                "relatedLot": lot_2
            }],
            "requiresElectronicCatalogue": False,
            "submissionMethod": ["electronicSubmission"],
            "submissionMethodRationale": [
                "Ofertele vor fi primite prin intermediul unei platforme electronice de achiziții publice"],
            "submissionMethodDetails": "Lista platformelor: achizitii, ebs, licitatie, yptender",
            "documents": [{
                "id": document_1[0][0],
                "documentType": "contractArrangements",
                "title": "title of document",
                "description": "descrition of document",
                "relatedLots": [f"{lot_1}"]
            }, {
                "id": document_2[0][0],
                "documentType": "contractArrangements",
                "title": "title of document",
                "description": "descrition of document",
                "relatedLots": [f"{lot_2}"]
            }]
        }
    }
    if is_european_funding == False:
        del json_access_tender["planning"]["budget"]["budgetBreakdown"][0]["europeanUnionFunding"]

    session.execute(
        f"INSERT INTO access_tender (cp_id,stage,token_entity, created_date, json_data, owner) VALUES("
        f"'{cpid}', 'PN',{pn_token},{timestamp},'{json.dumps(json_access_tender)}', '{owner}');").one()

    json_notice_compiled_release_multistage = {
        "ocid": cpid,
        "id": cpid + "-" + f"{timestamp}",
        "date": start_date,
        "tag": ["compiled"],
        "language": language,
        "initiationType": "tender",
        "planning": {
            "budget": {
                "description": "description of budget",
                "amount": {
                    "amount": amount,
                    "currency": currency
                },
                "isEuropeanUnionFunded": True,
                "budgetBreakdown": [{
                    "id": fs_ocid,
                    "amount": {
                        "amount": amount,
                        "currency": currency
                    },
                    "period": {
                        "startDate": start_date,
                        "endDate": end_date
                    },
                    "sourceParty": {
                        "id": f"{buyer_identifier_scheme}-{buyer_id}",
                        "name": buyer_name
                    },
                    "europeanUnionFunding": {
                        "projectName": european_project_name,
                        "projectIdentifier": european_project_id,
                        "uri": european_project_uri
                    }
                }]
            },
            "rationale": "reason for budget"
        },
        "tender": {
            "id": "d4419c10-de2f-4a81-9e30-424eb3611b25",
            "title": "title of tender",
            "description": "desription of tender",
            "status": tender_status,
            "statusDetails": tender_status_details_ms,
            "value": {
                "amount": lot_1_amount + lot_2_amount,
                "currency": currency
            },
            "procurementMethod": "open",
            "procurementMethodDetails": "testOpenTender",
            "procurementMethodRationale": "procurementMethodRationale",
            "mainProcurementCategory": main_procurement_category,
            "hasEnquiries": False,
            "eligibilityCriteria": "Regulile generale privind naționalitatea și originea, precum și alte criterii de "
                                   "eligibilitate sunt enumerate în Ghidul practic privind procedurile de contractare "
                                   "a acțiunilor externe ale UE (PRAG)",
            "contractPeriod": {
                "startDate": contract_start,
                "endDate": contract_end
            },
            "procuringEntity": {
                "id": f"{procuring_entity_identifier_scheme}-{procuring_entity_id}",
                "name": procuring_entity_name
            },
            "acceleratedProcedure": {
                "isAcceleratedProcedure": False
            },
            "classification": {
                "scheme": "CPV",
                "id": classification_id,
                "description": "Lucrări de rambleiere şi de asanare a terenului"
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
            "legalBasis": "REGULATION_966_2012",
            "procedureOutsourcing": {
                "procedureOutsourced": False
            },
            "procurementMethodAdditionalInfo": "procurementMethodAdditionalInfo",
            "dynamicPurchasingSystem": {
                "hasDynamicPurchasingSystem": False
            },
            "framework": {
                "isAFramework": False
            }
        },
        "parties": [{
            "id": f"{buyer_identifier_scheme}-{buyer_id}",
            "name": "Directia Cultura a Primariei mun.Chisinau",
            "identifier": {
                "scheme": buyer_identifier_scheme,
                "id": buyer_id,
                "legalName": "Directia Cultura a Primariei mun.Chisinau",
                "uri": "tttt"
            },
            "address": {
                "streetAddress": "str.Bucuresti 68",
                "addressDetails": {
                    "country": {
                        "scheme": "iso-alpha2",
                        "id": "MD",
                        "description": "Moldova, Republica",
                        "uri": "https://www.iso.org"
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
            },
            "additionalIdentifiers": [{
                "scheme": "MD-IDNO",
                "id": "string",
                "legalName": "380935103469",
                "uri": "http://petrusenko.com/svetlana"
            }],
            "contactPoint": {
                "name": "Dumitru Popa",
                "email": "directiacultшra@yahoo.com",
                "telephone": "022242290",
                "url": "jkjk"
            },
            "details": {
                "typeOfBuyer": "NATIONAL_AGENCY",
                "mainGeneralActivity": "HEALTH",
                "mainSectoralActivity": "WATER"
            },
            "roles": ["buyer"]
        }, {
            "id": f"{payer_identifier_scheme}-{payer_id}",
            "name": "Procuring Entity Name",
            "identifier": {
                "scheme": payer_identifier_scheme,
                "id": payer_id,
                "legalName": "Legal Name"

            },
            "address": {
                "streetAddress": "street",
                "addressDetails": {
                    "country": {
                        "scheme": "iso-alpha2",
                        "id": "MD",
                        "description": "Moldova, Republica",
                        "uri": "https://www.iso.org"
                    },
                    "region": {
                        "scheme": "CUATM",
                        "id": "3400000",
                        "description": "Donduşeni",
                        "uri": "http://statistica.md"
                    },
                    "locality": {
                        "scheme": "CUATM",
                        "id": "3401000",
                        "description": "or.Donduşeni (r-l Donduşeni)",
                        "uri": "http://statistica.md"
                    }
                }
            },
            "contactPoint": {
                "name": "contact person",
                "email": "string@mail.ccc",
                "telephone": "98-79-87"
            },
            "roles": ["payer"]
        }, {
            "id": f"{funder_identifier_scheme}-{funder_id}",
            "name": "buyer name",
            "identifier": {
                "scheme": funder_identifier_scheme,
                "id": funder_id,
                "legalName": "legal Name"
            },
            "address": {
                "streetAddress": "street address of buyer",
                "addressDetails": {
                    "country": {
                        "scheme": "iso-alpha2",
                        "id": "MD",
                        "description": "Moldova, Republica",
                        "uri": "https://www.iso.org"
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
                "name": "contact point of buyer",
                "email": "email.com",
                "telephone": "32-22-23"
            },
            "roles": ["funder"]
        }, {
            "id": f"{procuring_entity_identifier_scheme}-{procuring_entity_id}",
            "name": "name of PE",
            "identifier": {
                "scheme": procuring_entity_identifier_scheme,
                "id": procuring_entity_id,
                "legalName": "legal name",
                "uri": "uri"
            },
            "address": {
                "streetAddress": "street address",
                "postalCode": "02232",
                "addressDetails": {
                    "country": {
                        "scheme": "iso-alpha2",
                        "id": "MD",
                        "description": "Moldova, Republica",
                        "uri": "https://www.iso.org"
                    },
                    "region": {
                        "scheme": "CUATM",
                        "id": "3400000",
                        "description": "Donduşeni",
                        "uri": "http://statistica.md"
                    },
                    "locality": {
                        "scheme": "CUATM",
                        "id": "3401000",
                        "description": "or.Donduşeni (r-l Donduşeni)",
                        "uri": "http://statistica.md"
                    }
                }
            },
            "additionalIdentifiers": [{
                "scheme": "md-idno",
                "id": "445521",
                "legalName": "legalName",
                "uri": "uri"
            }],
            "contactPoint": {
                "name": "name",
                "email": "email",
                "telephone": "456-95-96",
                "faxNumber": "fax-number",
                "url": "url"
            },
            "roles": ["procuringEntity"]
        }],
        "relatedProcesses": [{
            "id": "fe9797d0-80ac-11eb-a463-451f6f68192e",
            "relationship": ["planning"],
            "scheme": "ocid",
            "identifier": pn_ocid,
            "uri": f"http://dev.public.eprocurement.systems/tenders/{cpid}/{pn_ocid}"
        }, {
            "id": "fe9797d1-80ac-11eb-a463-451f6f68192e",
            "relationship": ["x_expenditureItem"],
            "scheme": "ocid",
            "identifier": ei_id,
            "uri": f"http://dev.public.eprocurement.systems/budgets/{ei_id}/{ei_id}"
        }, {
            "id": "fe9797d2-80ac-11eb-a463-451f6f68192e",
            "relationship": ["x_fundingSource"],
            "scheme": "ocid",
            "identifier": fs_ocid,
            "uri": f"http://dev.public.eprocurement.systems/budgets/{ei_id}/{fs_ocid}"
        }]
    }
    if is_european_funding == False:
        del json_notice_compiled_release_multistage["planning"]["budget"]["budgetBreakdown"][0]["europeanUnionFunding"]

    session.execute(
        f"INSERT INTO notice_compiled_release (cp_id,oc_id,json_data,publish_date,release_date,release_id,stage,"
        f"status) VALUES ('{cpid}','{cpid}','{json.dumps(json_notice_compiled_release_multistage)}',{period[2]},"
        f"{period[2]},'{cpid + '-' + str(timestamp)}','','planning');").one()

    json_notice_compiled_release_PN = {
        "ocid": pn_ocid,
        "id": pn_ocid + "-" + f"{timestamp}",
        "date": start_date,
        "tag": ["planning"],
        "language": language,
        "initiationType": "tender",
        "tender": {
            "id": "980ea5aa-2903-4d19-be23-78432707513e",
            "title": "Planning Notice",
            "description": "Contracting process is planned",
            "status": tender_status,
            "statusDetails": tender_status_details_pn,
            "items": [{
                "id": item_1,
                "internalId": "item 1",
                "description": "description",
                "classification": {
                    "scheme": "CPV",
                    "id": item_1_classification_id,
                    "description": "Lucrări de valorificare a terenurilor virane"
                },
                "additionalClassifications": [{
                    "scheme": "CPVS",
                    "id": "AA12-4",
                    "description": "Oţel carbon"
                }],
                "quantity": 0.010,
                "unit": {
                    "name": "Parsec",
                    "id": "10"
                },
                "relatedLot": lot_1
            }, {
                "id": item_2,
                "internalId": "item 2",
                "description": "description",
                "classification": {
                    "scheme": "CPV",
                    "id": item_2_classification_id,
                    "description": "Lucrări de reabilitare a terenului"
                },
                "additionalClassifications": [{
                    "scheme": "CPVS",
                    "id": "AA12-4",
                    "description": "Oţel carbon"
                }],
                "quantity": 0.010,
                "unit": {
                    "name": "Parsec",
                    "id": "10"
                },
                "relatedLot": lot_2
            }],
            "lots": [{
                "id": lot_1,
                "internalId": "lot 1",
                "title": "title",
                "description": "description",
                "status": lot_1_status,
                "statusDetails": lot_1_status_details,
                "value": {
                    "amount": lot_1_amount,
                    "currency": currency
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
                    "startDate": contract_start,
                    "endDate": contract_end
                },
                "placeOfPerformance": {
                    "address": {
                        "streetAddress": lot_1_place_performance_address_street,
                        "postalCode": lot_1_place_performance_address_postal,
                        "addressDetails": {
                            "country": {
                                "scheme": lot_1_place_performance_country_scheme,
                                "id": lot_1_place_performance_country_id,
                                "description": lot_1_place_performance_country_description,
                                "uri": lot_1_place_performance_country_uri
                            },
                            "region": {
                                "scheme": lot_1_place_performance_region_scheme,
                                "id": lot_1_place_performance_region_id,
                                "description": lot_1_place_performance_region_description,
                                "uri": lot_1_place_performance_region_uri
                            },
                            "locality": {
                                "scheme": lot_1_place_performance_locality_scheme,
                                "id": lot_1_place_performance_locality_id,
                                "description": lot_1_place_performance_locality_description,
                                "uri": lot_1_place_performance_locality_uri
                            }
                        }
                    },
                    "description": "description of lot"
                },
                "options": [{
                    "hasOptions": False
                }]
            }, {
                "id": lot_2,
                "internalId": "lot 2",
                "title": "title",
                "description": "description",
                "status": lot_2_status,
                "statusDetails": lot_2_status_details,
                "value": {
                    "amount": lot_2_amount,
                    "currency": currency
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
                    "startDate": contract_start,
                    "endDate": contract_end
                },
                "placeOfPerformance": {
                    "address": {
                        "streetAddress": lot_2_place_performance_address_street,
                        "postalCode": lot_2_place_performance_address_postal,
                        "addressDetails": {
                            "country": {
                                "scheme": lot_2_place_performance_country_scheme,
                                "id": lot_2_place_performance_country_id,
                                "description": lot_2_place_performance_country_description,
                                "uri": lot_2_place_performance_country_uri
                            },
                            "region": {
                                "scheme": lot_2_place_performance_region_scheme,
                                "id": lot_2_place_performance_region_id,
                                "description": lot_2_place_performance_region_description,
                                "uri": lot_2_place_performance_region_uri
                            },
                            "locality": {
                                "scheme": lot_2_place_performance_locality_scheme,
                                "id": lot_2_place_performance_locality_id,
                                "description": lot_2_place_performance_locality_description,
                                "uri": lot_2_place_performance_locality_uri
                            }
                        }
                    },
                    "description": "description of lot"
                },
                "options": [{
                    "hasOptions": False
                }]
            }],
            "lotGroups": [{
                "optionToCombine": False
            }],
            "tenderPeriod": {
                "startDate": tender_period
            },
            "hasEnquiries": False,
            "documents": [{
                "id": document_1[0][0],
                "documentType": "contractArrangements",
                "title": "title of document",
                "description": "descrition of document",
                "url": f"http://dev.bpe.eprocurement.systems/api/v1/storage/get/{document_1[0][0]}",
                "datePublished": f"{time_at_now()}",
                "relatedLots": [f"{lot_1}"]
            }, {
                "id": document_2[0][0],
                "documentType": "contractArrangements",
                "title": "title of document",
                "description": "descrition of document",
                "url": f"http://dev.bpe.eprocurement.systems/api/v1/storage/get/{document_2[0][0]}",
                "datePublished": f"{time_at_now()}",
                "relatedLots": [f"{lot_2}"]
            }],
            "submissionMethod": ["electronicSubmission"],
            "submissionMethodDetails": "Lista platformelor: achizitii, ebs, licitatie, yptender",
            "submissionMethodRationale": [
                "Ofertele vor fi primite prin intermediul unei platforme electronice de achiziții publice"],
            "requiresElectronicCatalogue": False,
            "procurementMethodRationale": "procurementMethodRationale",
            "classification": {
                "scheme": "CPV",
                "id": "45112300-8",
                "description": "Lucrări de rambleiere şi de asanare a terenului"
            },
            "value": {
                "amount": lot_1_amount + lot_2_amount,
                "currency": currency
            },
            "procuringEntity": {
                "id": f"{procuring_entity_identifier_scheme}-{procuring_entity_id}",
                "name": procuring_entity_name,
                "identifier": {
                    "scheme": procuring_entity_identifier_scheme,
                    "id": procuring_entity_id,
                    "legalName": procuring_entity_name,
                    "uri": "uri"
                },
                "address": {
                    "streetAddress": procuring_entity_address_street,
                    "postalCode": "02232",
                    "addressDetails": {
                        "country": {
                            "scheme": country_scheme,
                            "id": country_id,
                            "description": country_description,
                            "uri": country_uri
                        },
                        "region": {
                            "scheme": region_scheme,
                            "id": region_id,
                            "description": region_description,
                            "uri": region_uri
                        },
                        "locality": {
                            "scheme": locality_scheme,
                            "id": locality_id,
                            "description": locality_description,
                            "uri": "http://statistica.md"

                        }
                    }
                },
                "additionalIdentifiers": [{
                    "scheme": "md-idno",
                    "id": "445521",
                    "legalName": "legalName",
                    "uri": "uri"
                }],
                "contactPoint": {
                    "name": contact_point_name,
                    "email": contact_point_email,
                    "telephone": contact_point_telephone,
                    "faxNumber": "fax-number",
                    "url": "url"
                }
            }
        },
        "hasPreviousNotice": False,
        "purposeOfNotice": {
            "isACallForCompetition": False
        },
        "relatedProcesses": [{
            "id": f"{uuid4()}",
            "relationship": ["parent"],
            "scheme": "ocid",
            "identifier": cpid,
            "uri": f"http://dev.public.eprocurement.systems/tenders/{cpid}/{cpid}"
        }]
    }
    session.execute(
        f"INSERT INTO notice_compiled_release (cp_id,oc_id,json_data,publish_date,release_date,release_id,stage,"
        f"status) VALUES ('{cpid}','{pn_ocid}','{json.dumps(json_notice_compiled_release_PN)}',{period[2]},"
        f"{period[2]},'{pn_ocid + '-' + str(timestamp)}','PN','planning');").one()

    session.execute(
        f"INSERT INTO notice_offset (cp_id, release_date, stage, status) VALUES ('{cpid}',{period[2]},'PN',"
        f"'planning');").one()

    session.execute(f"INSERT INTO notice_release (cp_id,oc_id, release_id,json_data,release_date, "
                    f"stage) VALUES ('{cpid}','{cpid}','{cpid + '-' + str(timestamp)}',"
                    f"'{json.dumps(json_notice_compiled_release_multistage)}',{period[2]}, '');").one()

    session.execute(f"INSERT INTO notice_release (cp_id,oc_id, release_id,json_data,release_date, "
                    f"stage) VALUES ('{cpid}','{pn_ocid}','{pn_ocid + '-' + str(timestamp)}',"
                    f"'{json.dumps(json_notice_compiled_release_PN)}',{period[2]}, 'PN');").one()

    return f"http://dev.public.eprocurement.systems/tenders/{cpid}", cpid, fs_ocid, pn_ocid, str(
        pn_token), lot_1, lot_2, item_1, item_2, document_1[0][0], document_2[0][0]


def insert_into_db_create_pn_obligatory_data_model(cpid, ei_id, additional_value, start_date=get_period()[0],
                                                   end_date=get_period()[1], tender_period=get_contract_period()[2],
                                                   timestamp=get_timestamp_from_human_date(get_period()[0]),
                                                   language="ro",
                                                   country="MD", is_european_funding=True,
                                                   european_project_name="test eropean name",
                                                   european_project_id="test european id",
                                                   european_project_uri="european uri", amount=2000.00, currency="EUR",
                                                   lot_1_amount=1500.00, lot_2_amount=150.00,
                                                   classification_id="45100000-8", main_procurement_category="works",
                                                   buyer_identifier_scheme="MD-IDNO", buyer_id="1",
                                                   payer_identifier_scheme="MD-IDNO", buyer_name="LLC Dmitro",
                                                   procuring_entity_identifier_scheme="MD-IDNO",
                                                   procuring_entity_id="4",
                                                   procuring_entity_name="LLC Petrovich",
                                                   procuring_entity_address_street="street",
                                                   country_id="MD",
                                                   country_scheme="iso-alpha2", region_scheme="CUATM",
                                                   region_id="3400000",
                                                   region_description="Donduşeni", locality_scheme="CUATM",
                                                   locality_id="3401000",
                                                   locality_description="or.Donduşeni (r-l Donduşeni)",
                                                   country_description="Moldova, Republica",
                                                   country_uri="https://www.iso.org",
                                                   region_uri="http://statistica.md",
                                                   contact_point_name="Petrusenko Svitlana",
                                                   contact_point_email="svetik@gmail.com",
                                                   contact_point_telephone="888999666", payer_id="2",
                                                   funder_id="3", funder_identifier_scheme="MD-IDNO",
                                                   tender_status="planning", tender_status_details_pn="planning",
                                                   tender_status_details_ms="planning notice"):
    auth_provider = PlainTextAuthProvider(username=username, password=password)
    cluster = Cluster([host], auth_provider=auth_provider)
    session = cluster.connect('ocds')
    pn_token = uuid4()
    owner = "445f6851-c908-407d-9b45-14b92f3e964b"
    pn_ocid = prepared_pn_ocid(cpid)

    fs_ocid = prepared_fs_ocid(ei_id)
    period = get_period()

    json_orchestrator_context = {
        "operationId": f"{uuid4()}",
        "requestId": f"{uuid4()}",
        "cpid": cpid,
        "ocid": pn_ocid,
        "stage": "PN",
        "processType": "createPN",
        "operationType": "createPN",
        "phase": "planning",
        "owner": owner,
        "country": country,
        "language": language,
        "pmd": additional_value,
        "token": f"{pn_token}",
        "startDate": start_date,
        "timeStamp": timestamp,
        "isAuction": False,
        "testMode": False
    }

    session.execute(f"INSERT INTO orchestrator_context (cp_id,context) VALUES ("
                    f"'{cpid}','{json.dumps(json_orchestrator_context)}');").one()

    json_access_tender = {
        "ocid": cpid,
        "planning": {
            "budget": {
                "amount": {
                    "amount": amount,
                    "currency": currency
                },
                "isEuropeanUnionFunded": is_european_funding,
                "budgetBreakdown": [{
                    "id": fs_ocid,
                    "description": "description",
                    "amount": {
                        "amount": amount,
                        "currency": currency
                    },
                    "period": {
                        "startDate": start_date,
                        "endDate": end_date
                    },
                    "sourceParty": {
                        "id": f"{buyer_identifier_scheme}-{buyer_id}",
                        "name": buyer_name
                    },
                    "europeanUnionFunding": {
                        "projectName": european_project_name,
                        "projectIdentifier": european_project_id,
                        "uri": european_project_uri
                    }
                }]
            }
        },
        "tender": {
            "id": "6e8e42b5-f01d-44b1-9896-a8383a2351e4",
            "status": tender_status,
            "statusDetails": tender_status_details_pn,
            "title": "title of tender",
            "description": "desription of tender",
            "classification": {
                "scheme": "CPV",
                "id": classification_id,
                "description": "Lucrări de pregătire a şantierului"
            },
            "mainProcurementCategory": main_procurement_category,
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
            "legalBasis": "REGULATION_966_2012",
            "procurementMethod": "open",
            "procurementMethodDetails": "testOpenTender",
            "eligibilityCriteria": "Regulile generale privind naționalitatea și originea, precum și alte criterii de eligibilitate sunt enumerate în Ghidul practic privind procedurile de contractare a acțiunilor externe ale UE (PRAG)",
            "tenderPeriod": {
                "startDate": tender_period
            },
            "procuringEntity": {
                "id": f"{procuring_entity_identifier_scheme}-{procuring_entity_id}",
                "name": procuring_entity_name,
                "identifier": {
                    "scheme": procuring_entity_identifier_scheme,
                    "id": procuring_entity_id,
                    "legalName": procuring_entity_name
                },
                "address": {
                    "streetAddress": procuring_entity_address_street,
                    "addressDetails": {
                        "country": {
                            "scheme": country_scheme,
                            "id": country_id,
                            "description": country_description,
                            "uri": country_uri
                        },
                        "region": {
                            "scheme": region_scheme,
                            "id": region_id,
                            "description": region_description,
                            "uri": region_uri
                        },
                        "locality": {
                            "scheme": locality_scheme,
                            "id": locality_id,
                            "description": locality_description

                        }
                    }
                },
                "contactPoint": {
                    "name": contact_point_name,
                    "email": contact_point_email,
                    "telephone": contact_point_telephone
                }
            },
            "value": {
                "amount": lot_1_amount + lot_2_amount,
                "currency": currency
            },
            "lotGroups": [{
                "optionToCombine": False
            }],
            "lots": [],
            "items": [],
            "requiresElectronicCatalogue": False,
            "submissionMethod": ["electronicSubmission"],
            "submissionMethodRationale": [
                "Ofertele vor fi primite prin intermediul unei platforme electronice de achiziții publice"],
            "submissionMethodDetails": "Lista platformelor: achizitii, ebs, licitatie, yptender"
        }
    }
    if is_european_funding == False:
        del json_access_tender["planning"]["budget"]["budgetBreakdown"][0]["europeanUnionFunding"]

    session.execute(
        f"INSERT INTO access_tender (cp_id,stage,token_entity, created_date, json_data, owner) VALUES("
        f"'{cpid}', 'PN',{pn_token},{timestamp},'{json.dumps(json_access_tender)}', '{owner}');").one()

    json_notice_compiled_release_multistage = {
        "ocid": cpid,
        "id": cpid + "-" + f"{timestamp}",
        "date": start_date,
        "tag": [
            "compiled"],
        "language": language,
        "initiationType": "tender",
        "planning": {
            "budget": {
                "amount": {
                    "amount": amount,
                    "currency": currency
                },
                "isEuropeanUnionFunded": True,
                "budgetBreakdown": [
                    {
                        "id": fs_ocid,

                        "amount": {
                            "amount": amount,
                            "currency": currency
                        },
                        "period": {
                            "startDate": start_date,
                            "endDate": end_date
                        },
                        "sourceParty": {
                            "id": f"{buyer_identifier_scheme}-{buyer_id}",
                            "name": buyer_name
                        },
                        "europeanUnionFunding": {
                            "projectName": european_project_name,
                            "projectIdentifier": european_project_id,
                            "uri": european_project_uri
                        }
                    }]
            }
        },
        "tender": {
            "id": "6e8e42b5-f01d-44b1-9896-a8383a2351e4",
            "title": "title of tender",
            "description": "desription of tender",
            "status": tender_status,
            "statusDetails": tender_status_details_ms,
            "value": {
                "amount": amount,
                "currency": currency
            },
            "procurementMethod": "open",
            "procurementMethodDetails": "testOpenTender",
            "mainProcurementCategory": main_procurement_category,
            "hasEnquiries": False,
            "eligibilityCriteria": "Regulile generale privind naționalitatea și originea, precum și alte criterii "
                                   "de eligibilitate sunt enumerate în Ghidul practic privind procedurile de "
                                   "contractare a acțiunilor externe ale UE (PRAG)",
            "procuringEntity": {
                "id": f"{procuring_entity_identifier_scheme}-{procuring_entity_id}",
                "name": procuring_entity_name
            },
            "acceleratedProcedure": {
                "isAcceleratedProcedure": False
            },
            "classification": {
                "scheme": "CPV",
                "id": classification_id,
                "description": "Lucrări de pregătire a şantierului"
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
            "legalBasis": "REGULATION_966_2012",
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
            "id": f"{buyer_identifier_scheme}-{buyer_id}",
            "name": "Directia Cultura a Primariei mun.Chisinau",
            "identifier": {
                "scheme": buyer_identifier_scheme,
                "id": buyer_id,
                "legalName": "Directia Cultura a Primariei mun.Chisinau",
                "uri": "tttt"
            },
            "address": {
                "streetAddress": "str.Bucuresti 68",
                "postalCode": "02217",
                "addressDetails": {
                    "country": {
                        "scheme": "iso-alpha2",
                        "id": "MD",
                        "description": "Moldova, Republica",
                        "uri": "https://www.iso.org"
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
            },
            "additionalIdentifiers": [{
                "scheme": "MD-IDNO",
                "id": "string",
                "legalName": "380935103469",
                "uri": "http://petrusenko.com/svetlana"
            }],
            "contactPoint": {
                "name": "Dumitru Popa",
                "email": "directiacultшra@yahoo.com",
                "telephone": "022242290",
                "url": "http://petrusenko.com/svetlana"
            },
            "details": {
                "typeOfBuyer": "NATIONAL_AGENCY",
                "mainGeneralActivity": "HEALTH",
                "mainSectoralActivity": "WATER"
            },
            "roles": ["buyer"]
        }, {
            "id": f"{payer_identifier_scheme}-{payer_id}",
            "name": "Procuring Entity Name",
            "identifier": {
                "scheme": payer_identifier_scheme,
                "id": payer_id,
                "legalName": "Legal Name"
            },
            "address": {
                "streetAddress": "street",
                "addressDetails": {
                    "country": {
                        "scheme": "iso-alpha2",
                        "id": "MD",
                        "description": "Moldova, Republica",
                        "uri": "https://www.iso.org"
                    },
                    "region": {
                        "scheme": "CUATM",
                        "id": "3400000",
                        "description": "Donduşeni",
                        "uri": "http://statistica.md"
                    },
                    "locality": {
                        "scheme": "CUATM",
                        "id": "3401000",
                        "description": "or.Donduşeni (r-l Donduşeni)",
                        "uri": "http://statistica.md"
                    }
                }
            },
            "contactPoint": {
                "name": "contact person",
                "email": "string@mail.ccc",
                "telephone": "98-79-87"
            },
            "roles": ["payer"]
        }, {
            "id": f"{funder_identifier_scheme}-{funder_id}",
            "name": "buyer name",
            "identifier": {
                "scheme": funder_identifier_scheme,
                "id": funder_id,
                "legalName": "legal Name"
            },
            "address": {
                "streetAddress": "street address of buyer",
                "addressDetails": {
                    "country": {
                        "scheme": "iso-alpha2",
                        "id": "MD",
                        "description": "Moldova, Republica",
                        "uri": "https://www.iso.org"
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
                "name": "contact point of buyer",
                "email": "email.com",
                "telephone": "32-22-23"
            },
            "roles": ["funder"]
        }, {
            "id": f"{procuring_entity_identifier_scheme}-{procuring_entity_id}",
            "name": "name of PE",
            "identifier": {
                "scheme": procuring_entity_identifier_scheme,
                "id": procuring_entity_id,
                "legalName": "legal name"
            },
            "address": {
                "streetAddress": "street address",
                "addressDetails": {
                    "country": {
                        "scheme": "iso-alpha2",
                        "id": "MD",
                        "description": "Moldova, Republica",
                        "uri": "https://www.iso.org"
                    },
                    "region": {
                        "scheme": "CUATM",
                        "id": "0101000",
                        "description": "mun.Chişinău",
                        "uri": "http://statistica.md"
                    },
                    "locality": {
                        "scheme": "other",
                        "id": "locality",
                        "description": "4596"
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
        "relatedProcesses": [
            {
                "id": "aebc2410-828c-11eb-a463-451f6f68192e",
                "relationship": ["planning"],
                "scheme": "ocid",
                "identifier": pn_ocid,
                "uri": f"http://dev.public.eprocurement.systems/tenders/{cpid}/{pn_ocid}"
            },
            {
                "id": "aebc2411-828c-11eb-a463-451f6f68192e",
                "relationship": ["x_expenditureItem"],
                "scheme": "ocid",
                "identifier": ei_id,
                "uri": f"http://dev.public.eprocurement.systems/budgets/{ei_id}/{ei_id}"
            },
            {
                "id": "aebc2412-828c-11eb-a463-451f6f68192e",
                "relationship": ["x_fundingSource"],
                "scheme": "ocid",
                "identifier": fs_ocid,
                "uri": f"http://dev.public.eprocurement.systems/budgets/{ei_id}/{fs_ocid}"
            }]
    }
    if is_european_funding == False:
        del json_notice_compiled_release_multistage["planning"]["budget"]["budgetBreakdown"][0]["europeanUnionFunding"]

    session.execute(
        f"INSERT INTO notice_compiled_release (cp_id,oc_id,json_data,publish_date,release_date,release_id,stage,"
        f"status) VALUES ('{cpid}','{cpid}','{json.dumps(json_notice_compiled_release_multistage)}',{period[2]},"
        f"{period[2]},'{cpid + '-' + str(timestamp)}','','planning');").one()

    json_notice_compiled_release_PN = {
        "ocid": pn_ocid,
        "id": pn_ocid + "-" + f"{timestamp}",
        "date": start_date,
        "tag": ["planning"],
        "language": language,
        "initiationType": "tender",
        "tender": {
            "id": "e32fb4e7-184b-45f7-983e-055352400719",
            "title": "Planning Notice",
            "description": "Contracting process is planned",
            "status": tender_status,
            "statusDetails": tender_status_details_pn,
            "lotGroups": [{
                "optionToCombine": False
            }],
            "tenderPeriod": {
                "startDate": tender_period
            },
            "hasEnquiries": False,
            "submissionMethod": ["electronicSubmission"],
            "submissionMethodDetails": "Lista platformelor: achizitii, ebs, licitatie, yptender",
            "submissionMethodRationale": [
                "Ofertele vor fi primite prin intermediul unei platforme electronice de achiziții publice"],
            "requiresElectronicCatalogue": False,
            "classification": {
                "scheme": "CPV",
                "id": "45100000-8",
                "description": "Lucrări de pregătire a şantierului"
            },
            "value": {
                "amount": amount,
                "currency": currency
            },
            "procuringEntity": {
                "id": f"{procuring_entity_identifier_scheme}-{procuring_entity_id}",
                "name": procuring_entity_name,
                "identifier": {
                    "scheme": procuring_entity_identifier_scheme,
                    "id": procuring_entity_id,
                    "legalName": procuring_entity_name
                },
                "address": {
                    "streetAddress": procuring_entity_address_street,
                    "addressDetails": {
                        "country": {
                            "scheme": country_scheme,
                            "id": country_id,
                            "description": country_description,
                            "uri": country_uri
                        },
                        "region": {
                            "scheme": region_scheme,
                            "id": region_id,
                            "description": region_description,
                            "uri": region_uri
                        },
                        "locality": {
                            "scheme": locality_scheme,
                            "id": locality_id,
                            "description": locality_description

                        }
                    }
                },
                "contactPoint": {
                    "name": contact_point_name,
                    "email": contact_point_email,
                    "telephone": contact_point_telephone
                }
            }
        },
        "hasPreviousNotice": False,
        "purposeOfNotice": {
            "isACallForCompetition": False
        },
        "relatedProcesses": [{
            "id": f"{uuid4()}",
            "relationship": ["parent"],
            "scheme": "ocid",
            "identifier": cpid,
            "uri": f"http://dev.public.eprocurement.systems/tenders/{cpid}/{cpid}"
        }]
    }

    session.execute(
        f"INSERT INTO notice_compiled_release (cp_id,oc_id,json_data,publish_date,release_date,release_id,stage,"
        f"status) VALUES ('{cpid}','{pn_ocid}','{json.dumps(json_notice_compiled_release_PN)}',{period[2]},"
        f"{period[2]},'{pn_ocid + '-' + str(timestamp)}','PN','planning');").one()

    session.execute(
        f"INSERT INTO notice_offset (cp_id, release_date, stage, status) VALUES ('{cpid}',{period[2]},'PN',"
        f"'planning');").one()

    session.execute(f"INSERT INTO notice_release (cp_id,oc_id, release_id,json_data,release_date, "
                    f"stage) VALUES ('{cpid}','{cpid}','{cpid + '-' + str(timestamp)}',"
                    f"'{json.dumps(json_notice_compiled_release_multistage)}',{period[2]}, '');").one()

    session.execute(f"INSERT INTO notice_release (cp_id,oc_id, release_id,json_data,release_date, "
                    f"stage) VALUES ('{cpid}','{pn_ocid}','{pn_ocid + '-' + str(timestamp)}',"
                    f"'{json.dumps(json_notice_compiled_release_PN)}',{period[2]}, 'PN');").one()

    return f"http://dev.public.eprocurement.systems/tenders/{cpid}", cpid, fs_ocid, pn_ocid, str(pn_token)
