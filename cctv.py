import re,hashlib
import time
import requests
import os
md5 = lambda value: hashlib.md5(value.encode('utf-8')).hexdigest()

def get_info_url(url):
    headers = {
        'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/100.0.4896.127"
    }
    response = requests.get(url=url, headers=headers).content.decode('utf-8')

    if 'v.cctv.com' in url:
        guid = re.findall('var guid = "(.+?)"', response)[0]
    elif 'webapp.cctv.com' in url:
        guid = re.findall('data-guid="(.+?)"',response)[0]
    else:
        guid = ''
    

    client = 'flash'
    staticCheck = "47899B86370B879139C08EA3B5E88267"
    im = '0'
    tsp = str(int(time.time()))
    vn = '2049'
    vdn_uid = '58A95E29B1D1B65CA79B86F1C25431CD'
    vc = md5((tsp + vn + staticCheck + vdn_uid))
    vnData = f"pid={guid}&client={client}&im={im}&tsp={tsp}&vn={vn}&vc={vc}&uid={vdn_uid}&wlan="
    info_url = 'https://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?' + vnData
    return info_url


def run(url):
    infourl = get_info_url(url)
    headers = {
        'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/100.0.4896.127"
    }
    response = requests.get(url=infourl,headers=headers).json()
    m3u8url = response['hls_url']
    title=response['title'].split()[1]
    os.system(f"downloadm3u8 -o {title}.mp4 {m3u8url}")

while True:
      url = input('输入cctv视频网址：')
      if url=="0":
         exit()
      else:
         run(url)
