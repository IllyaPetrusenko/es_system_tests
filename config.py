from tests.presets import choose_instance

instance = choose_instance()
if instance == "dev":
    host = 'http://10.0.20.126:8900/api/v1'
    platform_1 = 'Basic dXNlcjpwYXNzd29yZA=='
    platform_2 = 'Basic YXV0b21hdGlvbl91c2VyOnBhc3N3b3Jk'
elif instance == "sandbox":
    host = 'http://10.0.10.116:8900/api/v1'
    platform_1 = 'Basic dXNlcjpwYXNzd29yZA=='
    platform_2 = 'Basic YXV0b21hdGlvbl91c2VyOnBhc3N3b3Jk'

kafka_host = 'http://82.144.223.29:5000'
create_ei = '/do/ei'
update_ei = '/do/ei/'
create_fs = '/do/fs/'
update_fs = '/do/fs/'

# for home kafka_host = 'http://192.168.0.101:5000'  or 'http://192.168.0.102:5000'
#for office kafka_host = 'http://192.168.88.137:5000'
#sandbox = 'http://10.0.10.116:8900/api/v1'
#dev = 'http://10.0.20.126:8900/api/v1'