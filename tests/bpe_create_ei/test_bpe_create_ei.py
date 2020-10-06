import copy
import datetime
import fnmatch

import pytest
import requests
from pytest_testrail.plugin import pytestrail


from tests.bpe_create_ei.create_ei import bpe_create_ei
from tests.bpe_create_ei.payloads import ei_full


class TestBpeCreateEI(object):

    @pytestrail.case('22132')
    def test_22132_1(self):
        ei = copy.deepcopy(ei_full)
        del ei['tender']
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.00.00.00'
        assert create_ei_response[1]['errors'][0]['description'] == 'Data processing exception.'

    @pytestrail.case('22132')
    def test_22132_2(self):
        ei = copy.deepcopy(ei_full)
        del ei['tender']['title']
        create_ei_response = bpe_create_ei(ei)
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
    def test_22132_3(self):
        ei = copy.deepcopy(ei_full)
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
    def test_22132_4(self):
        ei = copy.deepcopy(ei_full)
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
                                     '->com.procurement.mdm.model.dto.data.ei.EIRequest$Tender$Classification[\"id\"])'

    @pytestrail.case('22132')
    def test_22132_5(self):
        ei = copy.deepcopy(ei_full)
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
    def test_22132_6(self):
        ei = copy.deepcopy(ei_full)
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
    def test_22132_7(self):
        ei = copy.deepcopy(ei_full)
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
    def test_22132_8(self):
        ei = copy.deepcopy(ei_full)
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
    def test_22132_9(self):
        ei = copy.deepcopy(ei_full)
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
    def test_22132_10(self):
        ei = copy.deepcopy(ei_full)
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
    def test_22132_11(self):
        ei = copy.deepcopy(ei_full)
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
    def test_22132_12(self):
        ei = copy.deepcopy(ei_full)
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
    def test_22132_13(self):
        ei = copy.deepcopy(ei_full)
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
    def test_22132_14(self):
        ei = copy.deepcopy(ei_full)
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
    def test_22132_15(self):
        ei = copy.deepcopy(ei_full)
        del ei['buyer']['identifier']['legalName']
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_ei_response[1]['errors'][0][
                   'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: Instantiation of [simple type, class com.procurement.budget.model.dto.ocds.Identifier] value failed for JSON property legalName due to missing (therefore NULL) value for creator parameter legalName which is a non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1] (through reference chain: com.procurement.budget.model.dto.ei.request.EiCreate[\"buyer\"]->com.procurement.budget.model.dto.ei.OrganizationReferenceEi[\"identifier\"]->com.procurement.budget.model.dto.ocds.Identifier[\"legalName\"])'

    @pytestrail.case('22132')
    def test_22132_16(self):
        ei = copy.deepcopy(ei_full)
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
    def test_22132_17(self):
        ei = copy.deepcopy(ei_full)
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
    def test_22132_18(self):
        ei = copy.deepcopy(ei_full)
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
    def test_22132_19(self):
        ei = copy.deepcopy(ei_full)
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
    def test_22132_20(self):
        ei = copy.deepcopy(ei_full)
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
    def test_22132_21(self):
        ei = copy.deepcopy(ei_full)
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
    def test_22132_22(self):
        ei = copy.deepcopy(ei_full)
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
    def test_22132_23(self):
        ei = copy.deepcopy(ei_full)
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
    def test_22132_24(self):
        ei = copy.deepcopy(ei_full)
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
    def test_22132_25(self):
        ei = copy.deepcopy(ei_full)
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
    def test_22132_26(self):
        ei = copy.deepcopy(ei_full)
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
    def test_22132_27(self):
        ei = copy.deepcopy(ei_full)
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
    def test_22132_28(self):
        ei = copy.deepcopy(ei_full)
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
    def test_22132_29(self):
        ei = copy.deepcopy(ei_full)
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
    def test_22132_30(self):
        ei = copy.deepcopy(ei_full)
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

    @pytestrail.case('22133')
    def test_22133_1(self):
        ei = copy.deepcopy(ei_full)
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202

    @pytestrail.case('22133')
    def test_22133_2(self):
        ei = copy.deepcopy(ei_full)
        create_ei_response = bpe_create_ei(ei)
        result_of_compare_cpid = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
                                                 'ocds-t1s2t3-MD-*')
        result_of_compare_token = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
                                                  '*')
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert result_of_compare_cpid == True
        assert result_of_compare_token == True

    @pytestrail.case('22133')
    def test_22133_3(self):
        ei = copy.deepcopy(ei_full)
        create_ei_response = bpe_create_ei(ei)
        url = create_ei_response[1]['data']['url'] + '/' + str(create_ei_response[1]['data']['outcomes']['ei'][0]['id'])
        publicPoint = requests.get(url=url).json()
        get_json = publicPoint

        assert get_json['releases'][0]['tender']['title'] == ei['tender']['title']
        assert get_json['releases'][0]['tender']['description'] == ei['tender']['description']
        assert get_json['releases'][0]['tender']['classification']['scheme'] == ei['tender']['classification']['scheme']
        assert get_json['releases'][0]['tender']['classification']['id'] == ei['tender']['classification']['id']
        assert get_json['releases'][0]['tender']['classification'][
                   'description'] == 'Lucrări de pregătire a şantierului'
        assert get_json['releases'][0]['planning']['budget']['id'] == ei['planning']['budget']['id']
        assert get_json['releases'][0]['planning']['budget']['period']['startDate'] == \
               ei['planning']['budget']['period']['startDate']
        assert get_json['releases'][0]['planning']['budget']['period']['endDate'] == ei['planning']['budget']['period'][
            'endDate']
        assert get_json['releases'][0]['planning']['rationale'] == ei['planning']['rationale']
        assert get_json['releases'][0]['buyer']['id'] == ei['buyer']['identifier']['scheme'] + '-' + ei['buyer']['identifier'][
            'id']
        assert get_json['releases'][0]['buyer']['name'] == ei['buyer']['name']
        assert get_json['releases'][0]['parties'][0]['id'] == ei['buyer']['identifier']['scheme']+ '-' + ei['buyer']['identifier'][
            'id']
        assert get_json['releases'][0]['parties'][0]['name'] == ei['buyer']['name']
        assert get_json['releases'][0]['parties'][0]['identifier']['scheme'] == ei['buyer']['identifier']['scheme']
        assert get_json['releases'][0]['parties'][0]['identifier']['id'] == ei['buyer']['identifier']['id']
        assert get_json['releases'][0]['parties'][0]['identifier']['legalName'] == ei['buyer']['identifier']['legalName']
        assert get_json['releases'][0]['parties'][0]['identifier']['uri'] == ei['buyer']['identifier']['uri']
        assert get_json['releases'][0]['parties'][0]['address']['streetAddress'] == ei['buyer']['address']['streetAddress']
        assert get_json['releases'][0]['parties'][0]['address']['postalCode'] == ei['buyer']['address']['postalCode']
        assert get_json['releases'][0]['parties'][0]['address']['addressDetails']['country']['scheme'] == 'iso-alpha2'
        assert get_json['releases'][0]['parties'][0]['address']['addressDetails']['country']['id'] == \
               ei['buyer']['address']['addressDetails']['country']['id']
        assert get_json['releases'][0]['parties'][0]['address']['addressDetails']['country'][
                   'description'] == 'Moldova, Republica'
        assert get_json['releases'][0]['parties'][0]['address']['addressDetails']['country'][
                   'uri'] == 'https://www.iso.org'
        assert get_json['releases'][0]['parties'][0]['address']['addressDetails']['region']['scheme'] == 'CUATM'
        assert get_json['releases'][0]['parties'][0]['address']['addressDetails']['region']['id'] == '1700000'
        assert get_json['releases'][0]['parties'][0]['address']['addressDetails']['region']['description'] == 'Cahul'
        assert get_json['releases'][0]['parties'][0]['address']['addressDetails']['region'][
                   'uri'] == 'http://statistica.md'
        assert get_json['releases'][0]['parties'][0]['address']['addressDetails']['locality']['scheme'] == 'CUATM'
        assert get_json['releases'][0]['parties'][0]['address']['addressDetails']['locality']['id'] == '1701000'
        assert get_json['releases'][0]['parties'][0]['address']['addressDetails']['locality'][
                   'uri'] == 'http://statistica.md'
        assert get_json['releases'][0]['parties'][0]['additionalIdentifiers'][0] == \
               ei['buyer']['additionalIdentifiers'][0]
        assert get_json['releases'][0]['parties'][0]['contactPoint'] == \
               ei['buyer']['contactPoint']
        assert get_json['releases'][0]['parties'][0]['details'] == \
               ei['buyer']['details']

    @pytestrail.case('22135')
    def test_22135_1(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['country']['id'] = 'MD'
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]

    @pytestrail.case('22135')
    def test_22135_2(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['country']['id'] = 'MD'
        create_ei_response = bpe_create_ei(ei)
        cpid = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
                               'ocds-t1s2t3-MD-*')
        token = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
                                '*')

        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert cpid == True
        assert token == True

    @pytestrail.case('22135')
    def test_22135_3(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['country']['id'] = 'MD'
        create_ei_response = bpe_create_ei(ei)
        url = create_ei_response[1]['data']['url'] + '/' + str(create_ei_response[1]['data']['outcomes']['ei'][0]['id'])
        publicPoint = requests.get(url=url).json()

        assert publicPoint['releases'][0]['parties'][0]['address']['addressDetails']['country']['id'] == 'MD'
        assert publicPoint['releases'][0]['parties'][0]['address']['addressDetails']['country'][
                   'scheme'] == 'iso-alpha2'
        assert publicPoint['releases'][0]['parties'][0]['address']['addressDetails']['country'][
                   'description'] == 'Moldova, Republica'
        assert publicPoint['releases'][0]['parties'][0]['address']['addressDetails']['country'][
                   'uri'] == 'https://www.iso.org'

    @pytestrail.case('22136')
    def test_22136_1(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['country']['id'] = 'MD'
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]

    @pytestrail.case('22136')
    def test_22136_2(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['country']['id'] = 'MD'
        create_ei_response = bpe_create_ei(ei)
        cpid = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
                               'ocds-t1s2t3-MD-*')
        token = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
                                '*')

        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert cpid == True
        assert token == True

    @pytestrail.case('22136')
    def test_22136_3(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['country']['id'] = 'MD'
        ei['buyer']['address']['addressDetails']['country']['scheme'] = 'sheme for test'
        create_ei_response = bpe_create_ei(ei)
        url = create_ei_response[1]['data']['url'] + '/' + str(create_ei_response[1]['data']['outcomes']['ei'][0]['id'])
        publicPoint = requests.get(url=url).json()
        print(url)

        assert publicPoint['releases'][0]['parties'][0]['address']['addressDetails']['country'][
                   'scheme'] == 'iso-alpha2'


    @pytestrail.case('22137')
    def test_22137_1(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['country']['id'] = 'MD'
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]

    @pytestrail.case('22137')
    def test_22137_2(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['country']['id'] = 'MD'
        create_ei_response = bpe_create_ei(ei)
        cpid = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
                               'ocds-t1s2t3-MD-*')
        token = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
                                '*')

        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert cpid == True
        assert token == True

    @pytestrail.case('22137')
    def test_22137_3(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['country']['id'] = 'MD'
        ei['buyer']['address']['addressDetails']['country']['uri'] = 'uri for test'
        create_ei_response = bpe_create_ei(ei)
        url = create_ei_response[1]['data']['url'] + '/' + str(create_ei_response[1]['data']['outcomes']['ei'][0]['id'])
        publicPoint = requests.get(url=url).json()
        print(url)

        assert publicPoint['releases'][0]['parties'][0]['address']['addressDetails']['country'][
                   'uri'] == 'https://www.iso.org'


    @pytestrail.case('22138')
    def test_22138_1(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['country']['id'] = 'MD'
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]

    @pytestrail.case('22138')
    def test_22138_2(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['country']['id'] = 'MD'
        create_ei_response = bpe_create_ei(ei)
        cpid = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
                               'ocds-t1s2t3-MD-*')
        token = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
                                '*')

        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert cpid == True
        assert token == True

    @pytestrail.case('22138')
    def test_22138_3(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['country']['id'] = 'MD'
        ei['buyer']['address']['addressDetails']['country']['description'] = 'description for test'
        create_ei_response = bpe_create_ei(ei)
        url = create_ei_response[1]['data']['url'] + '/' + str(create_ei_response[1]['data']['outcomes']['ei'][0]['id'])
        publicPoint = requests.get(url=url).json()
        print(url)

        assert publicPoint['releases'][0]['parties'][0]['address']['addressDetails']['country'][
                   'description'] == 'Moldova, Republica'

    @pytestrail.case('22139')
    def test_22139_1(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['country']['id'] = 'UK'
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]

    @pytestrail.case('22139')
    def test_22139_2(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['country']['id'] = 'UK'
        create_ei_response = bpe_create_ei(ei)
        print(create_ei_response[1])
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.20.01.10'
        assert create_ei_response[1]['errors'][0]['description'] == 'Invalid country. '

    @pytestrail.case('22140')
    def test_22140_1(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['region']['id'] = '3400000'
        ei['buyer']['address']['addressDetails']['locality']['id'] = '3401000'
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]

    @pytestrail.case('22140')
    def test_22140_2(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['region']['id'] = '3400000'
        ei['buyer']['address']['addressDetails']['locality']['id'] = '3401000'
        create_ei_response = bpe_create_ei(ei)
        cpid = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
                               'ocds-t1s2t3-MD-*')
        token = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
                                '*')

        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert cpid == True
        assert token == True

    @pytestrail.case('22140')
    def test_22140_3(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['region']['id'] = '3400000'
        ei['buyer']['address']['addressDetails']['locality']['id'] = '3401000'
        create_ei_response = bpe_create_ei(ei)
        url = create_ei_response[1]['data']['url'] + '/' + str(create_ei_response[1]['data']['outcomes']['ei'][0]['id'])
        publicPoint = requests.get(url=url).json()
        print(url)

        assert publicPoint['releases'][0]['parties'][0]['address']['addressDetails']['region']['scheme'] == 'CUATM'
        assert publicPoint['releases'][0]['parties'][0]['address']['addressDetails']['region']['id'] == \
               ei['buyer']['address']['addressDetails']['region']['id']
        assert publicPoint['releases'][0]['parties'][0]['address']['addressDetails']['region'][
                   'description'] == 'Donduşeni'
        assert publicPoint['releases'][0]['parties'][0]['address']['addressDetails']['region'][
                   'uri'] == 'http://statistica.md'

    @pytestrail.case('22141')
    def test_22141_1(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['region']['id'] = '3400000'
        ei['buyer']['address']['addressDetails']['region']['scheme'] = 'other'
        ei['buyer']['address']['addressDetails']['locality']['id'] = '3401000'
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]

    @pytestrail.case('22141')
    def test_22141_2(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['region']['id'] = '3400000'
        ei['buyer']['address']['addressDetails']['region']['scheme'] = 'other'
        ei['buyer']['address']['addressDetails']['locality']['id'] = '3401000'
        create_ei_response = bpe_create_ei(ei)
        cpid = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
                               'ocds-t1s2t3-MD-*')
        token = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
                                '*')

        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert cpid == True
        assert token == True

    @pytestrail.case('22141')
    def test_22141_3(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['region']['id'] = '3400000'
        ei['buyer']['address']['addressDetails']['region']['scheme'] = 'other'
        ei['buyer']['address']['addressDetails']['locality']['id'] = '3401000'
        create_ei_response = bpe_create_ei(ei)
        url = create_ei_response[1]['data']['url'] + '/' + str(create_ei_response[1]['data']['outcomes']['ei'][0]['id'])
        publicPoint = requests.get(url=url).json()
        print(url)

        assert publicPoint['releases'][0]['parties'][0]['address']['addressDetails']['region']['scheme'] == 'CUATM'

    @pytestrail.case('22142')
    def test_22142_1(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['region']['id'] = '3400000'
        ei['buyer']['address']['addressDetails']['region']['url'] = 'test fro uri'
        ei['buyer']['address']['addressDetails']['locality']['id'] = '3401000'
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]

    @pytestrail.case('22142')
    def test_22142_2(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['region']['id'] = '3400000'
        ei['buyer']['address']['addressDetails']['region']['url'] = 'test fro uri'
        ei['buyer']['address']['addressDetails']['locality']['id'] = '3401000'
        create_ei_response = bpe_create_ei(ei)
        cpid = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
                               'ocds-t1s2t3-MD-*')
        token = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
                                '*')

        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert cpid == True
        assert token == True

    @pytestrail.case('22142')
    def test_22142_3(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['region']['id'] = '3400000'
        ei['buyer']['address']['addressDetails']['region']['url'] = 'test fro uri'
        ei['buyer']['address']['addressDetails']['locality']['id'] = '3401000'
        create_ei_response = bpe_create_ei(ei)
        url = create_ei_response[1]['data']['url'] + '/' + str(create_ei_response[1]['data']['outcomes']['ei'][0]['id'])
        publicPoint = requests.get(url=url).json()
        print(url)

        assert publicPoint['releases'][0]['parties'][0]['address']['addressDetails']['region'][
                   'uri'] == 'http://statistica.md'

    @pytestrail.case('22143')
    def test_22143_1(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['region']['id'] = '3400000'
        ei['buyer']['address']['addressDetails']['region']['description'] = 'test for description'
        ei['buyer']['address']['addressDetails']['locality']['id'] = '3401000'
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]

    @pytestrail.case('22143')
    def test_22143_2(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['region']['id'] = '3400000'
        ei['buyer']['address']['addressDetails']['region']['description'] = 'test for description'
        ei['buyer']['address']['addressDetails']['locality']['id'] = '3401000'
        create_ei_response = bpe_create_ei(ei)
        cpid = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
                               'ocds-t1s2t3-MD-*')
        token = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
                                '*')

        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert cpid == True
        assert token == True

    @pytestrail.case('22143')
    def test_22143_3(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['region']['id'] = '3400000'
        ei['buyer']['address']['addressDetails']['region']['description'] = 'test for description'
        ei['buyer']['address']['addressDetails']['locality']['id'] = '3401000'
        create_ei_response = bpe_create_ei(ei)
        url = create_ei_response[1]['data']['url'] + '/' + str(create_ei_response[1]['data']['outcomes']['ei'][0]['id'])
        publicPoint = requests.get(url=url).json()
        print(url)

        assert publicPoint['releases'][0]['parties'][0]['address']['addressDetails']['region'][
                   'description'] == 'Donduşeni'

    @pytestrail.case('22144')
    def test_22144_1(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['region']['id'] = '3400000aa'
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]

    @pytestrail.case('22144')
    def test_22144_2(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['region']['id'] = '3400000aa'
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.20.00.13'
        assert create_ei_response[1]['errors'][0]['description'] == 'Region not found. '

    @pytestrail.case('22145')
    def test_22145_1(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['region']['id'] = '3400000'
        ei['buyer']['address']['addressDetails']['locality']['scheme'] = 'CUATM'
        ei['buyer']['address']['addressDetails']['locality']['id'] = '1701000'
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]

    @pytestrail.case('22145')
    def test_22145_2(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['region']['id'] = '3400000'
        ei['buyer']['address']['addressDetails']['locality']['scheme'] = 'CUATM'
        ei['buyer']['address']['addressDetails']['locality']['id'] = '1701000'
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[1]['errors'][0]['code'] == '400.20.00.14'
        assert create_ei_response[1]['errors'][0]['description'] == 'Locality not found. '

    @pytestrail.case('22146')
    def test_22146_1(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['region']['id'] = '3400000'
        ei['buyer']['address']['addressDetails']['locality']['id'] = '3401000'
        ei['buyer']['address']['addressDetails']['locality']['scheme'] = 'CUATM'
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]

    @pytestrail.case('22146')
    def test_22146_2(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['region']['id'] = '3400000'
        ei['buyer']['address']['addressDetails']['locality']['id'] = '3401000'
        ei['buyer']['address']['addressDetails']['locality']['scheme'] = 'CUATM'
        create_ei_response = bpe_create_ei(ei)
        cpid = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
                               'ocds-t1s2t3-MD-*')
        token = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
                                '*')

        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert cpid == True
        assert token == True

    @pytestrail.case('22146')
    def test_22146_3(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['region']['id'] = '3400000'
        ei['buyer']['address']['addressDetails']['locality']['id'] = '3401000'
        ei['buyer']['address']['addressDetails']['locality']['scheme'] = 'CUATM'
        create_ei_response = bpe_create_ei(ei)
        url = create_ei_response[1]['data']['url'] + '/' + str(create_ei_response[1]['data']['outcomes']['ei'][0]['id'])
        publicPoint = requests.get(url=url).json()
        print(url)

        assert publicPoint['releases'][0]['parties'][0]['address']['addressDetails']['locality']['scheme'] == 'CUATM'
        assert publicPoint['releases'][0]['parties'][0]['address']['addressDetails']['locality']['id'] == \
               ei['buyer']['address']['addressDetails']['locality']['id']
        assert publicPoint['releases'][0]['parties'][0]['address']['addressDetails']['locality'][
                   'description'] == 'or.Donduşeni (r-l Donduşeni)'
        assert publicPoint['releases'][0]['parties'][0]['address']['addressDetails']['locality'][
                   'uri'] == 'http://statistica.md'

    @pytestrail.case('22147')
    def test_22147_1(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['locality']['id'] = '3401000'
        ei['buyer']['address']['addressDetails']['locality']['scheme'] = 'other'
        del ei['buyer']['address']['addressDetails']['locality']['description']
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]

    @pytestrail.case('22147')
    def test_22147_2(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['locality']['id'] = '3401000'
        ei['buyer']['address']['addressDetails']['locality']['scheme'] = 'other'
        del ei['buyer']['address']['addressDetails']['locality']['description']
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_ei_response[1]['errors'][0][
                   'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
                                     'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.' \
                                     'LocalityDetails] value failed for JSON property description due to missing ' \
                                     '(therefore NULL) value for creator parameter description which is a ' \
                                     'non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1] (through ' \
                                     'reference chain: com.procurement.mdm.model.dto.data.ei.EIRequest' \
                                     '[\"buyer\"]->com.procurement.mdm.model.dto.data.OrganizationReference' \
                                     '[\"address\"]->com.procurement.mdm.model.dto.data.Address' \
                                     '[\"addressDetails\"]->com.procurement.mdm.model.dto.data.AddressDetails' \
                                     '[\"locality\"]->com.procurement.mdm.model.dto.data.Locality' \
                                     'Details[\"description\"])'

    @pytestrail.case('22148')
    def test_22148_1(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['region']['id'] = '3400000'
        ei['buyer']['address']['addressDetails']['locality']['id'] = 'own value'
        ei['buyer']['address']['addressDetails']['locality']['scheme'] = 'other'
        ei['buyer']['address']['addressDetails']['locality']['description'] = 'own locality'
        del ei['buyer']['address']['addressDetails']['locality']['uri']
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]

    @pytestrail.case('22148')
    def test_22148_2(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['region']['id'] = '3400000'
        ei['buyer']['address']['addressDetails']['locality']['id'] = 'own value'
        ei['buyer']['address']['addressDetails']['locality']['scheme'] = 'other'
        ei['buyer']['address']['addressDetails']['locality']['description'] = 'own locality'
        del ei['buyer']['address']['addressDetails']['locality']['uri']
        create_ei_response = bpe_create_ei(ei)
        cpid = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
                               'ocds-t1s2t3-MD-*')
        token = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
                                '*')

        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert cpid == True
        assert token == True

    @pytestrail.case('22148')
    def test_22148_3(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['address']['addressDetails']['region']['id'] = '3400000'
        ei['buyer']['address']['addressDetails']['locality']['id'] = 'own value'
        ei['buyer']['address']['addressDetails']['locality']['scheme'] = 'other'
        ei['buyer']['address']['addressDetails']['locality']['description'] = 'own locality'
        del ei['buyer']['address']['addressDetails']['locality']['uri']
        create_ei_response = bpe_create_ei(ei)
        url = create_ei_response[1]['data']['url'] + '/' + str(create_ei_response[1]['data']['outcomes']['ei'][0]['id'])
        publicPoint = requests.get(url=url).json()
        print(url)

        assert publicPoint['releases'][0]['parties'][0]['address']['addressDetails']['locality']['scheme'] == \
               ei['buyer']['address']['addressDetails']['locality']['scheme']
        assert publicPoint['releases'][0]['parties'][0]['address']['addressDetails']['locality']['id'] == \
               ei['buyer']['address']['addressDetails']['locality']['id']
        assert publicPoint['releases'][0]['parties'][0]['address']['addressDetails']['locality'][
                   'description'] == ei['buyer']['address']['addressDetails']['locality']['description']

    @pytestrail.case('22149')
    def test_22149_1(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['identifier']['scheme'] = 'MD-IDNO'
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]

    @pytestrail.case('22149')
    def test_22149_2(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['identifier']['scheme'] = 'MD-IDNO'
        create_ei_response = bpe_create_ei(ei)
        cpid = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
                               'ocds-t1s2t3-MD-*')
        token = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
                                '*')

        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert cpid == True
        assert token == True

    @pytestrail.case('22149')
    def test_22149_3(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['identifier']['scheme'] = 'MD-IDNO'
        create_ei_response = bpe_create_ei(ei)
        url = create_ei_response[1]['data']['url'] + '/' + str(create_ei_response[1]['data']['outcomes']['ei'][0]['id'])
        publicPoint = requests.get(url=url).json()
        print(url)

        assert publicPoint['releases'][0]['parties'][0]['identifier']['scheme'] == ei['buyer']['identifier']['scheme']

    @pytestrail.case('22150')
    def test_22150_1(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['identifier']['scheme'] = 'MD-NE-DNO'
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]

    @pytestrail.case('22150')
    def test_22150_2(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['identifier']['scheme'] = 'MD-NE-IDNO'
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.20.00.12'
        assert create_ei_response[1]['errors'][0]['description'] == 'Registration scheme not found. '

    @pytestrail.case('22151')
    def test_22151_1(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['details']['typeOfBuyer'] = 'MINISTRY'
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]

    @pytestrail.case('22151')
    def test_22151_2(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['details']['typeOfBuyer'] = 'MINISTRY'
        create_ei_response = bpe_create_ei(ei)
        cpid = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
                               'ocds-t1s2t3-MD-*')
        token = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
                                '*')

        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert cpid == True
        assert token == True

    @pytestrail.case('22151')
    def test_22151_3(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['details']['typeOfBuyer'] = 'MINISTRY'
        create_ei_response = bpe_create_ei(ei)
        url = create_ei_response[1]['data']['url'] + '/' + str(create_ei_response[1]['data']['outcomes']['ei'][0]['id'])
        publicPoint = requests.get(url=url).json()
        print(url)

        assert publicPoint['releases'][0]['parties'][0]['details']['typeOfBuyer'] == ei['buyer']['details']['typeOfBuyer']

    @pytestrail.case('22152')
    def test_22152_1(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['details']['typeOfBuyer'] = 'SCHOOL IS NOT HOME'
        create_ei_response = bpe_create_ei(ei)


        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]

    @pytestrail.case('22152')
    def test_22152_2(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['details']['typeOfBuyer'] = 'SCHOOL IS NOT HOME'
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_ei_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.databind.exc.Invalid' \
                                                                    'FormatException: Cannot deserialize value of ' \
                                                                    'type `com.procurement.mdm.model.dto.data.' \
                                                                    'TypeOfBuyer` from String \"SCHOOL IS NOT ' \
                                                                    'HOME\": value not one of declared Enum ' \
                                                                    'instance names: [NATIONAL_AGENCY, REGIONAL_' \
                                                                    'AUTHORITY, REGIONAL_AGENCY, BODY_PUBLIC, EU_' \
                                                                    'INSTITUTION, MINISTRY]\n at [Source: UNKNOWN; ' \
                                                                    'line: -1, column: -1] (through reference chain: ' \
                                                                    'com.procurement.mdm.model.dto.data.ei.' \
                                                                    'EIRequest[\"buyer\"]->com.procurement.mdm.model.' \
                                                                    'dto.data.OrganizationReference' \
                                                                    '[\"details\"]->com.procurement.mdm.model.dto.' \
                                                                    'data.Details[\"typeOfBuyer\"])'

    @pytestrail.case('22153')
    def test_22153_1(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['details']['mainGeneralActivity'] = 'SOCIAL_PROTECTION'
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]

    @pytestrail.case('22153')
    def test_22153_2(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['details']['mainGeneralActivity'] = 'SOCIAL_PROTECTION'
        create_ei_response = bpe_create_ei(ei)
        cpid = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
                               'ocds-t1s2t3-MD-*')
        token = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
                                '*')

        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert cpid == True
        assert token == True

    @pytestrail.case('22153')
    def test_22153_3(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['details']['mainGeneralActivity'] = 'SOCIAL_PROTECTION'
        create_ei_response = bpe_create_ei(ei)
        url = create_ei_response[1]['data']['url'] + '/' + str(create_ei_response[1]['data']['outcomes']['ei'][0]['id'])
        publicPoint = requests.get(url=url).json()
        print(url)

        assert publicPoint['releases'][0]['parties'][0]['details']['mainGeneralActivity'] == ei['buyer']['details'][
            'mainGeneralActivity']

    @pytestrail.case('22154')
    def test_22154_1(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['details']['mainGeneralActivity'] = 'SOC'
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]

    @pytestrail.case('22154')
    def test_22154_2(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['details']['mainGeneralActivity'] = 'SOC'
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_ei_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.databind.exc.InvalidFormatException: Cannot ' \
                                     'deserialize value of type `com.procurement.mdm.model.dto.data.' \
                                     'MainGeneralActivity` from String \"SOC\": value not one of declared Enum ' \
                                     'instance names: [DEFENCE, PUBLIC_ORDER_AND_SAFETY, ECONOMIC_AND_FINANCIAL_' \
                                     'AFFAIRS, ENVIRONMENT, RECREATION_CULTURE_AND_RELIGION, EDUCATION, SOCIAL_' \
                                     'PROTECTION, HEALTH, GENERAL_PUBLIC_SERVICES, HOUSING_AND_COMMUNITY_' \
                                     'AMENITIES]\n at [Source: UNKNOWN; line: -1, column: -1] (through ' \
                                     'reference chain: com.procurement.mdm.model.dto.data.ei.EIRequest[\"buyer\"]' \
                                     '->com.procurement.mdm.model.dto.data.OrganizationReference' \
                                     '[\"details\"]->com.procurement.mdm.model.dto.data.Details' \
                                     '[\"mainGeneralActivity\"])'

    @pytestrail.case('22155')
    def test_22155_1(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['details']['mainSectoralActivity'] = 'WATER'
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]

    @pytestrail.case('22155')
    def test_22155_2(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['details']['mainSectoralActivity'] = 'WATER'
        create_ei_response = bpe_create_ei(ei)
        cpid = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
                               'ocds-t1s2t3-MD-*')
        token = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
                                '*')

        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert cpid == True
        assert token == True

    @pytestrail.case('22155')
    def test_22155_3(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['details']['mainSectoralActivity'] = 'WATER'
        create_ei_response = bpe_create_ei(ei)
        url = create_ei_response[1]['data']['url'] + '/' + str(create_ei_response[1]['data']['outcomes']['ei'][0]['id'])
        publicPoint = requests.get(url=url).json()
        print(url)

        assert publicPoint['releases'][0]['parties'][0]['details']['mainSectoralActivity'] == ei['buyer']['details'][
            'mainSectoralActivity']

    @pytestrail.case('22156')
    def test_22156_1(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['details']['mainSectoralActivity'] = 'WAT'
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]

    @pytestrail.case('22156')
    def test_22156_2(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['details']['mainSectoralActivity'] = 'WAT'
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_ei_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.databind.exc.' \
                                                                    'InvalidFormatException: Cannot deserialize ' \
                                                                    'value of type `com.procurement.mdm.model.dto.' \
                                                                    'data.MainSectoralActivity` from String ' \
                                                                    '\"WAT\": value not one of declared Enum ' \
                                                                    'instance names: [EXPLORATION_EXTRACTION_GAS_' \
                                                                    'OIL, ELECTRICITY, POSTAL_SERVICES, PRODUCTION_' \
                                                                    'TRANSPORT_DISTRIBUTION_GAS_HEAT, WATER, URBAN_' \
                                                                    'RAILWAY_TRAMWAY_TROLLEYBUS_BUS_SERVICES, PORT_R' \
                                                                    'ELATED_ACTIVITIES, RAILWAY_SERVICES, ' \
                                                                    'EXPLORATION_EXTRACTION_COAL_OTHER_SOLID_FUEL, ' \
                                                                    'AIRPORT_RELATED_ACTIVITIES]\n at [Source: ' \
                                                                    'UNKNOWN; line: -1, column: -1] (through ' \
                                                                    'reference chain: com.procurement.mdm.model.' \
                                                                    'dto.data.ei.EIRequest[\"buyer\"]->com.' \
                                                                    'procurement.mdm.model.dto.data.Organization' \
                                                                    'Reference[\"details\"]->com.procurement.' \
                                                                    'mdm.model.dto.data.Details[\"mainSectoral' \
                                                                    'Activity\"])'

    @pytestrail.case('22157')
    def test_22157_1(self):
        ei = copy.deepcopy(ei_full)
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]

    @pytestrail.case('22157')
    def test_22157_2(self):
        ei = copy.deepcopy(ei_full)
        create_ei_response = bpe_create_ei(ei)
        cpid = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
                               '*')
        token = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
                                '*')

        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert cpid == True
        assert token == True

    @pytestrail.case('22157')
    def test_22157_3(self):
        ei = copy.deepcopy(ei_full)
        create_ei_response = bpe_create_ei(ei)
        url = create_ei_response[1]['data']['url'] + '/' + str(create_ei_response[1]['data']['outcomes']['ei'][0]['id'])
        cpid = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
                               'ocds-t1s2t3-MD-*')
        assert cpid == True

    @pytestrail.case('22158')
    def test_22158_1(self):
        ei = copy.deepcopy(ei_full)
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]

    @pytestrail.case('22158')
    def test_22158_2(self):
        ei = copy.deepcopy(ei_full)
        create_ei_response = bpe_create_ei(ei)
        cpid = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
                               '*')
        token = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
                                '*')

        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert cpid == True
        assert token == True

    @pytestrail.case('22158')
    def test_22158_3(self):
        ei = copy.deepcopy(ei_full)
        create_ei_response = bpe_create_ei(ei)
        url = create_ei_response[1]['data']['url'] + '/' + str(create_ei_response[1]['data']['outcomes']['ei'][0]['id'])
        publicPoint = requests.get(url=url).json()
        release_id = publicPoint['releases'][0]['id']
        timestamp = int(release_id[29:39])
        date = datetime.datetime.utcfromtimestamp(timestamp)
        human_date = date.strftime('%Y-%m-%dT%H:%M:%SZ')

        assert create_ei_response[1]['data']['operationDate'] == human_date

    @pytestrail.case('22159')
    def test_22159_1(self):
        ei = copy.deepcopy(ei_full)
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]

    @pytestrail.case('22159')
    def test_22159_2(self):
        ei = copy.deepcopy(ei_full)
        create_ei_response = bpe_create_ei(ei)
        cpid = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
                               '*')
        token = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
                                '*')

        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert cpid == True
        assert token == True

    @pytestrail.case('22159')
    def test_22159_3(self):
        ei = copy.deepcopy(ei_full)
        create_ei_response = bpe_create_ei(ei)
        url = create_ei_response[1]['data']['url'] + '/' + str(create_ei_response[1]['data']['outcomes']['ei'][0]['id'])
        publicPoint = requests.get(url=url).json()

        assert create_ei_response[1]['data']['operationDate'] == publicPoint['releases'][0]['date']

    @pytestrail.case('22160')
    def test_22160_1(self):
        ei = copy.deepcopy(ei_full)
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]

    @pytestrail.case('22160')
    def test_22160_2(self):
        ei = copy.deepcopy(ei_full)
        create_ei_response = bpe_create_ei(ei)
        cpid = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
                               '*')
        token = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
                                '*')

        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert cpid == True
        assert token == True

    @pytestrail.case('22160')
    def test_22160_3(self):
        ei = copy.deepcopy(ei_full)
        create_ei_response = bpe_create_ei(ei)
        url = create_ei_response[1]['data']['url'] + '/' + str(create_ei_response[1]['data']['outcomes']['ei'][0]['id'])
        publicPoint = requests.get(url=url).json()
        tender_id = fnmatch.fnmatch(publicPoint['releases'][0]['tender']['id'], '*')
        print(tender_id)
        assert tender_id == True

    @pytestrail.case('22161')
    def test_22161_1(self):
        ei = copy.deepcopy(ei_full)
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]

    @pytestrail.case('22161')
    def test_22162_2(self):
        ei = copy.deepcopy(ei_full)
        create_ei_response = bpe_create_ei(ei)
        cpid = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
                               '*')
        token = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
                                '*')

        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert cpid == True
        assert token == True

    @pytestrail.case('22161')
    def test_22163_3(self):
        ei = copy.deepcopy(ei_full)
        create_ei_response = bpe_create_ei(ei)
        url = create_ei_response[1]['data']['url'] + '/' + str(create_ei_response[1]['data']['outcomes']['ei'][0]['id'])
        publicPoint = requests.get(url=url).json()

        assert publicPoint['releases'][0]['tender']['status'] == 'planning'

    @pytestrail.case('22162')
    def test_22162_1(self):
        ei = copy.deepcopy(ei_full)
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]

    @pytestrail.case('22162')
    def test_22162_2(self):
        ei = copy.deepcopy(ei_full)
        create_ei_response = bpe_create_ei(ei)
        cpid = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
                               '*')
        token = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
                                '*')

        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert cpid == True
        assert token == True

    @pytestrail.case('22162')
    def test_22162_3(self):
        ei = copy.deepcopy(ei_full)
        create_ei_response = bpe_create_ei(ei)
        url = create_ei_response[1]['data']['url'] + '/' + str(create_ei_response[1]['data']['outcomes']['ei'][0]['id'])
        publicPoint = requests.get(url=url).json()

        assert publicPoint['releases'][0]['tender']['statusDetails'] == 'empty'

    @pytestrail.case('22163')
    def test_22163_1(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['identifier']['id'] = '1010101010'
        ei['buyer']['identifier']['scheme'] = 'MD-IDNO'
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]

    @pytestrail.case('22163')
    def test_22163_2(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['identifier']['id'] = '1010101010'
        ei['buyer']['identifier']['scheme'] = 'MD-IDNO'
        create_ei_response = bpe_create_ei(ei)
        cpid = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
                               '*')
        token = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
                                '*')

        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert cpid == True
        assert token == True

    @pytestrail.case('22163')
    def test_22163_3(self):
        ei = copy.deepcopy(ei_full)
        ei['buyer']['identifier']['id'] = '1010101010'
        ei['buyer']['identifier']['scheme'] = 'MD-IDNO'
        create_ei_response = bpe_create_ei(ei)
        url = create_ei_response[1]['data']['url'] + '/' + str(create_ei_response[1]['data']['outcomes']['ei'][0]['id'])
        publicPoint = requests.get(url=url).json()

        assert publicPoint['releases'][0]['buyer']['id'] == ei['buyer']['identifier']['scheme'] + '-' + \
               ei['buyer']['identifier']['id']

    @pytestrail.case('22164')
    def test_22164_1(self):
        ei = copy.deepcopy(ei_full)
        ei['tender']['classification']['id'] = '24200000-6'
        ei['planning']['budget']['id'] = ei['tender']['classification']['id']
        ei['tender']['classification']['scheme'] = 'CPV'
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]

    @pytestrail.case('22164')
    def test_22164_2(self):
        ei = copy.deepcopy(ei_full)
        ei['tender']['classification']['id'] = '24200000-6'
        ei['planning']['budget']['id'] = ei['tender']['classification']['id']
        ei['tender']['classification']['scheme'] = 'CPV'
        create_ei_response = bpe_create_ei(ei)
        cpid = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
                               '*')
        token = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
                                '*')

        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert cpid == True
        assert token == True

    @pytestrail.case('22164')
    def test_22164_3(self):
        ei = copy.deepcopy(ei_full)
        ei['tender']['classification']['id'] = '24200000-6'
        ei['planning']['budget']['id'] = ei['tender']['classification']['id']
        ei['tender']['classification']['scheme'] = 'CPV'
        create_ei_response = bpe_create_ei(ei)
        url = create_ei_response[1]['data']['url'] + '/' + str(create_ei_response[1]['data']['outcomes']['ei'][0]['id'])
        publicPoint = requests.get(url=url).json()

        assert publicPoint['releases'][0]['tender']['classification']['id'] == ei['tender']['classification']['id']

    @pytestrail.case('22165')
    def test_22165_1(self):
        ei = copy.deepcopy(ei_full)
        currentDate = datetime.datetime.now()
        startDate = currentDate.strftime('%Y-%m-%dT%H:%M:%SZ')
        duration_date = currentDate + datetime.timedelta(minutes=10)
        endDate = duration_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        ei['planning']['budget']['period']['startDate'] = startDate
        ei['planning']['budget']['period']['endDate'] = endDate
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]


    @pytestrail.case('22165')
    def test_22165_2(self):
        ei = copy.deepcopy(ei_full)
        currentDate = datetime.datetime.now()
        startDate = currentDate.strftime('%Y-%m-%dT%H:%M:%SZ')
        duration_date = currentDate + datetime.timedelta(minutes=10)
        endDate = duration_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        ei['planning']['budget']['period']['startDate'] = startDate
        ei['planning']['budget']['period']['endDate'] = endDate
        create_ei_response = bpe_create_ei(ei)
        cpid = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
                               '*')
        token = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
                                '*')

        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert cpid == True
        assert token == True

    @pytestrail.case('22165')
    def test_22165_3(self):
        ei = copy.deepcopy(ei_full)
        currentDate = datetime.datetime.now()
        startDate = currentDate.strftime('%Y-%m-%dT%H:%M:%SZ')
        duration_date = currentDate + datetime.timedelta(minutes=10)
        endDate = duration_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        ei['planning']['budget']['period']['startDate'] = startDate
        ei['planning']['budget']['period']['endDate'] = endDate
        create_ei_response = bpe_create_ei(ei)

        url = create_ei_response[1]['data']['url'] + '/' + str(create_ei_response[1]['data']['outcomes']['ei'][0]['id'])
        publicPoint = requests.get(url=url).json()
        result = publicPoint['releases'][0]['planning']['budget']['period']['endDate'] > \
                 publicPoint['releases'][0]['planning']['budget']['period']['startDate']

        assert publicPoint['releases'][0]['planning']['budget']['period']['startDate'] == \
               ei['planning']['budget']['period'][
                   'startDate']
        assert publicPoint['releases'][0]['planning']['budget']['period']['endDate'] == \
               ei['planning']['budget']['period'][
                   'endDate']
        assert result == True

    @pytestrail.case('22166')
    def test_22166_1(self):
        ei = copy.deepcopy(ei_full)
        currentDate = datetime.datetime.now()
        startDate = currentDate.strftime('%Y/%m/%dT%H:%M:%SZ')
        duration_date = currentDate + datetime.timedelta(minutes=10)
        endDate = duration_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        ei['planning']['budget']['period']['startDate'] = startDate
        ei['planning']['budget']['period']['endDate'] = endDate
        create_ei_response = bpe_create_ei(ei)
        print(startDate)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]

    @pytestrail.case('22166')
    def test_22166_2(self):
        ei = copy.deepcopy(ei_full)
        currentDate = datetime.datetime.now()
        startDate = currentDate.strftime('%Y/%m/%dT%H:%M:%SZ')
        duration_date = currentDate + datetime.timedelta(minutes=10)
        endDate = duration_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        ei['planning']['budget']['period']['startDate'] = startDate
        ei['planning']['budget']['period']['endDate'] = endDate
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_ei_response[1]['errors'][0]['description'] == f"com.fasterxml.jackson.databind.JsonMapping" \
                                                                    f"Exception: Text '{startDate}' could not be " \
                                                                    f"parsed at index 4 (through reference chain: " \
                                                                    f"com.procurement.budget.model.dto.ei.request." \
                                                                    f"EiCreate[\"planning\"]->com.procurement." \
                                                                    f"budget.model.dto.ei.request.EiCreate$Planning" \
                                                                    f"EiCreate[\"budget\"]->com.procurement.budget." \
                                                                    f"model.dto.ei.request.EiCreate$PlanningEi" \
                                                                    f"Create$BudgetEiCreate[\"period\"]->com." \
                                                                    f"procurement.budget.model.dto.ocds." \
                                                                    f"Period[\"startDate\"])"

    @pytestrail.case('22168')
    @pytest.mark.xfail(reason='This rule is not implemented')
    def test_22168_1(self):
        ei = copy.deepcopy(ei_full)
        startDate = '2019-02-31T12:40:00Z'
        endDate = '2020-12-31T12:40:00Z'
        ei['planning']['budget']['period']['startDate'] = startDate
        ei['planning']['budget']['period']['endDate'] = endDate
        create_ei_response =bpe_create_ei(ei)

        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]


    @pytestrail.case('22168')
    @pytest.mark.xfail(reason='This rule is not implemented')
    def test_22168_2(self):
        ei = copy.deepcopy(ei_full)
        startDate = '2019-02-31T12:40:00Z'
        endDate = '2020-12-31T12:40:00Z'
        ei['planning']['budget']['period']['startDate'] = startDate
        ei['planning']['budget']['period']['endDate'] = endDate
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.04.01.02'
        assert create_ei_response[1]['errors'][0]['description'] == 'Invalid period.'