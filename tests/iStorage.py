import hashlib
import os

import requests

from tests.presets import set_instance_for_services

host = set_instance_for_services()


def document_upload(payload, dir_path, file_name):
    doc_id = requests.post(
        url=f"{host}:9131/storage/registration/",
        headers={'Content-Type': 'application/json'},
        json=payload).json()['data']['id']
    file = {'file': open(dir_path + file_name, 'rb')}
    document_uploading = requests.post(
        url=f"{host}:9131/storage/upload/{doc_id}",
        files=file).json()
    return doc_id, document_uploading


def get_hash_md5(filename):
    with open(filename, 'rb') as f:
        m = hashlib.md5()
        while True:
            data = f.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()


# This is document will be registered and uploaded
# API.pdf has path = "/home/roman/Documents/git/es_system_tests/API.pdf"
# path = os.path.abspath('API.pdf')
# hash_sum = get_hash_md5(path)
# weight = os.stat(path).st_size
# payload = {
#     "fileName": "API.pdf",
#     "hash": f"{hash_sum}",
#     "weight": weight
# }
# dir_path = "/home/roman/Documents/git/es_system_tests/"
# file_name = "API.pdf"
# document = document_upload(payload, dir_path, file_name)
