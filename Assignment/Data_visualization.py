"""{"provinceName": "台湾", "provinceShortName": "台湾", "currentConfirmedCount": 7860598, "confirmedCount": 7887538,
 "suspectedCount": 485, "curedCount": 13742, "deadCount": 13198, "comment": "", "locationId": 710000,
 "statisticsData": "https://file1.dxycdn.com/2020/0223/045/3398299749526003760-135.json", "highDangerCount": 0,
 "midDangerCount": 0, "detectOrgCount": 0, "vaccinationOrgCount": 0, "cities": [], "dangerAreas": []}"""

from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.options import *
from pyecharts.charts import Timeline
from corona_virus_situation import CoronaVirusSpider
from pyecharts.charts import Map

class DataVisualzation(CoronaVirusSpider):
    def Create_Barchart(self):   #构建全国疫情情况的基本柱状图
        lastday_corona_virus_of_china=super().Load('data/lastday_corona_virus_of_china.json')  #加载数据
        x_axis=[]  #x轴坐标，为省份
        y_axis=[]  #y轴坐标，为当前累计确诊人数
        for province in lastday_corona_virus_of_china:
            if province['provinceShortName']!='台湾' and province['provinceShortName']!='香港': #台湾和香港的数量远大于我国其他省，为了做图暂不统计
                x_axis.append(province['provinceShortName'])   #将省级行政区的简称添加到x轴坐标的列表中
                y_axis.append(province['confirmedCount'])      #将各省累计确诊人数添加到x轴坐标的列表中
        bar=Bar(init_opts=opts.InitOpts(width='500px',height='500px'))    #设置图标长宽
        bar.add_xaxis(x_axis)
        bar.add_yaxis('当前累计确诊人数',y_axis,label_opts=LabelOpts(position='right'))   #将数组显示在柱状图的右边
        bar.reversal_axis()    #反转x轴y轴
        bar.render('最近一天全国各省疫情情况柱状图.html')  #设置标题，生成图表的html文件

    def Create_Map(self):    #构建全国疫情地图
        data_str=super().Load('data/lastday_corona_virus_of_china.json')
        data_list=[]
        for province in data_str:
            provinceShortName=province['provinceShortName']
            confirmedCount=province['confirmedCount']
            data_list.append((provinceShortName,confirmedCount))
        map=Map()
        map.add("各省确诊人数",data_list,"china")
        map.set_global_opts(
            title_opts=TitleOpts(title='全国疫情地图'),
            visualmap_opts=VisualMapOpts(
                is_show=True,
                is_piecewise=True,
                pieces=[
                    {"min":1,"max":99,"lable":"1-99人","color":"#CCFFFF"},
                    {"min": 100, "max": 999, "lable": "100-999人", "color": "#FFFF99"},
                    {"min": 1000, "max": 4999, "lable": "1000-4999人", "color": "#FF9966"},
                    {"min": 5000, "max": 9999, "lable": "5000-9999人", "color": "#FF6666"},
                    {"min": 10000, "max": 99999, "lable": "10000-99999人", "color": "#CC3333"},
                    {"min": 100000, "lable": "100000+人", "color": "#990033"},
                ]
            )
        )
        map.render("全国疫情地图.html")

    def Runs(self):
        self.Create_Barchart()
        self.Create_Map()

if __name__ == '__main__':
    a=DataVisualzation()
    a.Runs()



