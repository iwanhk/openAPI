
from rich.console import Console
from pprint import pprint
from datetime import datetime
import hashlib
import requests
import sys
import os
import time
import random

from rich import print
from rich import pretty
pretty.install()
console = Console(style="white on black", stderr=True)

apiKey = '755c8ae1dc6c9dfdd36369fd8776e4e2'
apiSecret = '10e48c5da76719117ae45e4c3fffcd6f8033a29df3b7119346479ddd66b76e88'

chain_id= 1226

def makeHeader(body):
    sortArgs = {}
    header = {}
    hash = hashlib.md5()

    # 当前日期和时间
    now = datetime.timestamp(datetime.now())
    header['timestamp'] = str(int(now))
    header['nonce'] = str(int(now*1000000))
    header['apiKey'] = apiKey
    sortArgs.update(header)
    sortArgs.update(body)
    # print(f"{sortArgs=}")

    content = ''
    for item in sorted(sortArgs):
        content += item+sortArgs[item]

    content += apiSecret
    # print("-----------------------------"+content)

    hash.update(content.encode(encoding='utf-8'))

    # print(hash.hexdigest())

    # print(response.json())

    header["content-type"] = "application/x-www-form-urlencoded"
    header['sign'] = hash.hexdigest()

    # print(header)
    # print(body)
    # print(hash.hexdigest())
    # print(header)
    # console.print(Panel(header))
    return header


def makeHeader2(body):
    sortArgs = {}
    header = {}
    hash = hashlib.md5()

    # 当前日期和时间
    now = datetime.timestamp(datetime.now())
    header['timestamp'] = str(int(now))
    header['nonce'] = str(int(now*1000000))
    header['apiKey'] = 'f7166420c811e129716fd2893732e128'
    sortArgs.update(header)
    sortArgs.update(body)
    # print(f"{sortArgs=}")

    content = ''
    for item in sorted(sortArgs):
        content += item+sortArgs[item]

    content += '8e7792237deafef05c84e676c9b81408d23c33bbacdb80e136ebe60ca61370ff'
    # print("-----------------------------"+content)

    hash.update(content.encode(encoding='utf-8'))
    header["content-type"] = "application/x-www-form-urlencoded"
    header['sign'] = hash.hexdigest()

    print(header)
    # print(body)
    # print(hash.hexdigest())
    # print(header)
    # console.print(Panel(header))
    return header


def getTransactionByHash(hash):
    body = {}
    body['chainid'] = chain_id
    body['hash'] = hash
    body['id'] = user_id

    api_url = "https://www.binghetao.com/chain-api/api/v1/chain/getTransactionByHash"

    header = makeHeader(body)
    response = requests.get(api_url, params=body, headers=header)

    json = response.json()
    if json['success'] == True:
        return json['data']
    else:
        print(json)


def queryUser():
    body = {}
    body['chainid'] = chain_id
    body['id'] = user_id

    header = makeHeader(body)
    api_url = "https://www.binghetao.com/chain-api/api/v1/chain/queryUser"
    response = requests.get(api_url, params=body, headers=header)

    json = response.json()
    if json['success'] == True:
        return json['data']
    else:
        console.print(json, style="bold red")


def createUser():
    body = {}
    body['chainid'] = chain_id
    body['id'] = user_id

    header = makeHeader(body)
    api_url = "https://www.binghetao.com/chain-api/api/v1/chain/create"
    print(f"{header} {body} {api_url}")
    response = requests.post(api_url, params=body, headers=header)

    print(response)
    json = response.json()
    if json['success'] == True:
        return json['data']
    else:
        console.print(json, style="bold red")

def mintTicketToAddress(tokenId):
    body = {}
    body['tokenId'] = tokenId
    body['operationId'] = str(time.time_ns())
    body['accountAddress'] = "0x8A27A4a26b7CbF1A1627906BA8A84df9bCDbC053"
    body['contractAddress'] = "0x6C3384D0bDf752Dce4984385AbA8b44CC03896a5"

    #header= makePostHeader(body)
    api_url = "https://tickets.cctvyb.com/ticket-api/v1/ticket/mintTicketToAddress"
    header = makeHeader(body)
    response = requests.post(api_url, params=body, headers=header)

    json = response.json()
    # print(json)
    if 'msg' in json and json['msg'] == "成功":
        print('成功' + tokenId+ '['+ str(len(tokenId))+']')
        return json['results']
    else:
        # console.print(json, style="bold red")   
        # console.print("重新调用本操作请使用operationId：" + body['operationId'], style="bold red") 
        print('失败' + tokenId+ '['+ str(len(tokenId))+']')
        return None


if __name__ == "__main__":
    for i in range(100):
        mintTicketToAddress(str(random.randrange(10**3, 10**9)))

