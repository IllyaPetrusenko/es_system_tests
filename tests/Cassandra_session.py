import json

from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster


# def execute_cql_from_orchestrator_context(cpid):
#     auth_provider = PlainTextAuthProvider(username=username, password=password)
#     cluster = Cluster([host], auth_provider=auth_provider)
#     session = cluster.connect('ocds')
#
#     rows = session.execute(f"SELECT * FROM orchestrator_context WHERE cp_id = '{cpid}';").one()
#     json_data = json.loads(rows.context)
#     # print(json_data)
#     return json_data
#
#


class Cassandra:
    def __init__(self, cp_id, instance, cassandra_username, cassandra_password):
        self.cp_id = cp_id
        self.instance = instance
        self.cassandra_username = cassandra_username
        self.cassandra_password = cassandra_password
        if instance == "dev":
            self.cassandra_cluster = "10.0.20.104"
        elif instance == "sandbox":
            self.cassandra_cluster = "10.0.10.106"

    def execute_cql_from_orchestrator_operation_step(self, task_id):
        auth_provider = PlainTextAuthProvider(username=self.cassandra_username, password=self.cassandra_password)
        cluster = Cluster([self.cassandra_cluster], auth_provider=auth_provider)
        session = cluster.connect('ocds')
        rows = session.execute(
            f"SELECT * FROM orchestrator_operation_step WHERE "
            f"cp_id = '{self.cp_id}' AND task_id='{task_id}'ALLOW FILTERING;").one()
        response_data = json.loads(rows.response_data)
        return response_data

    def execute_cql_from_orchestrator_operation_step_by_oper_id(self, operation_id, task_id):
        auth_provider = PlainTextAuthProvider(username=self.cassandra_username, password=self.cassandra_password)
        cluster = Cluster([self.cassandra_cluster], auth_provider=auth_provider)
        session = cluster.connect('ocds')

        rows_1 = session.execute(f"SELECT * FROM orchestrator_operation WHERE operation_id = '{operation_id}';").one()
        process_id = rows_1.process_id
        rows_2 = session.execute(
            f"SELECT * FROM orchestrator_operation_step WHERE process_id = '{process_id}' AND "
            f"task_id='{task_id}';").one()
        request_data = json.loads(rows_2.request_data)
        response_data = json.loads(rows_2.response_data)
        step_date = rows_2.step_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        context = json.loads(rows_2.context)

        return request_data, response_data, step_date, context

# def get_date_execute_cql_from_orchestrator_operation_step_by_oper_id(operation_id, task_id):
#     auth_provider = PlainTextAuthProvider(username=username, password=password)
#     cluster = Cluster([host], auth_provider=auth_provider)
#     session = cluster.connect('ocds')
#
#     rows_1 = session.execute(f"SELECT * FROM orchestrator_operation WHERE operation_id = '{operation_id}';").one()
#     process_id = rows_1.process_id
#     rows_2 = session.execute(
#         f"SELECT * FROM orchestrator_operation_step WHERE process_id = '{process_id}' AND task_id='{task_id}';").one()
#     get_date = rows_2.step_date
#
#     return get_date
#
#
# def get_release_date(cpid, stage):
#     auth_provider = PlainTextAuthProvider(username=username, password=password)
#     cluster = Cluster([host], auth_provider=auth_provider)
#     session = cluster.connect('ocds')
#
#     release_date = session.execute(
#         f"SELECT release_date FROM notice_budget_compiled_release WHERE cp_id = '{cpid}' and stage ='{stage}' "
#         f"ALLOW FILTERING;").one()
#     return release_date[0]
#
#
# def get_publish_date(cpid, stage):
#     auth_provider = PlainTextAuthProvider(username=username, password=password)
#     cluster = Cluster([host], auth_provider=auth_provider)
#     session = cluster.connect('ocds')
#
#     publish_date = session.execute(
#         f"SELECT publish_date FROM notice_budget_compiled_release WHERE cp_id = '{cpid}' and stage ='{stage}' "
#         f"ALLOW FILTERING;").one()
#     return publish_date[0]
#
#
# def clear_auctions_auctions_by_cpid(cpid):
#     auth_provider = PlainTextAuthProvider(username=username, password=password)
#     cluster = Cluster([host], auth_provider=auth_provider)
#     session = cluster.connect('ocds')
#     del_auction_from_database = session.execute(f"DELETE FROM access_tender WHERE cp_id='{cpid}';").one()
#
#     return del_auction_from_database
