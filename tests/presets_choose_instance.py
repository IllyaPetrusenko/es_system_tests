# You have to choose instance


def set_instance():
    instance = input("Choose your instance: dev or sandbox -> Type it, please: ")
    if instance == "dev":
        cassandra_cluster = "10.0.20.104"
        cassandra_password = "6AH7vbrkMWnfK"
        cassandra_username = "caclient"
        return cassandra_cluster, cassandra_username,cassandra_password, print("Your instance is 'dev'")
    elif instance == "sandbox":
        cassandra_cluster = "10.0.10.104"
        cassandra_password = "brT4Kn27RQs"
        cassandra_username = "caclient"
        return cassandra_cluster, cassandra_password, cassandra_username, print("Your instance is 'sandbox'")
    else:
        return print("I don't know what you mean")

instance = set_instance()