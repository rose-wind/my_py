"""{"provinceName": "台湾", "provinceShortName": "台湾", "currentConfirmedCount": 7860598, "confirmedCount": 7887538,
 "suspectedCount": 485, "curedCount": 13742, "deadCount": 13198, "comment": "", "locationId": 710000,
 "statisticsData": "https://file1.dxycdn.com/2020/0223/045/3398299749526003760-135.json", "highDangerCount": 0,
 "midDangerCount": 0, "detectOrgCount": 0, "vaccinationOrgCount": 0, "cities": [], "dangerAreas": []}"""

from pyecharts.charts import Bar
from pyecharts.options import LabelOpts
from corona_virus_situation import CoronaVirusSpider

class DataVisualzation(CoronaVirusSpider):
    def __init__(self):
        super().Run()

    def Create_Barchart(self):   #构建最近一天全国疫情情况的基本柱状图
        super().Load('data/lastday_corona_virus_of_china.json')




