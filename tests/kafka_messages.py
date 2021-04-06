import allure
import requests, json
from config import kafka_host
from pprint import pprint


def get_message_from_kafka(x_operation_id):
    kafka_message = requests.get(
        url=kafka_host + '/x-operation-id/' + x_operation_id
    )
    allure.attach(kafka_message, "Message from Kafka")
    kafka_message = kafka_message.json()
    del kafka_message['_id']
    return kafka_message

