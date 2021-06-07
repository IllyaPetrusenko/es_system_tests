from useful_functions import create_enquiry_and_tender_period

enquiry_and_tender_period = create_enquiry_and_tender_period()
period = get_new_period()
create_cn_on_pn_payload_full_data_model_with_auction = {
    "planning": {
        "rationale": "create CNonPN: planning.rationale",
        "budget": {
            "description": "create CNonPN: planning.description"
        }
    },
    "tender": {
        "title": "create CNonPN: tender.title",
        "description": "create CNonPN: tender.description",
        "procurementMethodRationale": "create CNonPN: tender.procurementMethodRationale",
        "procurementMethodAdditionalInfo": "create CNonPN: tender.procurementMethodAdditionalInfo",
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
                    "title": "create CNonPN: procuringEntity.persones[0].title",
                    "name": "create CNonPN: procuringEntity.persones[0].name",
                    "identifier": {
                        "scheme": "MD-IDNO",
                        "id": "create CNonPN: procuringEntity.persones[0].identifier.id =1",
                        "uri": "create CNonPN: procuringEntity.persones[0].identifier.uri"
                    },
                    "businessFunctions": [
                        {
                            "id": "create CNonPN: procuringEntity.persones[0].businessFunctions[0].id =1",
                            "type": "chairman",
                            "jobTitle": "Chief Executive Officer",
                            "period": {
                                "startDate": period[2]
                            },
                            "documents": [
                                {
                                    "id": "create CNonPN: procuringEntity.persones[0].businessFunctions[0]."
                                          "documents[0].id =1",
                                    "documentType": "regulatoryDocument",
                                    "title": "create CNonPN: procuringEntity.persones[0].businessFunctions[0].title",
                                    "description": "create CNonPN: procuringEntity.persones[0].businessFunctions[0]."
                                                   "description"
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        "criteria": [
            {
                "id": "001",
                "title": "Bankruptcy",
                "relatesTo": "tender",
                "classification": {
                    "id": "CRITERION.SELECTION.ECONOMIC_FINANCIAL_STANDING.TURNOVER.GENERAL_YEARLY",
                    "scheme": "ESPD"
                },
                "description": "Is the economic operator bankrupt?",
                "requirementGroups": [
                    {
                        "id": "001-1",
                        "requirements": [
                            {
                                "id": "001-1-1",
                                "title": "Your answer?",
                                "dataType": "boolean",
                                "expectedValue": false,
                                "eligibleEvidences": [
                                    {
                                        "id": "1",
                                        "title": "title of eligibleEvidences 1",
                                        "description": "description of eligibleEvidences 1",
                                        "type": "document",
                                        "relatedDocument": {
                                            "id": "{{Document-2}}"
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "id": "002",
                "title": "Product warranty",
                "classification": {
                    "id": "CRITERION.EXCLUSION.CONVICTIONS.PARTICIPATION_IN_CRIMINAL_ORGANISATION",
                    "scheme": "ESPD"
                },
                "description": "A minimum product warranty of 1 year is required for all bids.",
                "relatesTo": "item",
                "relatedItem": "1",
                "requirementGroups": [
                    {
                        "id": "002-1",
                        "description": "A minimum product warranty of 1 year is required for all bids.",
                        "requirements": [
                            {
                                "id": "002-1-1",
                                "title": "A minimum product warranty of 1 year is guaranteed",
                                "dataType": "boolean",
                                "expectedValue": true
                            },
                            {
                                "id": "002-1-2",
                                "title": "The number of years for proposed product warranty",
                                "dataType": "number",
                                "minValue": 1.0,
                                "maxValue": 3.0,
                                "period": {
                                    "startDate": "2021-03-01T16:00:00Z",
                                    "endDate": "2021-03-30T16:00:00Z"
                                },
                                "eligibleEvidences": [
                                    {
                                        "id": "1",
                                        "title": "title of eligibleEvidences 1",
                                        "description": "description of eligibleEvidences 1",
                                        "type": "document",
                                        "relatedDocument": {
                                            "id": "{{Document-2}}"
                                        }
                                    }
                                ]
                            },

                        ]
                    }
                ]
            },
            {
                "id": "003",
                "title": "Product",
                "classification": {
                    "id": "CRITERION.EXCLUSION.NATIONAL.OTHER",
                    "scheme": "ESPD"
                },
                "description": "Country of origin",
                "relatesTo": "tender",
                "requirementGroups": [
                    {
                        "id": "003-1",
                        "requirements": [
                            {
                                "id": "003-1-1",
                                "title": "Product has to be manufactured in the EU",
                                "dataType": "boolean",
                                "expectedValue": true
                            },
                            {
                                "id": "003-1-2",
                                "title": "Country of origin",
                                "dataType": "string"
                            }
                        ]
                    }
                ]
            },
            {
                "id": "004",
                "title": "Product warranty 2",
                "relatesTo": "tender",
                "classification": {
                    "id": "CRITERION.OTHER.EO_DATA.SHELTERED_WORKSHOP",
                    "scheme": "ESPD"
                },
                "description": "A minimum product warranty of 1 year is required for all bids 2",
                "requirementGroups": [
                    {
                        "id": "004-1",
                        "requirements": [
                            {
                                "id": "004-1-1",
                                "title": "The number of years for proposed product warranty",
                                "dataType": "number",
                                "minValue": 1.0,
                                "maxValue": 3.0,
                                "period": {
                                    "startDate": "2021-03-01T16:00:00Z",
                                    "endDate": "2021-03-30T16:00:00Z"
                                }
                            }
                        ]
                    }
                ]
            }, {
                "id": "005",
                "title": "Product 2",
                "relatesTo": "",
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
                "id": "{{lot_id_1}}",
                "internalId": "internalId of lot",
                "title": "title of lot",
                "description": "description of lot",
                "value": {
                    "amount": 10000,
                    "currency": "EUR"
                },
                "contractPeriod": {
                    "startDate": "2021-03-19T16:00:00Z",
                    "endDate": "2021-03-20T16:00:00Z"
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
                "hasOptions": true,
                "options": [
                    {
                        "description": "The buyer has the option to buy an additional hundred uniforms.",
                        "period": {
                            "durationInDays": 180,
                            "startDate": "2021-02-10T00:00:00Z",
                            "endDate": "2024-02-10T00:00:00Z",
                            "maxExtentDate": "2024-02-10T00:00:00Z"
                        }
                    }
                ],
                "hasRecurrence": true,
                "recurrence": {
                    "dates": [
                        {
                            "startDate": "2020-01-01T00:00:00Z"
                        },
                        {
                            "startDate": "2021-01-01T00:00:00Z"
                        }
                    ],
                    "description": "The duration of this contract and recurrent contracts will not exceed three years."
                },
                "hasRenewal": true,
                "renewal": {
                    "description": "The contracting authority reserves the right to extend the term for a period or periods of up to 1 year with a maximum of 2 such extensions on the same terms and conditions, subject to the contracting authority's obligations at law.",
                    "minimumRenewals": 2,
                    "maximumRenewals": 5,
                    "period": {
                        "durationInDays": 365,
                        "startDate": "2021-02-10T00:00:00Z",
                        "endDate": "2024-02-10T00:00:00Z",
                        "maxExtentDate": "2024-02-10T00:00:00Z"
                    }
                }
            }
        ],
        "items": [
            {
                "id": "{{item_id_1}}",
                "internalId": "internalId of item",
                "classification": {
                    "id": "03100000-2"
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
                "relatedLot": "{{lot_id_1}}"
            }
        ],
        "documents": [
            {
                "documentType": "illustration",
                "id": "{{Document-1}}",
                "title": "title of document 1",
                "description": "description of of document 1",
                "relatedLots": [
                    "{{lot_id_1}}"
                ]
            },
            {
                "documentType": "illustration",
                "id": "{{Document-2}}",
                "title": "title of document 2",
                "description": "description of of document 2",
                "relatedLots": [
                    "{{lot_id_1}}"
                ]
            }
        ]
    }
}
