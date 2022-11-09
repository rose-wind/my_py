#-*-coding:utf-8-*-
"""{"provinceName": "台湾", "provinceShortName": "台湾", "currentConfirmedCount": 7860598, "confirmedCount": 7887538,
 "suspectedCount": 485, "curedCount": 13742, "deadCount": 13198, "comment": "", "locationId": 710000,
 "statisticsData": "https://file1.dxycdn.com/2020/0223/045/3398299749526003760-135.json", "highDangerCount": 0,
 "midDangerCount": 0, "detectOrgCount": 0, "vaccinationOrgCount": 0, "cities": [], "dangerAreas": []}
"""
"""
{"id": 22652737, "createTime": 1667903964000, "modifyTime": 1667903964000, "tags": "", "countryType": 2, "continents": "欧洲", "provinceId": "5", "provinceName": "法国", "provinceShortName": "", "cityName": "", "currentConfirmedCount": 36457019, "confirmedCount": 36982388, "confirmedCountRank": 3, "suspectedCount": 0, "curedCount": 368023, "deadCount": 157346, "deadCountRank": 10, "deadRate": "0.42", "deadRateRank": 169, "comment": "", "sort": 0, "operator": "sunyanna", "locationId": 961002, "countryShortCode": "FRA", "countryFullName": "France", "statisticsData": "https://file1.dxycdn.com/2020/0315/929/3402160538577857318-135.json", "incrVo": {"currentConfirmedIncr": 0, "confirmedIncr": 0, "curedIncr": 0, "deadIncr": 0}, "showRank": true, "yesterdayConfirmedCount": 2147383647, "yesterdayLocalConfirmedCount": 2147383647, "yesterdayOtherConfirmedCount": 2147383647, "yesterdayAsymptomaticCount": 2147383647, "highDanger": "", "midDanger": "", "highInDesc": "", "lowInDesc": "", "outDesc": ""}
 """






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

    def Create_World_Map(self):
        world_data_str=super().Load('data/lastday_coronavirus.json')
        world_data_list=[]
        new_world_data_list=[]
        country_name_dict=super().Load('data/country.json')
        new_country_name_dict={value:key for key, value in country_name_dict.items()}
        for country in world_data_str:
            country_name=new_country_name_dict.get(country['provinceName'])
            country_current_confirmed_count=country['confirmedCount']
            world_data_list.append((country_name,country_current_confirmed_count))
        map = Map()
        pieces = [
            {"max": 0, "label": "0人", "color": "#FFFFFF"},
            {"min": 1, "max": 9, "label": "1-9人", "color": "#FFEBCD"},
            {"min": 10, "max": 99, "label": "10-99人", "color": "#FFA07A"},
            {"min": 100, "max": 499, "label": "100-499人", "color": "#FF7F50"},
            {"min": 500, "max": 999, "label": "500-999人", "color": "#CD4F39"},
            {'min': 1000, "max": 10000, "label": "1000-10000人", "color": "#CD3333"},
            {'min': 10000, "label": ">10000人", "color": "#8B0000"}  # 不指定 max，表示 max 为无限大
        ]
        map1 = Map()
        map1.set_global_opts(
            title_opts=opts.TitleOpts(title='全球疫情状况', pos_right='right'),
            visualmap_opts=opts.VisualMapOpts(
                is_piecewise=True,  # 设置为分段显示
                #     自定义每一段的范围，以及每一段的文字，每一段特别的样式
                pieces=pieces
            )
        )
        map1.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        map1.add('全球现存确诊人数',world_data_list, maptype='world', is_map_symbol_show=False,
                 label_opts=opts.LabelOpts(is_show=False))
        map1.render("全球疫情地图.html")


    def Runs(self):
        self.Create_Barchart()
        self.Create_Map()
        self.Create_World_Map()

if __name__ == '__main__':
    a=DataVisualzation()
    a.Runs()



