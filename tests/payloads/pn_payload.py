import random
from useful_functions import get_contract_period
from tests.iStorage import Document

document = Document(instance="dev",
                    path="/home/roman/Documents/git/es_system_tests/API.pdf",
                    file_name="API.pdf")
document_one_was_uploaded = document.uploading_document()
document_two_was_uploaded = document.uploading_document()

period = get_contract_period()
legal_basis = ("DIRECTIVE_2014_23_EU",
               "DIRECTIVE_2014_24_EU",
               "DIRECTIVE_2014_25_EU",
               "DIRECTIVE_2009_81_EC",
               "REGULATION_966_2012",
               "NATIONAL_PROCUREMENT_LAW",)
create_pn_payload_obligatory_data_model_without_documents = {
    "planning": {
        "budget": {
            "budgetBreakdown": [
                {
                    "id": "fs-id",
                    "amount": {
                        "amount": 2000.0,
                        "currency": "EUR"
                    }
                }
            ]
        }
    },
    "tender": {
        "title": "PN tender.title",
        "description": "PN  tender.description",
        "legalBasis": f'{random.choice(legal_basis)}',
        "tenderPeriod": {
            "startDate": period[2]
        },
        "procuringEntity": {
            "name": "uStudio QA Team",
            "identifier": {
                "scheme": "MD-IDNO",
                "id": "111-111",
                "legalName": "uStudio QA Team LLC"
            },
            "address": {
                "streetAddress": "Mircea cel Batrin bd. nr.7  of.151",
                "addressDetails": {
                    "country": {
                        "id": "MD"
                    },
                    "region": {
                        "id": "0101000"
                    },
                    "locality": {
                        "scheme": "other",
                        "id": "999999999",
                        "description": "Chisinau"
                    }
                }
            },
            "contactPoint": {
                "name": "Ocds Ustudio",
                "email": "ocdsustudio@gmail.com",
                "telephone": "060000000"
            }
        }
    }
}

create_pn_payload_full_data_model_with_documents = {
    "planning": {
        "rationale": "reason for budget",
        "budget": {
            "description": "description of budget",
            "budgetBreakdown": [
                {
                    "id": "{{fs-id}}",
                    "amount": {
                        "amount": 2000.0,
                        "currency": "EUR"
                    }
                }
            ]
        }
    },
    "tender": {
        "title": "title of tender",
        "description": "desription of tender",
        "legalBasis": f'{random.choice(legal_basis)}',
        "procurementMethodRationale": "procurementMethodRationale",
        "procurementMethodAdditionalInfo": "procurementMethodAdditionalInfo",
        "tenderPeriod": {
            "startDate": period[2]
        },
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
            "additionalIdentifiers": [
                {
                    "scheme": "md-idno",
                    "id": "445521",
                    "legalName": "legalName",
                    "uri": "uri"
                }
            ],
            "address": {
                "streetAddress": "street address",
                "postalCode": "02232",
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
                        "description": "4596"

                    }
                }
            }
        },
        "lots": [
            {
                "id": "1",
                "internalId": "lot 1",
                "title": "title",
                "description": "description",
                "value": {
                    "amount": 1500.0,
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
                "id": "2",
                "internalId": "lot 2",
                "title": "title",
                "description": "description",
                "value": {
                    "amount": 150.0,
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
                "id": "1",
                "internalId": "item 1",
                "classification": {
                    "id": "45112350-3"
                },
                "additionalClassifications": [
                    {
                        "id": "AA12-4"

                    }
                ],
                "quantity": 0.01,
                "unit": {
                    "id": "10"

                },
                "description": "description",
                "relatedLot": "1"
            },
            {
                "id": "2",
                "internalId": "item 2",
                "classification": {
                    "id": "45112360-6"

                },
                "additionalClassifications": [
                    {
                        "id": "AA12-4"

                    }
                ],
                "quantity": 0.01,
                "unit": {
                    "id": "10"

                },
                "description": "description",
                "relatedLot": "2"
            }

        ],
        "documents": [
            {
                "documentType": "contractArrangements",
                "id": document_one_was_uploaded[0]["data"]["id"],
                "title": "title of document",
                "description": "descrition of document",
                "relatedLots": [
                    "1"
                ]
            },
            {
                "documentType": "contractArrangements",
                "id": document_two_was_uploaded[0]["data"]["id"],
                "title": "title of document",
                "description": "descrition of document",
                "relatedLots": [
                    "2"
                ]
            }
        ]
    }
}
