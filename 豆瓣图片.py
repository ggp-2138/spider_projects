import requests
from bs4 import BeautifulSoup
headers={"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36 Edg/140.0.0.0"}
r1=requests.get("https://movie.douban.com/top250",headers=headers)
r2=BeautifulSoup(r1.text,"html.parser")
r3=r2.find_all("div",attrs={"class":"pic"})
for i in r3:
    r4=i.find_all("img")
    for ph in r4:
        #print(ph.get("src"))
        y1=ph.get("src")
        u1=requests.get(y1,headers=headers)
        u2=y1.split("/")[-1]
        with open("D:\\photo1\\"+u2,"wb") as h1:
            h1.write(u1.content)
        print(f'{u2}ok')
print(r1.status_code)
        
        
    
