# Chain Open API

- [**入门指引**](#入门指引)

    - [**创建API Key**](#创建api-key)
    - [**接口调用方式说明**](#接口调用方式说明)

- [**REST API**](#rest-api)

    - [**接入 URL**](#接入-url)
    - [**请求交互**](#请求交互)
    - [**签名认证**](#签名认证)
    - [**REST API列表**](#rest-api列表)
    - [**创建账户**](#查询系统支持的所有交易对及精度)
    - [**查询账户**](#获取所有交易对行情)
    - [**查询资产**](#获取各个币对最新成交价)
    - [**查询合约地址接口是否支持某个功能**](#获取指定币对当前行情)
  
## 入门指引

**提供了简单易用的API接口，通过API可以创建账户查询资产等**

### 创建api-key

联系管理员获取APIKEY

> **请不要泄露API Key 与 Secret Key信息，以免造成资产损失**

### 接口调用方式说明

- REST API

  提供账户创建，资产查询等操作

<br>

## REST API

### 接入 URL

- ** 待定 **


### 请求交互

#### 介绍

REST API 提供创建账户、查询账户、资产查询、合约是否支持某接口功能

请求头信息中content-type需要统一设置为表单格式:

- **content-type:application/x-www-form-urlencoded**

#### 状态码

状态码    | 说明               | 备注
------ | ---------------- | ---------------------
0      | 成功               | code=0 成功， code >0 失败
403      | No permission             | 没有权限
405      | invalid apiKey          |API Key 无效
406      | signature error          | 签名错误
408      | expire time           | 请求过期
409      | invalid nonce            | nonce 无效
301     | 请求参数错误             | 请求参数错误


### 签名认证

#### 签名说明

API 请求在通过网络传输的过程中极有可能被篡改，为了确保请求未被更改，私有接口均必须使用您的 API Key 做签名认证，以校验参数或参数值在传输途中是否发生了更改。
- 1.所有接口都需要进行鉴权，header参数为apiKey, timestamp, nonce, sign
- 2.timestamp为当前时间戳（秒级），与服务器时间差正负10分钟会被拒绝，nonce为随机字符串（16位），不能与上次请求所使用相同
- 3.签名方法, apiKey, timestamp, nonce，接口参数进行排序连接，使用md5方法进行签名

#### 签名步骤

**以获取账户地址为例**

- 接口

    - GET /api/v1/chain/queryUser

- 示例API秘钥

    - apiKey = 7956ca03fe44238ef1d254799de1b556

    - apiSecret = bd09139024cdd3136a4f6cf60038c1194e6641063e413c47f517a579fbb158ba

**1\. 按照ASCII码的顺序对参数名进行排序**

- 原始参数顺序为:
  - api_key = 7956ca03fe44238ef1d254799de1b556
  - nonce = 1659936393439541
  - timestamp =1659936393
  - id = 15866665555
  - chainid=1
    

- 按照ASCII码顺序对参数名进行排序：
  - api_key = 0816016bb06417f50327e2b557d39aaa
  - chainid = 1
  - id = 15866665555
  - nonce = 1659936589419161
  - timestamp= 1659936589
  
**2\. 所有参数按"参数名参数值"格式拼接在一起组成要签名计算的字符串**

-       apiKey7956ca03fe44238ef1d254799de1b556chainid1id15866665555nonce1659936589419161timestamp1659936589

**3\. 签名计算的字符串与秘钥(Secret Key)拼接形成最终计算的字符串，使用32位MD5算法进行计算生成数字签名**

- MD5(第二步字符串+秘钥)
- MD5(apiKey7956ca03fe44238ef1d254799de1b556chainid1id15866665555nonce1659936589419161timestamp1659936589bd09139024cdd3136a4f6cf60038c1194e6641063e413c47f517a579fbb158ba)

- 签名结果中字母全部小写:

    - sign = bca925c9e774baf35288dc993c160df2

**4\. 将生成的数字签名加入header参数里**

**5\. header参数**
- api_key = 7956ca03fe44238ef1d254799de1b556
- nonce = 1659936393439541
- timestamp =1659936393
- sign = bca925c9e774baf35288dc993c160df2

**6\. body业务参数**
- chainid = 1
- id = 15866665555

### REST API列表

API    | 接口类型       | 说明
------ | ---------|---------------------
[POST /api/v1/chain/create](#创建账户) | 私有接口 | 创建账户
[GET /api/v1/chain/queryUser](#查询用户在链上账户地址)        | 私有接口 | 查询用户在链上账户地址
[GET /api/v1/chain/queryAsset](#查询用户链上资产)            | 私有接口 | 查询用户链上资产
[GET /api/v1/chain/supportsInterface](#查询合约地址接口是否支持某个功能) | 私有接口 | 查询合约地址接口是否支持某个功能
[POST /api/v1/chain/dynamicCall](#动态调用合约方法) | 私有接口 | 动态调用合约方法
[GET /api/v1/chain/getTransactionByHash](#根据交易Hash查询交易信息) | 私有接口 | 根据交易Hash查询交易信息

### 创建账户

#### POST [/api/v1/chain/create]

#### 输入参数:

参数名称   | 是否必须 | 数据类型   | 描述  | 取值范围
------ | ---- | ------ | --- | -----------------------------
id | true | string | 会员手机号 | 1586666555
chainid | true | int | 链id | 1,1029


#### 返回参数:

参数名称   | 数据类型   | 描述
------ | ------ | ---------------------
code   | string | code=0 成功， code >0 失败
success    | bool | true：成功 false:失败
data   | string | 新的地址

#### 返回示例:

```json
{
  "success":true,
  "code":"0",
  "data":"cfxtest:aas4n7d0f4484ety7p9b399kffd3u8p3cajkdsr4tn"
}
```

### 查询用户在链上账户地址

#### GET [/api/v1/chain/queryUser]

#### 输入参数: 
参数名称   | 是否必须 | 数据类型   | 描述  | 取值范围
------ | ---- | ------ | --- | -----------------------------
id | true | string | 会员手机号 | 1586666555
chainid | true | int | 链id | 1,1029
#### 返回参数:

参数名称 | 数据类型   | 描述
---- | ------ | ---------------------
code | string | code=0 成功， code >0 失败
success    | bool | true：成功 false:失败
data   | 数组 | 地址集合

#### 返回示例:

```json
{
  "success":true,
  "code":"0",
  "data":["cfxtest:aardvffhv7mgvpbm3naaycbejr7vvjtc5epsjt22bv","cfxtest:aat050mxjwuxz5wge6r3xhw224y8zd5s1jrm94b8d1","cfxtest:aas4n7d0f4484ety7p9b399kffd3u8p3cajkdsr4tn"]
}

```

### 查询用户链上资产

#### GET [/api/v1/chain/queryAsset]

#### 输入参数:
参数名称   | 是否必须 | 数据类型   | 描述  | 取值范围
------ | ---- | ------ | --- | -----------------------------
tokenId | true | string | token id | 1
chainid | true | int | 链id | 1,1029
contract | true | string | 合约地址 | conflux合约地址
#### 返回参数:

参数名称 | 数据类型   | 描述
---- | ------ | ---------------------
code | string | code=0 成功， code >0 失败
success    | bool | true：成功 false:失败
data   | string | tokenURI

#### 返回示例:

```json
{
  "success":true,
  "code":"0",
  "data":"https://nftstorage.link/ipfs/bafybeicsfqe2q4rwea7pnn3tpymfayoumbfgclbhtfza7f2eza7sarjqrm/1.json"}
```
### 查询合约地址接口是否支持某个功能

#### GET [/api/v1/chain/supportsInterface]

#### 输入参数:

参数名称   | 是否必须 | 数据类型   | 描述  | 取值范围
------ | ---- | ------ | --- | -----------------------------
interfaceID | true | string | interface ID | 十六进制字符串  0x01ffc9a7
chainid | true | int | 链id | 1,1029
contract | true | string | 合约地址 | conflux合约地址

#### 返回参数:

参数名称   | 数据类型   | 描述
------ | ------ | ---------------------
code | string | code=0 成功， code >0 失败
success    | bool | true：成功 false:失败
data   | bool | true:支持，false:不支持

#### 返回示例:

```json
{
  "success":true,
  "code":"0",
  "data":true
}
```

### 动态调用合约方法

#### POST [/api/v1/chain/dynamicCall]

#### 输入参数:

参数名称   | 是否必须 | 数据类型   | 描述  | 取值范围
------ | ---- | ------ | --- | -----------------------------
data | true | string | data | 
chainid | true | int | 链id | 1,1029
contract | true | string | 合约地址 | conflux合约地址

#### 返回参数:

参数名称   | 数据类型   | 描述
------ | ------ | ---------------------
code | string | code=0 成功， code >0 失败
success    | bool | true：成功 false:失败
data   | string | 交易hash

#### 返回示例:

```json
{
  "success":true,
  "code":"0",
  "data":"0x81065643975146780aea7ed79b393bd3f97d3dd8145f0c78441f1dbfe5510681"
}
```

### 根据交易Hash查询交易信息

#### GET [/api/v1/chain/getTransactionByHash]

#### 输入参数:

参数名称   | 是否必须 | 数据类型   | 描述  | 取值范围
------ | ---- | ------ | --- | -----------------------------
chainid | true | int | 链id | 1,1029
hash | true | string | 交易hash id | 

#### 返回参数:

参数名称   | 数据类型   | 描述
------ | ------ | ---------------------
code | string | code=0 成功， code >0 失败
success    | bool | true：成功 false:失败
data   | json | 交易信息

#### 返回示例:

```json
{
  "success":true,
  "code":"0",
  "data":{
    "hash":"0x2b3c532af6ce2b15039b6aead1b8e4c59a453ed4b1f6b4e0f5fc04e97e176c90",
    "nonce":32,
    "blockHash":"0xa52f65da9dd716c0598ff01cfc53f78155f409b067a02084875372dcf281a734",
    "transactionIndex":0,
    "from":"cfxtest:aaj3u3efxtt0yk9jv4hp7egf8r9tee08gy9777z73a",
    "to":"cfxtest:acfpbb9kn2b2z3bev2435dk6j236gzc0kjjj4hwm45",
    "value":0,
    "gasPrice":1000000000,
    "gas":150000,
    "contractCreated":null,
    "data":"0xe4445210000000000000000000000000000000000000000000000000000000000000007b0000000000000000000000000000000000000000000000000000000000000001",
    "storageLimit":0,
    "epochHeight":87255643,
    "chainId":1,
    "status":0,
    "v":0,
    "r":48244449714512018821650909603302023667601838446831864372152677559202493356686,
    "s":768745959168584954437305344220535200287905191887785827617504601230246963072}
}
