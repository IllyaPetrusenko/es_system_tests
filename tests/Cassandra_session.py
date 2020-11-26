import json

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

def execute_cql(cpid):
    auth_provider = PlainTextAuthProvider(username='caclient', password='6AH7vbrkMWnfK')
    cluster = Cluster(['10.0.20.104'], auth_provider=auth_provider)
    session = cluster.connect('ocds')

    rows =session.execute(f"SELECT * FROM orchestrator_context WHERE cp_id = '{cpid}';").one()
    json_data = json.loads(rows.context)
    # print(json_data)
    return json_data