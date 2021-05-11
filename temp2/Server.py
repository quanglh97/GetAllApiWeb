
from fastapi import FastAPI
import uvicorn
from typing import Optional
from datetime import datetime
from elasticsearch import Elasticsearch
import uvicorn
from typing import Optional
import base64


es = Elasticsearch(hosts='192.168.100.248', port=19200)

app = FastAPI()

# commandTemp = {
#     'domain': 'test',
#     'url': 'test',
#     'time': datetime.now(),
#     'status': 'done',
# }
# res = es.index(index="domain", body=commandTemp)
# print(res['result'])

def insertCommand(domain, url, depth, proxy):
    command = {
        'domain': domain,
        'url': url,
        'depth': depth,
        'time': datetime.now(),
        'proxy': proxy,
        'status': 'not_run',
    }
    res = es.index(index="domain", body=command)
    return res

def searchAllCommand():
    searchParam = {
        "query": {
            "match_all" : {}
        }
    }
    res = es.search(index = "domain", body=searchParam)
    return res

def checkCommandNotRun(domainx):
    searchParam = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "domain": domainx
                        }
                    }
                ],
                "must_not": [
                    {
                        "match": {
                            "status": "done"
                        }
                    }
                ]
            }
        }
    }
    res = es.search(index="domain", body=searchParam)
    if res['hits']['total']['value'] > 0:
        return res
    return False

def checkStatusCommand(domain, url, commandId):
    searchParamByCommandId = {
        "query": {
            "bool": {
                "must": [
                    {
                        "term": {
                            "_id": commandId
                        }
                    }
                ]
            }
        }
    }

    searchParamByUrl ={
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "domain": domain
                        }
                    },
                    {
                        "match": {
                            "url": url
                        }
                    }
                ]
            }
        }
    }

    if commandId is not None:
        res = es.search(index="domain", body=searchParamByCommandId)
        return res["hits"]["hits"]
    else:
        res = es.search(index="domain", body=searchParamByUrl)
        print("quang: ", res)
        return res["hits"]["hits"]

def searchApiCommand(commandId):
    searchParamApiCommand = {
        "query": {
            "match": {
            "commandId": commandId
            }
        },
        "size": 20
    }

    res = es.search(index="api", body=searchParamApiCommand)
    return res['hits']['hits']

def insertProxy(host, port, country=None, authUser= None, authPass = None, status = None):
    data = {
        'host': host,
        'port': port, 
        'status': status,
        'country': country,
        'authuser': authUser,
        'authpass': authPass,
    }

    proxyId = host + ':'+ port
    proxyId_bytes = proxyId.encode('ascii')
    base64_bytes = base64.b64encode(proxyId_bytes)
    base64_proxyId = base64_bytes.decode('ascii')

    res = es.index(index="proxy", id= base64_proxyId, body=data)
    return res

def searchAllProxy():
    query = {
        "query": {
            "match_all": {}
        }
    }
    res = es.search(index="proxy", body=query)
    return res['hits']['hits']

def searchProxyById(proxyId):
    res = es.search(index='proxy', id=proxyId)
    return res


def deleteProxy(proxyId):
    res = es.delete(index='proxy', id=proxyId)
    return res

#root link
@app.get("/")
async def home():
    return '''<h1>SCAN API WEB</h1>
            <p>HERE IS SERVER SUPPORT FOR SCAN API WEBSITE</p>'''
########################## API FOR COMMAND ################################################################################
#post command to domain index
@app.post('/api/post/command')
def api_post_command(domain: str, url: str, depth: int, proxy: int):
    check = checkCommandNotRun(domain)
    if check :
        return "Command is not done in server", check['hits']['hits']
    resp = insertCommand(domain, url, depth, proxy)
    return resp

#get all domain exists in domain index
@app.get('/api/get/command/all')
def api_get_command_all():
    allCommand = searchAllCommand()
    return allCommand['hits']['hits']

#get status command
@app.get('/api/get/command/status')
def api_get_command_status(domain: Optional[str] = None, url: Optional[str] = None, commandId: Optional[str] = None):
    statusCommand = checkStatusCommand(domain, url, commandId)
    return statusCommand

#get api scanned of command
@app.get('/api/get/command/api')
def api_get_command_api(commandId: str): 
    listApi = searchApiCommand(commandId)
    return listApi

########################## API FOR PROXY ########################################################################################
#post proxy for scan 
@app.post('/api/post/proxy') #(host, port, country=None, authUser= None, authPass = None, status = None)
def api_post_proxy(host:str, port:str, country: Optional[str] = None, authUser: Optional[str] = None, authPass: Optional[str] = None, status: Optional[int] = None):
    resp = insertProxy(host, port, country, authUser, authPass, status)
    return resp

#get list proxy for scan
@app.get('/api/get/proxy/all')
def api_get_proxy_all():
    resp = searchAllProxy()
    return resp

#get proxy with proxyId
@app.get('/api/get/proxy/id')
def api_get_proxy(proxyId: str):
    resp = searchProxyById(proxyId)
    return resp


#delete proxy 
@app.delete('/api/delete/proxy')
def api_delete_proxy(proxyId: str):
    resp = deleteProxy(proxyId)
    return resp

if __name__  == '__main__':
    uvicorn.run(app, host = "0.0.0.0", port = 8005)