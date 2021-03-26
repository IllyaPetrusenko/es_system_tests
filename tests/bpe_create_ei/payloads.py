import random

from useful_functions import get_period

period = get_period()
typeOfBuyer = ("BODY_PUBLIC", "EU_INSTITUTION", "MINISTRY", "NATIONAL_AGENCY", "REGIONAL_AGENCY", "REGIONAL_AUTHORITY",)
mainGeneralActivity = (
    "DEFENCE", "ECONOMIC_AND_FINANCIAL_AFFAIRS", "EDUCATION", "ENVIRONMENT", "GENERAL_PUBLIC_SERVICES", "HEALTH",
    "HOUSING_AND_COMMUNITY_AMENITIES", "PUBLIC_ORDER_AND_SAFETY", "RECREATION_CULTURE_AND_RELIGION",
    "SOCIAL_PROTECTION",)
mainSectoralActivity = ("AIRPORT_RELATED_ACTIVITIES", "ELECTRICITY", "EXPLORATION_EXTRACTION_COAL_OTHER_SOLID_FUEL",
                        "EXPLORATION_EXTRACTION_GAS_OIL",
                        "PORT_RELATED_ACTIVITIES", "POSTAL_SERVICES", "PRODUCTION_TRANSPORT_DISTRIBUTION_GAS_HEAT",
                        "RAILWAY_SERVICES", "URBAN_RAILWAY_TRAMWAY_TROLLEYBUS_BUS_SERVICES", "WATER",)
cpv_goods = ("03100000-2", "39100000-3", "48600000-4",)
cpv_works = ("45100000-8", "45200000-9", "45100000-8",)
cpv_services = ("76100000-4", "76200000-5", "90900000-6",)
locality_scheme = ("CUATM", "other",)
payload_ei_full_data_model= {
    "tender": {
        "title": "EI_FULL_WORKS",
        "description": "description of finansical sourse",
        "mainProcurementCategory": "",
        "classification": {
            "id": "45100000-8",
            "scheme": "CPV",
            "description": "classification.description"
        },
        "items": [
            {
                "id": "1",
                "description": "item 1",
                "classification": {
                    "id": "45100000-8"
                },
                "additionalClassifications": [
                    {
                        "id": "AA12-4"
                    }
                ],
                "deliveryAddress": {
                    "streetAddress": "хрещатик",
                    "postalCode": "02235",
                    "addressDetails": {
                        "country": {
                            "id": "MD",
                            "description": "ОПИСАНИЕ",
                            "scheme": "other"
                        },
                        "region": {
                            "id": "1700000",
                            "description": "ОПИСАНИЕ",
                            "scheme": "CUATM"
                        },
                        "locality": {
                            "id": "1701000",
                            "description": "ОПИСАНИЕ33pizza",
                            "scheme": f'{random.choice(locality_scheme)}'
                        }

                    }
                },
                "quantity": 1,
                "unit": {
                    "id": "10",
                    "name": "name"
                }
            }
        ]
    },
    "planning": {
        "budget": {

            "period": {
                "startDate": period[0],
                "endDate": period[1]
            }
        },
        "rationale": "planning.rationale"
    },
    "buyer": {
        "name": "LLC Petrusenko",
        "identifier": {
            "id": "380632074071",
            "scheme": "MD-IDNO",
            "legalName": "LLC Petrusenko",
            "uri": "http://petrusenko.com/fop"
        },
        "address": {
            "streetAddress": "Zakrevskogo",
            "postalCode": "02217",
            "addressDetails": {
                "country": {
                    "id": "MD",
                    "scheme": "",
                    "description": "",
                    "uri": ""
                },
                "region": {
                    "id": "1700000",
                    "scheme": "",
                    "description": "",
                    "uri": ""
                },
                "locality": {
                    "scheme": "CUATM",
                    "id": "1701000",
                    "description": "description",
                    "uri": ""
                }
            }
        },
        "additionalIdentifiers": [
            {
                "id": "string",
                "scheme": "MD-IDNO",
                "legalName": "380935103469",
                "uri": "http://petrusenko.com/svetlana"
            }
        ],
        "contactPoint": {
            "name": "Petrusenko Svitlana",
            "email": "svetik@gmail.com",
            "telephone": "888999666",
            "faxNumber": "5552233",
            "url": "http://petrusenko.com/svetlana"
        },
        "details": {
            "typeOfBuyer": f'{random.choice(typeOfBuyer)}',
            "mainGeneralActivity": f'{random.choice(mainGeneralActivity)}',
            "mainSectoralActivity": f'{random.choice(mainSectoralActivity)}'

        }
    }
}

ei_obligatory = {
    "tender": {
        "title": "EI_FULL_WORKS",

        "mainProcurementCategory": "",
        "classification": {
            "id": "45100000-8"

        },
        "items": [
            {
                "id": "1",
                "description": "item 1",
                "classification": {
                    "id": "45100000-8"
                },

                "deliveryAddress": {

                    "addressDetails": {
                        "country": {
                            "id": "MD"

                        },
                        "region": {
                            "id": "1700000"

                        }

                    }
                },
                "quantity": 1,
                "unit": {
                    "id": "10"

                }
            }
        ]
    },
    "planning": {
        "budget": {

            "period": {
                "startDate": period[0],
                "endDate": period[1]
            }
        }

    },
    "buyer": {
        "name": "LLC Petrusenko",
        "identifier": {
            "id": "380632074071",
            "scheme": "MD-IDNO",
            "legalName": "LLC Petrusenko"

        },
        "address": {
            "streetAddress": "Zakrevskogo",

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
                    "description": "description"

                }
            }
        },

        "contactPoint": {
            "name": "Petrusenko Svitlana",
            "email": "svetik@gmail.com",
            "telephone": "888999666"

        }

    }
}
