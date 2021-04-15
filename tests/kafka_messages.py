import allure
import requests, json
from config import kafka_host
from pprint import pprint

@allure.step('Receive message in feed-point')
def get_message_from_kafka(x_operation_id):
    kafka_message = requests.get(
        url=kafka_host + '/x-operation-id/' + x_operation_id
    ).json()
    del kafka_message['_id']
    allure.attach(json.dumps(kafka_message), 'Message in feed-point')
    return kafka_message

