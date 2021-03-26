import time
import requests
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from tests.authorization import get_access_token_for_platform_one, get_x_operation_id
from tests.kafka_messages import get_message_from_kafka
from tests.presets import set_instance_for_cassandra, set_instance_for_request, create_ei

password_dev = '6AH7vbrkMWnfK'
password_sandbox = 'brT4Kn27RQs'
cluster_dev = '10.0.20.104'
cluster_sandbox = '10.0.10.104'

instance = set_instance_for_cassandra()
username = instance[1]
password = instance[2]
host = instance[0]


class EI:
    def __init__(self):
        self.access_token = get_access_token_for_platform_one()
        self.x_operation_id = get_x_operation_id(self.access_token)

    def create_request_ei(self, payload, country='MD', lang='ro'):
        self.payload = payload
        self.country = country
        self.lang = lang
        host = set_instance_for_request()
        ei = requests.post(
            url=host + create_ei,
            headers={
                'Authorization': 'Bearer ' + self.access_token,
                'X-OPERATION-ID': self.x_operation_id,
                'Content-Type': 'application/json'},
            params={
                'country': country,
                'lang': lang
            },
            json=self.payload)
        return ei

    def get_message_from_kafka(self):
        time.sleep(1.8)
        message_from_kafka = get_message_from_kafka(self.x_operation_id)
        return message_from_kafka

    def delete_data_from_database(self, cpid):
        self.cpid = cpid
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
