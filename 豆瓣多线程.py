import requests
from lxml import etree
import time
import random
from concurrent.futures import ThreadPoolExecutor
headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 658N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36 Edg/140.0.0.0"
}
a1=[]
def n1(url):
    time.sleep(random.uniform(1,3))
    r1 = requests.get(url, headers=headers)
    r2=etree.HTML(r1.text)
    r3=r2.xpath('/html/body/div[3]/div[1]/div/div[1]/ol/li/div/div[2]/div[1]/a/span[1]/text()')
    for i in r3:
        print(i)
        a1.append(i)
    print("ok!")    
if __name__=='__main__':
    with ThreadPoolExecutor(10) as x:
        for i in range(0,250,25):
            url=f'https://movie.douban.com/top250?start={i}&filter='
            x.submit(n1,url)
q1=requests.get("https://movie.douban.com/top250", headers=headers)
print(q1.status_code)
print(len(a1))
        
    
            

        
        
    
