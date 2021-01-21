
from useful_functions import get_new_period

period = get_new_period()

fs_update_full_treasury_money = {
    "planning": {
        "budget": {
            "id": "IBAN - 102030",
            "description": "description",
            "period": {
                "startDate": period[0],
                "endDate": period[1]
            },
            "amount": {
                "amount": 2000.00,
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

fs_update_obligatory_treasury_money = {
    "planning": {
        "budget": {
            "period": {
                "startDate": period[0],
                "endDate": period[1]
            },
            "amount": {
                "amount": 2000.00,
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

fs_update_full_own_money = {
    "planning": {
        "budget": {
            "id": "update_fs",
            "description": "update_fs",
            "period": {
                "startDate": period[0],
                "endDate": period[1]
            },
            "amount": {
                "amount": 99.99,
                "currency": "EUR"
            },
            "isEuropeanUnionFunded": True,
            "europeanUnionFunding": {
                "projectName": "update_fs",
                "projectIdentifier": "update_fs",
                "uri": "update_fs"
            },
            "project": "update_fs",
            "projectID": "update_fs",
            "uri": "update_fs"
        },
        "rationale": "update_fs"
    },
    "tender": {
        "procuringEntity": {
            "name": "update_fs",
            "identifier": {
                "id": "44_update_fs",
                "scheme": "MD-IDNO",
                "legalName": "update_fs",
                "uri": "update_fs"
            },
            "additionalIdentifiers": [
                {
                    "id": "update_fs",
                    "scheme": "update_fs",
                    "legalName": "update_fs",
                    "uri": "update_fs"
                }
            ],
            "address": {
                "streetAddress": "update_fs",
                "postalCode": "update_fs",
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
                "name": "update_fs",
                "email": "update_fs",
                "telephone": "update_fs",
                "faxNumber": "update_fs",
                "url": "update_fs"
            }
        }
    },
    "buyer": {
        "name": "update_fs",
        "identifier": {
            "id": "55_update_fs",
            "scheme": "MD-IDNO",
            "legalName": "update_fs",
            "uri": "update_fs"
        },
        "address": {
            "streetAddress": "update_fs",
            "postalCode": "update_fs",
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
                    "description": "update_fs"
                }
            }
        },
        "additionalIdentifiers": [
            {
                "id": "update_fs",
                "scheme": "update_fs",
                "legalName": "update_fs",
                "uri": "update_fs"
            }
        ],
        "contactPoint": {
            "name": "update_fs",
            "email": "update_fs",
            "telephone": "update_fs",
            "faxNumber": "update_fs",
            "url": "update_fs"
        }
    }
}

fs_update_obligatory_own_money = {
    "planning": {
        "budget": {
            "period": {
                "startDate": period[0],
                "endDate": period[1]
            },
            "amount": {
                "amount": 2000.00,
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
        "name": "buyer name",
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
