import uuid

import requests

from useful_functions import get_period, get_contract_period

period = get_period()
contract_period = get_contract_period()


class MdmService:
    def __init__(self, instance, lang='ro', country_id='MD', region_id='1700000', locality_id='1701000',
                 ei_tender_classification_id='45100000-8', ei_tender_item_classification_id='45100000-8',
                 ei_tender_item_additional_classifications_id='AA12-4', ei_tender_item_unit_id='10',
                 ei_tender_items_delivery_details_country_id='MD', ei_tender_items_delivery_details_region_id='3400000',
                 ei_tender_items_delivery_details_locality_scheme='CUATM',
                 ei_tender_items_delivery_details_locality_id='3401000', buyer_address_details_country_id='MD',
                 buyer_address_details_region_id='1700000', buyer_address_details_locality_scheme='CUATM',
                 buyer_address_details_locality_id='1701000', currency='EUR', payer_address_details_country_id='MD',
                 payer_address_details_region_id='1700000', payer_address_details_locality_scheme='CUATM',
                 payer_address_details_locality_id='1701000', funder_address_details_country_id='MD',
                 funder_address_details_region_id='1700000', funder_address_details_locality_scheme='CUATM',
                 funder_address_details_locality_id='1701000', pn_lot_address_details_country_id='MD',
                 pn_lot_address_details_region_id='1700000', pn_lot_address_details_locality_scheme='CUATM',
                 pn_lot_address_details_locality_id='1701000', procuring_address_details_country_id='MD',
                 procuring_address_details_region_id='1700000', procuring_address_details_locality_scheme='CUATM',
                 procuring_address_details_locality_id='1701000', pn_tender_classification_id='45112300',
                 pn_tender_item_one_classification_id='45112350-3',
                 pn_tender_item_one_additional_classifications_id='AA12-4', pn_tender_item_one_unit_id='10',
                 pn_tender_item_two_classification_id='45112360-6',
                 pn_tender_item_two_additional_classifications_id='AA12-4', pn_tender_item_two_unit_id='10'
                 ):
        if instance == "dev":
            self.host_of_services = "http://10.0.20.126:9161"
        elif instance == "sandbox":
            self.host_of_services = "http://10.0.10.116:9161"
        self.lang = lang
        self.country_id = country_id
        self.region_id = region_id
        self.locality_id = locality_id
        self.ei_tender_classification_id = ei_tender_classification_id
        self.ei_tender_item_classification_id = ei_tender_item_classification_id
        self.ei_tender_item_additional_classifications_id = ei_tender_item_additional_classifications_id
        self.ei_tender_item_unit_id = ei_tender_item_unit_id
        self.ei_tender_items_delivery_details_country_id = ei_tender_items_delivery_details_country_id
        self.ei_tender_items_delivery_details_region_id = ei_tender_items_delivery_details_region_id
        self.ei_tender_items_delivery_details_locality_scheme = ei_tender_items_delivery_details_locality_scheme
        self.ei_tender_items_delivery_details_locality_id = ei_tender_items_delivery_details_locality_id
        self.buyer_address_details_country_id = buyer_address_details_country_id
        self.buyer_address_details_region_id = buyer_address_details_region_id
        self.buyer_address_details_locality_scheme = buyer_address_details_locality_scheme
        self.buyer_address_details_locality_id = buyer_address_details_locality_id
        self.currency = currency
        self.payer_address_details_country_id = payer_address_details_country_id
        self.payer_address_details_region_id = payer_address_details_region_id
        self.payer_address_details_locality_scheme = payer_address_details_locality_scheme
        self.payer_address_details_locality_id = payer_address_details_locality_id
        self.funder_address_details_country_id = funder_address_details_country_id
        self.funder_address_details_region_id = funder_address_details_region_id
        self.funder_address_details_locality_scheme = funder_address_details_locality_scheme
        self.funder_address_details_locality_id = funder_address_details_locality_id
        self.pn_lot_address_details_country_id = pn_lot_address_details_country_id
        self.pn_lot_address_details_region_id = pn_lot_address_details_region_id
        self.pn_lot_address_details_locality_scheme = pn_lot_address_details_locality_scheme
        self.pn_lot_address_details_locality_id = pn_lot_address_details_locality_id
        self.procuring_address_details_country_id = procuring_address_details_country_id
        self.procuring_address_details_region_id = procuring_address_details_region_id
        self.procuring_address_details_locality_scheme = procuring_address_details_locality_scheme
        self.procuring_address_details_locality_id = procuring_address_details_locality_id
        self.pn_tender_classification_id = pn_tender_classification_id
        self.pn_tender_item_one_classification_id = pn_tender_item_one_classification_id
        self.pn_tender_item_one_additional_classifications_id = pn_tender_item_one_additional_classifications_id
        self.pn_tender_item_one_unit_id = pn_tender_item_one_unit_id
        self.pn_tender_item_two_classification_id = pn_tender_item_two_classification_id
        self.pn_tender_item_two_additional_classifications_id = pn_tender_item_two_additional_classifications_id
        self.pn_tender_item_two_unit_id = pn_tender_item_two_unit_id

    def get_country(self):
        country = requests.get(
            url=self.host_of_services + "/addresses/countries/" + self.country_id,
            params={
                'lang': self.lang
            }
        )
        return country

    def get_region(self):
        region = requests.get(
            url=self.host_of_services + "/addresses/countries/" + self.country_id + "/regions/" + self.region_id,
            params={
                'lang': self.lang
            }
        )
        return region

    def get_locality(self):
        url = self.host_of_services + "/addresses/countries/" + self.country_id + "/regions/" + self.region_id + \
              "/localities/" + self.locality_id
        locality = requests.get(
            url=url,
            params={
                'lang': self.lang
            }
        )
        return locality

    def process_ei_data(self):
        data = requests.post(
            url=self.host_of_services + "/command",
            json={
                "id": str(uuid.uuid1()),
                "command": "processEiData",
                "context": {
                    "operationId": str(uuid.uuid4()),
                    "requestId": str(uuid.uuid1()),
                    "stage": "EI",
                    "processType": "ei",
                    "operationType": "createEI",
                    "owner": "445f6851-c908-407d-9b45-14b92f3e964b",
                    "country": self.country_id,
                    "language": self.lang,
                    "startDate": period[0],
                    "timeStamp": period[2],
                    "isAuction": False,
                    "testMode": False
                },
                "data": {
                    "tender": {
                        "classification": {
                            "id": self.ei_tender_classification_id
                        },
                        "items": [{
                            "id": "1",
                            "description": "item 1",
                            "classification": {
                                "id": self.ei_tender_item_classification_id
                            },
                            "additionalClassifications": [{
                                "id": self.ei_tender_item_additional_classifications_id
                            }],
                            "deliveryAddress": {
                                "streetAddress": "street",
                                "postalCode": "postal",
                                "addressDetails": {
                                    "country": {
                                        "id": self.ei_tender_items_delivery_details_country_id
                                    },
                                    "region": {
                                        "id": self.ei_tender_items_delivery_details_region_id
                                    },
                                    "locality": {
                                        "id": self.ei_tender_items_delivery_details_locality_id,
                                        "description": "qwe",
                                        "scheme": self.ei_tender_items_delivery_details_locality_scheme
                                    }
                                }
                            },
                            "quantity": 1,
                            "unit": {
                                "id": self.ei_tender_item_unit_id
                            }
                        }]
                    },
                    "buyer": {
                        "name": "buyer",
                        "identifier": {
                            "id": "1",
                            "scheme": "MD-IDNO",
                            "legalName": "Directia Cultura a Primariei mun.Chisinau",
                            "uri": "uri"
                        },
                        "address": {
                            "streetAddress": "str.Bucuresti 68",
                            "postalCode": "postal_2",
                            "addressDetails": {
                                "country": {
                                    "id": self.buyer_address_details_country_id
                                },
                                "region": {
                                    "id": self.buyer_address_details_region_id
                                },
                                "locality": {
                                    "scheme": self.buyer_address_details_locality_scheme,
                                    "id": self.buyer_address_details_locality_id,
                                    "description": "qwe"
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
                            "name": "Dumitru Popa",
                            "email": "directiacultшra@yahoo.com",
                            "telephone": "022242290",
                            "faxNumber": "fax",
                            "url": "url_3"
                        },
                        "details": {
                            "typeOfBuyer": "NATIONAL_AGENCY",
                            "mainGeneralActivity": "HEALTH",
                            "mainSectoralActivity": "WATER"
                        }
                    }
                },
                "version": "0.0.1"
            }
        )
        return data

    def process_fs_data(self, ei_id):
        data = requests.post(
            url=self.host_of_services + "/command",
            json={
                "id": str(uuid.uuid1()),
                "command": "processFsData",
                "context": {
                    "operationId": str(uuid.uuid4()),
                    "requestId": str(uuid.uuid1()),
                    "cpid": ei_id,
                    "stage": "FS",
                    "processType": "fs",
                    "operationType": "createFS",
                    "owner": "445f6851-c908-407d-9b45-14b92f3e964b",
                    "country": self.country_id,
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
                            "name": "payer",
                            "identifier": {
                                "id": "2",
                                "scheme": "MD-IDNO",
                                "legalName": "Legal Name",
                                "uri": "http://454.to"
                            },
                            "additionalIdentifiers": [{
                                "id": "additional identifier",
                                "scheme": "MD-K",
                                "legalName": "legalname",
                                "uri": "http://k.to"
                            }],
                            "address": {
                                "streetAddress": "street",
                                "postalCode": "785412",
                                "addressDetails": {
                                    "country": {
                                        "id": self.payer_address_details_country_id
                                    },
                                    "region": {
                                        "id": self.payer_address_details_region_id
                                    },
                                    "locality": {
                                        "scheme": self.payer_address_details_locality_scheme,
                                        "id": self.payer_address_details_locality_id,
                                        "description": "qwe"
                                    }
                                }
                            },
                            "contactPoint": {
                                "name": "contact person",
                                "email": "string@mail.ccc",
                                "telephone": "98-79-87",
                                "faxNumber": "78-56-55",
                                "url": "http://url.com"
                            }
                        }
                    },
                    "buyer": {
                        "name": "funder",
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
                                    "id": self.funder_address_details_country_id
                                },
                                "region": {
                                    "id": self.funder_address_details_region_id
                                },
                                "locality": {
                                    "scheme": self.funder_address_details_locality_scheme,
                                    "id": self.funder_address_details_locality_id,
                                    "description": "qwe"
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
                    }
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
                    "country": self.country_id,
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
                                            "id": self.pn_lot_address_details_country_id
                                        },
                                        "region": {
                                            "id": self.pn_lot_address_details_region_id
                                        },
                                        "locality": {
                                            "scheme": self.pn_lot_address_details_locality_scheme,
                                            "id": self.pn_lot_address_details_locality_id,
                                            "description": "qwe"
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
                                            "id": self.pn_lot_address_details_country_id
                                        },
                                        "region": {
                                            "id": self.pn_lot_address_details_region_id
                                        },
                                        "locality": {
                                            "scheme": self.pn_lot_address_details_locality_scheme,
                                            "id": self.pn_lot_address_details_locality_id,
                                            "description": "qwe"
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
                                        "id": self.procuring_address_details_country_id
                                    },
                                    "region": {
                                        "id": self.procuring_address_details_region_id
                                    },
                                    "locality": {
                                        "scheme": self.procuring_address_details_locality_scheme,
                                        "id": self.procuring_address_details_locality_id,
                                        "description": "qwe"

                                    }
                                }
                            }
                        },
                        "classification": {
                            "id": self.pn_tender_classification_id
                        },
                        "items": [{
                            "id": "1",
                            "internalId": "item 1",
                            "classification": {
                                "id": self.pn_tender_item_one_classification_id
                            },
                            "additionalClassifications": [{
                                "id": self.pn_tender_item_one_additional_classifications_id
                            }],
                            "quantity": 0.01,
                            "unit": {
                                "id": self.pn_tender_item_one_unit_id
                            },
                            "description": "description",
                            "relatedLot": "1"
                        }, {
                            "id": "2",
                            "internalId": "item 2",
                            "classification": {
                                "id": self.pn_tender_item_two_classification_id
                            },
                            "additionalClassifications": [{
                                "id": self.pn_tender_item_two_additional_classifications_id
                            }],
                            "quantity": 0.01,
                            "unit": {
                                "id": self.pn_tender_item_two_unit_id
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
