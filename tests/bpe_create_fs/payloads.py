from useful_functions import get_period

period = get_period()
fs_create_full_treasury_money = {
    "planning": {
        "budget": {
            "id": "IBAN - 102030",
            "description": "description",
            "period": {
                "startDate": period[0],
                "endDate": period[1]
            },
            "amount": {
                "amount": 8000,
                "currency": "EUR"
            },
            "isEuropeanUnionFunded": True,
            "europeanUnionFunding": {
                "projectName": "Name of this project",
                "projectIdentifier": "projectIdentifier",
                "uri": "http://uriuri.th"
            },
            "project": "project",
            "projectID": "projectID",
            "uri": "http://uri.ur"
        },
        "rationale": "reason for the budget"
    },
    "tender": {
        "procuringEntity": {
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
                        "id": "MD"
                    },
                    "region": {
                        "id": "3400000"
                    },
                    "locality": {
                        "scheme": "CUATM",
                        "id": "3401000",
                        "description": ""
                    }
                }
            },
            "additionalIdentifiers": [
                {
                    "id": "additional identifier",
                    "scheme": "MD-K",
                    "legalName": "legalname",
                    "uri": "http://k.to"
                }
            ],
            "contactPoint": {
                "name": "contact person",
                "email": "string@mail.ccc",
                "telephone": "98-79-87",
                "faxNumber": "78-56-55",
                "url": "http://url.com"
            }
        }
    }

}

fs_create_obligatory_treasury_money ={
    "planning": {
        "budget": {
            "period": {
                "startDate": period[0],
                "endDate": period[1]
            },
            "amount": {
                "amount": 2000,
                "currency": "EUR"
            },
            "isEuropeanUnionFunded": False
        }
    },
    "tender": {
        "procuringEntity": {
            "name": "Procuring Entity Name",
            "identifier": {
                "id": "123456789000",
                "scheme": "MD-IDNO",
                "legalName": "Legal Name"
            },
            "address": {
                "streetAddress": "street",
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
                        "description": ""
                    }
                }
            },
            "contactPoint": {
                "name": "contact person",
                "email": "string@mail.ccc",
                "telephone": "98-79-87"
            }
        }
    }
}

fs_create_full_own_money ={
    "planning": {
        "budget": {
            "id": "IBAN - 102030",
            "description": "description",
            "period": {
                "startDate": period[0],
                "endDate": period[1]
            },
            "amount": {
                "amount": 2000,
                "currency": "EUR"
            },
            "isEuropeanUnionFunded": True,
            "europeanUnionFunding": {
                "projectName": "Name of this project",
                "projectIdentifier": "projectIdentifier",
                "uri": "http://uriuri.th"
            },
            "project": "project",
            "projectID": "projectID",
            "uri": "http://uri.ur"
        },
        "rationale": "reason for the budget"
    },
    "tender": {
        "procuringEntity": {
            "name": "Procuring Entity Name",
            "identifier": {
                "id": "123456789000",
                "scheme": "MD-IDNO",
                "legalName": "Legal Name",
                "uri": "http://454.to"
            },
            "additionalIdentifiers": [
                {
                    "id": "additional identifier",
                    "scheme": "MD-K",
                    "legalName": "legalname",
                    "uri": "http://k.to"
                }
            ],
            "address": {
                "streetAddress": "street",
                "postalCode": "785412",
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
                        "description": ""
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
        "name": "buyer's name",
        "identifier": {
            "id": "123654789000",
            "scheme": "MD-IDNO",
            "legalName": "legal Name",
            "uri": "http://buyer.com"
        },
        "address": {
            "streetAddress": "street address of buyer",
            "postalCode": "02054",
            "addressDetails": {
                "country": {
                    "id": "MD"
                },
                "region": {
                    "id": "1700000"
                },
                "locality": {
                    "scheme": "CUATM",
                    "id": "1701000",
                    "description": "description of locality"
                }
            }
        },
        "additionalIdentifiers": [
            {
                "id": "additional identifier",
                "scheme": "scheme",
                "legalName": "legal name",
                "uri": "http://addtIdent.com"
            }
        ],
        "contactPoint": {
            "name": "contact point of buyer",
            "email": "email.com",
            "telephone": "32-22-23",
            "faxNumber": "12-22-21",
            "url": "http://url.com"
        }
    }
}

fs_create_obligatory_own_money = {
    "planning": {
        "budget": {
            "period": {
                "startDate": period[0],
                "endDate": period[1]
            },
            "amount": {
                "amount": 4000,
                "currency": "EUR"
            },
            "isEuropeanUnionFunded": False
        }
    },
    "tender": {
        "procuringEntity": {
            "name": "Procuring Entity Name",
            "identifier": {
                "id": "123456789000",
                "scheme": "MD-IDNO",
                "legalName": "Legal Name"
            },
            "address": {
                "streetAddress": "street",
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
                        "description": ""
                    }
                }
            },
            "contactPoint": {
                "name": "contact person",
                "email": "string@mail.ccc",
                "telephone": "98-79-87"
            }
        }
    },
    "buyer": {
        "name": "buyer's name",
        "identifier": {
            "id": "123654789000",
            "scheme": "MD-IDNO",
            "legalName": "legal Name"
        },
        "address": {
            "streetAddress": "street address of buyer",
            "addressDetails": {
                "country": {
                    "id": "MD"
                },
                "region": {
                    "id": "1700000"
                },
                "locality": {
                    "scheme": "CUATM",
                    "id": "1701000",
                    "description": "description of locality"
                }
            }
        },
        "contactPoint": {
            "name": "contact point of buyer",
            "email": "email.com",
            "telephone": "32-22-23"
        }
    }
}