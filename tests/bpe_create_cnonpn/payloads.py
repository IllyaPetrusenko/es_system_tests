from tests.iStorage import Document
from useful_functions import create_enquiry_and_tender_period, get_contract_period, get_new_period

enquiry_and_tender_period = create_enquiry_and_tender_period()
document_one = Document("/home/roman/Documents/git/es_system_tests/API.pdf", "API.pdf")
document_one_was_uploaded = document_one.uploading_document()

document_two = Document("/home/roman/Documents/git/es_system_tests/API.pdf", "API.pdf")
document_two_was_uploaded = document_two.uploading_document()

document_three = Document("/home/roman/Documents/git/es_system_tests/API.pdf", "API.pdf")
document_three_was_uploaded = document_three.uploading_document()

document_four = Document("/home/roman/Documents/git/es_system_tests/API.pdf", "API.pdf")
document_four_was_uploaded = document_four.uploading_document()

contract_period = get_contract_period()
period = get_new_period()

payload_cnonpn_auction_full_data_model = {
    "planning": {
        "rationale": "reason for budget in CN",
        "budget": {
            "description": "description of budget in CN"
        }
    },
    "tender": {
        "title": "title of tender in CN",
        "description": "description of tender in CN",
        "procurementMethodRationale": "procurementMethodRationale in CN",
        "procurementMethodAdditionalInfo": "procurementMethodAdditionalInfo in CN",
        "awardCriteria": "costOnly",
        "awardCriteriaDetails": "automated",
        "tenderPeriod": {
            "endDate": enquiry_and_tender_period[3]
        },
        "enquiryPeriod": {
            "endDate": enquiry_and_tender_period[1]
        },
        "procurementMethodModalities": [
            "electronicAuction"
        ],
        "electronicAuctions": {
            "details": [
                {
                    "id": "1",
                    "relatedLot": "1",
                    "electronicAuctionModalities": [
                        {
                            "eligibleMinimumDifference": {
                                "amount": 100.00,
                                "currency": "EUR"
                            }
                        }
                    ]
                }
            ]
        },
        "procuringEntity": {
            "id": "MD-IDNO-4",
            "persones": [
                {
                    "title": "title of person",
                    "name": "name of person",
                    "identifier": {
                        "scheme": "MD-IDNO",
                        "id": "2",
                        "uri": "http://person.ua/"
                    },
                    "businessFunctions": [
                        {
                            "id": "1",
                            "type": "chairman",
                            "jobTitle": "Chief Executive Officer",
                            "period": {
                                "startDate": period[2]
                            },
                            "documents": [
                                {
                                    "id": document_one_was_uploaded[0]["data"]["id"],
                                    "documentType": "regulatoryDocument",
                                    "title": "title of businessFunctions document",
                                    "description": "description of businessFunctions document"
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        "criteria": [
            {
                "id": "1",
                "title": "Bankruptcy",
                "relatesTo": "tenderer",
                "classification": {
                    "id": "CRITERION.SELECTION.ECONOMIC_FINANCIAL_STANDING.TURNOVER.GENERAL_YEARLY",
                    "scheme": "ESPD"
                },
                "description": "Is the economic operator bankrupt?",
                "requirementGroups": [
                    {
                        "id": "1",
                        "requirements": [
                            {
                                "id": "1",
                                "title": "Your answer?",
                                "dataType": "string",
                                "expectedValue": "string",
                                "eligibleEvidences": [
                                    {
                                        "id": "1",
                                        "title": "title of eligibleEvidences 1",
                                        "description": "description of eligibleEvidences 1",
                                        "type": "document",
                                        "relatedDocument": {
                                            "id": document_two_was_uploaded[0]["data"]["id"]
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "id": "2",
                "title": "Product warranty",
                "relatesTo": "item",
                "relatedItem": "1",
                "classification": {
                    "id": "CRITERION.EXCLUSION.CONVICTIONS.PARTICIPATION_IN_CRIMINAL_ORGANISATION",
                    "scheme": "ESPD"
                },
                "description": "A minimum product warranty of 1 year is required for all bids.",
                "requirementGroups": [
                    {
                        "id": "2",
                        "requirements": [
                            {
                                "id": "2",
                                "title": "A minimum product warranty of 1 year is guaranteed",
                                "dataType": "boolean",
                                "expectedValue": True
                            }
                        ]
                    }
                ]
            },
            {
                "id": "3",
                "title": "Product",
                "relatesTo": "tender",
                "classification": {
                    "id": "CRITERION.EXCLUSION.NATIONAL.OTHER",
                    "scheme": "ESPD"
                },
                "description": "Country of origin",
                "requirementGroups": [
                    {
                        "id": "3",
                        "requirements": [
                            {
                                "id": "3",
                                "title": "Product has to be manufactured in the EU",
                                "dataType": "boolean",
                                "expectedValue": True
                            }]}]},
            {
                "id": "4",
                "title": "Product warranty 2",
                "relatesTo": "tender",
                "classification": {
                    "id": "CRITERION.OTHER.EO_DATA.SHELTERED_WORKSHOP",
                    "scheme": "ESPD"
                },
                "description": "A minimum product warranty of 1 year is required for all bids 2",
                "requirementGroups": [
                    {
                        "id": "4",
                        "requirements": [
                            {
                                "id": "4",
                                "title": "The number of years for proposed product warranty",
                                "dataType": "number",
                                "minValue": 1.0,
                                "maxValue": 3.0,
                                "period": {
                                    "startDate": period[2],
                                    "endDate": period[4]
                                }
                            }
                        ]
                    }
                ]
            }, {
                "id": "5",
                "title": "Product 2",
                "relatesTo": "tenderer",
                "classification": {
                    "id": "CRITERION.OTHER.EO_DATA.RELIES_ON_OTHER_CAPACITIES",
                    "scheme": "ESPD"
                },
                "description": "Country of origin",
                "requirementGroups": [
                    {
                        "id": "5",
                        "requirements": [
                            {
                                "id": "5",
                                "title": "Country of origin",
                                "dataType": "string"
                            }
                        ]
                    }
                ]
            }
        ],
        "conversions": [
            {
                "id": "conversion 1",
                "relatesTo": "requirement",
                "relatedItem": "4",
                "rationale": "Number of years for product guarantee",
                "description": "description of conversion 1",
                "coefficients": [
                    {
                        "id": "coefficient-1",
                        "value": 1.0,
                        "coefficient": 1
                    },
                    {
                        "id": "coefficient-2",
                        "value": 2.0,
                        "coefficient": 0.8
                    },
                    {
                        "id": "coefficient-3",
                        "value": 3.0,
                        "coefficient": 0.9
                    }
                ]
            }
        ],
        "lots": [
            {
                "id": "1",
                "internalId": "internalId of lot",
                "title": "title of lot",
                "description": "description of lot",
                "value": {
                    "amount": 1500,
                    "currency": "EUR"
                },
                "contractPeriod": {
                    "startDate": contract_period[0],
                    "endDate": contract_period[1]
                },
                "placeOfPerformance": {
                    "address": {
                        "streetAddress": "street of placeOfPerformance",
                        "postalCode": "postalCode of placeOfPerformance",
                        "addressDetails": {
                            "country": {
                                "id": "MD"
                            },
                            "region": {
                                "id": "5700000"
                            },
                            "locality": {
                                "scheme": "CUATM",
                                "id": "5711001",
                                "description": "description of locality"
                            }
                        }
                    },
                    "description": "description of placeOfPerformance"
                },
                "hasOptions": True,
                "options": [
                    {
                        "description": "The buyer has the option to buy an additional hundred uniforms.",
                        "period": {
                            "durationInDays": 180,
                            "startDate": period[2],
                            "endDate": period[3],
                            "maxExtentDate": period[3]
                        }
                    }
                ],
                "hasRecurrence": True,
                "recurrence": {
                    "dates": [
                        {
                            "startDate": period[2]
                        },
                        {
                            "startDate": period[2]
                        }
                    ],
                    "description": "The duration of this contract and recurrent contracts will not exceed three years."
                },
                "hasRenewal": True,
                "renewal": {
                    "description": "The contracting authority reserves the right to extend the term for a period or "
                                   "periods of up to 1 year with a maximum of 2 such extensions on the same terms and "
                                   "conditions, subject to the contracting authority's obligations at law.",
                    "minimumRenewals": 2,
                    "maximumRenewals": 5,
                    "period": {
                        "durationInDays": 365,
                        "startDate": period[2],
                        "endDate": period[1],
                        "maxExtentDate": period[3]
                    }
                }
            }

        ],
        "items": [
            {
                "id": "1",
                "internalId": "internalId of item",
                "classification": {
                    "id": "45112350-3"
                },
                "additionalClassifications": [
                    {
                        "id": "AA12-4"
                    }
                ],
                "quantity": 10,
                "unit": {
                    "id": "10"
                },
                "description": "description of item",
                "relatedLot": "1"
            }

        ],
        "documents": [
            {
                "documentType": "illustration",
                "id": document_one_was_uploaded[0]["data"]["id"],
                "title": "title of document 1",
                "description": "description of of document 1",
                "relatedLots": [
                    "1"
                ]
            },
            {
                "documentType": "illustration",
                "id": document_three_was_uploaded[0]["data"]["id"],
                "title": "title of document 2",
                "description": "description of of document 2",
                "relatedLots": [
                    "1"
                ]
            },
{
                "documentType": "illustration",
                "id": document_two_was_uploaded[0]["data"]["id"],
                "title": "title of document 1",
                "description": "description of of document 1",
                "relatedLots": [
                    "1"
                ]
            }
        ]
    }
}

payload_cnonpn_obligatory_data_model = {
    "tender": {
        "awardCriteria": "priceOnly",
        "awardCriteriaDetails": "automated",
        "tenderPeriod": {
            "endDate": enquiry_and_tender_period[3]
        },
        "enquiryPeriod": {
            "endDate": enquiry_and_tender_period[1]
        },
        "lots": [
            {
                "id": "1",
                "title": "title of lot",
                "description": "description of lot",
                "value": {
                    "amount": 1500,
                    "currency": "EUR"
                },
                "contractPeriod": {
                    "startDate": contract_period[0],
                    "endDate": contract_period[1]
                },
                "placeOfPerformance": {
                    "address": {
                        "streetAddress": "street of placeOfPerformance",
                        "addressDetails": {
                            "country": {
                                "id": "MD"
                            },
                            "region": {
                                "id": "5700000"
                            },
                            "locality": {
                                "scheme": "CUATM",
                                "id": "5711001",
                                "description": "description of locality"
                            }
                        }
                    }
                }
            }
        ],
        "items": [
            {
                "id": "{{item_id_1}}",
                "classification": {
                    "id": "45112350-3"
                },
                "quantity": 10,
                "unit": {
                    "id": "10"
                },
                "description": "description of item",
                "relatedLot": "1"
            }
        ],
        "documents": [
            {
                "documentType": "illustration",
                "id": document_one_was_uploaded[0]["data"]["id"],
                "title": "title of document"
            }
        ]
    }
}
