import json
import time
import datetime
from uuid import uuid4

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

from tests.presets import set_instance_for_cassandra
from useful_functions import prepared_fs_ocid

# password_dev = '6AH7vbrkMWnfK'
# password_sandbox = 'brT4Kn27RQs'
# cluster_dev = '10.0.20.104'
# cluster_sandbox = '10.0.10.104'

instance = set_instance_for_cassandra()
username = instance[1]
password = instance[2]
host = instance[0]


def insert_into_db_create_ei(cpid):
    auth_provider = PlainTextAuthProvider(username=username, password=password)
    cluster = Cluster([host], auth_provider=auth_provider)
    session = cluster.connect('ocds')
    ei_token = uuid4()
    owner = "445f6851-c908-407d-9b45-14b92f3e964b"

    date = datetime.datetime.now()
    time_at_now = date.strftime('%Y-%m-%dT%H:%M:%SZ')
    time_at_now_miliseconds = date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    timestamp = int(
        time.mktime(datetime.datetime.strptime(time_at_now_miliseconds, "%Y-%m-%dT%H:%M:%S.%fZ").timetuple())) * 1000

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
        "startDate": f"{time_at_now}",
        "timeStamp": timestamp,
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

    json_notice_budget_release_ei = {
        "ocid": cpid,
        "id": cpid + '-' + f'{timestamp}',
        "date": f"{time_at_now}",
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

    json_notice_budget_compiled_release_ei = {
        "ocid": cpid,
        "id": cpid + "-" + f"{timestamp}",
        "date": f"{time_at_now}",
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
                    f"1609943491271,1609943491271,'{cpid + '-' + f'{timestamp}'}',"
                    f"'EI');").one()

    return f"http://dev.public.eprocurement.systems/budgets/{cpid}/{cpid}", ei_token


def insert_into_db_update_ei(cpid):
    auth_provider = PlainTextAuthProvider(username=username, password=password)
    cluster = Cluster([host], auth_provider=auth_provider)
    session = cluster.connect('ocds')
    ei_token = uuid4()
    owner = "445f6851-c908-407d-9b45-14b92f3e964b"

    date = datetime.datetime.now()
    time_at_now = date.strftime('%Y-%m-%dT%H:%M:%SZ')
    time_at_now_miliseconds = date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    timestamp = int(
        time.mktime(datetime.datetime.strptime(time_at_now_miliseconds, "%Y-%m-%dT%H:%M:%S.%fZ").timetuple())) * 1000

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
        "startDate": f"{time_at_now}",
        "timeStamp": timestamp,
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
                    "startDate": "2021-01-01T00:00:00Z",
                    "endDate": "2021-12-31T00:00:00Z"
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
        "id": cpid + "-" + f"{timestamp}",
        "date": f"{time_at_now}",
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
                    "startDate": "2021-01-01T00:00:00Z",
                    "endDate": "2021-12-31T00:00:00Z"
                }
            },
            "rationale": "for EI updating from 2021 year"
        }
    }

    json_notice_budget_compiled_release_ei = {
        "ocid": cpid,
        "id": cpid + "-" + f"{timestamp}",
        "date": f"{time_at_now}",
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
                    "startDate": "2021-01-01T00:00:00Z",
                    "endDate": "2021-12-31T00:00:00Z"
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
                    f"1609943491271,1609943491271,'{cpid + '-' + f'{timestamp}'}',"
                    f"'EI');").one()

    return f"http://dev.public.eprocurement.systems/budgets/{cpid}/{cpid}", ei_token


def insert_into_db_create_fs(cpid):
    auth_provider = PlainTextAuthProvider(username=username, password=password)
    cluster = Cluster([host], auth_provider=auth_provider)
    session = cluster.connect('ocds')
    fs_token = uuid4()
    ei_token = uuid4()
    owner = "445f6851-c908-407d-9b45-14b92f3e964b"

    date = datetime.datetime.now()
    time_at_now = date.strftime('%Y-%m-%dT%H:%M:%SZ')
    time_at_now_miliseconds = date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    timestamp = int(
        time.mktime(datetime.datetime.strptime(time_at_now_miliseconds, "%Y-%m-%dT%H:%M:%S.%fZ").timetuple())) * 1000
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
        "startDate": f"{time_at_now}",
        "timeStamp": timestamp,
        "isAuction": False
    }

    json_budget_ei = {
        "ocid": cpid,
        "tender": {
            "id": "7f025771-0c6b-4fa9-bac5-75c36575c5e7",
            "title": "Cardurilor de acces pentru Bibliotecii Municipale B.P. Hasdeu ",
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
                    "startDate": "2021-01-10T00:00:00Z",
                    "endDate": "2021-12-31T12:40:00Z"
                },
                "amount": {
                    "amount": 2000.00,
                    "currency": "EUR"
                }
            }
        },
        "buyer": {
            "id": "MD-IDNO-123654789000",
            "name": "Directia Cultura a Primariei mun.Chisinau",
            "identifier": {
                "id": "123654789000",
                "scheme": "MD-IDNO",
                "legalName": "Directia Cultura a Primariei mun.Chisinau"
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
            "contactPoint": {
                "name": "Dumitru Popa",
                "email": "directiacultшra@yahoo.com",
                "telephone": "022242290"
            }
        }
    }

    json_notice_budget_release_ei = {
        "ocid": cpid,
        "id": cpid + '-' + f'{timestamp}',
        "date": f"{time_at_now}",
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

    json_notice_budget_compiled_release_ei = {
        "ocid": cpid,
        "id": cpid + "-" + f"{timestamp}",
        "date": f"{time_at_now}",
        "tag": ["compiled"],
        "initiationType": "tender",
        "tender": {
            "id": "7f025771-0c6b-4fa9-bac5-75c36575c5e7",
            "title": "Cardurilor de acces pentru Bibliotecii Municipale B.P. Hasdeu ",
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
            "id": "MD-IDNO-123654789000",
            "name": "Directia Cultura a Primariei mun.Chisinau"
        },
        "parties": [{
            "id": "MD-IDNO-123654789000",
            "name": "Directia Cultura a Primariei mun.Chisinau",
            "identifier": {
                "scheme": "MD-IDNO",
                "id": "123654789000",
                "legalName": "Directia Cultura a Primariei mun.Chisinau"
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
            "contactPoint": {
                "name": "Dumitru Popa",
                "email": "directiacultшra@yahoo.com",
                "telephone": "022242290"
            },
            "roles": ["buyer"]
        }],
        "planning": {
            "budget": {
                "id": "45100000-8",
                "period": {
                    "startDate": "2021-01-10T00:00:00Z",
                    "endDate": "2021-12-31T12:40:00Z"
                },
                "amount": {
                    "amount": 2000.00,
                    "currency": "EUR"
                }
            }
        },
        "relatedProcesses": [{
            "id": "d8f7e390-5460-11eb-9c4c-99558c405434",
            "relationship": ["x_fundingSource"],
            "scheme": "ocid",
            "identifier": "ocds-t1s2t3-MD-1610406045049-FS-1610406049844",
            "uri": f"http://dev.public.eprocurement.systems/budgets/{cpid}/{fs_ocid}"
        }]
    }

    json_budget_fs = {
        "ocid": fs_ocid,
        "tender": {
            "id": "d5752f3a-40b1-4b0e-bbbb-98fff7e77753",
            "status": "planning",
            "statusDetails": "empty"
        },
        "planning": {
            "budget": {
                "id": "IBAN - 102030",
                "description": "description",
                "period": {
                    "startDate": "2021-02-20T00:00:00Z",
                    "endDate": "2021-12-31T00:00:00Z"
                },
                "amount": {
                    "amount": 2000.00,
                    "currency": "EUR"
                },
                "europeanUnionFunding": {
                    "projectName": "Name of this project",
                    "projectIdentifier": "projectIdentifier",
                    "uri": "http://uriuri.th"
                },
                "isEuropeanUnionFunded": True,
                "verified": False,
                "sourceEntity": {
                    "id": "MD-IDNO-380632074071",
                    "name": "LLC Petrusenko"
                },
                "verificationDetails": None,
                "project": "project",
                "projectID": "projectID",
                "uri": "http://uri.ur"
            },
            "rationale": "reason for the budget"
        },
        "payer": {
            "id": "MD-IDNO-123456789000",
            "name": "Procuring Entity Name",
            "identifier": {
                "id": "123456789000",
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
        "id": fs_ocid + "-" + f"{timestamp}",
        "date": f"{time_at_now}",
        "tag": ["planning"],
        "initiationType": "tender",
        "tender": {
            "id": "d5752f3a-40b1-4b0e-bbbb-98fff7e77753",
            "status": "planning",
            "statusDetails": "empty"
        },
        "parties": [{
            "id": "MD-IDNO-123456789000",
            "name": "Procuring Entity Name",
            "identifier": {
                "scheme": "MD-IDNO",
                "id": "123456789000",
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
                "description": "description",
                "period": {
                    "startDate": "2021-02-20T00:00:00Z",
                    "endDate": "2021-12-31T00:00:00Z"
                },
                "amount": {
                    "amount": 2000.00,
                    "currency": "EUR"
                },
                "europeanUnionFunding": {
                    "projectIdentifier": "projectIdentifier",
                    "projectName": "Name of this project",
                    "uri": "http://uriuri.th"
                },
                "isEuropeanUnionFunded": True,
                "verified": False,
                "sourceEntity": {
                    "id": "MD-IDNO-380632074071",
                    "name": "LLC Petrusenko"
                },
                "project": "project",
                "projectID": "projectID",
                "uri": "http://uri.ur"
            },
            "rationale": "reason for the budget"
        },
        "relatedProcesses": [{
            "id": "376490a0-529e-11eb-a7d4-3b1c06125f07",
            "relationship": ["parent"],
            "scheme": "ocid",
            "identifier": cpid,
            "uri": f"http://dev.public.eprocurement.systems/budgets/{cpid}/{cpid}"
        }]
    }

    json_budget_compiled_release_fs = {
        "ocid": fs_ocid,
        "id": fs_ocid + "-" + f"{timestamp}",
        "date": f"{time_at_now}",
        "tag": ["planning"],
        "initiationType": "tender",
        "tender": {
            "id": "d5752f3a-40b1-4b0e-bbbb-98fff7e77753",
            "status": "planning",
            "statusDetails": "empty"
        },
        "parties": [{
            "id": "MD-IDNO-123456789000",
            "name": "Procuring Entity Name",
            "identifier": {
                "scheme": "MD-IDNO",
                "id": "123456789000",
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
                "description": "description",
                "period": {
                    "startDate": "2021-02-20T00:00:00Z",
                    "endDate": "2021-12-31T00:00:00Z"
                },
                "amount": {
                    "amount": 2000.00,
                    "currency": "EUR"
                },
                "europeanUnionFunding": {
                    "projectIdentifier": "projectIdentifier",
                    "projectName": "Name of this project",
                    "uri": "http://uriuri.th"
                },
                "isEuropeanUnionFunded": True,
                "verified": False,
                "sourceEntity": {
                    "id": "MD-IDNO-380632074071",
                    "name": "LLC Petrusenko"
                },
                "project": "project",
                "projectID": "projectID",
                "uri": "http://uri.ur"
            },
            "rationale": "reason for the budget"
        },
        "relatedProcesses": [{
            "id": "376490a0-529e-11eb-a7d4-3b1c06125f07",
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
                    f"1609943491271,1609943491271,'{cpid + '-' + f'{timestamp}'}',"
                    f"'EI');").one()

    session.execute(f"INSERT INTO budget_ei (cp_id,token_entity,created_date,json_data,owner) VALUES("
                    f"'{cpid}',{ei_token},1609927348000,'{json.dumps(json_budget_ei)}','{owner}');").one()

    session.execute(f"INSERT INTO orchestrator_context (cp_id,context) VALUES ("
                    f"'{cpid}','{json.dumps(json_orchestrator_context)}');").one()

    session.execute(
        f"INSERT INTO budget_fs (cp_id,token_entity,amount,amount_reserved,created_date,json_data,oc_id,owner) "
        f"VALUES ('{cpid}',{fs_token},8000.00,0,{timestamp},'{json.dumps(json_budget_fs)}','{fs_ocid}',"
        f"'{owner}');").one()

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

    return f"http://dev.public.eprocurement.systems/budgets/{cpid}/{fs_ocid}", fs_token, fs_ocid


def insert_into_db_update_fs(cpid):
    auth_provider = PlainTextAuthProvider(username=username, password=password)
    cluster = Cluster([host], auth_provider=auth_provider)
    session = cluster.connect('ocds')
    fs_token = uuid4()
    ei_token = uuid4()
    owner = "445f6851-c908-407d-9b45-14b92f3e964b"

    date = datetime.datetime.now()
    time_at_now = date.strftime('%Y-%m-%dT%H:%M:%SZ')
    time_at_now_miliseconds = date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    timestamp = int(
        time.mktime(datetime.datetime.strptime(time_at_now_miliseconds, "%Y-%m-%dT%H:%M:%S.%fZ").timetuple())) * 1000
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
        "startDate": f"{time_at_now}",
        "timeStamp": timestamp,
        "isAuction": False
    }

    json_budget_ei = {
        "ocid": cpid,
        "tender": {
            "id": "7f025771-0c6b-4fa9-bac5-75c36575c5e7",
            "title": "Cardurilor de acces pentru Bibliotecii Municipale B.P. Hasdeu ",
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
                    "startDate": "2021-01-10T00:00:00Z",
                    "endDate": "2021-12-31T12:40:00Z"
                },
                "amount": {
                    "amount": 2000.00,
                    "currency": "EUR"
                }
            }
        },
        "buyer": {
            "id": "MD-IDNO-123654789000",
            "name": "Directia Cultura a Primariei mun.Chisinau",
            "identifier": {
                "id": "123654789000",
                "scheme": "MD-IDNO",
                "legalName": "Directia Cultura a Primariei mun.Chisinau"
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
            "contactPoint": {
                "name": "Dumitru Popa",
                "email": "directiacultшra@yahoo.com",
                "telephone": "022242290"
            }
        }
    }

    json_notice_budget_release_ei = {
        "ocid": cpid,
        "id": cpid + '-' + f'{timestamp}',
        "date": f"{time_at_now}",
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

    json_notice_budget_compiled_release_ei = {
        "ocid": cpid,
        "id": cpid + "-" + f"{timestamp}",
        "date": f"{time_at_now}",
        "tag": ["compiled"],
        "initiationType": "tender",
        "tender": {
            "id": "bb58a236-dc45-4f62-baf5-7a4a28778bc3",
            "title": "Cardurilor de acces pentru Bibliotecii Municipale B.P. Hasdeu ",
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
            "id": "MD-IDNO-123654789000",
            "name": "Directia Cultura a Primariei mun.Chisinau"
        },
        "parties": [{
            "id": "MD-IDNO-123654789000",
            "name": "Directia Cultura a Primariei mun.Chisinau",
            "identifier": {
                "scheme": "MD-IDNO",
                "id": "123654789000",
                "legalName": "Directia Cultura a Primariei mun.Chisinau"
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
            "contactPoint": {
                "name": "Dumitru Popa",
                "email": "directiacultшra@yahoo.com",
                "telephone": "022242290"
            },
            "roles": ["buyer"]
        }],
        "planning": {
            "budget": {
                "id": "45100000-8",
                "period": {
                    "startDate": "2021-01-10T00:00:00Z",
                    "endDate": "2021-12-31T12:40:00Z"
                },
                "amount": {
                    "amount": 24.00,
                    "currency": "EUR"
                }
            }
        },
        "relatedProcesses": [{
            "id": "e23a0c90-5464-11eb-9c4c-99558c405434",
            "relationship": ["x_fundingSource"],
            "scheme": "ocid",
            "identifier": "ocds-t1s2t3-MD-1610407775380-FS-1610407783365",
            "uri": f"http://dev.public.eprocurement.systems/budgets/{cpid}/{fs_ocid}"
        }]
    }

    json_budget_fs = {
        "ocid": fs_ocid,
        "tender": {
            "id": "d5752f3a-40b1-4b0e-bbbb-98fff7e77753",
            "status": "planning",
            "statusDetails": "empty"
        },
        "planning": {
            "budget": {
                "id": "IBAN - 102030",
                "description": "for FS updating from 2021 year",
                "period": {
                    "startDate": "2021-12-20T00:00:00Z",
                    "endDate": "2021-12-25T00:00:00Z"
                },
                "amount": {
                    "amount": 2000.00,
                    "currency": "EUR"
                },
                "europeanUnionFunding": {
                    "projectName": "for FS updating from 2021 year",
                    "projectIdentifier": "for FS updating from 2021 year",
                    "uri": "for FS updating from 2021 year"
                },
                "isEuropeanUnionFunded": True,
                "verified": False,
                "sourceEntity": {
                    "id": "MD-IDNO-380632074071",
                    "name": "LLC Petrusenko"
                },
                "verificationDetails": None,
                "project": "for FS updating from 2021 year",
                "projectID": "for FS updating from 2021 year",
                "uri": "for FS updating from 2021 year"
            },
            "rationale": "for FS updating from 2021 year"
        },
        "payer": {
            "id": "MD-IDNO-123456789000",
            "name": "Procuring Entity Name",
            "identifier": {
                "id": "123456789000",
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
        "id": fs_ocid + "-" + f"{timestamp}",
        "date": f"{time_at_now}",
        "tag": ["planning"],
        "initiationType": "tender",
        "tender": {
            "id": "d5752f3a-40b1-4b0e-bbbb-98fff7e77753",
            "status": "planning",
            "statusDetails": "empty"
        },
        "parties": [{
            "id": "MD-IDNO-123456789000",
            "name": "Procuring Entity Name",
            "identifier": {
                "scheme": "MD-IDNO",
                "id": "123456789000",
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
                "description": "for FS updating from 2021 year",
                "period": {
                    "startDate": "2021-12-20T00:00:00Z",
                    "endDate": "2021-12-25T00:00:00Z"
                },
                "amount": {
                    "amount": 2000.00,
                    "currency": "EUR"
                },
                "europeanUnionFunding": {
                    "projectIdentifier": "for FS updating from 2021 year",
                    "projectName": "for FS updating from 2021 year",
                    "uri": "for FS updating from 2021 year"
                },
                "isEuropeanUnionFunded": True,
                "verified": False,
                "sourceEntity": {
                    "id": "MD-IDNO-380632074071",
                    "name": "LLC Petrusenko"
                },
                "project": "for FS updating from 2021 year",
                "projectID": "for FS updating from 2021 year",
                "uri": "for FS updating from 2021 year"
            },
            "rationale": "for FS updating from 2021 year"
        },
        "relatedProcesses": [{
            "id": "376490a0-529e-11eb-a7d4-3b1c06125f07",
            "relationship": ["parent"],
            "scheme": "ocid",
            "identifier": cpid,
            "uri": f"http://dev.public.eprocurement.systems/budgets/{cpid}/{cpid}"
        }]
    }

    json_budget_compiled_release_fs = {
        "ocid": fs_ocid,
        "id": fs_ocid + "-" + f"{timestamp}",
        "date": f"{time_at_now}",
        "tag": ["planning"],
        "initiationType": "tender",
        "tender": {
            "id": "d5752f3a-40b1-4b0e-bbbb-98fff7e77753",
            "status": "planning",
            "statusDetails": "empty"
        },
        "parties": [{
            "id": "MD-IDNO-123456789000",
            "name": "Procuring Entity Name",
            "identifier": {
                "scheme": "MD-IDNO",
                "id": "123456789000",
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
                "description": "for FS updating from 2021 year",
                "period": {
                    "startDate": "2021-12-20T00:00:00Z",
                    "endDate": "2021-12-25T00:00:00Z"
                },
                "amount": {
                    "amount": 3000.99,
                    "currency": "EUR"
                },
                "europeanUnionFunding": {
                    "projectIdentifier": "for FS updating from 2021 year",
                    "projectName": "for FS updating from 2021 year",
                    "uri": "for FS updating from 2021 year"
                },
                "isEuropeanUnionFunded": True,
                "verified": False,
                "sourceEntity": {
                    "id": "MD-IDNO-380632074071",
                    "name": "LLC Petrusenko"
                },
                "project": "for FS updating from 2021 year",
                "projectID": "for FS updating from 2021 year",
                "uri": "for FS updating from 2021 year"
            },
            "rationale": "for FS updating from 2021 year"
        },
        "relatedProcesses": [{
            "id": "376490a0-529e-11eb-a7d4-3b1c06125f07",
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
                    f"1609943491271,1609943491271,'{cpid + '-' + f'{timestamp}'}',"
                    f"'EI');").one()

    session.execute(f"INSERT INTO budget_ei (cp_id,token_entity,created_date,json_data,owner) VALUES("
                    f"'{cpid}',{ei_token},1609927348000,'{json.dumps(json_budget_ei)}','{owner}');").one()

    session.execute(f"INSERT INTO orchestrator_context (cp_id,context) VALUES ("
                    f"'{cpid}','{json.dumps(json_orchestrator_context)}');").one()

    session.execute(
        f"INSERT INTO budget_fs (cp_id,token_entity,amount,amount_reserved,created_date,json_data,oc_id,owner) "
        f"VALUES ('{cpid}',{fs_token},8000.00,0,{timestamp},'{json.dumps(json_budget_fs)}','{fs_ocid}','{owner}');").one()

    session.execute(f"INSERT INTO notice_budget_offset (cp_id,release_date) "
                    f"VALUES ('{cpid}',{timestamp});").one()

    session.execute(
        f"INSERT INTO notice_budget_release (cp_id,oc_id,release_id,json_data,release_date,stage) "
        f"VALUES ('{cpid}','{fs_ocid}','{fs_ocid + '-' + str(timestamp)}','{json.dumps(json_notice_budget_release_fs)}',"
        f"1610212505151,'FS');").one()

    session.execute(
        f"INSERT INTO notice_budget_compiled_release (cp_id,oc_id,amount,json_data,publish_date,release_date,"
        f"release_id,stage) VALUES ('{cpid}','{fs_ocid}',8000.00,'{json.dumps(json_budget_compiled_release_fs)}',{timestamp},"
        f"{timestamp},'{fs_ocid + '-' + str(timestamp)}','FS');")

    return f"http://dev.public.eprocurement.systems/budgets/{cpid}/{fs_ocid}", fs_token, fs_ocid
