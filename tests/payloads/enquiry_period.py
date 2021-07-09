create_enquiry_full_data_model = {
    "enquiry": {
        "author": {
            "name": "create_enquiry: enquiry.author.name",
            "identifier": {
                "scheme": "MD-IDNO",
                "id": "7",
                "legalName": "create_enquiry: enquiry.author.identifier.legalName",
                "uri": "create_enquiry: enquiry.author.identifier.uri"
            },
            "additionalIdentifiers": [{
                "scheme": "create_enquiry: enquiry.author.additionalIdentifiers[0].scheme",
                "id": "create_enquiry: enquiry.author.additionalIdentifiers[0].id",
                "legalName": "create_enquiry: enquiry.author.additionalIdentifiers[0].legalName",
                "uri": "create_enquiry: enquiry.author.additionalIdentifiers[0].uri"
            }],
            "address": {
                "streetAddress": "create_enquiry: enquiry.author.address.streetAddress",
                "postalCode": "create_enquiry: enquiry.author.address.postalCode",
                "addressDetails": {
                    "country": {
                        "id": "MD"
                    },
                    "region": {
                        "id": "1000000"
                    },
                    "locality": {
                        "scheme": "CUATM",
                        "id": "1001005",
                        "description": "create_enquiry: enquiry.author.address.addressDetails.locality.description"
                    }
                }
            },
            "details": {
                "scale": "sme"
            },
            "contactPoint": {
                "name": "create_enquiry: enquiry.author.contactPoint.name",
                "email": "create_enquiry: enquiry.author.contactPoint.email",
                "telephone": "create_enquiry: enquiry.author.contactPoint.telephone",
                "faxNumber": "create_enquiry: enquiry.author.contactPoint.faxNumber",
                "url": "create_enquiry: enquiry.author.contactPoint.url"
            }
        },
        "title": "create_enquiry: enquiry.title",
        "description": "create_enquiry: enquiry.description",
        "relatedLot": "{{lot-id-1}}"
    }
}

create_enquiry_obligatory_data_model = {
    "enquiry": {
        "author": {
            "name": "create_enquiry: enquiry.author.name",
            "identifier": {
                "scheme": "MD-IDNO",
                "id": "7",
                "legalName": "create_enquiry: enquiry.author.identifier.legalName"
            },
            "address": {
                "streetAddress": "create_enquiry: enquiry.author.address.streetAddress",
                "addressDetails": {
                    "country": {
                        "id": "MD"
                    },
                    "region": {
                        "id": "1000000"
                    },
                    "locality": {
                        "scheme": "CUATM",
                        "id": "1001005",
                        "description": "create_enquiry: enquiry.author.address.addressDetails.locality.description"
                    }
                }
            },
            "details": {
                "scale": "sme"
            },
            "contactPoint": {
                "name": "create_enquiry: enquiry.author.contactPoint.name",
                "email": "create_enquiry: enquiry.author.contactPoint.email",
                "telephone": "create_enquiry: enquiry.author.contactPoint.telephone"
            }
        },
        "title": "create_enquiry: enquiry.title",
        "description": "create_enquiry: enquiry.description"
    }
}

create_answer_full_data_model = {
    "enquiry": {
        "author": {
            "name": "create_answer: enquiry.author.name",
            "identifier": {
                "scheme": "MD-IDNO",
                "id": "8",
                "legalName": "create_answer: enquiry.author.identifier.legalName",
                "uri": "create_answer: enquiry.author.identifier.uri"
            },
            "additionalIdentifiers": [{
                "scheme": "create_answer: enquiry.author.additionalIdentifiers[0].scheme",
                "id": "create_answer: enquiry.author.additionalIdentifiers[0].id",
                "legalName": "create_answer: enquiry.author.additionalIdentifiers[0].legalName",
                "uri": "create_answer.author.additionalIdentifiers[0].uri"
            }],
            "address": {
                "streetAddress": "create_answer: enquiry.author.address.streetAddress",
                "postalCode": "create_answer: enquiry.author.address.postalCode",
                "addressDetails": {
                    "country": {
                        "id": "MD"
                    },
                    "region": {
                        "id": "1000000"
                    },
                    "locality": {
                        "scheme": "CUATM",
                        "id": "1001005",
                        "description": "create_answer: enquiry.author.address.addressDetails.locality.description"
                    }
                }
            },
            "details": {
                "scale": "sme"
            },
            "contactPoint": {
                "name": "create_answer: enquiry.author.contactPoint.name",
                "email": "create_answer: enquiry.author.contactPoint.email",
                "telephone": "create_answer: enquiry.author.contactPoint.telephone",
                "faxNumber": "create_answer: enquiry.author.contactPoint.faxNumber",
                "url": "create_answer: enquiry.author.contactPoint.url"
            }
        },
        "title": "create_answer: enquiry.title",
        "description": "create_answer: enquiry.description",
        "relatedLot": "{{lot-id-1}}"
    }
}

create_answer_obligatory_data_model = {
    "enquiry": {
        "author": {
            "name": "create_answer: enquiry.author.name",
            "identifier": {
                "scheme": "MD-IDNO",
                "id": "8",
                "legalName": "create_answer: enquiry.author.identifier.legalName"
            },
            "address": {
                "streetAddress": "create_answer: enquiry.author.address.streetAddress",
                "addressDetails": {
                    "country": {
                        "id": "MD"
                    },
                    "region": {
                        "id": "1000000"
                    },
                    "locality": {
                        "scheme": "CUATM",
                        "id": "1001005",
                        "description": "create_answer: enquiry.author.address.addressDetails.locality.description"
                    }
                }
            },
            "details": {
                "scale": "sme"
            },
            "contactPoint": {
                "name": "create_answer: enquiry.author.contactPoint.name",
                "email": "create_answer: enquiry.author.contactPoint.email",
                "telephone": "create_answer: enquiry.author.contactPoint.telephone"
            }
        },
        "title": "create_answer: enquiry.title",
        "description": "create_answer: enquiry.description"

    }
}