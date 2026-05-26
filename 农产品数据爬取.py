import requests
from lxml import etree
import re
import time
import random
import json
r1 = requests.Session()
r1.verify = False
proxy_index=0
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
    "Refer":"https://www.cnhnb.com/",
    "origin":"https://www.cnhnb.com"
}
cookie={}
#代理需要更新
proxies_list = [
    {"http": "http://18.163.99.118:80"},
    {"http": "http://16.162.88.123:8080"},
    {"http": "http://122.10.82.237:80"},
    {"http": "http://47.57.233.126:80"},
    {"http": "http://27.124.3.251:9000"},
    {"http": "http://16.163.88.228:80"},
    {"http": "http://34.80.86.90:8080"}
]
def crawl_data(url,t):
    try:
        b1=r1.get(url,headers=headers,timeout=(10))
        #print(b1.text)
        r2=etree.HTML(b1.text)
        a1=[]
        r3=r2.xpath('//*[@id="__layout"]/div/div/div[2]/div[1]/div[3]/div/div[1]/div/div[1]/div[2]/ul/li')
        for i in r3:
            r4=i.xpath("./a/span[position()<=4]")
            for j in r4:
                a1.append(j.text)
        #print(a1)
        return a1
    except Exception as e:
        print(f"第{t}页爬取失败：{str(e)}")
        return []
def get_proxy():        #循环轮询
    global proxy_index
    proxy=proxies_list[proxy_index]
    proxy_index=(proxy_index+1)%len(proxies_list)
    return  proxy
def get_url_n(name,url):
    try:
        b1=r1.get(url,headers=headers,proxies=get_proxy(),timeout=10)
        print(b1.status_code)
        r2=etree.HTML(b1.text)                  #n应为产品类的最大页数
        r3 = r2.xpath('//*[@id="__layout"]/div/div/div[2]/div[1]/div[3]/div/div[1]/div/div[2]/div/div/a[last()]/text()')
        time.sleep(random.uniform(2, 3))
        n = re.findall(r'\d+', r3[0])[0]
        if n:
            return [n]
        else:
            print(f"{name}价格页数为空")
            return [1]          #出错默认爬取一页
    except Exception as e:
        print(f"{name}页面爬取出错:{str(e)}")
        return [1]

def get_all(name,url,n):
    a4=[]
    a5=[]
    e1 = re.compile(r'cdlist-(.*?)-0')          #提取地址中的特殊数字为m区分产品类别
    m = re.findall(e1, url)
    x1=list(range(1,n+1))
    random.shuffle(x1)       #打乱爬取页数顺序，降低反爬风险
    for t in x1:
        url_1= f"https://www.cnhnb.com/hangqing/cdlist-{m[0]}-0-14-0-0-{t}/"
        page__data=crawl_data(url_1,t)
        if page__data:
            a4.extend(page__data)       #各页数据合并
        time.sleep(random.uniform(2, 3))
    if n!=[1]:
        print(f"{name}价格爬取完成")
    else:
        print(f"{name}价格爬取错误")
    return  a4
#存储到txt文件
# def process_data_txt(data):
    a2=[]
    #组内换行
    # for k in range(0,len(a1),4):
    #     s1 = "\n".join(a1[k:k + 4])
    #     a2.append(s1)
    # a3=[]
    #a3="\n\n".join(a2)         #每组分割
    # print(a3)

#存储为json文件
def process_data_json(name,data):
    d2={}       #外套字典
    a2=[]       #外套列表
    data2 = [line.strip() for line in data if line.strip()]         #过滤空白行和去除空白
    keys = ["日期", "商品名称", "地区", "价格"]
    print(f"{name}价格爬取{len(data2)//4}组")
    for  k in range(0, len(data2), 4):
        y1 = data2[k:k + 4]              #四个独立元素为一组
        if len(y1) == 4:
            d1=dict(zip(keys, y1))              #将keys和元素打包
            d2[f"第{k//4+1}组"]=d1           #添加字典到字典 中
            #a2.append(d1)                   #添加字典到列表中
    # 写入数据
    with open(f"{name}.json", "w+", encoding="utf-8") as f:
        f.write(json.dumps(d2, ensure_ascii=False, indent=4))       #可选择外套类型
        if d2:
            print(f"{name}价格已存储{name}.json")
        else:
            print(f"{name}价格存储失败")
if __name__ == '__main__':
    #江西各产品大类的首页
    url_all={"url_fruit":"https://www.cnhnb.com/hangqing/cdlist-2003191-0-14-0-0-1/"
        ,"url_vegetable":"https://www.cnhnb.com/hangqing/cdlist-2003192-0-14-0-0-1/"
        ,"url_meat_egg":"https://www.cnhnb.com/hangqing/cdlist-2003193-0-14-0-0-1/"
        ,"url_grain_oil":"https://www.cnhnb.com/hangqing/cdlist-2003196-0-14-0-0-1/"}
#爬取水果价格                     #连续爬取多个品类价格503
    # print("正在爬取水果价格...")
    # n_1=get_url_n("水果",url_all["url_fruit"])
    # n1=int(n_1[0])
    # print("水果价格页数:",n1)
    # fruit_data=get_all("水果价格",url_all["url_fruit"],n1)
    # process_data_json("水果价格", fruit_data)
    #print(fruit_data)
#爬取蔬菜价格
    # time.sleep(random.uniform(5,7))
    # print("正在爬取蔬菜价格...")
    # n_3 = get_url_n("蔬菜",url_all["url_vegetable"])
    # n3 = int(n_3[0])
    # print("蔬菜价格页数:", n3)
    # vegetable_data = get_all("蔬菜价格", url_all["url_vegetable"], n3)
    # process_data_json("蔬菜价格", vegetable_data)
    # #print(vegetable_data)
#爬取禽畜肉蛋价格
    # time.sleep(random.uniform(5,7))
    # print("正在爬取禽畜肉蛋价格...")
    # n_4 = get_url_n("禽畜肉蛋",url_all["url_meat_egg"])
    # n4 = int(n_4[0])
    # print("禽畜肉蛋价格页数:", n4)
    # meat_egg_data = get_all("禽畜肉蛋", url_all["url_meat_egg"], n4)
    # process_data_json("禽畜肉蛋",meat_egg_data)
    # print(meat_egg_data)
#爬取粮油米面价格
    # time.sleep(random.uniform(5,7))
    # print("正在爬取粮油米面价格...")
    # n_2=get_url_n("粮油米面",url_all["url_grain_oil"])
    # n2=int(n_2[0])
    # print("粮油米面价格页数:", n2)
    # grain_oil_data=get_all("粮油米面",url_all["url_grain_oil"],n2)
    # process_data_json("粮油米面", grain_oil_data)
    # print(grain_oil_data)






