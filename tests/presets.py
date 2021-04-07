# You have to choose instance
import time

import allure


def choose_instance():
    instance = "dev"
    return instance


def set_instance_for_cassandra():
    instance = choose_instance()
    if instance == "dev":
        cassandra_cluster = "10.0.20.104"
        cassandra_password = "6AH7vbrkMWnfK"
        cassandra_username = "caclient"
        return cassandra_cluster, cassandra_username, cassandra_password, print("Your instance is 'dev'")
    elif instance == "sandbox":
        cassandra_cluster = "10.0.10.106"
        cassandra_password = "brT4Kn27RQs"
        cassandra_username = "caclient"
        return cassandra_cluster, cassandra_password, cassandra_username, print("Your instance is 'sandbox'")
    else:
        return print("I don't know what you mean")


def set_instance_for_request():
    instance = choose_instance()
    if instance == "dev":
        host = 'http://10.0.20.126:8900/api/v1'
        allure.attach(host, 'HOST')
        return host
    elif instance == "sandbox":
        host = 'http://10.0.10.116:8900/api/v1'
        allure.attach(host, 'HOST')
        return host


def set_instance_for_services():
    instance = choose_instance()
    if instance == "dev":
        host = 'http://10.0.20.126'
        return host
    elif instance == "sandbox":
        host = 'http://10.0.10.116'
        return host


kafka_host = 'http://192.168.0.102:5000'
create_ei = '/do/ei'
update_ei = '/do/ei/'
create_fs = '/do/fs/'
update_fs = '/do/fs/'
create_pn = '/do/pn'
update_pn = '/do/pn/'
create_cn = '/do/cn/'



# for home kafka_host = 'http://192.168.0.101:5000'
#for office kafka_host = 'http://192.168.88.137:5000'
#sandbox = 'http://10.0.10.116:8900/api/v1'
#dev = 'http://10.0.20.126:8900/api/v1'