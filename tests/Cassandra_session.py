import datetime
import json
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

from tests.presets import set_instance_for_cassandra

password_dev = '6AH7vbrkMWnfK'
password_sandbox = 'brT4Kn27RQs'
cluster_dev = '10.0.20.104'
cluster_sandbox = '10.0.10.104'

instance = set_instance_for_cassandra()
username = instance[1]
password = instance[2]
host = instance[0]


def execute_cql_from_orchestrator_context(cpid):
    auth_provider = PlainTextAuthProvider(username=username, password=password)
    cluster = Cluster([host], auth_provider=auth_provider)
    session = cluster.connect('ocds')

    rows = session.execute(f"SELECT * FROM orchestrator_context WHERE cp_id = '{cpid}';").one()
    json_data = json.loads(rows.context)
    # print(json_data)
    return json_data


def execute_cql_from_orchestrator_operation_step_by_oper_id(operation_id, task_id):
    auth_provider = PlainTextAuthProvider(username=username, password=password)
    cluster = Cluster([host], auth_provider=auth_provider)
    session = cluster.connect('ocds')

    rows_1 = session.execute(f"SELECT * FROM orchestrator_operation WHERE operation_id = '{operation_id}';").one()
    process_id = rows_1.process_id
    rows_2 = session.execute(
        f"SELECT * FROM orchestrator_operation_step WHERE process_id = '{process_id}' AND task_id='{task_id}';").one()
    request_data = json.loads(rows_2.request_data)
    response_data = json.loads(rows_2.response_data)
    step_date = rows_2.step_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    context = json.loads(rows_2.context)

    return request_data, response_data, step_date, context




def execute_cql_from_orchestrator_operation_step(cp_id, task_id):
    auth_provider = PlainTextAuthProvider(username=username, password=password)
    cluster = Cluster([host], auth_provider=auth_provider)
    session = cluster.connect('ocds')

    rows = session.execute(
        f"SELECT * FROM orchestrator_operation_step WHERE "
        f"cp_id = '{cp_id}' AND task_id='{task_id}'ALLOW FILTERING;").one()
    response_data = json.loads(rows.response_data)

    return response_data


def get_date_execute_cql_from_orchestrator_operation_step_by_oper_id(operation_id, task_id):
    auth_provider = PlainTextAuthProvider(username=username, password=password)
    cluster = Cluster([host], auth_provider=auth_provider)
    session = cluster.connect('ocds')

    rows_1 = session.execute(f"SELECT * FROM orchestrator_operation WHERE operation_id = '{operation_id}';").one()
    process_id = rows_1.process_id
    rows_2 = session.execute(
        f"SELECT * FROM orchestrator_operation_step WHERE process_id = '{process_id}' AND task_id='{task_id}';").one()
    get_date = rows_2.step_date

    return get_date


def get_release_date(cpid, stage):
    auth_provider = PlainTextAuthProvider(username=username, password=password)
    cluster = Cluster([host], auth_provider=auth_provider)
    session = cluster.connect('ocds')

    release_date = session.execute(
        f"SELECT release_date FROM notice_budget_compiled_release WHERE cp_id = '{cpid}' and stage ='{stage}' "
        f"ALLOW FILTERING;").one()
    return release_date[0]

def get_publish_date(cpid, stage):
    auth_provider = PlainTextAuthProvider(username=username, password=password)
    cluster = Cluster([host], auth_provider=auth_provider)
    session = cluster.connect('ocds')

    publish_date = session.execute(
        f"SELECT publish_date FROM notice_budget_compiled_release WHERE cp_id = '{cpid}' and stage ='{stage}' "
        f"ALLOW FILTERING;").one()
    return publish_date[0]