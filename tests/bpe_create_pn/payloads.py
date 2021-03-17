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


pn_create_full_data_model_with_documents = {
    "planning": {
        "rationale": "reason for budget",
        "budget": {
            "description": "description of budget",
            "budgetBreakdown": [
                {
                    "id": "{{fs-id}}",
                    "amount": {
                        "amount": 2000,
                        "currency": "EUR"
                    }
                }
            ]
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
                "id": "2",
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
                "id": document_1[0],
                "title": "title of document",
                "description": "descrition of document",
                "relatedLots": [
                    "1"
                ]
            },
            {
                "documentType": "contractArrangements",
                "id": document_2[0],
                "title": "title of document",
                "description": "descrition of document",
                "relatedLots": [

                ]
            }
        ]
    }
}

pn_create_full_data_model_without_documents = {
    "planning": {
        "rationale": "nh",
        "budget": {
            "description": "nh",
            "budgetBreakdown": [
                {
                    "id": "{{fs-id}}",
                    "amount": {
                        "amount": 2000,
                        "currency": "EUR"
                    }
                }
            ]
        }
    },
    "tender": {
        "title": "t",
        "description": "t",
        "legalBasis": "REGULATION_966_2012",
        "procurementMethodRationale": "t",
        "procurementMethodAdditionalInfo": "t",
        "tenderPeriod": {
            "startDate": period[2]
        },
        "procuringEntity": {
            "name": "t",
            "identifier": {
                "scheme": "MD-IDNO",
                "id": "t",
                "legalName": "t",
                "uri": "t"
            },
            "contactPoint": {
                "name": "t",
                "email": "t",
                "telephone": "t",
                "faxNumber": "t",
                "url": "t"
            },
            "additionalIdentifiers": [
                {
                    "scheme": "t",
                    "id": "t",
                    "legalName": "t",
                    "uri": "t"
                }
            ],
            "address": {
                "streetAddress": "t",
                "postalCode": "t",
                "addressDetails": {
                    "country": {
                        "id": "MD"
                    },
                    "region": {
                        "id": "3400000"
                    },
                    "locality": {
                        "scheme": "t",
                        "id": "t",
                        "description": "t"

                    }
                }
            }
        },
        "lots": [
            {
                "id": "t",
                "internalId": "f",
                "title": "t",
                "description": "t",
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
                        "streetAddress": "t",
                        "postalCode": "t",
                        "addressDetails": {
                            "country": {
                                "id": "MD"
                            },
                            "region": {
                                "id": "3400000"
                            },
                            "locality": {
                                "scheme": "t",
                                "id": "t",
                                "description": "t"

                            }
                        }
                    },
                    "description": "d"
                }
            }

        ],
        "items": [
            {
                "id": "f",
                "internalId": "f",
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
                "description": "t",
                "relatedLot": "t"
            }

        ]

    }
}

pn_create_obligatory_data_model_with_documents = {
    "planning": {
        "budget": {
            "budgetBreakdown": [
                {
                    "id": "{{fs-id}}",
                    "amount": {
                        "amount": 2000,
                        "currency": "EUR"
                    }
                }
            ]
        }
    },
    "tender": {
        "title": "title of tender",
        "description": "desription of tender",
        "legalBasis": "REGULATION_966_2012",
        "tenderPeriod": {
            "startDate": period[2]
        },
        "procuringEntity": {
            "name": "name of PE",
            "identifier": {
                "scheme": "MD-IDNO",
                "id": "123654789000",
                "legalName": "legal name"
            },
            "contactPoint": {
                "name": "name",
                "email": "email",
                "telephone": "456-95-96"
            },
            "address": {
                "streetAddress": "street address",
                "addressDetails": {
                    "country": {
                        "id": "MD"
                    },
                    "region": {
                        "id": "0101000"
                    },
                    "locality": {
                        "scheme": "other",
                        "id": "locality",
                        "description": "4596"
                    }
                }
            }
        },
        "documents": [
            {
                "documentType": "contractArrangements",
                "id": document_1[0],
                "title": "title of document"

            }
        ]
    }
}

pn_create_obligatory_data_model_without_documents = {
    "planning": {
        "budget": {
            "budgetBreakdown": [
                {
                    "id": "{{fs-id}}",
                    "amount": {
                        "amount": 2000,
                        "currency": "EUR"
                    }
                }
            ]
        }
    },
    "tender": {
        "title": "title of tender",
        "description": "desription of tender",
        "legalBasis": "REGULATION_966_2012",
        "tenderPeriod": {
            "startDate": period[2]
        },
        "procuringEntity": {
            "name": "name of PE",
            "identifier": {
                "scheme": "MD-IDNO",
                "id": "123654789000",
                "legalName": "legal name"
            },
            "contactPoint": {
                "name": "name",
                "email": "email",
                "telephone": "456-95-96"
            },
            "address": {
                "streetAddress": "street address",
                "addressDetails": {
                    "country": {
                        "id": "MD"
                    },
                    "region": {
                        "id": "0101000"
                    },
                    "locality": {
                        "scheme": "other",
                        "id": "locality",
                        "description": "4596"
                    }
                }
            }
        }

    }
}
