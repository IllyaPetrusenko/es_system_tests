import fnmatch
import json
import time

import allure
import requests
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from tests.authorization import get_access_token_for_platform_one, get_x_operation_id
from tests.kafka_messages import get_message_from_kafka
from tests.presets import set_instance_for_cassandra, set_instance_for_request, create_ei
from useful_functions import is_it_uuid

password_dev = '6AH7vbrkMWnfK'
password_sandbox = 'brT4Kn27RQs'
cluster_dev = '10.0.20.104'
cluster_sandbox = '10.0.10.104'

instance = set_instance_for_cassandra()
username = instance[1]
password = instance[2]
host = instance[0]


class EI:
    def __init__(self, payload, country='MD', lang='ro'):
        self.payload = payload
        self.country = country
        self.lang = lang
        self.access_token = get_access_token_for_platform_one()
        self.x_operation_id = get_x_operation_id(self.access_token)

    @allure.step('Create EI')
    def create_ei(self):
        environment_host = set_instance_for_request()
        ei = requests.post(
            url=environment_host + create_ei,
            headers={
                'Authorization': 'Bearer ' + self.access_token,
                'X-OPERATION-ID': self.x_operation_id,
                'Content-Type': 'application/json'},
            params={
                'country': self.country,
                'lang': self.lang
            },
            json=self.payload)
        allure.attach(environment_host + create_ei, 'URL')
        allure.attach(json.dumps(self.payload), 'Prepared payload')
        return ei

    @allure.step('Receive message in feed-point')
    def get_message_from_kafka(self):
        time.sleep(1.8)
        message_from_kafka = get_message_from_kafka(self.x_operation_id)
        allure.attach(json.dumps(message_from_kafka), 'Message in feed-point')
        return message_from_kafka

    def delete_data_from_database(self):
        cpid = get_message_from_kafka(self.x_operation_id)['data']['outcomes']['ei'][0]['id']
        auth_provider = PlainTextAuthProvider(username=username, password=password)
        cluster = Cluster([host], auth_provider=auth_provider)
        session = cluster.connect('ocds')
        del_orchestrator_context_from_database = session.execute(
            f"DELETE FROM orchestrator_context WHERE cp_id='{cpid}';").one()
        del_budget_ei_from_database = session.execute(f"DELETE FROM budget_ei WHERE cp_id='{cpid}';").one()
        del_notice_budget_release_from_database = session.execute(
            f"DELETE FROM notice_budget_release WHERE cp_id='{cpid}';").one()
        del_notice_budget_offset_from_database = session.execute(
            f"DELETE FROM notice_budget_offset WHERE cp_id='{cpid}';").one()
        del_notice_budget_compiled_release_from_database = session.execute(
            f"DELETE FROM notice_budget_compiled_release WHERE cp_id='{cpid}';").one()
        return del_orchestrator_context_from_database, del_budget_ei_from_database, \
               del_notice_budget_release_from_database, del_notice_budget_offset_from_database, \
               del_notice_budget_compiled_release_from_database

    def check_on_that_message_is_successfull(self):
        message = get_message_from_kafka(self.x_operation_id)
        check_x_operartion_id = is_it_uuid(message["X-OPERATION-ID"], 4)
        check_x_response_id = is_it_uuid(message["X-RESPONSE-ID"], 1)
        check_initiator = fnmatch.fnmatch(message["initiator"], "platform")
        check_ocid = fnmatch.fnmatch(message["data"]["ocid"], "ocds-t1s2t3-MD-*")
        check_url = fnmatch.fnmatch(message["data"]["url"],
                                    f"http://dev.public.eprocurement.systems/budgets/{message['data']['ocid']}")
        check_operation_date = fnmatch.fnmatch(message["data"]["operationDate"], "202*-*-*T*:*:*Z")
        check_ei_id = fnmatch.fnmatch(message["data"]["outcomes"]["ei"][0]["id"], "ocds-t1s2t3-MD-*")
        check_ei_token = is_it_uuid(message["data"]["outcomes"]["ei"][0]["X-TOKEN"], 4)
        if check_x_operartion_id == True and check_x_response_id == True and check_initiator == True and \
                check_ocid == True and check_url == True and check_operation_date == True and check_ei_id == True and \
                check_ei_token == True:
            return True
        else:
            return False
