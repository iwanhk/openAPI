
from rich.console import Console
from pprint import pprint
from datetime import datetime
import hashlib
import requests
import sys
import os
import time

from rich import print
from rich import pretty
pretty.install()
console = Console(style="white on black", stderr=True)

apiKey = os.getenv("ISOTOP_APPKEY")
apiSecret = os.getenv("ISOTOP_SECRET")
# contract_add="cfxtest:acdeym6gccnx752abhpupmmtar5e635uu6xcv2cfgy"
# contract_add='0x05271BB6F2387fbFf5cacdDBCBD5a7C1021A4b11'
# contract_add=='cfxtest:acdk44u31uwr42hy4h6ux03r5kw4ffx9ausk8k53kg'
# contract_add = 'cfx:acak9mwwemm4tgvs7j798je832mrptyrpa9d6ea78s'
contract_add = '0x5067CE4dC9a2fb2c3E1898fc24B067cd8d92A000'
# chain_id='5555'
chain_id = '1226'
# user_id = '13911024683'
# user_id = '18518517787'
# user_id = '13121189506'
# user_id = '18067008266'
# user_id = '18886038683'
# user_id = '13911024683'
user_id = '18812345678'
operationId=0


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

    print(header)
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

def importAccount(private_key):
    body = {}
    body['chainid'] = chain_id
    body['privateKey'] = private_key
    # body['id'] = ''
    body['id'] = user_id

    api_url = "https://www.binghetao.com/chain-api/api/v1/chain/importAddress"

    header = makeHeader(body)
    response = requests.post(api_url, params=body, headers=header)

    json = response.json()
    if json['success'] == True:
        return json['data']
    else:
        print(json)


def exportAccount(address):
    body = {}
    body['chainid'] = chain_id
    body['address'] = address
    body['id'] = user_id

    api_url = "https://www.binghetao.com/chain-api/api/v1/chain/exportAddress"

    header = makeHeader(body)
    response = requests.get(api_url, params=body, headers=header)
    print(header)
    print(body)

    json = response.json()
    if json['success'] == True:
        return json['data']
    else:
        print(json)


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


def writeCall(_from, data):
    body = {}
    body['chainid'] = chain_id
    body['data'] = data
    body['fromAddress'] = _from
    body['contract'] = contract_add
    body['id'] = user_id

    api_url = "https://www.binghetao.com/chain-api/api/v1/chain/writeCall"

    header = makeHeader(body)
    console.print(body, style="bold yellow")

    response = requests.post(api_url, params=body, headers=header)

    json = response.json()
    if json['success'] == True:
        return json['data']
    else:
        console.print(json, style="bold red")


def readCall(data):
    body = {}
    body['chainid'] = chain_id
    body['data'] = data
    body['contract'] = contract_add
    body['id'] = user_id

    api_url = "https://www.binghetao.com/chain-api/api/v1/chain/readCall"

    header = makeHeader(body)
    # print(body)
    response = requests.get(api_url, params=body, headers=header)

    json = response.json()
    print(response.content)
    if json['success'] == True:
        return json['data']
    else:
        console.print(json, style="bold red")


def supportsInterface(erc):
    body = {}
    body['chainid'] = chain_id
    body['interfaceID'] = erc
    body['contract'] = contract_add

    api_url = "https://www.binghetao.com/chain-api/api/v1/chain/supportsInterface"

    header = makeHeader(body)
    response = requests.get(api_url, params=body, headers=header)

    json = response.json()
    if json['success'] == True:
        return json['data']
    else:
        console.print(json, style="bold red")


def queryAsset(tokenId):
    body = {}
    body['chainid'] = chain_id
    body['tokenId'] = tokenId
    body['contract'] = contract_add

    api_url = "https://www.binghetao.com/chain-api/api/v1/chain/queryAsset"

    header = makeHeader(body)
    response = requests.get(api_url, params=body, headers=header)

    json = response.json()
    if json['success'] == True:
        return json['data']
    else:
        console.print(json, style="bold red")


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

def mintTicketToAddress(to, tokenId):
    body = {}
    body['accountAddress'] = to
    body['operationId'] = time.asctime()
    body['contractAddress'] = contract_add
    body['tokenId'] = tokenId
    body['chainid'] = chain_id

    #header= makePostHeader(body)
    api_url = "https://tjtest.pugongyinghulian.com/ticket-api/v1/ticket/mintTicketToAddress"
    header = makeHeader2(body)
    response = requests.post(api_url, params=body, headers=header)

    json = response.json()
    # print(json)
    if 'msg' in json and json['msg'] == "成功":
        return json['results']
    else:
        console.print(json, style="bold red")   
        console.print("重新调用本操作请使用operationId：" + body['operationId'], style="bold red") 
        return None


if __name__ == "__main__":
    if len(sys.argv) == 3:
        contract_add = sys.argv[1]
        chain_id = sys.argv[2]
    print(f"{contract_add=} {chain_id=}")

    while True:
        choice = input(
            "1) createUser\n2) queryUser\n3) queryAsset [tokenId]\n4) supportsInterface [selector]\n5) readCall [data]\n6) writeCall [from, data]\n7) getTransactionReceiptByHash [hash]\n8) importAccount [private-key]\n9) exportAccount [account]\na) mint a ticket [to] [tokenId]\nq) to exit:\n\n")

        commands = choice.split()
        if len(commands) == 0 or commands[0] == "q":
            break
        if commands[0] == '1':
            ret = createUser()
        if commands[0] == '2':
            ret = queryUser()
        if commands[0] == '3':
            ret = queryAsset(commands[1])
        if commands[0] == '4':
            ret = supportsInterface(commands[1])
        if commands[0] == '5':
            ret = readCall(commands[1])
        if commands[0] == '6':
            ret = writeCall(commands[1], commands[2])
        if commands[0] == '7':
            ret = getTransactionByHash(commands[1])
        if commands[0] == '8':
            ret = importAccount(commands[1])
        if commands[0] == '9':
            ret = exportAccount(commands[1])
        if commands[0] == 'a' or commands[0] == 'A':
            ret = mintTicketToAddress(commands[1], commands[2])
        console.print(ret, style="white on black")
