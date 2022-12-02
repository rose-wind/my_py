#-*-coding:utf-8-*-
from pyecharts.options import *      #图表设置选项
from pyecharts.charts import Timeline    #时间线库
from corona_virus_situation import CoronaVirusSpider   #数据分析库
from pyecharts.charts import Map   #地图库
from tqdm import tqdm    #进度条库

class DataVisualzation(CoronaVirusSpider):
    def __init__(self):
        super().__init__()
        super().Run()

    def Parse_data(self,data_str,key_1,key_2):
        data_list = []      #定义数据列表
        for province in data_str:
            provinceName = province[key_1]
            confirmedCount = province[key_2]
            data_list.append((provinceName, confirmedCount))
        return data_list

    def Create_Map(self,title,data_list): #构建全国疫情地图
        map=Map()
        map.add("累计确诊人数",data_list,"china",is_map_symbol_show=False)    #不显示定位点
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
                    {"min": 10000, "max": 49999, "lable": "10000-49999人", "color": "#CC5959"},
                    {"min": 50000, "max": 99999, "lable": "50000-99999人", "color": "#CC3333"},
                    {"min": 100000,"max":149999, "lable": "100000-159999人", "color": "#992626"},
                    {"min": 150000,"lable":"150000+人","color":"#730026"}
                ]
            )
        )
        return map

    def Create_china_map(self):
        data_str=super().Load('data/lastday_corona_virus_of_china.json')
        data_list=self.Parse_data(data_str,'provinceShortName','confirmedCount')
        map=self.Create_Map('全国疫情地图',data_list)

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
            is_auto_play=False,   #是否自动播放
            is_loop_play=True   #是否循环播放
        )
        timeline.render('全国疫情变化.html')   #生成图表的.html文件

    def Search_map(self):      #搜索各省的疫情地图
        provincename = input("请输入想要查询的省名：")
        data_str = super().Load('data/lastday_corona_virus_of_china.json')
        provincedata = []
        if provincename!="台湾" and provincename!="香港" and provincename!="澳门":
            for province in data_str:
                if province['provinceShortName'] == provincename:
                    print(f"累计确诊人数：{province['confirmedCount']}")
                    print(f"治愈人数：{province['curedCount']}")
                    print(f"死亡人数：{province['deadCount']}")
                    for city in province['cities']:
                        if "大兴安岭" in city['cityName']:
                            cityname=city['cityName']+"地区"
                        elif "自治" in city['cityName']:
                            cityname=city['cityName']
                        elif "县" in city['cityName']:
                            cityname=city['cityName']
                        elif "区" in city['cityName']:
                            cityname=city['cityName']
                        else:
                            cityname = city['cityName']+'市'
                        confirmedCount = city['confirmedCount']
                        provincedata.append((cityname, confirmedCount))
            province_map = Map()
            province_map.add('当前确诊', provincedata, provincename)
            province_map.set_global_opts(
                title_opts=TitleOpts(title='当前确诊'),  # 设置图表名
                visualmap_opts=VisualMapOpts(
                    is_show=True,
                    is_piecewise=True,  # 分段显示
                    pieces=[  # 标识列表
                        {"min": 1, "max": 49, "lable": "1-49人", "color": "#CCFFFF"},
                        {"min": 50, "max": 99, "lable": "10-99人", "color": "#FFFF99"},
                        {"min": 100, "max": 499, "lable": "100-499人", "color": "#FF9966"},
                        {"min": 500, "max": 999, "lable": "500-999人", "color": "#FF6666"},
                        {"min": 1000, "max": 9999, "lable": "1000-9999人", "color": "#CC3333"},
                        {"min": 10000, "lable": "10000+人", "color": "#990033"},
                    ]
                )
            )
            province_map.render(f"data/province/{provincename}.html")
        else:
            print("缺少疫情信息。")

    def Runs(self):     #调用成员函数测试
        self.Search_map()

if __name__ == '__main__':
    a=DataVisualzation()
    a.Runs()