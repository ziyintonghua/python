import requests 
import re
import os
import tqdm
from tqdm import tqdm

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}
response=requests.get("http://www.576tv.com/cate/1-1.html",headers=headers).text
result=re.findall('/cluster/pdetail\?id=\d{6}',response)
url="http://www.576tv.com/"+result[0]
#视频地址
response=requests.get(url,headers=headers).text
title=re.findall('<h2.*?h2>',response)
title=title[-1][11:-5]
#视频标题
video=re.findall(r'https://videofile1.cutv.com.*?mp4',response)[-1]
video_data=requests.get(url=video,stream=True)
content=int(video_data.headers['Content-Length'])/1024
#视频二进制数据
with open(f"{title}.mp4",mode="ab") as f:
        for data in  tqdm(iterable=video_data.iter_content(1024),
                 total=content,
                 unit='k',
                 desc='视频下载'):
                 f.write(data)
