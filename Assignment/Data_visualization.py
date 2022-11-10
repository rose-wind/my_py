#-*-coding:utf-8-*-

"""
各省数据json串格式：
{"provinceName": "台湾", "provinceShortName": "台湾", "currentConfirmedCount": 7860598, "confirmedCount": 7887538,
 "suspectedCount": 485, "curedCount": 13742, "deadCount": 13198, "comment": "", "locationId": 710000,
 "statisticsData": "https://file1.dxycdn.com/2020/0223/045/3398299749526003760-135.json", "highDangerCount": 0,
 "midDangerCount": 0, "detectOrgCount": 0, "vaccinationOrgCount": 0, "cities": [], "dangerAreas": []}
"""

"""
各国数据json串格式：
{"id": 22652737, "createTime": 1667903964000, "modifyTime": 1667903964000, "tags": "", "countryType": 2, "continents": "欧洲", "provinceId": "5", "provinceName": "法国", "provinceShortName": "", "cityName": "", "currentConfirmedCount": 36457019, "confirmedCount": 36982388, "confirmedCountRank": 3, "suspectedCount": 0, "curedCount": 368023, "deadCount": 157346, "deadCountRank": 10, "deadRate": "0.42", "deadRateRank": 169, "comment": "", "sort": 0, "operator": "sunyanna", "locationId": 961002, "countryShortCode": "FRA", "countryFullName": "France", "statisticsData": "https://file1.dxycdn.com/2020/0315/929/3402160538577857318-135.json", "incrVo": {"currentConfirmedIncr": 0, "confirmedIncr": 0, "curedIncr": 0, "deadIncr": 0}, "showRank": true, "yesterdayConfirmedCount": 2147383647, "yesterdayLocalConfirmedCount": 2147383647, "yesterdayOtherConfirmedCount": 2147383647, "yesterdayAsymptomaticCount": 2147383647, "highDanger": "", "midDanger": "", "highInDesc": "", "lowInDesc": "", "outDesc": ""}
 """


from pyecharts.charts import Bar     #柱状图库
from pyecharts import options as opts    #图表设置库
from pyecharts.options import *
from pyecharts.charts import Timeline    #时间线库
from corona_virus_situation import CoronaVirusSpider   #数据分析库
from pyecharts.charts import Map   #地图库
from tqdm import tqdm    #进度条库

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

    def Parse_data(self,data_str,key_1,key_2):
        data_list = []      #定义数据列表
        for province in data_str:
            provinceName = province[key_1]
            confirmedCount = province[key_2]
            data_list.append((provinceName, confirmedCount))
        return data_list

    def Create_Map(self,title,data_list):    #构建全国疫情地图
        map=Map()
        map.add("确诊人数",data_list,"china",is_map_symbol_show=False)    #不显示定位点
        map.set_global_opts(
            title_opts=TitleOpts(title=title),    #设置图表名
            visualmap_opts=VisualMapOpts(
                is_show=True,
                is_piecewise=True,    #分段显示
                pieces=[    #标识列表
                    {"min":1,"max":99,"lable":"1-99人","color":"#CCFFFF"},
                    {"min": 100, "max": 999, "lable": "100-999人", "color": "#FFFF99"},
                    {"min": 1000, "max": 4999, "lable": "1000-4999人", "color": "#FF9966"},
                    {"min": 5000, "max": 9999, "lable": "5000-9999人", "color": "#FF6666"},
                    {"min": 10000, "max": 99999, "lable": "10000-99999人", "color": "#CC3333"},
                    {"min": 100000, "lable": "100000+人", "color": "#990033"},
                ]
            )
        )
        return map

    def Create_china_map(self):
        data_list=self.Parse_data('data/lastday_corona_virus_of_china.json','provinceShortName','confirmedCount')
        map=self.Create_Map('全国疫情地图',data_list)
        map.render("全国疫情地图.html")

    def Create_World_Map(self):
        world_data_str=super().Load('data/lastday_coronavirus.json')    #装载数据
        world_data_list=[]
        country_name_dict=super().Load('data/country.json')     #加载国家中英文名对照表
        new_country_name_dict={value:key for key, value in country_name_dict.items()}   #交换对照表中value和key的值
        for country in world_data_str:                   #将数据串中的所有中文国家名转换为英文国家名，与累计确诊数据压缩成元组添加到数据列表中
            country_name=new_country_name_dict.get(country['provinceName'])
            country_current_confirmed_count=country['confirmedCount']
            world_data_list.append((country_name,country_current_confirmed_count))
        pieces = [
            {"min": 0,"max":99 ,"label": "0-99人", "color": "#FFFFFF"},
            {"min": 100, "max": 9999, "label": "100-9999人", "color": "#FFEBCD"},
            {"min": 1000, "max": 49999, "label": "1000-99999人", "color": "#FFA07A"},
            {"min": 50000, "max": 99999, "label": "50000-99999人", "color": "#FF7F50"},
            {"min": 100000, "max": 999999, "label": "100000-999999人", "color": "#CD4F39"},
            {'min': 1000000, "max": 9999999, "label": "1000000-99999999人", "color": "#CD3333"},
            {'min': 10000000, "label": ">10000000人", "color": "#8B0000"}  # 不指定 max，表示 max 为无限大
        ]
        map1 = Map()
        map1.set_global_opts(
            title_opts=opts.TitleOpts(title='全球疫情状况', pos_right='right'),
            visualmap_opts=opts.VisualMapOpts(
                is_piecewise=True,  #设置为分段显示
                #自定义每一段的范围，以及每一段的文字，每一段特别的样式
                pieces=pieces
            )
        )
        map1.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        map1.add('现存确诊人数',world_data_list, maptype='world', is_map_symbol_show=False,
                 label_opts=opts.LabelOpts(is_show=False))
        map1.render("全球疫情地图.html")

    def Timeline_Map(self):
        corona_virus_of_china_list=super().Load('data/corona_virus_of_china.json')    #加载信息
        date_list=[]   #初始化日期列表
        data=[]   #初始化数据列表
        for province in corona_virus_of_china_list:
            date_list.append(province['dateId'])     #取日期数据，存到日期列表里
        mylist = list(dict.fromkeys(date_list))      #为了去除重复的数据，将列表转成字典类型
        mylist.sort()       #日期递增排序
        timeline=Timeline()   #定义时间线变量
        for i in tqdm(mylist[-62:],'数据解析中'):      #进度条
            for province in corona_virus_of_china_list:
                if province['dateId']==i:    #按日期存储疫情信息
                    provinceName=province['provinceName']  #取数据中的所有省名
                    if "省" in provinceName:      #为了和pyecharts库自带的中国地图匹配，删除除省名以外的字符
                        provinceName=provinceName.replace('省','')
                    if "自治区" in provinceName:
                        if "壮族" in provinceName:
                            provinceName=provinceName.replace('壮族自治区','')
                        if "维吾尔" in provinceName:
                            provinceName=provinceName.replace('维吾尔自治区','')
                        if "回族" in provinceName:
                            provinceName=provinceName.replace('回族自治区','')
                        provinceName=provinceName.replace('自治区','')
                    if "市" in provinceName:
                        provinceName=provinceName.replace('市','')
                    confirmedcount=province['confirmedCount']
                    data.append((provinceName,confirmedcount))    #压缩为元组添加到data列表
            map=self.Create_Map(f'全国疫情地图{i}',data)    #按日期画疫情地图
            timeline.add(map,i)      #将所有地图添加到时间线上，以i作为每个点的名称
        timeline.add_schema(
            play_interval=500,      #自动播放的时间间隔
            is_timeline_show=True,    #是否显示时间线
            is_auto_play=True,   #是否自动播放
            is_loop_play=True   #是否循环播放
        )
        timeline.render('全国疫情变化.html')   #生成图表的.html文件

    def Runs(self):     #调用成员函数
        self.Create_Barchart()
        self.Create_china_map()
        self.Create_World_Map()
        self.Timeline_Map()

if __name__ == '__main__':
    a=DataVisualzation()
    a.Runs()



