from tests.presets import choose_instance

instance = choose_instance()
if instance == "dev":
    host = 'http://10.0.20.126:8900/api/v1'

elif instance == "sandbox":
    host = 'http://10.0.10.116:8900/api/v1'

kafka_host = 'http://127.0.0.1:5000'
create_ei = '/do/ei?country=MD'
update_ei = '/do/ei/'
create_fs = '/do/fs/'
update_fs = '/do/fs/'

# for home kafka_host = 'http://192.168.0.101:5000'  or 'http://192.168.0.102:5000'
#for office kafka_host = 'http://192.168.88.137:5000'
#sandbox = 'http://10.0.10.116:8900/api/v1'
#dev = 'http://10.0.20.126:8900/api/v1'