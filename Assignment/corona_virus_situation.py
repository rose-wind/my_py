#导入模块
import requests as req    #请求库，用于发送请求，抓取网页信息
import re    #正则库，用于解析数据
import json    #用于json和python字符串的转换
from bs4 import BeautifulSoup    #从html中获取数据
from tqdm import tqdm     #进度条

#定义疫情信息爬虫类
class CoronaVirusSpider(object):
    def __init__(self):
        self.home_url='https://ncov.dxy.cn/ncovh5/view/pneumonia'

    def Get_coronavirus_home_page(self,url):           #发送请求，获取疫情首页
        response=req.get(url)
        return response.content.decode()

    def Parse_home(self,home_page,tag_id):            #解析主页数据
        soup=BeautifulSoup(home_page,'lxml')
        script=soup.find(id=tag_id)
        text=script.text
        json_str=re.findall(r'\[.+\]',text)[0]   #使用正则表达式处理数据，获取json串
        data=json.loads(json_str)   #把json串转换为python串
        return data    #返回python串

    def Parse_corona_virus(self, lastday_global_coronavirus,desc):     #解析2020年1月23日以来的疫情信息
        corona_virus = []
        for country in tqdm(lastday_global_coronavirus, desc):
            statistical_data_url = country['statisticsData']
            statistical_data_url_json_str = self.Get_coronavirus_home_page(statistical_data_url)
            statsmodel_data = json.loads(statistical_data_url_json_str)['data']
            for one_day in statsmodel_data:
                one_day['provinceName'] = country['provinceName']
                if country.get('countryShortCode'):  #判断数据中是否存在键countryShortCode
                    one_day['countryShortCode'] = country['countryShortCode']
            corona_virus.extend(statsmodel_data)
        return corona_virus

    def Load(self,path):    #根据路径加载数据
        with open(path,encoding='utf8') as fp:
            data=json.load(fp)
        return data

    def Save(self,data,path):       #将数据保存
        with open(path,'w',encoding='utf8') as fp:
            json.dump(data,fp,ensure_ascii=False)

    def Crawl_lastday_coronavirus(self):    #获取最近一日各国疫情数据
        home_page=self.Get_coronavirus_home_page(self.home_url)   #请求主页，获取信息
        lastday_coronavirus=self.Parse_home(home_page,'getListByCountryTypeService2true')   #解析主页数据
        self.Save(lastday_coronavirus,'data/lastday_coronavirus.json')

    def Crawl_coronavirus(self):             #采集2020年1月23日以来的各个国家疫情数据
        lastday_global_coronavirus=self.Load('data/lastday_coronavirus.json')
        corona_virus = self.Parse_corona_virus(lastday_global_coronavirus,desc='采集2020年1月23日以来的各个国家疫情数据')
        self.Save(corona_virus,'data/corona_virus.json')

    def Crawl_lastday_china_coronavirus(self):            #采集最近一日全国各省疫情数据
        home_page=self.Get_coronavirus_home_page(self.home_url)
        last_day_corona_virus_of_china=self.Parse_home(home_page,'getAreaStat')
        self.Save(last_day_corona_virus_of_china,'data/lastday_corona_virus_of_china.json')

    def Crawl_coronavirus_of_china(self):     #采集2020年1月22日以来的中国各省的疫情数据
        lastday_china_coronavirus=self.Load('data/lastday_corona_virus_of_china.json')
        corona_virus = self.Parse_corona_virus(lastday_china_coronavirus,desc='采集2020年1月22日以来的中国各省的疫情数据')
        self.Save(corona_virus,'data/corona_virus_of_china.json')

    def Run(self):   #运行
        self.Crawl_coronavirus()
        self.Crawl_lastday_coronavirus()
        self.Crawl_coronavirus_of_china()
        self.Crawl_lastday_china_coronavirus()

# if __name__ == '__main__':
#     spyder=CoronaVirusSpider()
#     spyder.Run()








