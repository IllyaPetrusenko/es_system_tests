from pytest_testrail.plugin import pytestrail

from tests.bpe_create_ei.create_ei import bpe_create_ei
from tests.bpe_create_ei.payloads import ei_full


@pytestrail.case('22132')
class TestBpeCreateEI(object):

    def test_22132_1(self):
        ei = ei_full.copy()
        del ei['tender']
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.00.00.00'
        assert create_ei_response[1]['errors'][0]['description'] == 'Data processing exception.'


@pytestrail.case('22132')
class TestBpeCreateEI(object):
    def test_22132_2(self):
        ei = ei_full.copy()
        del ei['tender']['title']
        print(ei)
        create_ei_response = bpe_create_ei(ei)
        print(create_ei_response)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_ei_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.' \
                                                                    'MissingKotlinParameterException: Instantiation ' \
                                                                    'of [simple type, class com.procurement.budget.' \
                                                                    'model.dto.ei.request.EiCreate$TenderEiCreate] ' \
                                                                    'value failed for JSON property title due to ' \
                                                                    'missing (therefore NULL) value for creator ' \
                                                                    'parameter title which is a non-nullable type\n ' \
                                                                    'at [Source: UNKNOWN; line: -1, column: -1] ' \
                                                                    '(through reference chain: com.procurement.' \
                                                                    'budget.model.dto.ei.request.EiCreate' \
                                                                    '[\"tender\"]->com.procurement.budget.model.' \
                                                                    'dto.ei.request.EiCreate$TenderEiCreate[\"title\"])'


@pytestrail.case('22132')
class TestBpeCreateEI(object):

    def test_22132_3(self):
        ei = ei_full.copy()
        del ei['tender']['classification']
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_ei_response[1]['errors'][0][
                   'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
                                     'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.ei.' \
                                     'EIRequest$Tender] value failed for JSON property classification due to missing ' \
                                     '(therefore NULL) value for creator parameter classification which is a ' \
                                     'non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1] (through ' \
                                     'reference chain: com.procurement.mdm.model.dto.data.ei.EIRequest[\"tender\"]' \
                                     '->com.procurement.mdm.model.dto.data.ei.EIRequest$Tender[\"classification\"])'


@pytestrail.case('22132')
class TestBpeCreateEI(object):

    def test_22132_4(self):
        ei = ei_full.copy()
        del ei['tender']['classification']['id']
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_ei_response[1]['errors'][0][
                   'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
                                     'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.ei.' \
                                     'EIRequest$Tender$Classification] value failed for JSON property id due to ' \
                                     'missing (therefore NULL) value for creator parameter id which is a ' \
                                     'non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1] (through ' \
                                     'reference chain: com.procurement.mdm.model.dto.data.ei.EIRequest[\"tender\"]' \
                                     '->com.procurement.mdm.model.dto.data.ei.EIRequest$Tender[\"classification\"]' \
                                     '->com.procurement.mdm.model.dto.data.ei.EIRequest$Tender$Classification[\"id\"]'


@pytestrail.case('22132')
class TestBpeCreateEI(object):

    def test_22132_5(self):
        ei = ei_full.copy()
        del ei['planning']
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_ei_response[1]['errors'][0][
                   'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
                                     'Instantiation of [simple type, class com.procurement.budget.model.dto.ei.' \
                                     'request.EiCreate] value failed for JSON property planning due to missing ' \
                                     '(therefore NULL) value for creator parameter planning which is a non-nullable ' \
                                     'type\n at [Source: UNKNOWN; line: -1, column: -1] (through reference chain: ' \
                                     'com.procurement.budget.model.dto.ei.request.EiCreate[\"planning\"])'


@pytestrail.case('22132')
class TestBpeCreateEI(object):

    def test_22132_6(self):
        ei = ei_full.copy()
        del ei['planning']['budget']
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_ei_response[1]['errors'][0][
                   'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
                                     'Instantiation of [simple type, class com.procurement.budget.model.dto.ei.' \
                                     'request.EiCreate$PlanningEiCreate] value failed for JSON property budget due ' \
                                     'to missing (therefore NULL) value for creator parameter budget which is a ' \
                                     'non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1] (through ' \
                                     'reference chain: com.procurement.budget.model.dto.ei.request.' \
                                     'EiCreate[\"planning\"]->com.procurement.budget.model.dto.ei.request.' \
                                     'EiCreate$PlanningEiCreate[\"budget\"])'


@pytestrail.case('22132')
class TestBpeCreateEI(object):

    def test_22132_7(self):
        ei = ei_full.copy()
        del ei['planning']['budget']['period']
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_ei_response[1]['errors'][0][
                   'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
                                     'Instantiation of [simple type, class com.procurement.budget.model.dto.ei.' \
                                     'request.EiCreate$PlanningEiCreate$BudgetEiCreate] value failed for JSON ' \
                                     'property period due to missing (therefore NULL) value for creator parameter ' \
                                     'period which is a non-nullable type\n at [Source: UNKNOWN; line: -1, column:' \
                                     ' -1] (through reference chain: com.procurement.budget.model.dto.ei.request.' \
                                     'EiCreate[\"planning\"]->com.procurement.budget.model.dto.ei.request.' \
                                     'EiCreate$PlanningEiCreate[\"budget\"]->com.procurement.budget.model.dto.ei.' \
                                     'request.EiCreate$PlanningEiCreate$BudgetEiCreate[\"period\"])'

@pytestrail.case('22132')
class TestBpeCreateEI(object):

    def test_22132_8(self):
        ei = ei_full.copy()
        del ei['planning']['budget']['period']['startDate']
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_ei_response[1]['errors'][0][
                   'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
                                     'Instantiation of [simple type, class com.procurement.budget.model.dto.ocds.' \
                                     'Period] value failed for JSON property startDate due to missing (therefore ' \
                                     'NULL) value for creator parameter startDate which is a non-nullable type\n at ' \
                                     '[Source: UNKNOWN; line: -1, column: -1] (through reference chain: com.' \
                                     'procurement.budget.model.dto.ei.request.EiCreate[\"planning\"]->com.' \
                                     'procurement.budget.model.dto.ei.request.EiCreate$PlanningEiCreate[\"budget\"]' \
                                     '->com.procurement.budget.model.dto.ei.request.EiCreate$Planning' \
                                     'EiCreate$BudgetEiCreate[\"period\"]->com.procurement.budget.model.dto.ocds.' \
                                     'Period[\"startDate\"])'

@pytestrail.case('22132')
class TestBpeCreateEI(object):

    def test_22132_9(self):
        ei = ei_full.copy()
        del ei['planning']['budget']['period']['endDate']
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_ei_response[1]['errors'][0][
                   'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
                                     'Instantiation of [simple type, class com.procurement.budget.model.dto.ocds.' \
                                     'Period] value failed for JSON property endDate due to missing (therefore NULL) ' \
                                     'value for creator parameter endDate which is a non-nullable type\n at [Source: ' \
                                     'UNKNOWN; line: -1, column: -1] (through reference chain: com.procurement.' \
                                     'budget.model.dto.ei.request.EiCreate[\"planning\"]->com.procurement.budget.' \
                                     'model.dto.ei.request.EiCreate$PlanningEiCreate[\"budget\"]->com.procurement.' \
                                     'budget.model.dto.ei.request.EiCreate$PlanningEiCreate$BudgetEiCreate' \
                                     '[\"period\"]->com.procurement.budget.model.dto.ocds.Period[\"endDate\"])'

@pytestrail.case('22132')
class TestBpeCreateEI(object):

    def test_22132_10(self):
        ei = ei_full.copy()
        del ei['buyer']
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_ei_response[1]['errors'][0][
                   'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
                                     'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.ei.' \
                                     'EIRequest] value failed for JSON property buyer due to missing (therefore ' \
                                     'NULL) value for creator parameter buyer which is a non-nullable type\n at ' \
                                     '[Source: UNKNOWN; line: -1, column: -1] (through reference chain: com.' \
                                     'procurement.mdm.model.dto.data.ei.EIRequest[\"buyer\"])'

@pytestrail.case('22132')
class TestBpeCreateEI(object):

    def test_22132_11(self):
        ei = ei_full.copy()
        del ei['buyer']['name']
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_ei_response[1]['errors'][0][
                   'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
                                     'Instantiation of [simple type, class com.procurement.budget.model.dto.ei.' \
                                     'OrganizationReferenceEi] value failed for JSON property name due to missing ' \
                                     '(therefore NULL) value for creator parameter name which is a non-nullable ' \
                                     'type\n at [Source: UNKNOWN; line: -1, column: -1] (through reference chain: ' \
                                     'com.procurement.budget.model.dto.ei.request.EiCreate[\"buyer\"]->com.' \
                                     'procurement.budget.model.dto.ei.OrganizationReferenceEi[\"name\"])'

@pytestrail.case('22132')
class TestBpeCreateEI(object):

    def test_22132_12(self):
        ei = ei_full.copy()
        del ei['buyer']['identifier']
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_ei_response[1]['errors'][0][
                   'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
                                     'Instantiation of [simple type, class com.procurement.budget.model.dto.ei.' \
                                     'OrganizationReferenceEi] value failed for JSON property identifier due to ' \
                                     'missing (therefore NULL) value for creator parameter identifier which is a ' \
                                     'non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1] (through ' \
                                     'reference chain: com.procurement.budget.model.dto.ei.request.EiCreate' \
                                     '[\"buyer\"]->com.procurement.budget.model.dto.ei.' \
                                     'OrganizationReferenceEi[\"identifier\"])'

@pytestrail.case('22132')
class TestBpeCreateEI(object):

    def test_22132_13(self):
        ei = ei_full.copy()
        del ei['buyer']['identifier']['scheme']
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_ei_response[1]['errors'][0][
                   'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
                                     'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.' \
                                     'Identifier] value failed for JSON property scheme due to missing (therefore ' \
                                     'NULL) value for creator parameter scheme which is a non-nullable type\n at ' \
                                     '[Source: UNKNOWN; line: -1, column: -1] (through reference chain: com.' \
                                     'procurement.mdm.model.dto.data.ei.EIRequest[\"buyer\"]->com.procurement.' \
                                     'mdm.model.dto.data.OrganizationReference[\"identifier\"]->com.procurement.' \
                                     'mdm.model.dto.data.Identifier[\"scheme\"])'
@pytestrail.case('22132')
class TestBpeCreateEI(object):

    def test_22132_14(self):
        ei = ei_full.copy()
        del ei['buyer']['identifier']['id']
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_ei_response[1]['errors'][0][
                   'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
                                     'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.' \
                                     'Identifier] value failed for JSON property id due to missing (therefore NULL) ' \
                                     'value for creator parameter id which is a non-nullable type\n at [Source: ' \
                                     'UNKNOWN; line: -1, column: -1] (through reference chain: com.procurement.mdm.' \
                                     'model.dto.data.ei.EIRequest[\"buyer\"]->com.procurement.mdm.model.dto.data.' \
                                     'OrganizationReference[\"identifier\"]->com.procurement.mdm.model.dto.data.' \
                                     'Identifier[\"id\"])'

@pytestrail.case('22132')
class TestBpeCreateEI(object):

    def test_22132_15(self):
        ei = ei_full.copy()
        del ei['buyer']['identifier']['legalName']
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_ei_response[1]['errors'][0][
                   'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: Instantiation of [simple type, class com.procurement.budget.model.dto.ocds.Identifier] value failed for JSON property legalName due to missing (therefore NULL) value for creator parameter legalName which is a non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1] (through reference chain: com.procurement.budget.model.dto.ei.request.EiCreate[\"buyer\"]->com.procurement.budget.model.dto.ei.OrganizationReferenceEi[\"identifier\"]->com.procurement.budget.model.dto.ocds.Identifier[\"legalName\"])'

@pytestrail.case('22132')
class TestBpeCreateEI(object):

    def test_22132_16(self):
        ei = ei_full.copy()
        del ei['buyer']['address']
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_ei_response[1]['errors'][0][
                   'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
                                     'Instantiation of [simple type, class com.procurement.budget.model.dto.ei.' \
                                     'OrganizationReferenceEi] value failed for JSON property address due to missing ' \
                                     '(therefore NULL) value for creator parameter address which is a non-nullable ' \
                                     'type\n at [Source: UNKNOWN; line: -1, column: -1] (through reference chain: ' \
                                     'com.procurement.budget.model.dto.ei.request.EiCreate[\"buyer\"]->com.' \
                                     'procurement.budget.model.dto.ei.OrganizationReferenceEi[\"address\"])'

@pytestrail.case('22132')
class TestBpeCreateEI(object):

    def test_22132_17(self):
        ei = ei_full.copy()
        del ei['buyer']['address']['streetAddress']
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_ei_response[1]['errors'][0][
                   'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
                                     'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.' \
                                     'Address] value failed for JSON property streetAddress due to missing ' \
                                     '(therefore NULL) value for creator parameter streetAddress which is a ' \
                                     'non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1] (through ' \
                                     'reference chain: com.procurement.mdm.model.dto.data.ei.EIRequest[\"buyer\"]' \
                                     '->com.procurement.mdm.model.dto.data.OrganizationReference[\"address\"]->' \
                                     'com.procurement.mdm.model.dto.data.Address[\"streetAddress\"])'

@pytestrail.case('22132')
class TestBpeCreateEI(object):

    def test_22132_18(self):
        ei = ei_full.copy()
        del ei['buyer']['address']['addressDetails']
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_ei_response[1]['errors'][0][
                   'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
                                     'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.' \
                                     'Address] value failed for JSON property addressDetails due to missing ' \
                                     '(therefore NULL) value for creator parameter addressDetails which is a ' \
                                     'non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1] (through ' \
                                     'reference chain: com.procurement.mdm.model.dto.data.ei.EIRequest' \
                                     '[\"buyer\"]->com.procurement.mdm.model.dto.data.OrganizationReference' \
                                     '[\"address\"]->com.procurement.mdm.model.dto.data.Address[\"addressDetails\"])'

@pytestrail.case('22132')
class TestBpeCreateEI(object):

    def test_22132_19(self):
        ei = ei_full.copy()
        del ei['buyer']['address']['addressDetails']['country']
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_ei_response[1]['errors'][0][
                   'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
                                     'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.' \
                                     'AddressDetails] value failed for JSON property country due to missing ' \
                                     '(therefore NULL) value for creator parameter country which is a non-nullable ' \
                                     'type\n at [Source: UNKNOWN; line: -1, column: -1] (through reference chain: ' \
                                     'com.procurement.mdm.model.dto.data.ei.EIRequest[\"buyer\"]->com.procurement.' \
                                     'mdm.model.dto.data.OrganizationReference[\"address\"]->com.procurement.mdm.' \
                                     'model.dto.data.Address[\"addressDetails\"]->com.procurement.mdm.model.dto.' \
                                     'data.AddressDetails[\"country\"])'

@pytestrail.case('22132')
class TestBpeCreateEI(object):

    def test_22132_20(self):
        ei = ei_full.copy()
        del ei['buyer']['address']['addressDetails']['country']['id']
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_ei_response[1]['errors'][0][
                   'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
                                     'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.' \
                                     'CountryDetails] value failed for JSON property id due to missing (therefore ' \
                                     'NULL) value for creator parameter id which is a non-nullable type\n at ' \
                                     '[Source: UNKNOWN; line: -1, column: -1] (through reference chain: com.' \
                                     'procurement.mdm.model.dto.data.ei.EIRequest[\"buyer\"]->com.procurement.' \
                                     'mdm.model.dto.data.OrganizationReference[\"address\"]->com.procurement.mdm.' \
                                     'model.dto.data.Address[\"addressDetails\"]->com.procurement.mdm.model.dto.' \
                                     'data.AddressDetails[\"country\"]->com.procurement.mdm.model.dto.data.' \
                                     'CountryDetails[\"id\"])'

@pytestrail.case('22132')
class TestBpeCreateEI(object):

    def test_22132_21(self):
        ei = ei_full.copy()
        del ei['buyer']['address']['addressDetails']['region']
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_ei_response[1]['errors'][0][
                   'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
                                     'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.' \
                                     'AddressDetails] value failed for JSON property region due to missing ' \
                                     '(therefore NULL) value for creator parameter region which is a non-nullable ' \
                                     'type\n at [Source: UNKNOWN; line: -1, column: -1] (through reference chain: ' \
                                     'com.procurement.mdm.model.dto.data.ei.EIRequest[\"buyer\"]->com.procurement.' \
                                     'mdm.model.dto.data.OrganizationReference[\"address\"]->com.procurement.mdm.' \
                                     'model.dto.data.Address[\"addressDetails\"]->com.procurement.mdm.model.dto.' \
                                     'data.AddressDetails[\"region\"])'

@pytestrail.case('22132')
class TestBpeCreateEI(object):

    def test_22132_22(self):
        ei = ei_full.copy()
        del ei['buyer']['address']['addressDetails']['region']['id']
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_ei_response[1]['errors'][0][
                   'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
                                     'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.' \
                                     'RegionDetails] value failed for JSON property id due to missing (therefore ' \
                                     'NULL) value for creator parameter id which is a non-nullable type\n at ' \
                                     '[Source: UNKNOWN; line: -1, column: -1] (through reference chain: com.' \
                                     'procurement.mdm.model.dto.data.ei.EIRequest[\"buyer\"]->com.procurement.' \
                                     'mdm.model.dto.data.OrganizationReference[\"address\"]->com.procurement.mdm.' \
                                     'model.dto.data.Address[\"addressDetails\"]->com.procurement.mdm.model.dto.data.' \
                                     'AddressDetails[\"region\"]->com.procurement.mdm.model.dto.data.' \
                                     'RegionDetails[\"id\"])'

@pytestrail.case('22132')
class TestBpeCreateEI(object):

    def test_22132_23(self):
        ei = ei_full.copy()
        del ei['buyer']['address']['addressDetails']['locality']
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_ei_response[1]['errors'][0][
                   'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
                                     'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.' \
                                     'AddressDetails] value failed for JSON property locality due to missing ' \
                                     '(therefore NULL) value for creator parameter locality which is a non-nullable ' \
                                     'type\n at [Source: UNKNOWN; line: -1, column: -1] (through reference chain: ' \
                                     'com.procurement.mdm.model.dto.data.ei.EIRequest[\"buyer\"]->com.procurement.' \
                                     'mdm.model.dto.data.OrganizationReference[\"address\"]->com.procurement.mdm.' \
                                     'model.dto.data.Address[\"addressDetails\"]->com.procurement.mdm.model.dto.' \
                                     'data.AddressDetails[\"locality\"])'

@pytestrail.case('22132')
class TestBpeCreateEI(object):

    def test_22132_24(self):
        ei = ei_full.copy()
        del ei['buyer']['address']['addressDetails']['locality']['scheme']
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_ei_response[1]['errors'][0][
                   'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
                                     'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.' \
                                     'LocalityDetails] value failed for JSON property scheme due to missing ' \
                                     '(therefore NULL) value for creator parameter scheme which is a non-nullable ' \
                                     'type\n at [Source: UNKNOWN; line: -1, column: -1] (through reference chain: ' \
                                     'com.procurement.mdm.model.dto.data.ei.EIRequest[\"buyer\"]->com.procurement.' \
                                     'mdm.model.dto.data.OrganizationReference[\"address\"]->com.procurement.mdm.' \
                                     'model.dto.data.Address[\"addressDetails\"]->com.procurement.mdm.model.dto.' \
                                     'data.AddressDetails[\"locality\"]->com.procurement.mdm.model.dto.data.' \
                                     'LocalityDetails[\"scheme\"])'

@pytestrail.case('22132')
class TestBpeCreateEI(object):

    def test_22132_25(self):
        ei = ei_full.copy()
        del ei['buyer']['address']['addressDetails']['locality']['id']
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_ei_response[1]['errors'][0][
                   'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
                                     'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.' \
                                     'LocalityDetails] value failed for JSON property id due to missing ' \
                                     '(therefore NULL) value for creator parameter id which is a non-nullable ' \
                                     'type\n at [Source: UNKNOWN; line: -1, column: -1] (through reference chain: ' \
                                     'com.procurement.mdm.model.dto.data.ei.EIRequest[\"buyer\"]->com.procurement.' \
                                     'mdm.model.dto.data.OrganizationReference[\"address\"]->com.procurement.mdm.' \
                                     'model.dto.data.Address[\"addressDetails\"]->com.procurement.mdm.model.dto.' \
                                     'data.AddressDetails[\"locality\"]->com.procurement.mdm.model.dto.data.' \
                                     'LocalityDetails[\"id\"])'

@pytestrail.case('22132')
class TestBpeCreateEI(object):

    def test_22132_26(self):
        ei = ei_full.copy()
        del ei['buyer']['address']['addressDetails']['locality']['description']
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_ei_response[1]['errors'][0][
                   'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
                                     'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.' \
                                     'LocalityDetails] value failed for JSON property description due to missing ' \
                                     '(therefore NULL) value for creator parameter description which is a ' \
                                     'non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1] ' \
                                     '(through reference chain: com.procurement.mdm.model.dto.data.ei.' \
                                     'EIRequest[\"buyer\"]->com.procurement.mdm.model.dto.data.' \
                                     'OrganizationReference[\"address\"]->com.procurement.mdm.model.dto.data.' \
                                     'Address[\"addressDetails\"]->com.procurement.mdm.model.dto.data.' \
                                     'AddressDetails[\"locality\"]->com.procurement.mdm.model.dto.data.' \
                                     'LocalityDetails[\"description\"])'

@pytestrail.case('22132')
class TestBpeCreateEI(object):

    def test_22132_27(self):
        ei = ei_full.copy()
        del ei['buyer']['contactPoint']
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_ei_response[1]['errors'][0][
                   'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
                                     'Instantiation of [simple type, class com.procurement.budget.model.dto.ei.' \
                                     'OrganizationReferenceEi] value failed for JSON property contactPoint due ' \
                                     'to missing (therefore NULL) value for creator parameter contactPoint which is ' \
                                     'a non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1] (through ' \
                                     'reference chain: com.procurement.budget.model.dto.ei.request.EiCreate' \
                                     '[\"buyer\"]->com.procurement.budget.model.dto.ei.OrganizationReferenceEi' \
                                     '[\"contactPoint\"])'

@pytestrail.case('22132')
class TestBpeCreateEI(object):

    def test_22132_28(self):
        ei = ei_full.copy()
        del ei['buyer']['contactPoint']['name']
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_ei_response[1]['errors'][0][
                   'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
                                     'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.' \
                                     'ContactPoint] value failed for JSON property name due to missing (therefore ' \
                                     'NULL) value for creator parameter name which is a non-nullable type\n at ' \
                                     '[Source: UNKNOWN; line: -1, column: -1] (through reference chain: com.' \
                                     'procurement.mdm.model.dto.data.ei.EIRequest[\"buyer\"]->com.procurement.' \
                                     'mdm.model.dto.data.OrganizationReference[\"contactPoint\"]->com.procurement.' \
                                     'mdm.model.dto.data.ContactPoint[\"name\"])'

@pytestrail.case('22132')
class TestBpeCreateEI(object):

    def test_22132_29(self):
        ei = ei_full.copy()
        del ei['buyer']['contactPoint']['email']
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_ei_response[1]['errors'][0][
                   'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
                                     'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.' \
                                     'ContactPoint] value failed for JSON property email due to missing ' \
                                     '(therefore NULL) value for creator parameter email which is a ' \
                                     'non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1] ' \
                                     '(through reference chain: com.procurement.mdm.model.dto.data.ei.' \
                                     'EIRequest[\"buyer\"]->com.procurement.mdm.model.dto.data.' \
                                     'OrganizationReference[\"contactPoint\"]->com.procurement.mdm.model.' \
                                     'dto.data.ContactPoint[\"email\"])'

@pytestrail.case('22132')
class TestBpeCreateEI(object):

    def test_22132_30(self):
        ei = ei_full.copy()
        del ei['buyer']['contactPoint']['telephone']
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_ei_response[1]['errors'][0][
                   'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
                                     'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.' \
                                     'ContactPoint] value failed for JSON property telephone due to missing ' \
                                     '(therefore NULL) value for creator parameter telephone which is a non-nullable ' \
                                     'type\n at [Source: UNKNOWN; line: -1, column: -1] (through reference chain: ' \
                                     'com.procurement.mdm.model.dto.data.ei.EIRequest[\"buyer\"]->com.procurement.' \
                                     'mdm.model.dto.data.OrganizationReference[\"contactPoint\"]->com.procurement.' \
                                     'mdm.model.dto.data.ContactPoint[\"telephone\"])'

