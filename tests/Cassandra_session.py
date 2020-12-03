import json

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider


def execute_cql_from_orchestrator_context(cpid):
    auth_provider = PlainTextAuthProvider(username='caclient', password='6AH7vbrkMWnfK')
    cluster = Cluster(['10.0.20.104'], auth_provider=auth_provider)
    session = cluster.connect('ocds')

    rows = session.execute(f"SELECT * FROM orchestrator_context WHERE cp_id = '{cpid}';").one()
    json_data = json.loads(rows.context)
    # print(json_data)
    return json_data

def execute_cql_from_orchestrator_operation_step(operation_id, task_id):
    auth_provider = PlainTextAuthProvider(username='caclient', password='6AH7vbrkMWnfK')
    cluster = Cluster(['10.0.20.104'], auth_provider=auth_provider)
    session = cluster.connect('ocds')

    rows_1 = session.execute(f"SELECT * FROM orchestrator_operation WHERE operation_id = '{operation_id}';").one()
    process_id = rows_1.process_id
    rows_2 = session.execute(
        f"SELECT * FROM orchestrator_operation_step WHERE process_id = '{process_id}' AND task_id='{task_id}';").one()
    response_data = json.loads(rows_2.response_data)

    return response_data


a = '3fdc54ce-00c4-48d5-8c5f-e79640fe83e7'
task = 'SaveContextTask'
b = execute_cql_from_orchestrator_operation_step(a, task)
print(b)
