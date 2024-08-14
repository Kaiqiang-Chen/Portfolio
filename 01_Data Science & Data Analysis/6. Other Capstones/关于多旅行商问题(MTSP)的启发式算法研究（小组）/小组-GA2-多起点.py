# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 17:32:09 2022
name:GA_for_MTSP
"""
import numpy as np
import pandas as pd  # 提供DataFrame，是一种二维表格型数据
import matplotlib.pyplot as plt  # 画图包
import xlsxwriter  # 读取Excel文件包
import math
import copy
import random
import time
import vrplib

# Sol类，表示一个可行解，等于一条染色体,存储在model.pop中
class Sol():
    def __init__(self):
        self.chrom = None  # 染色体，对应于一个完整解方案
        self.Route = None  # 按载重划分后的车辆路径方案
        self.Route_dis = None  # 每条车辆路径对应的行驶里程
        self.obj = None  # 目标函数值
        self.fit = None  # 适应度值

# Node类，表示一个节点
class Node():
    def __init__(self):
        self.id = 0  # 节点的序号
        self.name = ''  # 节点的名称（客户点:C1，C2，...）
        self.x_coord = 0  # 节点的x坐标
        self.y_coord = 0  # 节点的y坐标
        self.demand = 0  # 节点的载重需求

# Model类，存储算法参数
class Model():
    def __init__(self):
        self.best_sol = None  # 全局最优解,值类型为Sol()
        self.pop = []  # 种群，值类型为Sol()
        self.depot = None  # 仓库点，值类型为Node()
        self.customer = []  # 客户点集合，值类型为Node(),编号0-99
        self.number = 0  # 客户点数量=染色体长度
        self.SeqID = []  # 客户点id映射集合，编号0-99
        self.opt_type = 1  # 优化目标类型，0：最小车辆数，1：最小行驶距离
        self.salemen = 10   # 多少个旅行商
        # self.salenum = []  # 旅行商管辖城市数
        self.capacity = 112  # 车辆最大载重
        self.pc = 0.7  # 交叉率
        self.pm = 0.2  # 变异率
        # self.n_select = 50     #采取精英保留策略时，优良个体选择数量
        self.popsize = 100  # 种群规模

# 函数：读取数据文件
def readExcel(filepath, model):
    instance = vrplib.read_instance(filepath)
    nodes = instance['node_coord']
    dist = instance['edge_weight']
    id_NO = -1  # 客户点id序号，初始赋值为-1（仓库点）
    for i in range(len(nodes)):  # shape[0]返回二维数组的行数，shape[1]返回列数
        node = Node()  # 每行数据都存储为一个节点
        node.id = id_NO  # 读取节点的id序号
        node.name = f'C{i - 1}'  # 节点名称，仓库为C-1，其余客户点从C0、C1...C99
        node.x_coord = int(nodes[i][0])  # 读取节点的x坐标值
        node.y_coord = int(nodes[i][1])  # 读取节点的y坐标值
        if i == 0:  # 若该节点为读取的第一个节点
            model.depot = node  # 那么该节点是仓库
        else:
            model.customer.append(node)  # 否则该点是客户点
            model.SeqID.append(id_NO)  # 存储客户点id映射集合[0,1,2,..,99]
        id_NO += 1
    model.number = len(model.customer)  # 读取总的客户点数量

# 函数：初始种群生成
'''
初始解的生成使用最近邻法，通过计算最短距离，将增加距离最短的客户点逐一插入到序列中
对MTSP问题的编码采用顺序编码，在TSP染色体的基础上插入负数，以分割不同的旅行商。具体操作是对最近邻法生成的初始序列，在相邻两客户点距离最大的位置插入m-1个旅行商，以形成包含多旅行商的初始解。
'''
def initialpop(model):
    m = model.salemen-1 # m=旅行商的数量-1
    temp_chrom = copy.deepcopy(model.SeqID)  # 初始模板染色体为[0,1,2,..,99]

    for i in range(model.popsize):
        rest_chrom = copy.deepcopy(temp_chrom)
        ok_chrom = []
        # 选择一个随机的客户点，这是起点
        start = random.choice(temp_chrom)
        rest_chrom.remove(start)
        ok_chrom.append(start)
        nearest = start
        # 计算这个点到剩余其他所有点的距离，形成一个list
        while len(rest_chrom):
            Dis = []
            for j in rest_chrom:
                dis = math.sqrt((model.customer[nearest].x_coord - model.customer[j].x_coord) ** 2 +
                                (model.customer[nearest].y_coord - model.customer[j].y_coord) ** 2)
                Dis.append(dis)
            nearest_dis = min(Dis)
            nearest = rest_chrom[Dis.index(nearest_dis)]
            rest_chrom.remove(nearest)
            ok_chrom.append(nearest)

        Next_dis = []
        for j in range(len(ok_chrom)-1):
            next_dis = math.sqrt((model.customer[j].x_coord - model.customer[j+1].x_coord) ** 2 +
                                (model.customer[j].y_coord - model.customer[j+1].y_coord) ** 2)
            Next_dis.append(next_dis)
        top_m = sorted(Next_dis, reverse=True)[:m]
        insert_points = []
        for top in top_m:
            insert_points.append(Next_dis.index(top))
        for _ in range(m):  # 插入m个负数
            insert_point = insert_points[_] + _
            ok_chrom.insert(insert_point, -_ - 1)
        sol = Sol()
        sol.chrom = copy.deepcopy(ok_chrom)  # 将该条染色体存储进sol中
        model.pop.append(sol)  # 将该条染色体对应的sol存入种群列表中
    model.number += m  # 由于插入了负数，改变number


# 函数：解码，按约束切分TSP，得到车辆路径方案解
'''
解码时根据负数位置将染色体中的序列拆分为不同的路径
'''
def decode(chrom, model):
    route = []  # 临时路径集合，用来储存迭代更新中的路径
    Routes = []  # 最终的车辆路径集合，嵌套了5个list
    for j in chrom:
        if j < 0:
            Routes.append(route.copy())
            route = []
        else:
            route.append(j)
    Routes.append(route) # 吸入最后一个route，按理说现在Routes里面应该存有5个route

    No_vehicle = len(Routes)
    return No_vehicle, Routes

# 函数：单条车辆路径里程计算
'''
与单起点MTSP问题不同的是，在车辆路径的计算上，仅需将每一条路径的第一个点到最后一个点连成回环计算即可，无需考虑出发点
'''
def caldistance(route, model):
    distance = 0  # 初始化单条路径里程为0
    if len(route):
        for i in range(len(route) - 1):  # 计算该路径上所有客户点间的行驶里程
            distance += math.sqrt((model.customer[route[i]].x_coord - model.customer[route[i + 1]].x_coord) ** 2 +
                                  (model.customer[route[i]].y_coord - model.customer[route[i + 1]].y_coord) ** 2)
        F_customer = model.customer[route[0]]  # 路径中的第一个客户点
        L_customer = model.customer[route[-1]]  # 路径中的最后一个客户点
        distance += math.sqrt((F_customer.x_coord - L_customer.x_coord) ** 2 + (F_customer.y_coord - L_customer.y_coord) ** 2)
    return distance

# 函数：适应度值计算：目标函数求行驶里程dis最小，有两种表示适应度值的方法，(1)fit=1/dis;(2)fit=dismax - dis，选(2)
def calFit(model):
    objMAX = -float('inf')
    best_sol = Sol()  # 存储当前种群的最优染色体，初始化为空
    best_sol.obj = float('inf')  # 初始化当前种群最优染色体目标函数值为无穷大
    for sol in model.pop:  # 对种群中的每一条染色体进行操作
        No_vehicle, Routes = decode(sol.chrom, model)  # 解码该条染色体，得到车辆路径方案
        if model.opt_type == 0:  # 针对目标函数为求车辆数最小
            sol.Route = Routes  # 存储该染色体的车辆路径方案
            sol.obj = No_vehicle  # 存储该染色体的用车数
            if sol.obj > objMAX:
                objMAX = sol.obj  # 更新当前种群最大目标值
            if sol.obj < best_sol.obj:
                best_sol = copy.deepcopy(sol)  # 更新当前种群的最优目标值
        else:  # 针对目标函数为求行驶里程最小
            Route_dis = []
            for route in Routes:
                Route_dis.append(caldistance(route, model))
            sol.Route = Routes  # 存储该染色体的车辆路径方案
            sol.Route_dis = Route_dis  # 存储该染色体每条路径的里程
            sol.obj = sum(Route_dis)  # 存储该染色体的总行驶里程
            if sol.obj > objMAX:
                objMAX = sol.obj  # 更新当前种群最大目标值
            if sol.obj < best_sol.obj:
                best_sol = copy.deepcopy(sol)  # 更新当前种群的最优目标值
    for sol in model.pop:
        sol.fit = objMAX - sol.obj  # 计算当前种群每条染色体的适应度值
    if best_sol.obj < model.best_sol.obj:
        model.best_sol = copy.deepcopy(best_sol)  # 若当前种群最优目标值优于全局最优目标值，更新全局最优解为当前种群最优染色体

#函数：选择算子（example），锦标赛方法,加精英选择(留下全局最优的)
'''
动态锦标赛选择算子，随着迭代次数的增加，逐渐改变锦标赛中参赛选手的数量k，以平衡exploration和exploitation
精英选择，留下全局最优的多个解，保留到下一代
'''
def select(model, n): # 在一定条件后，选择压力变大，n增加
    temp_pop = copy.deepcopy(model.pop)              #temp_pop充当父代种群
    model.pop = []                                   #初始化子代种群为空
    model.pop.append(model.best_sol)                 #留下全局最优的，精英
    for i in range(1, model.popsize):           #每次任选*个，选择其中最好的一个
        random_index = [random.randint(0,len(temp_pop)-1) for m in range(n)]
        random_fit = []
        for k in random_index:
            fit = temp_pop[k].fit
            random_fit.append(fit)
        max_fit = max(random_fit)
        model.pop.append(temp_pop[random_index[random_fit.index(max_fit)]])

# 函数：OX交叉算子（example），保留下来的个体随机性更大
def cross(model):
    temp_pop = copy.deepcopy(model.pop)  # 进行了选择但还未进行交叉的种群，父代种群
    model.pop = []  # 初始化交叉之后的子代种群为空
    while True:
        father_index = random.randint(0, model.popsize - 1)  # 随机选出父代1个体索引
        mother_index = random.randint(0, model.popsize - 1)  # 随机选出父代2个体索引
        if father_index != mother_index:  # 确保两个父代不为同一条染色体
            father = copy.deepcopy(temp_pop[father_index])  # 父代1，值类型sol
            mother = copy.deepcopy(temp_pop[mother_index])  # 父代2，值类型sol
            if random.random() < model.pc:  # 一定概率发生交叉
                cpoint1 = int(random.randint(0, model.number - 1))  # 交叉点1位置索引
                cpoint2 = int(random.randint(cpoint1, model.number - 1))  # 交叉点2位置索引
                new_father_f = []  # 父代1前段基因串
                new_father_m = father.chrom[cpoint1:cpoint2 + 1]  # 父代1交叉段基因串
                new_father_b = []  # 父代1后段基因串
                new_mother_f = []  # 父代2前段基因串
                new_mother_m = mother.chrom[cpoint1:cpoint2 + 1]  # 父代2交叉段基因串
                new_mother_b = []  # 父代2后段基因串
                for i in range(model.number):
                    if len(new_father_f) < cpoint1:  # 父代1前串基因还未填充完
                        if mother.chrom[i] not in new_father_m:  # 将不在父代1中段的父代2基因
                            new_father_f.append(mother.chrom[i])  # 添加至父代1前段
                    else:  # 父代1前串基因填充完，填充父代1后串基因
                        if mother.chrom[i] not in new_father_m:  # 将不在父代1中段的父代2基因
                            new_father_b.append(mother.chrom[i])  # 添加至父代2后段
                for i in range(model.number):  # 对父代2同样的操作
                    if len(new_mother_f) < cpoint1:
                        if father.chrom[i] not in new_mother_m:
                            new_mother_f.append(father.chrom[i])
                    else:
                        if father.chrom[i] not in new_mother_m:
                            new_mother_b.append(father.chrom[i])
                new_father = new_father_f + new_father_m + new_father_b  # 得到交叉后新的父代1染色体
                father.chrom = copy.deepcopy(new_father)
                new_mother = new_mother_f + new_mother_m + new_mother_b  # 得到交叉后新的父代2染色体
                mother.chrom = copy.deepcopy(new_mother)
                model.pop.append(copy.deepcopy(father))  # 将交叉后的父代1加入子代种群
                model.pop.append(copy.deepcopy(mother))  # 将交叉后的父代2加入子代种群
            else:  # 若未发生交叉，直接加入子代种群
                model.pop.append(copy.deepcopy(father))
                model.pop.append(copy.deepcopy(mother))
            if len(model.pop) == model.popsize:
                break

# 函数：变异算子，位翻转突变
def mutation(model):
    for i in range(model.popsize):
        if random.random() < model.pm:
            while True:
                start = random.randint(0, model.number - 1)
                end = random.randint(0, model.number - 1)
                if start != end:
                    break
            if start > end:
                start, end = end, start
            model.pop[i].chrom[start:end+1] = reversed(model.pop[i].chrom[start:end+1])

# 绘图函数：绘制收敛曲线图
def plot_obj(objlist):  # 传入的是每一代的最优目标函数值
    plt.figure()
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 更改运行配置参数中的字体（font）为黑体（SimHei），用来正常显示中文,这行代码可要可不要
    plt.rcParams['axes.unicode_minus'] = False  # 运行配置参数总的轴（axes）正常显示正负号（minus）
    plt.plot(np.arange(1, len(objlist) + 1), objlist)  # 画图，x坐标为[1,len(objlist)+1],y坐标为objlist
    plt.xlabel('迭代次数')
    plt.ylabel('最优目标函数值')
    plt.grid()  # 显示网格线，1=True=默认=显示，0=False=不显示
    plt.xlim(1, len(objlist) + 1)  # 显示的是x轴的作图范围

# 绘图函数：绘制车辆行驶路径图
def plot_route(model):
    plt.figure()
    for route in model.best_sol.Route:  # 对每条车辆路径进行绘制
        x_coord = []  # 生成绘图x坐标列表，先把仓库加进去，作为起点
        y_coord = []  # 生成绘图y坐标列表，先把仓库加进去，作为起点
        for i in route:  # 将路径中每个客户点坐标加进去
            x_coord.append(model.customer[i].x_coord)
            y_coord.append(model.customer[i].y_coord)
            plt.text(model.customer[i].x_coord, model.customer[i].y_coord, model.customer[i].name,
                     fontsize=5)  # 先在图上画出每个客户点的名称
        x_coord.append(model.customer[route[0]].x_coord)  # 最后再次加入仓库，作为终点
        y_coord.append(model.customer[route[0]].y_coord)  # 最后再次加入仓库，作为终点
        plt.grid()  # 显示网格线，1=True=默认=显示，0=False=不显示
        plt.plot(x_coord, y_coord, 'b:', linewidth=0.5, marker='o',
                 markersize=2)  # 设置每条路径的绘图参数，线型及颜色：蓝色、点线(b:)；点型：原点，大小为5
    # plt.plot(model.depot.x_coord, model.depot.y_coord, 'r', marker='*',
    #          markersize=10)  # 最后再次设置仓库参数：颜色：红色(r)，点型：五角星，大小为10
    plt.title('vehicle-route')  # 图片标题名称
    plt.xlabel('x_coord')  # y轴名称
    plt.ylabel('y_coord')  # y轴名称
    # plt.savefig('V-Route.png', dpi=300)  #指定分辨率保存

# 函数：求解结果输出
def output(model):
    excel = xlsxwriter.Workbook('result.xlsx')  # 生成一个新的Excel文件名称叫result，存放在Python代码同路径
    excelsheet = excel.add_worksheet()  # 为excel创建一个sheet，不设置名字时默认为sheet1
    excelsheet.write(0, 0, '最优目标函数值')  # 表格第1行第1列写入“最优目标函数值”
    excelsheet.write(0, 1, model.best_sol.obj)  # 表格第1行第2列写入最优目标函数值的数据
    for row, route in enumerate(model.best_sol.Route):  # enumerate返回对象中各个值和对应的位置索引
        excelsheet.write(row + 1, 0, f'v{row + 1}')  # 从第2行开始，依次在第1列中写入车辆编号
        excelsheet.write(row + 1, 1, str(route))  # 从第2行开始，依次在第2列中写入路径
    for row, dis in enumerate(model.best_sol.Route_dis):
        excelsheet.write(row + 1, 2, dis)
    excel.close()

# 主函数：GA算法框架
def GA(filepath, Iterations):
    model = Model()  # 初始化model
    readExcel(filepath, model)  # 读取数据并构造model
    best_sol = Sol()
    best_sol.obj = float('inf')
    model.best_sol = best_sol  # 初始化全局最优解为无穷大
    initialpop(model)  # 生成初始种群
    calFit(model)  # 计算当初始解每条染色体对应的Route、R_dis、obj、fit
    history_best_obj = []  # 历史最优解集合，记录每次迭代得到的最优目标函数值
    history_best_obj.append(model.best_sol.obj)  # 将初始最优解加入历史最优目标值列表中
    n = 2
    for i in range(Iterations):  # 进行Iterations次迭代
        select(model, 2)  # 选择操作，更新种群
        cross(model)  # 交叉操作，更新种群（注意此时只更新了染色体，没更新Route、R_dis、obj、fit）
        mutation(model)  # 变异操作，更新种群（注意此时只更新了染色体，没更新Route、R_dis、obj、fit）
        calFit(model)  # 计算当前种群每条染色体对应的Route、R_dis、obj、fit
        history_best_obj.append(model.best_sol.obj)  # 更新全局最优解
        print(f'{i}/{Iterations}，best obj:{model.best_sol.obj}')
    plot_obj(history_best_obj)
    plot_route(model)
    # 将计时器插入到这里
    run_end = time.perf_counter()  # 计时器，时间结束
    print(f'运行总用时={run_end - run_start}秒')
    plt.show()
    output(model)
    return model

run_start = time.perf_counter()

if __name__ == '__main__':
    filepath = r"作业\小组作业\测试样例\A-n80-k10.vrp"
    model = GA(filepath, Iterations=2000)
    print("-------------------------------------")
    print("最短里程：", model.best_sol.obj)
    print("最短车辆路径方案：", model.best_sol.Route)



