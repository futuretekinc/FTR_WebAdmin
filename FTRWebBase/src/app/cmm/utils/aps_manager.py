import requests
import json
import urllib.parse

class APSchManager(object):
    headers = {
        'content-type' : 'application/json'
    }
    def __init__(self,host='localhost',port=5000):
        self.url = "http://{}:{}".format(host,port)
    def create_job(self,job):
        target = self.urljoin('/scheduler/jobs')
        r = requests.post(target,headers=self.headers,data=json.dumps(job))
        if r.status_code == 200:
            return True
        print(r.text)
        return False
    def has_running_job(self,epid):
        pass
    def delete(self):
        pass
    def pause(self):
        pass
    def resume(self):
        pass
    def urljoin(self,extra):
        return urllib.parse.urljoin(self.url,extra) 


# r = requests.post('http://localhost:5000/scheduler/jobs',data=json.dumps(job),headers=headers)
# print(r.text)
# r = requests.post('http://localhost:5000/scheduler/jobs/job12/pause')
# r = requests.post('http://localhost:5000/scheduler/jobs/job1/resume')
'''
r = requests.delete('http://localhost:5000/scheduler/jobs/job1')
print(r.text)
'''
# print(r.status_code)