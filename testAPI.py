from csv import reader
from datetime import datetime
import hashlib
import requests

from rich import print
from rich import pretty
pretty.install()
from rich.console import Console 
from pprint import pprint
console = Console(style="black on green", stderr=True)
from rich.panel import Panel

apiKey = "7956ca03fe44238ef1d254799de1b556"
apiSecret = "bd09139024cdd3136a4f6cf60038c1194e6641063e413c47f517a579fbb158ba"

def makeHeader(body):
    sortArgs={}
    header={}
    hash = hashlib.md5()

    # 当前日期和时间
    now = datetime.timestamp(datetime.now())
    header['timestamp']= str(int(now))
    header['nonce']= str(int(now*1000000))
    header['apiKey']=apiKey

    sortArgs.update(header)
    sortArgs.update(body)
    # print(f"{args=}")

    content=''
    for item in sorted(sortArgs):
        content+= item+sortArgs[item]

    content+= apiSecret
    # print(content)

    hash.update(content.encode(encoding='utf-8'))

    # print(hash.hexdigest())

    # print(response.json())

    header["content-type"]="application/x-www-form-urlencoded"
    header['sign']= hash.hexdigest()
    
    # print(header)
    # print(body)
    # print(hash.hexdigest())
    # print(header)
    # console.print(Panel(header))
    return header

def getTransactionByHash(hash):
    body={}
    body['chainid']='1'
    body['hash']= hash

    api_url = "http://35.175.145.216:8087/api/v1/chain/getTransactionByHash"

    header= makeHeader(body)
    response = requests.get(api_url, params= body, headers=header)

    json= response.json()
    if json['success']==True:
        return json['data']
    else:
        print(json)

def dynamicCall(data):
    body={}
    body['chainid']='1'
    body['data']= data
    body['fromAddress']='cfxtest:aak9vkaj4cpuwghsn2vpsf7vgpxk80fa6af7w5uu5f'
    body['contract']='cfxtest:acdk44u31uwr42hy4h6ux03r5kw4ffx9ausk8k53kg'
    body['id']='13911024683'

    api_url = "http://35.175.145.216:8087/api/v1/chain/dynamicCall"

    header= makeHeader(body)
    print(body)
    response = requests.post(api_url, params= body, headers=header)

    json= response.json()
    if json['success']==True:
        return json['data']
    else:
        print(json)

def supportsInterface(selector):
    body={}
    body['chainid']='1'
    body['interfaceID']= selector
    body['contract']='cfxtest:acdk44u31uwr42hy4h6ux03r5kw4ffx9ausk8k53kg'

    api_url = "http://35.175.145.216:8087/api/v1/chain/supportsInterface"

    header= makeHeader(body)
    response = requests.get(api_url, params= body, headers=header)

    json= response.json()
    if json['success']==True:
        return json['data']
    else:
        print(json)


def queryAsset(tokenId):
    body={}
    body['chainid']='1'
    body['tokenId']= tokenId
    body['contract']='cfxtest:acdk44u31uwr42hy4h6ux03r5kw4ffx9ausk8k53kg'

    api_url = "http://35.175.145.216:8087/api/v1/chain/queryAsset"

    header= makeHeader(body)
    response = requests.get(api_url, params= body, headers=header)

    json= response.json()
    if json['success']==True:
        return json['data']
    else:
        print(json)

def queryUser():
    body={}
    body['chainid']='1'
    body['id']='13911024683'

    header= makeHeader(body)
    api_url = "http://35.175.145.216:8087/api/v1/chain/queryUser"
    response = requests.get(api_url, params= body, headers=header)

    json= response.json()
    if json['success']==True:
        return json['data']
    else:
        print(json)

def createUser():
    body={}
    body['chainid']='1'
    body['id']='13911024683'

    header= makeHeader(body)
    api_url = "http://35.175.145.216:8087/api/v1/chain/create"
    # print(f"{header} {body} {api_url}")
    response = requests.post(api_url, params= body, headers=header)

    print(response)
    json= response.json()
    if json['success']==True:
        return json['data']
    else:
        print(json)

if __name__=="__main__":
    while True:
        choice = input("1) createUser\n2) queryUser\n3) queryAsset\n4) supportsInterface\n5) dynamicCall\n6) getTransactionByHash\nq to exit:\n\n")

        commands= choice.split()
        if commands[0] == "q":
            break
        if commands[0] == '1':
            ret= createUser()
        if commands[0] == '2':
            ret= queryUser()
        if commands[0] == '3':
            ret= queryAsset(commands[1]) 
        if commands[0] == '4':
            ret= supportsInterface(commands[1])     
        if commands[0] == '5':
            ret= dynamicCall(commands[1])
        if commands[0] == '6':
            ret= getTransactionByHash(commands[1])
        console.print(Panel(str(ret)))