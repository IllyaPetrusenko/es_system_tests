import uuid

import requests

from useful_functions import get_period, get_contract_period

period = get_period()
contract_period = get_contract_period()


class MdmService:
    def __init__(self, instance, lang='ro', country='MD', region="3400000", locality="3401000", currency="EUR",
                 procuring_entity_name="Procuring Entity Name", procuring_entity_identifier_id="123456789000",
                 procuring_entity_identifier_scheme="MD-IDNO", procuring_entity_identifier_legal_name="Legal Name",
                 procuring_entity_contact_point_name="contact person", lot_country='MD', lot_region='3400000',
                 lot_locality='3401000',
                 procuring_entity_contact_point_email="string@mail.ccc",
                 procuring_entity_contact_point_telephone="98-79-87"):
        self.lot_country = lot_country
        self.lot_region = lot_region
        self.lot_locality = lot_locality
        self.procuring_entity_contact_point_telephone = procuring_entity_contact_point_telephone
        self.procuring_entity_contact_point_email = procuring_entity_contact_point_email
        self.procuring_entity_contact_point_name = procuring_entity_contact_point_name
        self.procuring_entity_identifier_legal_name = procuring_entity_identifier_legal_name
        self.procuring_entity_identifier_scheme = procuring_entity_identifier_scheme
        self.procuring_entity_identifier_id = procuring_entity_identifier_id
        self.procuring_entity_name = procuring_entity_name
        self.currency = currency
        self.instance = instance
        self.lang = lang
        self.country = country
        self.region = region
        self.locality = locality
        if instance == "dev":
            self.host_of_services = "http://10.0.20.126:9161"
        elif instance == "sandbox":
            self.host_of_services = "http://10.0.10.116:9161"

    def get_country(self):
        country = requests.get(
            url=self.host_of_services + "/addresses/countries/" + self.country,
            params={
                'lang': self.lang
            }
        )
        return country

    def get_region(self):
        region = requests.get(
            url=self.host_of_services + "/addresses/countries/" + self.country + "/regions/" + self.region,
            params={
                'lang': self.lang
            }
        )
        return region

    def get_locality(self):
        url = self.host_of_services + "/addresses/countries/" + self.country + "/regions/" + self.region + \
              "/localities/" + self.locality
        locality = requests.get(
            url=url,
            params={
                'lang': self.lang
            }
        )
        return locality

    def process_fs_data(self, cp_id):
        data = requests.post(
            url=self.host_of_services + "/command",
            json={
                "id": str(uuid.uuid1()),
                "command": "processFsData",
                "context": {
                    "operationId": str(uuid.uuid4()),
                    "requestId": str(uuid.uuid1()),
                    "cpid": cp_id,
                    "stage": "FS",
                    "processType": "fs",
                    "operationType": "createFS",
                    "owner": "445f6851-c908-407d-9b45-14b92f3e964b",
                    "country": self.country,
                    "language": self.lang,
                    "startDate": period[0],
                    "timeStamp": period[2],
                    "isAuction": False
                },
                "data": {
                    "planning": {
                        "budget": {
                            "amount": {
                                "currency": self.currency
                            }
                        }
                    },
                    "tender": {
                        "procuringEntity": {
                            "name": self.procuring_entity_name,
                            "identifier": {
                                "id": self.procuring_entity_identifier_id,
                                "scheme": self.procuring_entity_identifier_scheme,
                                "legalName": self.procuring_entity_identifier_legal_name
                            },
                            "address": {
                                "streetAddress": "street",
                                "addressDetails": {
                                    "country": {
                                        "id": self.country
                                    },
                                    "region": {
                                        "id": self.region
                                    },
                                    "locality": {
                                        "scheme": "CUATM",
                                        "id": self.locality,
                                        "description": ""
                                    }
                                }
                            },
                            "contactPoint": {
                                "name": self.procuring_entity_contact_point_name,
                                "email": self.procuring_entity_contact_point_email,
                                "telephone": self.procuring_entity_contact_point_telephone
                            }
                        }
                    },
                    "buyer": None
                },
                "version": "0.0.1"
            }
        )
        return data

    def process_tender_data(self, pmd):
        data = requests.post(
            url=self.host_of_services + "/command",
            json={
                "id": str(uuid.uuid1()),
                "command": "processTenderData",
                "context": {
                    "operationId": str(uuid.uuid4()),
                    "requestId": str(uuid.uuid1()),
                    "stage": "PN",
                    "processType": "createPN",
                    "operationType": "createPN",
                    "phase": "planning",
                    "owner": "445f6851-c908-407d-9b45-14b92f3e964b",
                    "country": self.country,
                    "language": self.lang,
                    "pmd": pmd,
                    "startDate": period[0],
                    "timeStamp": period[2],
                    "isAuction": False,
                    "testMode": False
                },
                "data": {
                    "tender": {
                        "lots": [{
                            "id": "1",
                            "internalId": "lot 1",
                            "title": "title",
                            "description": "description",
                            "value": {
                                "amount": 1500.0,
                                "currency": self.currency
                            },
                            "contractPeriod": {
                                "startDate": contract_period[0],
                                "endDate": contract_period[1]
                            },
                            "placeOfPerformance": {
                                "address": {
                                    "streetAddress": "street",
                                    "postalCode": "150009",
                                    "addressDetails": {
                                        "country": {
                                            "id": self.lot_country
                                        },
                                        "region": {
                                            "id": self.lot_region
                                        },
                                        "locality": {
                                            "scheme": "CUATM",
                                            "id": self.lot_locality,
                                            "description": "description"
                                        }
                                    }
                                },
                                "description": "description of lot"
                            }
                        }, {
                            "id": "2",
                            "internalId": "lot 2",
                            "title": "title",
                            "description": "description",
                            "value": {
                                "amount": 150.0,
                                "currency": self.currency
                            },
                            "contractPeriod": {
                                "startDate": contract_period[0],
                                "endDate": contract_period[1]
                            },
                            "placeOfPerformance": {
                                "address": {
                                    "streetAddress": "street",
                                    "postalCode": "150009",
                                    "addressDetails": {
                                        "country": {
                                            "id": self.lot_country
                                        },
                                        "region": {
                                            "id": self.lot_region
                                        },
                                        "locality": {
                                            "scheme": "CUATM",
                                            "id": self.lot_locality,
                                            "description": "description"
                                        }
                                    }
                                },
                                "description": "description of lot"
                            }
                        }],
                        "procuringEntity": {
                            "name": "name of PE",
                            "identifier": {
                                "scheme": "MD-IDNO",
                                "id": "123654789000",
                                "legalName": "legal name",
                                "uri": "uri"
                            },
                            "contactPoint": {
                                "name": "name",
                                "email": "email",
                                "telephone": "456-95-96",
                                "faxNumber": "fax-number",
                                "url": "url"
                            },
                            "additionalIdentifiers": [{
                                "scheme": "md-idno",
                                "id": "445521",
                                "legalName": "legalName",
                                "uri": "uri"
                            }],
                            "address": {
                                "streetAddress": "street address",
                                "postalCode": "02232",
                                "addressDetails": {
                                    "country": {
                                        "id": self.country
                                    },
                                    "region": {
                                        "id": self.region
                                    },
                                    "locality": {
                                        "scheme": "other",
                                        "id": self.locality,
                                        "description": "desc",
                                        "uri": "www segodnya"
                                    }
                                }
                            }
                        },
                        "classification": {
                            "id": "45112300"
                        },
                        "items": [{
                            "id": "1",
                            "internalId": "item 1",
                            "classification": {
                                "id": "45112350-3"
                            },
                            "additionalClassifications": [{
                                "id": "AA12-4"
                            }],
                            "quantity": 0.01,
                            "unit": {
                                "id": "10"
                            },
                            "description": "description",
                            "relatedLot": "1"
                        }, {
                            "id": "2",
                            "internalId": "item 2",
                            "classification": {
                                "id": "45112360-6"
                            },
                            "additionalClassifications": [{
                                "id": "AA12-4"
                            }],
                            "quantity": 0.01,
                            "unit": {
                                "id": "10"
                            },
                            "description": "description",
                            "relatedLot": "2"
                        }]
                    }
                },
                "version": "0.0.1"
            }
        )
        return data
