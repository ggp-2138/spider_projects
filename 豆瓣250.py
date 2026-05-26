import requests
import re
from bs4 import BeautifulSoup
with open("D:\\OneDrive\\桌面\\w1.txt","w",encoding="utf-8") as t1:
    for i in range(0,250,25):
        headers={"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36 Edg/140.0.0.0"}
        r1=requests.get(f"https://movie.douban.com/top250?start={i}&filter=",headers=headers).text
        s1=re.compile(r'<div class="item">.*?<span class="title">(?P<name>.*?)'
                      r'</span>.*?<br>(?P<year>.*?)&nbsp.*?'
                      r'class="rating_num" property="v:average">(?P<rating>.*?)</span>.*?'
                      r'<span>(?P<comment_count>.*?)人评价',re.S)
        a1=s1.finditer(r1)
        print(a1)
        for s in a1:
            name=s.group("name")
            year=s.group("year").strip()
            rating=s.group("rating")
            comment_count=s.group("comment_count")
            w1=f"名称:{name} 发布时间:{year} 评分:{rating} 评论数:{comment_count}\n"
            t1.write(w1)
            print(w1)
            
    
            

        
        
    
