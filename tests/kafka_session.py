import json
import uuid
from kafka import KafkaProducer


class Kafka:
    def __init__(self, instance):
        self.producer = None
        if instance == "dev":
            self.zookeeper_host = "10.0.20.107"
            self.broker_port = "9092"
        elif instance == "sandbox":
            self.zookeeper_host = "10.0.10.109"
            self.broker_port = "9092"

    def connect_kafka_producer(self):
        try:
            self.producer = KafkaProducer(bootstrap_servers=[f'{self.zookeeper_host}:{self.broker_port}'])
        except Exception as ex:
            print('Exception while connecting Kafka')
            print(str(ex))
        finally:
            return self.producer

    def publish_message_into_chronograph_in_clarification(self, cp_id, enquiry_end):
        try:
            topic_name = 'chronograph-in'
            value = json.dumps({
                "action": "SCHEDULE",
                "ocid": cp_id,
                "phase": "clarification",
                "launchTime": enquiry_end,
                "metaData": "{\"operationId\":\""+f"{uuid.uuid1()}" + "\","
                            "\"requestId\":\""+f"{uuid.uuid1()}" + "\","
                            f"\"cpid\":\"{cp_id}\","
                            "\"processType\":\"enquiryPeriodEnd\","
                            "\"isAuction\":true}"
            })

            value_bytes = bytes(value, encoding='utf-8')
            self.producer.send(topic_name, value=value_bytes)
            self.producer.flush()
            print('Message published successfully into chronograph-in topic.')
        except Exception as ex:
            print('Exception in publishing message')
            print(str(ex))

    def publish_message_into_chronograph_in_submission(self, cp_id, ev_id, tender_end, ):
        try:
            topic_name = 'chronograph-in'
            value = json.dumps({"action": "SCHEDULE", "ocid": f"{cp_id}",
                                "phase": "tendering",
                                "launchTime": tender_end,
                                "metaData": "{\"operationId\":\""+f"{uuid.uuid1()}" + "\","
                                            "\"requestId\":\""+f"{uuid.uuid1()}" + "\","
                                            f"\"cpid\":\"{cp_id}\","
                                            f"\"ocid\":\"{ev_id}\","
                                            "\"processType\":\"tenderPeriodEndAuction\","
                                            "\"isAuction\":false}"})
            value_bytes = bytes(value, encoding='utf-8')
            self.producer.send(topic_name, value=value_bytes)
            self.producer.flush()
            print('Message published successfully into chronograph-in topic.')
        except Exception as ex:
            print('Exception in publishing message')
            print(str(ex))
