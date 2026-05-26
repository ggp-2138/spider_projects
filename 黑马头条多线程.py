import requests
import json
from concurrent.futures import ThreadPoolExecutor
from spyder.plugins.projects.utils import cookie

cookie={
  
}
data={
"code":"246810",
"mobile":"12011111111"
}
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0"
    ,"Referer":"http://pc-toutiao-python.itheima.net/"
    ,"Origin":"http://pc-toutiao-python.itheima.net"
    ,"authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3OTQ1Nzg0NTEsInVzZXJfaWQiOjEsInJlZnJlc2giOmZhbHNlLCJ2ZXJpZmllZCI6dHJ1ZX0.AtZFMfaqDeS2S3BM_bLFzrflDqFJi02JPYBn3oHGE4k"
    }               #加入authorization后成功get网站

# print(q1.status_code)
# print(q2.status_code)
a2=[]
def n1(url):
    s1 = requests.Session()
    q1 = s1.post("http://api-toutiao-web.itheima.net/mp/v1_0/authorizations", headers=headers, json=data)
    q2 = s1.get(url,headers=headers, cookies=cookie)
    datas = json.loads(q2.text)
    h1 = datas["data"]["results"]
    for i in range(len(h1)):
        a1 = dict()
        a1["标题"] = h1[i]["title"]
        a1["评论状态"] = h1[i]["comment_status"]
        a1["总评论数"] = h1[i]["total_comment_count"]
        a1["评论粉丝数"] = h1[i]["fans_comment_count"]
        a1["ID"] = h1[i]["id"]
        if h1[i]["comment_status"] is True:
            a1["评论状态"] = "正常"
        else:
            a1["评论状态"] = "关闭"
        a2.append(a1)
    print(a2)

if __name__ == '__main__':
    with ThreadPoolExecutor(10) as x:
        for k in range(1,11):
            url = f'http://api-toutiao-web.itheima.net/mp/v1_0/articles?page={k}&per_page=10&response_type=comment'
            x.submit(n1, url)
    #去重
    t1=set()
    a3=[]
    for j in a2:
        if j["ID"] not in t1:
            t1.add(j["ID"])
            a3.append(j)
            print(j["ID"],"已记录")
    #写入json文件
    with open("hm.json","w+",encoding="utf-8") as f:
        f.write(json.dumps(a3,ensure_ascii=False,indent=2))
    print(f"总共{len(a3)}条数据已保存到hm.json")
    print(a3)

