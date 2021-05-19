import random

from useful_functions import get_contract_period

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
