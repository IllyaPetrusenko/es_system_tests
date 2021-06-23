from useful_functions import create_enquiry_and_tender_period, get_new_period, get_contract_period

enquiry_and_tender_period = create_enquiry_and_tender_period(second_enquiry=300, second_tender=600)
period = get_new_period()
contract_period = get_contract_period()

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
        "awardCriteria": "ratedCriteria",
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
                },
                {
                    "id": "2",
                    "relatedLot": "2",
                    "electronicAuctionModalities": [
                        {
                            "eligibleMinimumDifference": {
                                "amount": 10.00,
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
                "title": "create CNonPN: tender.criteria[0].title =Bankruptcy",
                "relatesTo": "tender",
                "classification": {
                    "id": "CRITERION.EXCLUSION.CONVICTIONS.PARTICIPATION_IN_CRIMINAL_ORGANISATION",
                    "scheme": "ESPD"
                },
                "description": "create CNonPN: tender.criteria[0].description ="
                               "Is the economic operator bankrupt? This information needs not be given if "
                               "exclusion of economic operators in this case has been made mandatory under the "
                               "applicable national law without any possibility of derogation where the economic "
                               "operator is nevertheless able to perform the contract.",
                "requirementGroups": [
                    {
                        "id": "001-1",
                        "description": "create CNonPN: tender.criteria[0].requirementGroups[0].description ="
                                       "approve that Bankruptcy requirement group",
                        "requirements": [
                            {
                                "id": "001-1-1",
                                "title": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements.title",
                                "description": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements."
                                               "description",
                                "dataType": "boolean",
                                "expectedValue": False,
                                "eligibleEvidences": [
                                    {
                                        "id": "1",
                                        "title": "create CNonPN: tender.criteria[0].requirementGroups[0]."
                                                 "requirements[0].eligibleEvidences[0].title",
                                        "description": "create CNonPN: tender.criteria[0].requirementGroups[0]."
                                                       "requirements[0].eligibleEvidences[0].description",
                                        "type": "document",
                                        "relatedDocument": {
                                            "id": "{{Document-1}}"
                                        }
                                    },
                                    {
                                        "id": "2",
                                        "title": "create CNonPN: tender.criteria[0].requirementGroups[0]."
                                                 "requirements[0].eligibleEvidences[1].title",
                                        "description": "create CNonPN: tender.criteria[0].requirementGroups[0]."
                                                       "requirements[0].eligibleEvidences[1].description",
                                        "type": "document",
                                        "relatedDocument": {
                                            "id": "{{Document-1}}"
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
                "title": "create CNonPN: tender.criteria[1].title",
                "description": "create CNonPN: tender.criteria[1].description",
                "relatesTo": "lot",
                "relatedItem": "1",
                "classification": {
                    "id": "CRITERION.SELECTION.ECONOMIC_FINANCIAL_STANDING.TURNOVER.GENERAL_YEARLY",
                    "scheme": "ESPD"
                },
                "requirementGroups": [
                    {
                        "id": "002-1",
                        "description": "create CNonPN: tender.criteria[1].requirementGroups[0].description",
                        "requirements": [
                            {
                                "id": "002-1-1",
                                "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[0].title",
                                "description": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements."
                                               "description",
                                "dataType": "boolean",
                                "expectedValue": True
                            },
                            {
                                "id": "002-1-2",
                                "title": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[1].title "
                                         "=The number of years for proposed product warranty",
                                "description": "create CNonPN: tender.criteria[1].requirementGroups[0].requirements[1]."
                                               "description",
                                "dataType": "number",
                                "minValue": 1.0,
                                "maxValue": 3.0,
                                "period": {
                                    "startDate": period[2],
                                    "endDate": period[4]
                                },
                                "eligibleEvidences": [
                                    {
                                        "id": "3",
                                        "title": "create CNonPN: tender.criteria[1].requirementGroups[0]."
                                                 "requirements[1].eligibleEvidences[0].title",
                                        "description": "create CNonPN: tender.criteria[1].requirementGroups[0]."
                                                       "requirements[1].eligibleEvidences[0].description",
                                        "type": "document",
                                        "relatedDocument": {
                                            "id": "{{Document-1}}"
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
                "title": "create CNonPN: tender.criteria[2].title",
                "classification": {
                    "id": "CRITERION.EXCLUSION.NATIONAL.OTHER",
                    "scheme": "ESPD"
                },
                "description": "create CNonPN: tender.criteria[2].description",
                "relatesTo": "tenderer",
                "requirementGroups": [
                    {
                        "id": "003-1",
                        "description": "create CNonPN: tender.criteria[2].requirementGroups[0].description",
                        "requirements": [
                            {
                                "id": "003-1-1",
                                "title": "create CNonPN: tender.criteria[2].requirementGroups[0].requirements[0]."
                                         "title =Product has to be manufactured in the EU",
                                "dataType": "boolean",
                                "expectedValue": True
                            },
                            {
                                "id": "003-1-2",
                                "title": "create CNonPN: tender.criteria[2].requirementGroups[0]..requirements[1]."
                                         "title =Country of origin",
                                "dataType": "string"
                            }
                        ]
                    }, {
                        "id": "003-2",
                        "description": "create CNonPN: tender.criteria[2].requirementGroups[1].description",
                        "requirements": [
                            {
                                "id": "003-2-1",
                                "title": "create CNonPN: tender.criteria[2].requirementGroups[1].requirements[0]."
                                         "title =Product has to be manufactured in the EU",
                                "dataType": "boolean",
                                "expectedValue": True
                            },
                            {
                                "id": "003-2-2",
                                "title": "create CNonPN: tender.criteria[2].requirementGroups[1]..requirements[1]."
                                         "title =Country of origin",
                                "dataType": "string"
                            }
                        ]
                    }
                ]
            },
            {
                "id": "004",
                "title": "create CNonPN: tender.criteria[3].title",
                "relatesTo": "item",
                "relatedItem": "1",
                "classification": {
                    "id": "CRITERION.OTHER.EO_DATA.RELIES_ON_OTHER_CAPACITIES",
                    "scheme": "ESPD"
                },
                "description": "create CNonPN: tender.criteria[3].description ="
                               "A minimum product warranty of 1 year is required for all bids 2",
                "requirementGroups": [
                    {
                        "id": "004-1",
                        "description": "create CNonPN: tender.criteria[3].requirementGroups[0].description",
                        "requirements": [
                            {
                                "id": "004-1-1",
                                "title": "create CNonPN: tender.criteria[3].requirementGroups[0].requirements[0]."
                                         "title = The number of years for proposed product warranty",
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
                "id": "005",
                "title": "create CNonPN: tender.criteria[4].title",
                "relatesTo": "tender",
                "classification": {
                    "id": "CRITERION.EXCLUSION.NATIONAL.OTHER",
                    "scheme": "ESPD"
                },
                "description": "create CNonPN: tender.criteria[4].description",
                "requirementGroups": [
                    {
                        "id": "005-1",
                        "description": "create CNonPN: tender.criteria[4].requirementGroups[0].description",
                        "requirements": [
                            {
                                "id": "005-1-1",
                                "title": "create CNonPN: tender.criteria[4].requirementGroups[0].requirements[0]."
                                         "title =Country of origin",
                                "dataType": "string"
                            }
                        ]
                    }
                ]
            },
            {
                "id": "006",
                "title": "create CNonPN: tender.criteria[4].title",
                "relatesTo": "tender",
                "classification": {
                    "id": "CRITERION.OTHER.EO_DATA.RELIES_ON_OTHER_CAPACITIES",
                    "scheme": "ESPD"
                },
                "description": "create CNonPN: tender.criteria[4].description",
                "requirementGroups": [
                    {
                        "id": "006-1",
                        "description": "create CNonPN: tender.criteria[4].requirementGroups[0].description",
                        "requirements": [
                            {
                                "id": "006-1-1",
                                "title": "create CNonPN: tender.criteria[4].requirementGroups[0].requirements[0]."
                                         "title =Country of origin",
                                "dataType": "string"
                            }
                        ]
                    }
                ]
            }
        ],
        "conversions": [
            {
                "id": "2",
                "relatesTo": "requirement",
                "relatedItem": "002-1-1",
                "rationale": "create CNonPN: tender.conversions[1].rationale",
                "description": "create CNonPN: tender.conversions[1].description",
                "coefficients": [
                    {
                        "id": "coefficient-1",
                        "value": False,
                        "coefficient": 1
                    }
                ]
            },
            {
                "id": "3",
                "relatesTo": "requirement",
                "relatedItem": "002-1-2",
                "rationale": "create CNonPN: tender.conversions[3].rationale",
                "description": "create CNonPN: tender.conversions[3].description",
                "coefficients": [
                    {
                        "id": "coefficient-1",
                        "value": 1.0,
                        "coefficient": 1
                    },
                    {
                        "id": "coefficient-2",
                        "value": 2.0,
                        "coefficient": 1
                    },
                    {
                        "id": "coefficient-3",
                        "value": 3.0,
                        "coefficient": 0.93
                    }
                ]
            },
            {
                "id": "6",
                "relatesTo": "requirement",
                "relatedItem": "004-1-1",
                "rationale": "create CNonPN: tender.conversions[6].rationale",
                "description": "create CNonPN: tender.conversions[6].description",
                "coefficients": [
                    {
                        "id": "coefficient-1",
                        "value": 1.0,
                        "coefficient": 1
                    },
                    {
                        "id": "coefficient-2",
                        "value": 2.0,
                        "coefficient": 1
                    },
                    {
                        "id": "coefficient-3",
                        "value": 3.0,
                        "coefficient": 0.93
                    }
                ]
            },
            {
                "id": "7",
                "relatesTo": "requirement",
                "relatedItem": "006-1-1",
                "rationale": "create CNonPN: tender.conversions[6].rationale",
                "description": "create CNonPN: tender.conversions[6].description",
                "coefficients": [
                    {
                        "id": "coefficient-1",
                        "value": "option_1",
                        "relatedOption": "option_1",
                        "coefficient": 1
                    },
                    {
                        "id": "coefficient-2",
                        "value": "option_2",
                        "relatedOption": "option_2",
                        "coefficient": 1
                    },
                    {
                        "id": "coefficient-3",
                        "value": "option_3",
                        "relatedOption": "option_3",
                        "coefficient": 0.93
                    }
                ]
            }
        ],
        "lots": [
            {
                "id": "1",
                "internalId": "create CNonPN: tender.lots[0].internalId",
                "title": "create CNonPN: tender.lots[0].title",
                "description": "create CNonPN: tender.lots[0].description",
                "value": {
                    "amount": 1500.0,
                    "currency": "EUR"
                },
                "contractPeriod": {
                    "startDate": contract_period[0],
                    "endDate": contract_period[1]
                },
                "placeOfPerformance": {
                    "address": {
                        "streetAddress": "create CNonPN: tender.lots[0].placeOfPerformance.address.street",
                        "postalCode": "create CNonPN: tender.lots[0].placeOfPerformance.address.postal",
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
                                "description": "create CNonPN: tender.lots[0].placeOfPerformance.address."
                                               "addressDetails.locality.description"
                            }
                        }
                    },
                    "description": "create CNonPN: tender.lots[0].placeOfPerformance.description"
                },
                "hasOptions": True,
                "options": [
                    {
                        "description": "create CNonPN: tender.lots[0].options.description",
                        "period": {
                            "durationInDays": 180,
                            "startDate": contract_period[0],
                            "endDate": contract_period[1],
                            "maxExtentDate": contract_period[1]
                        }
                    }
                ],
                "hasRecurrence": True,
                "recurrence": {
                    "dates": [
                        {
                            "startDate": contract_period[0]
                        },
                        {
                            "startDate": contract_period[0]
                        }
                    ],
                    "description": "create CNonPN: tender.lots[0].description ="
                                   "The duration of this contract and recurrent contracts will not exceed three years."
                },
                "hasRenewal": True,
                "renewal": {
                    "description": "create CNonPN: tender.lots[0].renewal ="
                                   "The contracting authority reserves the right to extend the term for a period "
                                   "or periods of up to 1 year with a maximum of 2 such extensions on the same "
                                   "terms and conditions, subject to the contracting authority's obligations at law.",
                    "minimumRenewals": 2,
                    "maximumRenewals": 5,
                    "period": {
                        "durationInDays": 365,
                        "startDate": contract_period[0],
                        "endDate": contract_period[1],
                        "maxExtentDate": contract_period[1]
                    }
                }
            },
            {
                "id": "2",
                "internalId": "create CNonPN: tender.lots[1].internalId",
                "title": "create CNonPN: tender.lots[1].title",
                "description": "create CNonPN: tender.lots[1].description",
                "value": {
                    "amount": 100.0,
                    "currency": "EUR"
                },
                "contractPeriod": {
                    "startDate": contract_period[0],
                    "endDate": contract_period[1]
                },
                "placeOfPerformance": {
                    "address": {
                        "streetAddress": "create CNonPN: tender.lots[1].placeOfPerformance.address.street",
                        "postalCode": "create CNonPN: tender.lots[1].placeOfPerformance.address.postal",
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
                                "description": "create CNonPN: tender.lots[1].placeOfPerformance.address."
                                               "addressDetails.locality.description"
                            }
                        }
                    },
                    "description": "create CNonPN: tender.lots[1].placeOfPerformance.description"
                },
                "hasOptions": True,
                "options": [
                    {
                        "description": "create CNonPN: tender.lots[0].options.description",
                        "period": {
                            "durationInDays": 180,
                            "startDate": contract_period[0],
                            "endDate": contract_period[1],
                            "maxExtentDate": contract_period[1]
                        }
                    }
                ],
                "hasRecurrence": True,
                "recurrence": {
                    "dates": [
                        {
                            "startDate": contract_period[0]
                        },
                        {
                            "startDate": contract_period[0]
                        }
                    ],
                    "description": "create CNonPN: tender.lots[0].description ="
                                   "The duration of this contract and recurrent contracts will not exceed three years."
                },
                "hasRenewal": True,
                "renewal": {
                    "description": "create CNonPN: tender.lots[0].renewal ="
                                   "The contracting authority reserves the right to extend the term for a period "
                                   "or periods of up to 1 year with a maximum of 2 such extensions on the same "
                                   "terms and conditions, subject to the contracting authority's obligations at law.",
                    "minimumRenewals": 2,
                    "maximumRenewals": 5,
                    "period": {
                        "durationInDays": 365,
                        "startDate": contract_period[0],
                        "endDate": contract_period[1],
                        "maxExtentDate": contract_period[1]
                    }
                }
            }
        ],
        "items": [
            {
                "id": "1",
                "internalId": "create CNonPN: tender.items[0].internalId",
                "classification": {
                    "id": "45112350-3",
                    "scheme": "CPV",
                    "description": "description"
                },
                "additionalClassifications": [
                    {
                        "id": "AA12-4",
                        "scheme": "CPVS",
                        "description": "description"
                    }
                ],
                "quantity": 10.0,
                "unit": {
                    "id": "10",
                    "name": "name"
                },
                "description": "create CNonPN: tender.items[0].description",
                "relatedLot": "1"
            },
            {
                "id": "2",
                "internalId": "create CNonPN: tender.items[1].internalId",
                "classification": {
                    "id": "45112360-6",
                    "scheme": "CPV",
                    "description": "description"
                },
                "additionalClassifications": [
                    {
                        "id": "AA12-4",
                        "scheme": "CPVS",
                        "description": "description"
                    }
                ],
                "quantity": 10.0,
                "unit": {
                    "id": "10",
                    "name": "name"
                },
                "description": "create CNonPN: tender.items[0].description",
                "relatedLot": "2"
            }
        ],
        "documents": [
            {
                "documentType": "procurementPlan",
                "id": "{{Document-1}}",
                "title": "create CNonPN: tender.documents[0].title",
                "description": "create CNonPN: tender.documents[0].description",
                "relatedLots": [
                    "1"
                ]
            },
            {
                "documentType": "tenderNotice",
                "id": "{{Document-2}}",
                "title": "create CNonPN: tender.documents[1].title",
                "description": "create CNonPN: tender.documents[1].description",
                "relatedLots": [
                    "2"
                ]
            },
            {
                "documentType": "eligibilityCriteria",
                "id": "{{Document-3}}",
                "title": "create CNonPN: tender.documents[1].title",
                "description": "create CNonPN: tender.documents[1].description",
                "relatedLots": [
                    "1"
                ]
            }
        ]
    }
}

create_cn_on_pn_payload_obligatory_data_model = {
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
                "title": "Create CN: title of lot",
                "description": "Create CN: description of lot",
                "value": {
                    "amount": 1500.0,
                    "currency": "EUR"
                },
                "contractPeriod": {
                    "startDate": contract_period[0],
                    "endDate": contract_period[1]
                },
                "placeOfPerformance": {
                    "address": {
                        "streetAddress": "Create CN: street of placeOfPerformance",
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
                "quantity": 10.0,
                "unit": {
                    "id": "10"
                },
                "description": "Create CN: description of item",
                "relatedLot": "1"
            }
        ],
        "documents": [
            {
                "documentType": "illustration",
                "id": "{{Document-1}}",
                "title": "Create CN: title of document"
            }
        ]
    }
}

update_cn_on_pn_payload_full_data_model_with_auction = {
    "planning": {
        "rationale": "update CNonPN: planning.rationale",
        "budget": {
            "description": "update CNonPN: planning.description"
        }
    },
    "tender": {
        "title": "update CNonPN: tender.title",
        "description": "update CNonPN: tender.description",
        "procurementMethodRationale": "update CNonPN: tender.procurementMethodRationale",
        "procurementMethodAdditionalInfo": "update CNonPN: tender.procurementMethodAdditionalInfo",
        "awardCriteria": "ratedCriteria",
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
                    "id": "9f8c8d7c-127a-42ab-b72d-d215e5cc6b40",
                    "relatedLot": "1",
                    "electronicAuctionModalities": [
                        {
                            "eligibleMinimumDifference": {
                                "amount": 105.00,
                                "currency": "EUR"
                            }
                        }
                    ]
                },
                {
                    "id": "5f2caa86-b76b-410f-b181-8528b233f43c",
                    "relatedLot": "2",
                    "electronicAuctionModalities": [
                        {
                            "eligibleMinimumDifference": {
                                "amount": 15.00,
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
                    "title": "update CNonPN: procuringEntity.persones[0].title",
                    "name": "update CNonPN: procuringEntity.persones[0].name",
                    "identifier": {
                        "scheme": "MD-IDNO",
                        "id": "update CNonPN: procuringEntity.persones[0].identifier.id =1",
                        "uri": "update CNonPN: procuringEntity.persones[0].identifier.uri"
                    },
                    "businessFunctions": [
                        {
                            "id": "update CNonPN: procuringEntity.persones[0].businessFunctions[0].id =1",
                            "type": "contactPoint",
                            "jobTitle": "update CNonPN: procuringEntity.persones[0].jobTitle",
                            "period": {
                                "startDate": period[2]
                            },
                            "documents": [
                                {
                                    "id": "update CNonPN: procuringEntity.persones[0].businessFunctions[0]."
                                          "documents[0].id =1",
                                    "documentType": "regulatoryDocument",
                                    "title": "update CNonPN: procuringEntity.persones[0].businessFunctions[0].title",
                                    "description": "update CNonPN: procuringEntity.persones[0].businessFunctions[0]."
                                                   "description"
                                }
                            ]
                        }
                    ]
                },
                {
                    "title": "update CNonPN: procuringEntity.persones[0].title",
                    "name": "update CNonPN: procuringEntity.persones[0].name",
                    "identifier": {
                        "scheme": "MD-IDNO",
                        "id": "update CNonPN: procuringEntity.persones[0].identifier.id =2",
                        "uri": "update CNonPN: procuringEntity.persones[0].identifier.uri"
                    },
                    "businessFunctions": [
                        {
                            "id": "update CNonPN: procuringEntity.persones[0].businessFunctions[0].id =2",
                            "type": "contactPoint",
                            "jobTitle": "update CNonPN: procuringEntity.persones[0].jobTitle",
                            "period": {
                                "startDate": period[2]
                            },
                            "documents": [
                                {
                                    "id": "update CNonPN: procuringEntity.persones[0].businessFunctions[0]."
                                          "documents[0].id =1",
                                    "documentType": "regulatoryDocument",
                                    "title": "update CNonPN: procuringEntity.persones[0].businessFunctions[0].title",
                                    "description": "update CNonPN: procuringEntity.persones[0].businessFunctions[0]."
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
                "title": "update CNonPN: tender.criteria[0].title =Bankruptcy",
                "relatesTo": "tender",
                "classification": {
                    "id": "CRITERION.EXCLUSION.CONVICTIONS.PARTICIPATION_IN_CRIMINAL_ORGANISATION",
                    "scheme": "ESPD"
                },
                "description": "update CNonPN: tender.criteria[0].description ="
                               "Is the economic operator bankrupt? This information needs not be given if "
                               "exclusion of economic operators in this case has been made mandatory under the "
                               "applicable national law without any possibility of derogation where the economic "
                               "operator is nevertheless able to perform the contract.",
                "requirementGroups": [
                    {
                        "id": "001-1",
                        "description": "update CNonPN: tender.criteria[0].requirementGroups[0].description ="
                                       "approve that Bankruptcy requirement group",
                        "requirements": [
                            {
                                "id": "001-1-1",
                                "title": "update CNonPN: tender.criteria[0].requirementGroups[0].requirements.title",
                                "description": "create CNonPN: tender.criteria[0].requirementGroups[0].requirements."
                                               "description",
                                "dataType": "boolean",
                                "expectedValue": True,
                                "eligibleEvidences": [
                                    {
                                        "id": "1",
                                        "title": "update CNonPN: tender.criteria[0].requirementGroups[0]."
                                                 "requirements[0].eligibleEvidences[0].title",
                                        "description": "update CNonPN: tender.criteria[0].requirementGroups[0]."
                                                       "requirements[0].eligibleEvidences[0].description",
                                        "type": "document",
                                        "relatedDocument": {
                                            "id": "{{Document-4}}"
                                        }
                                    },
                                    {
                                        "id": "2",
                                        "title": "update CNonPN: tender.criteria[0].requirementGroups[0]."
                                                 "requirements[0].eligibleEvidences[1].title",
                                        "description": "update CNonPN: tender.criteria[0].requirementGroups[0]."
                                                       "requirements[0].eligibleEvidences[1].description",
                                        "type": "document",
                                        "relatedDocument": {
                                            "id": "{{Document-4}}"
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
                "title": "update CNonPN: tender.criteria[1].title",
                "description": "update CNonPN: tender.criteria[1].description",
                "relatesTo": "lot",
                "relatedItem": "1",
                "classification": {
                    "id": "CRITERION.SELECTION.ECONOMIC_FINANCIAL_STANDING.TURNOVER.GENERAL_YEARLY",
                    "scheme": "ESPD"
                },
                "requirementGroups": [
                    {
                        "id": "002-1",
                        "description": "update CNonPN: tender.criteria[1].requirementGroups[0].description",
                        "requirements": [
                            {
                                "id": "002-1-1",
                                "title": "update CNonPN: tender.criteria[1].requirementGroups[0].requirements[0].title",
                                "description": "update CNonPN: tender.criteria[1].requirementGroups[0].requirements."
                                               "description",
                                "dataType": "boolean",
                                "expectedValue": False
                            },
                            {
                                "id": "002-1-2",
                                "title": "update CNonPN: tender.criteria[1].requirementGroups[0].requirements[1].title "
                                         "=The number of years for proposed product warranty",
                                "description": "update CNonPN: tender.criteria[1].requirementGroups[0].requirements[1]."
                                               "description",
                                "dataType": "number",
                                "minValue": 1.0,
                                "maxValue": 3.0,
                                "period": {
                                    "startDate": period[2],
                                    "endDate": period[4]
                                },
                                "eligibleEvidences": [
                                    {
                                        "id": "3",
                                        "title": "update CNonPN: tender.criteria[1].requirementGroups[0]."
                                                 "requirements[1].eligibleEvidences[0].title",
                                        "description": "update CNonPN: tender.criteria[1].requirementGroups[0]."
                                                       "requirements[1].eligibleEvidences[0].description",
                                        "type": "document",
                                        "relatedDocument": {
                                            "id": "{{Document-4}}"
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
                "title": "update CNonPN: tender.criteria[2].title",
                "classification": {
                    "id": "CRITERION.EXCLUSION.NATIONAL.OTHER",
                    "scheme": "ESPD"
                },
                "description": "update CNonPN: tender.criteria[2].description",
                "relatesTo": "tenderer",
                "requirementGroups": [
                    {
                        "id": "003-1",
                        "description": "update CNonPN: tender.criteria[2].requirementGroups[0].description",
                        "requirements": [
                            {
                                "id": "003-1-1",
                                "title": "update CNonPN: tender.criteria[2].requirementGroups[0].requirements[0]."
                                         "title =Product has to be manufactured in the EU",
                                "dataType": "boolean",
                                "expectedValue": False
                            },
                            {
                                "id": "003-1-2",
                                "title": "update CNonPN: tender.criteria[2].requirementGroups[0]..requirements[1]."
                                         "title =Country of origin",
                                "dataType": "string"
                            }
                        ]
                    }, {
                        "id": "003-2",
                        "description": "update  CNonPN: tender.criteria[2].requirementGroups[1].description",
                        "requirements": [
                            {
                                "id": "003-2-1",
                                "title": "update  CNonPN: tender.criteria[2].requirementGroups[1].requirements[0]."
                                         "title =Product has to be manufactured in the EU",
                                "dataType": "boolean",
                                "expectedValue": False
                            },
                            {
                                "id": "003-2-2",
                                "title": "update  CNonPN: tender.criteria[2].requirementGroups[1]..requirements[1]."
                                         "title =Country of origin",
                                "dataType": "string"
                            }
                        ]
                    }
                ]
            },
            {
                "id": "004",
                "title": "update  CNonPN: tender.criteria[3].title",
                "relatesTo": "item",
                "relatedItem": "1",
                "classification": {
                    "id": "CRITERION.OTHER.EO_DATA.RELIES_ON_OTHER_CAPACITIES",
                    "scheme": "ESPD"
                },
                "description": "update  CNonPN: tender.criteria[3].description ="
                               "A minimum product warranty of 1 year is required for all bids 2",
                "requirementGroups": [
                    {
                        "id": "004-1",
                        "description": "update  CNonPN: tender.criteria[3].requirementGroups[0].description",
                        "requirements": [
                            {
                                "id": "004-1-1",
                                "title": "update  CNonPN: tender.criteria[3].requirementGroups[0].requirements[0]."
                                         "title = The number of years for proposed product warranty",
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
                "id": "005",
                "title": "update  CNonPN: tender.criteria[4].title",
                "relatesTo": "tender",
                "classification": {
                    "id": "CRITERION.EXCLUSION.NATIONAL.OTHER",
                    "scheme": "ESPD"
                },
                "description": "update  CNonPN: tender.criteria[4].description",
                "requirementGroups": [
                    {
                        "id": "005-1",
                        "description": "update  CNonPN: tender.criteria[4].requirementGroups[0].description",
                        "requirements": [
                            {
                                "id": "005-1-1",
                                "title": "update  CNonPN: tender.criteria[4].requirementGroups[0].requirements[0]."
                                         "title =Country of origin",
                                "dataType": "string"
                            }
                        ]
                    }
                ]
            },
            {
                "id": "006",
                "title": "update  CNonPN: tender.criteria[4].title",
                "relatesTo": "tender",
                "classification": {
                    "id": "CRITERION.OTHER.EO_DATA.RELIES_ON_OTHER_CAPACITIES",
                    "scheme": "ESPD"
                },
                "description": "update  CNonPN: tender.criteria[4].description",
                "requirementGroups": [
                    {
                        "id": "006-1",
                        "description": "update  CNonPN: tender.criteria[4].requirementGroups[0].description",
                        "requirements": [
                            {
                                "id": "006-1-1",
                                "title": "update  CNonPN: tender.criteria[4].requirementGroups[0].requirements[0]."
                                         "title =Country of origin",
                                "dataType": "string"
                            }
                        ]
                    }
                ]
            }
        ],
        "conversions": [
            {
                "id": "2",
                "relatesTo": "requirement",
                "relatedItem": "002-1-1",
                "rationale": "update  CNonPN: tender.conversions[1].rationale",
                "description": "update  CNonPN: tender.conversions[1].description",
                "coefficients": [
                    {
                        "id": "coefficient-1",
                        "value": True,
                        "coefficient": 1
                    }
                ]
            },
            {
                "id": "3",
                "relatesTo": "requirement",
                "relatedItem": "002-1-2",
                "rationale": "update  CNonPN: tender.conversions[3].rationale",
                "description": "update  CNonPN: tender.conversions[3].description",
                "coefficients": [
                    {
                        "id": "coefficient-1",
                        "value": 1.0,
                        "coefficient": 1
                    },
                    {
                        "id": "coefficient-2",
                        "value": 2.0,
                        "coefficient": 1
                    },
                    {
                        "id": "coefficient-3",
                        "value": 3.0,
                        "coefficient": 0.93
                    }
                ]
            },
            {
                "id": "6",
                "relatesTo": "requirement",
                "relatedItem": "004-1-1",
                "rationale": "update  CNonPN: tender.conversions[6].rationale",
                "description": "update  CNonPN: tender.conversions[6].description",
                "coefficients": [
                    {
                        "id": "coefficient-1",
                        "value": 1.0,
                        "coefficient": 1
                    },
                    {
                        "id": "coefficient-2",
                        "value": 2.0,
                        "coefficient": 1
                    },
                    {
                        "id": "coefficient-3",
                        "value": 3.0,
                        "coefficient": 0.93
                    }
                ]
            },
            {
                "id": "7",
                "relatesTo": "requirement",
                "relatedItem": "006-1-1",
                "rationale": "update  CNonPN: tender.conversions[6].rationale",
                "description": "update  CNonPN: tender.conversions[6].description",
                "coefficients": [
                    {
                        "id": "coefficient-1",
                        "value": "option_1",
                        "relatedOption": "option_1",
                        "coefficient": 1
                    },
                    {
                        "id": "coefficient-2",
                        "value": "option_2",
                        "relatedOption": "option_2",
                        "coefficient": 1
                    },
                    {
                        "id": "coefficient-3",
                        "value": "option_3",
                        "relatedOption": "option_3",
                        "coefficient": 0.93
                    }
                ]
            }
        ],
        "lots": [
            {
                "id": "1",
                "internalId": "update  CNonPN: tender.lots[0].internalId",
                "title": "update  CNonPN: tender.lots[0].title",
                "description": "update  CNonPN: tender.lots[0].description",
                "value": {
                    "amount": 1505.0,
                    "currency": "EUR"
                },
                "contractPeriod": {
                    "startDate": contract_period[0],
                    "endDate": contract_period[1]
                },
                "placeOfPerformance": {
                    "address": {
                        "streetAddress": "update  CNonPN: tender.lots[0].placeOfPerformance.address.street",
                        "postalCode": "update  CNonPN: tender.lots[0].placeOfPerformance.address.postal",
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
                                "description": "update  CNonPN: tender.lots[0].placeOfPerformance.address."
                                               "addressDetails.locality.description"
                            }
                        }
                    },
                    "description": "update  CNonPN: tender.lots[0].placeOfPerformance.description"
                },
                "hasOptions": True,
                "options": [
                    {
                        "description": "update  CNonPN: tender.lots[0].options.description",
                        "period": {
                            "durationInDays": 181,
                            "startDate": contract_period[0],
                            "endDate": contract_period[1],
                            "maxExtentDate": contract_period[1]
                        }
                    }
                ],
                "hasRecurrence": True,
                "recurrence": {
                    "dates": [
                        {
                            "startDate": contract_period[0]
                        },
                        {
                            "startDate": contract_period[0]
                        }
                    ],
                    "description": "update  CNonPN: tender.lots[0].description ="
                                   "The duration of this contract and recurrent contracts will not exceed three years."
                },
                "hasRenewal": True,
                "renewal": {
                    "description": "update  CNonPN: tender.lots[0].renewal ="
                                   "The contracting authority reserves the right to extend the term for a period "
                                   "or periods of up to 1 year with a maximum of 2 such extensions on the same "
                                   "terms and conditions, subject to the contracting authority's obligations at law.",
                    "minimumRenewals": 2,
                    "maximumRenewals": 5,
                    "period": {
                        "durationInDays": 365,
                        "startDate": contract_period[0],
                        "endDate": contract_period[1],
                        "maxExtentDate": contract_period[1]
                    }
                }
            },
            {
                "id": "2",
                "internalId": "update  CNonPN: tender.lots[1].internalId",
                "title": "update  CNonPN: tender.lots[1].title",
                "description": "update  CNonPN: tender.lots[1].description",
                "value": {
                    "amount": 105.0,
                    "currency": "EUR"
                },
                "contractPeriod": {
                    "startDate": contract_period[0],
                    "endDate": contract_period[1]
                },
                "placeOfPerformance": {
                    "address": {
                        "streetAddress": "update  CNonPN: tender.lots[1].placeOfPerformance.address.street",
                        "postalCode": "update  CNonPN: tender.lots[1].placeOfPerformance.address.postal",
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
                                "description": "update  CNonPN: tender.lots[1].placeOfPerformance.address."
                                               "addressDetails.locality.description"
                            }
                        }
                    },
                    "description": "update  CNonPN: tender.lots[1].placeOfPerformance.description"
                },
                "hasOptions": True,
                "options": [
                    {
                        "description": "update  CNonPN: tender.lots[0].options.description",
                        "period": {
                            "durationInDays": 181,
                            "startDate": contract_period[0],
                            "endDate": contract_period[1],
                            "maxExtentDate": contract_period[1]
                        }
                    }
                ],
                "hasRecurrence": True,
                "recurrence": {
                    "dates": [
                        {
                            "startDate": contract_period[0]
                        },
                        {
                            "startDate": contract_period[0]
                        }
                    ],
                    "description": "update  CNonPN: tender.lots[0].description ="
                                   "The duration of this contract and recurrent contracts will not exceed three years."
                },
                "hasRenewal": True,
                "renewal": {
                    "description": "update CNonPN: tender.lots[0].renewal ="
                                   "The contracting authority reserves the right to extend the term for a period "
                                   "or periods of up to 1 year with a maximum of 2 such extensions on the same "
                                   "terms and conditions, subject to the contracting authority's obligations at law.",
                    "minimumRenewals": 2,
                    "maximumRenewals": 5,
                    "period": {
                        "durationInDays": 365,
                        "startDate": contract_period[0],
                        "endDate": contract_period[1],
                        "maxExtentDate": contract_period[1]
                    }
                }
            }
        ],
        "items": [
            {
                "id": "1",
                "internalId": "update  CNonPN: tender.items[0].internalId",
                "classification": {
                    "id": "45112350-3",
                    "scheme": "CPV",
                    "description": "update description"
                },
                "additionalClassifications": [
                    {
                        "id": "AA12-4",
                        "scheme": "CPVS",
                        "description": "description"
                    },
                    {
                        "id": "AA05-3",
                        "scheme": "CPVS",
                        "description": "description"
                    }
                ],
                "quantity": 10.0,
                "unit": {
                    "id": "120",
                    "name": "update unit.name"
                },
                "description": "update  CNonPN: tender.items[0].description",
                "relatedLot": "1"
            },
            {
                "id": "2",
                "internalId": "update  CNonPN: tender.items[1].internalId",
                "classification": {
                    "id": "45112360-6",
                    "scheme": "CPV",
                    "description": "update description"
                },
                "additionalClassifications": [
                    {
                        "id": "AA12-4",
                        "scheme": "CPVS",
                        "description": "update  description"
                    },
                    {
                        "id": "AA05-3",
                        "scheme": "CPVS",
                        "description": "description"
                    }
                ],
                "quantity": 10.0,
                "unit": {
                    "id": "120",
                    "name": "update  name"
                },
                "description": "update  CNonPN: tender.items[0].description",
                "relatedLot": "2"
            }
        ],
        "documents": [
            {
                "documentType": "procurementPlan",
                "id": "{{Document-1}}",
                "title": "update  CNonPN: tender.documents[0].title",
                "description": "update  CNonPN: tender.documents[0].description",
                "relatedLots": [
                    "1"
                ]
            },
            {
                "documentType": "tenderNotice",
                "id": "{{Document-2}}",
                "title": "update  CNonPN: tender.documents[1].title",
                "description": "update  CNonPN: tender.documents[1].description",
                "relatedLots": [
                    "2"
                ]
            },
            {
                "documentType": "eligibilityCriteria",
                "id": "{{Document-3}}",
                "title": "update  CNonPN: tender.documents[1].title",
                "description": "update  CNonPN: tender.documents[1].description",
                "relatedLots": [
                    "1"
                ]
            },
            {
                "documentType": "eligibilityCriteria",
                "id": "{{Document-4}}",
                "title": "update  CNonPN: tender.documents[4].title",
                "description": "update  CNonPN: tender.documents[1].description",
                "relatedLots": [
                    "1"
                ]
            }
        ]
    }
}

update_cn_on_pn_payload_obligatory_data_model = {
    "tender": {
        "title": "update CNonPN: tender.title",
        "description": "update CNonPN: tender.description",
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
                "title": "Create CN: title of lot",
                "description": "Create CN: description of lot",
                "value": {
                    "amount": 1501.1,
                    "currency": "EUR"
                },
                "contractPeriod": {
                    "startDate": contract_period[0],
                    "endDate": contract_period[1]
                },
                "placeOfPerformance": {
                    "address": {
                        "streetAddress": "Create CN: street of placeOfPerformance",
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
            },
            {
                "id": "2",
                "title": "Create CN: title of lot",
                "description": "Create CN: description of lot",
                "value": {
                    "amount": 151.1,
                    "currency": "EUR"
                },
                "contractPeriod": {
                    "startDate": contract_period[0],
                    "endDate": contract_period[1]
                },
                "placeOfPerformance": {
                    "address": {
                        "streetAddress": "Create CN: street of placeOfPerformance",
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
                "quantity": 1.01,
                "unit": {
                    "id": "121"
                },
                "description": "Create CN: description of item",
                "relatedLot": "1"
            },
            {
                "id": "{{item_id_2}}",
                "classification": {
                    "id": "45112360-6"
                },
                "quantity": 1.01,
                "unit": {
                    "id": "121"
                },
                "description": "Create CN: description of item",
                "relatedLot": "2"
            }
        ],
        "documents": [
            {
                "documentType": "illustration",
                "id": "{{Document-1}}",
                "title": "Create CN: title of document"
            }
        ]
    }
}
