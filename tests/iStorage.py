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


def get_weught(filepath):
    weight = os.stat(filepath).st_size
    return weight


def correct_document_uploading(path="/home/roman/Documents/git/es_system_tests/API.pdf", file_name="API.pdf",
                               dir_path="/home/roman/Documents/git/es_system_tests/"):
    path = os.path.abspath(path)
    hash_sum = get_hash_md5(path)
    weight = os.stat(path).st_size
    payload = {
        "fileName": file_name,
        "hash": f"{hash_sum}",
        "weight": weight
    }
    dir_path = dir_path
    file_name = file_name
    document = document_upload(payload, dir_path, file_name)
    return document, hash_sum, weight


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

class Document:
    def __init__(self, path, filename):
        self.path = os.path.abspath(path)
        self.filename = filename




    def uploading_document(self):
        with open(self.filename, 'rb') as f:
            self.m = hashlib.md5()
            while True:
                data = f.read(8192)
                if not data:
                    break
                self.m.update(data)

        self.weight = os.stat(self.path).st_size
        payload = {
            "fileName": self.filename,
            "hash": f"{self.m.hexdigest()}",
            "weight": self.weight
        }
        self.doc_id = requests.post(
            url=f"{host}:9131/storage/registration/",
            headers={'Content-Type': 'application/json'},
            json=payload).json()['data']['id']

        file = {'file': open(self.path, 'rb')}
        print(file)
        uploading = requests.post(
            url=f"{host}:9131/storage/upload/{self.doc_id}",
            files=file).json()
        return uploading, self.filename, self.m.hexdigest(), self.weight

# class Document:
#     def __init__(self, path, filename):
#             self.path = os.path.abspath(path)
#             self.filename = filename
#     def calculate_hash(self):
#
#         with open(self.filename, 'rb') as f:
#             self.m = hashlib.md5()
#             while True:
#                 data = f.read(8192)
#                 if not data:
#                     break
#                 self.m.update(data)
#             return self.m.hexdigest()
#
#     def calculate_weight(self):
#         self.weight = os.stat(self.path).st_size
#         return self.weight
#
#     def registration_document(self):
#         payload = {
#             "fileName": self.filename,
#             "hash": f"{self.m.hexdigest()}",
#             "weight": self.weight
#         }
#         self.doc_id = requests.post(
#             url=f"{host}:9131/storage/registration/",
#             headers={'Content-Type': 'application/json'},
#             json=payload).json()['data']['id']
#         return self.doc_id
#
#     def uploading_document(self):
#
#         file = {'file': open(self.path, 'rb')}
#         print(file)
#         uploading = requests.post(
#             url=f"{host}:9131/storage/upload/{self.doc_id}",
#             files=file).json()
#         return uploading