#网址https://erabbit.itheima.net/
import requests
from pymongo import MongoClient
import json
data={"categoryId": "1009000",
    "page": 1,      #page为请求的数据页码
    "pageSize": 20}     #pageSize为总页码数
j_data=json.dumps(data)     #转为json数据
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0"
         ,"content-type":"application/json"}        #加入content-type告诉服务器接口请求数据格式【非常重要】
r1=requests.post("https://apipc-xiaotuxian-front.itheima.net/category/goods/temporary",headers=headers,data=j_data)
#print(r1.status_code)
d1=dict(json.loads(r1.text))    #转为字典处理
d2=d1["result"]["items"]
a1=[]
#数据处理
for i in range(len(d2)):
    a2=dict()
    a3=[]
    b1=[]
    a4=[]
    a2["商品ID"]=d2[i]["id"]
    url_p="https://erabbit.itheima.net/#/product"+a2["商品ID"]
    a2["商品名称"]=d2[i]["name"]
    a2["商品描述"]=d2[i]["desc"]
    a2["商品链接"]=url_p
    a2["商品价格"]=d2[i]["price"]
    a2["商品图片链接"]=d2[i]["picture"]
    k1=int(a2["商品ID"])
    # 从源代码中获取每个商品的详细信息
    r2=requests.get(f'https://apipc-xiaotuxian-front.itheima.net/goods?id={k1}',headers=headers)
    b2=json.loads(r2.text)
    a3.append(b2)
    #去掉数据中的‘name’,‘value’,使数据更简洁
    for k in a3:
        b3=[]
        n1=k["result"]["details"]["properties"]
        for j in n1:
            name_1=j["name"]
            value_1=j["value"]
            b3.append(f"{name_1}:{value_1}")
        b1.append("\n".join(b3))        #将商品详情的每个要点换行
    a2["商品详情"]=b1
    #print(a2["商品详情"])
    #a4.append(a2) 测试输出结果
    a1.append(a2)
print("商品数量:",len(a1))
#存储到mongodb数据库中
m1=MongoClient("mongodb://localhost:27017")     #连接本地数据库
g1=m1['database_g1']    #创建数据库database_g1
c1=g1['商品信息']       #创建集合商品信息
for g in a1:
    c1.insert_one(g)
q1=c1.find()
for z in q1:
    print(z)

