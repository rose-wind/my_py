import time
from PyQt5 import QtCore, QtGui, QtWidgets
import pickle as pk
class Resource:     #对一种物资基本信息的封装
    def __init__(self,num,name,price,amount,category):
        self.num=num         #物资编号
        self.name=name       #物资名称
        self.price=price     #物资单价
        self.category=category  #物资所属类别（1表示食物；2表示日用品；3表示医疗用品）
        self.amount=0        #仓库中物资的数量
        self.Add_amount(amount)
        time.gmtime()
        timestr = time.strftime("%Y-%m-%d %H:%M:%S")
        self.inbound_time=timestr   #入库时间

    def Add_amount(self,amount):
        self.amount+=amount

    def disp(self):
        print(f"物资编号:{self.num}  物资名称：{self.name}  物资单价：{self.price}元/份\n  物资储量：{self.amount}份",end="")
        print(f"  物资所属类别：",end="")
        if self.category==1:
            print("食物")
        elif self.category==2:
            print("日用品")
        elif self.category==3:
            print("医疗用品")
        else:
            print("未知")

class ResourceManager():   #疫情物资管理系统
    def __init__(self):
        self.warehouse=[]
        self.shopping_carts=[]
        try:
            self.load("data/item_list.pkl")
        except EOFError:
            pass
        self.number=len(self.warehouse)

    def load(self,path):
        with open(path, 'rb') as f:
            self.warehouse = pk.load(f)

    def save(self,path):
        with open(path,'wb') as f:
            pk.dump(self.warehouse,f)

    def Add_resource(self):      #物资入库
        while(True):
            print("请输入")
            name = input("物资名：")
            while(True):
                try:
                    category = eval(input("物资类别(数字1、2、3)："))
                    price = eval(input("物资单价："))
                    amount = eval(input("入库数量："))
                    number=eval(input("物资编号："))
                    break
                except NameError:
                    print("请重新输入")
            r=Resource(number,name,price,amount,category)
            self.number+=1
            self.warehouse.append(r)
            i=eval(input("是否继续入库物资？（输入1继续；输入0退出）"))
            if i==0:
                break
        self.save("data/item_list.pkl")

    def Disp_info(self):      #展示仓库里的物资信息
        for i in range(0,self.number):
            self.warehouse[i].disp()

    def Del_resource(self):     #删除物资
        while(True):
            name=input("请输入要删除的物资名：")
            i=self.Research_resource(name)
            if i!=-1:
                del self.warehouse[i]
                self.number-=1
                print("删除成功")
            elif self.number!=0:
                print("仓库中没有该物品。")
            else:
                print("仓库为空。")
            i = eval(input("是否继续删除物资？（输入1继续；输入0退出）"))
            if i==0:
                break
        self.save("data/item_list.pkl")

    def Research_resource(self,name):  #搜索物资
        for i in range(0,self.number):
            if self.warehouse[i].name==name:
                print(f"找到物品：{name}")
                self.warehouse[i].disp()
                return i
        print(f"没有找到{name}")
        return -1

    def Request_resource(self):    #物资申请
        while(True):
            if self.number==0:
                print("抱歉，仓库目前没有物资，请等待后续物资补充。")
                break
            else:
                name=input("请输入您需要的物资名：")
                i=self.Research_resource(name)
                if i!=-1:
                    amount = eval(input("请输入您要购买的份数："))
                    if amount<=self.warehouse[i].amount:
                        cost=self.warehouse[i].price*amount
                        print(f"总价：{cost}元")
                        self.warehouse[i].Add_amount(-amount)
                        if len(self.shopping_carts)!=0:
                            for i in self.shopping_carts:
                                if i[0]!=name:
                                    self.shopping_carts.append([self.warehouse[i].name,amount,cost])
                                else:
                                    i[1]+=amount
                                    i[2]+=cost
                        else:
                            self.shopping_carts.append([self.warehouse[i].name, amount, cost])
                        print("申请成功，已添加到购物车")
                    else:
                        print("仓库中物资不足。")
                else:
                    print("申请失败。")
            flag = eval(input("是否继续申请物资？（输入1继续；输入0退出）"))
            if flag == 0:
                break

    def Checkout(self):
        total_cost=0
        for i in range(len(self.shopping_carts)):
            print(f"名称：{self.shopping_carts[i][0]}\n份数：{+self.shopping_carts[i][1]} 总价：{+self.shopping_carts[i][2]}")
            total_cost+=self.shopping_carts[i][2]
        print(f"您共需支付{total_cost}元")
        flag=eval(input("1支付               2取消"))
        if flag==1:
            print("支付成功！")
        self.save("data/item_list.pkl")

    def Run(self):
        # self.Add_resource()
        # self.Disp_info()
        # self.Del_resource()
        self.Request_resource()
        self.Checkout()
        # self.Disp_info()

if __name__ == '__main__':
    r=ResourceManager()
    r.Run()





