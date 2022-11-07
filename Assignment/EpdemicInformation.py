import requests as req
from bs4 import BeautifulSoup
import re
import json
response=req.get('https://ncov.dxy.cn/ncovh5/view/pneumonia')
html=response.content.decode()
soup=BeautifulSoup(html,'lxml')
script=soup.find(id='getListByCountryTypeService2true')
info=script.text
#使用正则表达式获取json字符串
json_str=re.findall(r'\[.*\]',info)[0]
last_day_corona_virus=json.loads(json_str)