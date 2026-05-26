import requests
from lxml import etree
import time
import random
import asyncio
import aiohttp
import aiofiles
import os
cookies = {
  
}
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0"
}
q1=requests.get("https://www.beqege.cc/2/", headers=headers,cookies=cookies)
print(q1.status_code)
async def n1(session,url,k,name):
    async with session.get(url,headers=headers,cookies=cookies) as e1:
        #e1=requests.get(url,headers=headers,cookies=cookies)
        h1=await e1.text()
        e2=etree.HTML(h1)
        e3=e2.xpath('//*[@id="content"]/p/text()')
        #print(e1.status_code)
        j1="D:\\OneDrive\\桌面\\凡人修仙传"
        j2=f't{k}.txt'
        j3=os.path.join(j1,j2)
        async with aiofiles.open(j3,mode="w+",encoding="utf-8") as f:
            await f.write(f"{name}\n\n{e3}")
        print(f"第{k}章下载完成:{name}")
    await asyncio.sleep(random.uniform(1,3))
async def main():
    start_time = time.perf_counter()
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.beqege.cc/2/",headers=headers,cookies=cookies) as r1:
            h2=await r1.text()
            r2=etree.HTML(h2)
            r3=r2.xpath('//*[@id="list"]/dl/dd[position()>=1 and position()<=10]/a')
            tasks=[]
            for k,i in enumerate (r3,start=1):
                name=i.xpath('./text()')
                r5=i.xpath('./@href')
                r5=''.join(r5)
                url=f"https://www.beqege.cc{r5}"
                task=asyncio.create_task(n1(session,url,k,name))
                tasks.append(task)
            await asyncio.wait(tasks)
    end_time = time.perf_counter()
    print(f"总运行时间：{end_time - start_time:.2f} 秒")
if __name__=='__main__':
    asyncio.run(main())



    
