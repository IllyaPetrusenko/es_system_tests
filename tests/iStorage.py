import hashlib
import os
import requests


class Document:
    def __init__(self, instance, path, file_name):
        self.path = os.path.abspath(path)
        self.filename = file_name
        self.m = None
        self.weight = None
        self.doc_id = None
        if instance == "dev":
            self.host_of_services = "http://10.0.20.126"
        elif instance == "sandbox":
            self.host_of_services = "http://10.0.10.116"

    def uploading_document(self):
        with open(self.filename, 'rb') as f:
            self.m = hashlib.md5()
            while True:
                # The 'API.pdf' file was divided into 8192-byte pieces, because 'API.pdf' has big weight.
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
            url=f"{self.host_of_services}:9131/storage/registration/",
            headers={'Content-Type': 'application/json'},
            json=payload).json()['data']['id']
        file = {'file': open(self.path, 'rb')}
        uploading = requests.post(
            url=f"{self.host_of_services}:9131/storage/upload/{self.doc_id}",
            files=file).json()
        return uploading, self.filename, self.m.hexdigest(), self.weight
