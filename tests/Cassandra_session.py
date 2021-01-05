import json
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

password_dev = '6AH7vbrkMWnfK'
password_sandbox = 'brT4Kn27RQs'
cluster_dev = '10.0.20.104'
cluster_sandbox = '10.0.10.104'


def execute_cql_from_orchestrator_context(cpid):
    auth_provider = PlainTextAuthProvider(username='caclient', password='brT4Kn27RQs')
    cluster = Cluster(['10.0.10.104'], auth_provider=auth_provider)
    session = cluster.connect('ocds')

    rows = session.execute(f"SELECT * FROM orchestrator_context WHERE cp_id = '{cpid}';").one()
    json_data = json.loads(rows.context)
    # print(json_data)
    return json_data


def execute_cql_from_orchestrator_operation_step_by_oper_id(operation_id, task_id):
    auth_provider = PlainTextAuthProvider(username='caclient', password='brT4Kn27RQs')
    cluster = Cluster(['10.0.10.104'], auth_provider=auth_provider)
    session = cluster.connect('ocds')

    rows_1 = session.execute(f"SELECT * FROM orchestrator_operation WHERE operation_id = '{operation_id}';").one()
    process_id = rows_1.process_id
    rows_2 = session.execute(
        f"SELECT * FROM orchestrator_operation_step WHERE process_id = '{process_id}' AND task_id='{task_id}';").one()
    response_data = json.loads(rows_2.response_data)

    return response_data


def execute_cql_from_orchestrator_operation_step(cp_id, task_id):
    auth_provider = PlainTextAuthProvider(username='caclient', password='brT4Kn27RQs')
    cluster = Cluster(['10.0.10.104'], auth_provider=auth_provider)
    session = cluster.connect('ocds')

    rows = session.execute(
        f"SELECT * FROM orchestrator_operation_step WHERE "
        f"cp_id = '{cp_id}' AND task_id='{task_id}'ALLOW FILTERING;").one()
    response_data = json.loads(rows.response_data)

    return response_data


def get_date_execute_cql_from_orchestrator_operation_step_by_oper_id(operation_id, task_id):
    auth_provider = PlainTextAuthProvider(username='caclient', password='brT4Kn27RQs')
    cluster = Cluster(['10.0.10.104'], auth_provider=auth_provider)
    session = cluster.connect('ocds')

    rows_1 = session.execute(f"SELECT * FROM orchestrator_operation WHERE operation_id = '{operation_id}';").one()
    process_id = rows_1.process_id
    rows_2 = session.execute(
        f"SELECT * FROM orchestrator_operation_step WHERE process_id = '{process_id}' AND task_id='{task_id}';").one()
    get_date = rows_2.step_date

    return get_date
