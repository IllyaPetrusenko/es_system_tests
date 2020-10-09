import random

typeOfBuyer = ('BODY_PUBLIC', 'EU_INSTITUTION', 'MINISTRY', 'NATIONAL_AGENCY', 'REGIONAL_AGENCY', 'REGIONAL_AUTHORITY',)
mainGeneralActivity = (
    'DEFENCE', 'ECONOMIC_AND_FINANCIAL_AFFAIRS', 'EDUCATION', 'ENVIRONMENT', 'GENERAL_PUBLIC_SERVICES', 'HEALTH',
    'HOUSING_AND_COMMUNITY_AMENITIES', 'PUBLIC_ORDER_AND_SAFETY', 'RECREATION_CULTURE_AND_RELIGION',
    'SOCIAL_PROTECTION',)
mainSectoralActivity = ('AIRPORT_RELATED_ACTIVITIES', 'ELECTRICITY', 'EXPLORATION_EXTRACTION_COAL_OTHER_SOLID_FUEL',
                        'EXPLORATION_EXTRACTION_GAS_OI',
                        'PORT_RELATED_ACTIVITIES', 'POSTAL_SERVICES', 'PRODUCTION_TRANSPORT_DISTRIBUTION_GAS_HEAT',
                        'RAILWAY_SERVICES', 'URBAN_RAILWAY_TRAMWAY_TROLLEYBUS_BUS_SERVICES', 'WATER',)
cpv_goods = ('03100000-2', '39100000-3', '48600000-4',)
cpv_works = ('45100000-8', '45200000-9', '45100000-8',)
cpv_services = ('76100000-4', '76200000-5', '90900000-6',)

ei_full = {
    "tender": {
        "title": "EI_FULL_WORKS",
        "description": "description of finansical sourse",
        "mainProcurementCategory": "",
        "classification": {
            "id": "45100000-8",
            "scheme": "CPV",
            "description": "classification.description"
        }
    },
    "planning": {
        "budget": {
            "id": "45100000-8",
            "period": {
                "startDate": "2020-01-01T00:00:00Z",
                "endDate": "2020-12-31T00:00:00Z"
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
        "title": "Cardurilor de acces pentru Bibliotecii Municipale B.P. Hasdeu ",
        "classification": {
            "id": "45100000-8"

        }
    },
    "planning": {
        "budget": {
            "id": "45100000-8",
            "period": {
                "startDate": "2020-01-01T00:00:00Z",
                "endDate": "2020-12-31T12:40:00Z"
            }
        }
    },
    "buyer": {
        "name": "Directia Cultura a Primariei mun.Chisinau",
        "identifier": {
            "id": "123654789000",
            "scheme": "MD-IDNO",
            "legalName": "Directia Cultura a Primariei mun.Chisinau"
        },
        "address": {
            "streetAddress": "str.Bucuresti 68",
            "addressDetails": {
                "country": {
                    "id": "MD"
                },
                "region": {
                    "id": "0101000"
                },
                "locality": {
                    "scheme": "CUATM",
                    "id": "0101000",
                    "description": "mun.Chişinău"
                }
            }

        },
        "contactPoint": {
            "name": "Dumitru Popa",
            "email": "directiacultшra@yahoo.com",
            "telephone": "022242290"
        }
    }
}
