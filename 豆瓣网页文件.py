import requests
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0"}
j=1
for i in range(0,250,25):
    r1=requests.get(f"https://movie.douban.com/top250?start={i}&filter=",headers=headers)
    with open(f"D:\\photo1\\h{j}.html",'w+',encoding="utf-8")as q1:
        q1.write(r1.text)
    print(f'h{j}:Ok')
    j+=1
print(r1.status_code)

