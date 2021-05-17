import requests, json
from config import kafka_host
from pprint import pprint


def get_message_from_kafka(x_operation_id):
    kafka_message = requests.get(
        url=kafka_host + '/x-operation-id/' + x_operation_id
    )
    if kafka_message.status_code == 404:
        while kafka_message.status_code == 404:
            kafka_message = requests.get(
                url=kafka_host + '/x-operation-id/' + x_operation_id
            )
            if kafka_message.status_code == 200:
                kafka_message = requests.get(
                    url=kafka_host + '/x-operation-id/' + x_operation_id
                ).json()
                del kafka_message['_id']
                return kafka_message
    if kafka_message.status_code == 200:
        kafka_message = requests.get(
            url=kafka_host + '/x-operation-id/' + x_operation_id
        ).json()
        del kafka_message['_id']
        return kafka_message

