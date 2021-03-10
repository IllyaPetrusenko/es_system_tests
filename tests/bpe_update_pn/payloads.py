import os

from tests.iStorage import document_upload, get_hash_md5
from useful_functions import get_contract_period

period = get_contract_period()
path = os.path.abspath('API.pdf')
hash_sum = get_hash_md5(path)
weight = os.stat(path).st_size
payload = {
    "fileName": path,
    "hash": f"{hash_sum}",
    "weight": weight
}
dir_path = "/home/roman/Documents/git/es_system_tests/"
file_name = "API.pdf"
document_1 = document_upload(payload, dir_path, file_name)
document_2 = document_upload(payload, dir_path, file_name)

pn_update_full_data_model_with_documents = {
    "planning": {
        "rationale": "reason for budget",
        "budget": {
            "description": "description of budget"
        }
    },
    "tender": {
        "title": "title of tender",
        "description": "desription of tender",
        "legalBasis": "REGULATION_966_2012",
        "procurementMethodRationale": "procurementMethodRationale",
        "procurementMethodAdditionalInfo": "procurementMethodAdditionalInfo",
        "tenderPeriod": {
            "startDate": period[2]
        },
        "lots": [
            {
                "id": "{{lot_id_1}}",
                "internalId": "lot 1",
                "title": "title",
                "description": "descriptio",
                "value": {
                    "amount": 1500,
                    "currency": "EUR"
                },
                "contractPeriod": {
                    "startDate": period[0],
                    "endDate": period[1]
                },
                "placeOfPerformance": {
                    "address": {
                        "streetAddress": "street",
                        "postalCode": "150009",
                        "addressDetails": {
                            "country": {
                                "id": "MD"
                            },
                            "region": {
                                "id": "3400000"
                            },
                            "locality": {
                                "scheme": "CUATM",
                                "id": "3401000",
                                "description": "description"

                            }
                        }
                    },
                    "description": "description of lot"
                }
            },
            {
                "id": "{{lot_id_2}}",
                "internalId": "lot 2",
                "title": "title",
                "description": "description",
                "value": {
                    "amount": 150,
                    "currency": "EUR"
                },
                "contractPeriod": {
                    "startDate": period[0],
                    "endDate": period[1]
                },
                "placeOfPerformance": {
                    "address": {
                        "streetAddress": "street",
                        "postalCode": "150009",
                        "addressDetails": {
                            "country": {
                                "id": "MD"
                            },
                            "region": {
                                "id": "3400000"
                            },
                            "locality": {
                                "scheme": "CUATM",
                                "id": "3401000",
                                "description": "description"

                            }
                        }
                    },
                    "description": "description of lot"
                }
            }

        ],
        "items": [
            {
                "id": "{{item_id_1}}",
                "internalId": "item 1",
                "classification": {
                    "id": "45112350-3",
                    "scheme": "CPV",
                    "description": "cpv description"

                },
                "additionalClassifications": [
                    {
                        "id": "AA12-4",
                        "scheme": "CPVs",
                        "description": "cpvs description"

                    }
                ],
                "quantity": 0.01,
                "unit": {
                    "id": "10",
                    "name": "name of unit"

                },
                "description": "description",
                "relatedLot": "{{lot_id_1}}"
            },
            {
                "id": "{{item_id_2}}",
                "internalId": "item 2",
                "classification": {
                    "id": "45112360-6",
                    "scheme": "CPV",
                    "description": "cpv description"
                },
                "additionalClassifications": [
                    {
                        "id": "AA12-4",
                        "scheme": "CPVs",
                        "description": "cpvs description"

                    }
                ],
                "quantity": 0.01,
                "unit": {
                    "id": "10",
                    "name": "name of unit"

                },
                "description": "description",
                "relatedLot": "{{lot_id_2}}"
            }

        ],
        "documents": [
            {
                "documentType": "contractArrangements",
                "id": document_1[0],
                "title": "title of document",
                "description": "descrition of document",
                "relatedLots": [
                    "{{lot_id_1}}"
                ]
            },
            {
                "documentType": "contractArrangements",
                "id": document_2[0],
                "title": "title of document",
                "description": "descrition of document",
                "relatedLots": [
                    "{{lot_id_2}}"
                ]
            }
        ]
    }
}
