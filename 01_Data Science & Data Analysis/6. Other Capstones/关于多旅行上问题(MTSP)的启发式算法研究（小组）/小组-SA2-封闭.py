# 创建日期:2024/5/3
# 创建日期:2024/5/1
# 创建日期:2024/4/20

import numpy as np
import pandas as pd  # 提供DataFrame，是一种二维表格型数据
import matplotlib.pyplot as plt  # 画图包
import xlsxwriter  # 读取Excel文件包
import math
import copy
import random
import time

# Sol类，表示一个可行解，等于一条染色体,存储在model.pop中
class Sol():
    def __init__(self):
        self.nodes_seq=None
        self.obj=None
        self.routes=None
        self.routes_dis = []
class Node():
    def __init__(self):
        self.id=0
        self.name=''
        self.seq_no=0
        self.x_coord=0
        self.y_coord=0
        self.demand=0
class Model():
    def __init__(self):
        self.best_sol=None
        self.node_list=[]
        self.node_seq_no_list=[]
        self.depot=None
        self.number_of_nodes=0
        self.opt_type=0
        self.vehicle_cap=0
        self.tabu_list = None  # 禁忌表，维度等于客户点数
        self.TL = 20  # 禁忌长度
        self.salemen = 10   # 多少个旅行商

# 函数：读取数据文件
import vrplib
def readExcel(filepath, model):
    instance = vrplib.read_instance(filepath)
    nodes = instance['node_coord']
    dist = instance['edge_weight']
    id_NO = 0  # 客户点id序号，初始赋值为-1（仓库点）
    for i in range(len(nodes)):  # shape[0]返回二维数组的行数，shape[1]返回列数
        node = Node()  # 每行数据都存储为一个节点
        node.id = id_NO  # 读取节点的id序号
        node.name = f'C{i}'  # 节点名称，仓库为C-1，其余客户点从C0、C1...C99
        node.x_coord = int(nodes[i][0])  # 读取节点的x坐标值
        node.y_coord = int(nodes[i][1])  # 读取节点的y坐标值
        model.node_list.append(node)  # 否则该点是客户点
        model.node_seq_no_list.append(id_NO)  # 存储客户点id映射集合[0,1,2,..,99]
        id_NO += 1
    model.number_of_nodes = len(model.node_list)  # 读取总的客户点数量

#函数：产生初始解
def genInitialSol(model):
    dist = np.zeros((model.number_of_nodes, model.number_of_nodes), dtype=float)
    for i in range(model.number_of_nodes):
        for j in range(model.number_of_nodes):
            dist[i, j] = math.sqrt((model.node_list[i].x_coord - model.node_list[j].x_coord) ** 2 +
                                   (model.node_list[i].y_coord - model.node_list[j].y_coord) ** 2)
    temp_seq = copy.deepcopy(model.node_seq_no_list)
    # 保存行程的路线
    way = []
    way.append(model.node_seq_no_list[1])
    temp_seq.pop(temp_seq.index(model.node_seq_no_list[1]))
    # 对剩下的进行插入
    for i in range(1, model.number_of_nodes):
        k = 0
        minimum = float('inf')
        for left in temp_seq:
            k_dist = min([dist[left][point] for point in way])
            if k_dist < minimum:
                minimum = k_dist
                k = left
        if len(way) == 1:
            way.append(k)
            temp_seq.pop(temp_seq.index(k))
            continue
        # 判断将k加入到哪个弧中
        dist_to_k = []  # 保存加入弧时，增加的dist
        short_index = 0
        for j in range(len(way) - 1):
            fore = way[j]
            back = way[j + 1]
            temp_dist = dist[k][fore] + dist[k][back] - dist[fore][back]
            dist_to_k.append(temp_dist)
            short = min(dist_to_k)
            short_index = dist_to_k.index(short) + 1
        way.insert(short_index, k)
        temp_seq.pop(temp_seq.index(k))
    node_seq=copy.deepcopy(way)
    m = model.salemen-1 # m=旅行商的数量-1
    for _ in range(m):    # 插入m个负数
        insert_point = random.randint(1,len(node_seq)-1)
        node_seq.insert(insert_point, -_-1)
    model.number_of_nodes += m # 由于插入了负数，改变number
    return node_seq

# 函数：构建*类邻域算子
def createActions(n, Tk):
    action_list = []
    nswap = int(n // 3)
    # 邻域算子1：互换-单双
    for i in range(n):
        while True:
            r = random.randint(0, n - 2)
            if r >= i + 2 or r <= i - 2: break
        action_list.append([1, i, r])
    # 邻域算子3：逆序翻转
    for i in range(nswap):
        rmore = random.randint(0, 200)
        action_list.append([3, rmore, 3])
    rm = random.randint(0, 3)
    # 邻域算子5：破坏插入
    for i in range(1):
        rm2 = random.randint(0, 100)
        action_list.append([5, rm, rm2])
    # 邻域算子2：破坏插入
    for i in range(2):
        rmore = random.randint(2, 10)
        action_list.append([2, rm, rmore])
    # 邻域算子4：破坏插入
    for i in range(2):
        rmore = random.randint(2, 10)
        action_list.append([4, rm, rmore])
    return action_list

# 函数：执行邻域算子
def doACtion(sol, action, dist, model):
    nodes_seq = copy.deepcopy(sol.nodes_seq)
    routes = sol.routes
    routes_dis = sol.routes_dis
    if action[0] == 1:
        # 执行邻域算子1
        index_1 = action[1]
        index_2 = action[2]
        length = random.randint(1, 2)
        temporary = nodes_seq[index_1:index_1+length]
        nodes_seq[index_1:index_1+length] = nodes_seq[index_2:index_2+length]
        nodes_seq[index_2:index_2+length] = temporary
        return nodes_seq
    elif action[0] == 2:
        # 执行邻域算子2
        num = action[2]
        pop = random.randint(0,len(nodes_seq)-num-1)
        pop = nodes_seq[pop:pop+num]
        # 保存行程的路线
        way = [i for i in nodes_seq if i not in pop]
        # 对pop进行插入
        for i in range(num):
            k = 0
            minimum = float('inf')
            for left in pop:
                k_dist = min([dist[left][point] for point in way])
                if k_dist < minimum:
                    minimum = k_dist
                    k = left
            # 判断将k加入到哪个弧中
            dist_to_k = []  # 保存加入弧时，增加的dist
            short_index = 0
            for j in range(len(way) - 1):
                fore = way[j]
                back = way[j + 1]
                temp_dist = dist[k][fore] + dist[k][back] - dist[fore][back]
                dist_to_k.append(temp_dist)
                short = min(dist_to_k)
                short_index = dist_to_k.index(short) + 1
            way.insert(short_index, k)
            pop.pop(pop.index(k))
        nodes_seq = copy.deepcopy(way)
        return nodes_seq
    elif action[0] == 3:
        # 执行邻域算子3
        index_1 = random.randint(0, len(nodes_seq)-1)
        index_2 = random.randint(0, len(nodes_seq)-1)
        if index_2 < index_1:
            t = index_1
            index_1 = index_2
            index_2 = t
        nodes_seq[index_1:index_2] = list(reversed(nodes_seq[index_1:index_2]))
        return nodes_seq
    elif action[0] == 4:
        # 执行邻域算子4
        num = action[2]
        pop = random.sample(nodes_seq, num)
        # 保存行程的路线
        way = [i for i in nodes_seq if i not in pop]
        # 对pop进行插入
        for i in range(num):
            k = 0
            minimum = float('inf')
            for left in pop:
                k_dist = min([dist[left][point] for point in way])
                if k_dist < minimum:
                    minimum = k_dist
                    k = left
            # 判断将k加入到哪个弧中
            dist_to_k = []  # 保存加入弧时，增加的dist
            short_index = 0
            for j in range(len(way) - 1):
                fore = way[j]
                back = way[j + 1]
                temp_dist = dist[k][fore] + dist[k][back] - dist[fore][back]
                dist_to_k.append(temp_dist)
                short = min(dist_to_k)
                short_index = dist_to_k.index(short) + 1
            way.insert(short_index, k)
            pop.pop(pop.index(k))
        nodes_seq = copy.deepcopy(way)
        return nodes_seq
    elif action[0] == 5:
        # 执行邻域算子5
        index = random.randint(0,len(routes)-1)
        pop = routes[index]
        # 保存行程的路线
        way = [i for i in nodes_seq if i not in pop]
        # 对pop进行插入
        for i in range(len(pop)):
            k = 0
            minimum = float('inf')
            for left in pop:
                k_dist = min([dist[left][point] for point in way])
                if k_dist < minimum:
                    minimum = k_dist
                    k = left
            # 判断将k加入到哪个弧中
            dist_to_k = []  # 保存加入弧时，增加的dist
            short_index = 0
            for j in range(len(way) - 1):
                fore = way[j]
                back = way[j + 1]
                temp_dist = dist[k][fore] + dist[k][back] - dist[fore][back]
                dist_to_k.append(temp_dist)
                short = min(dist_to_k)
                short_index = dist_to_k.index(short) + 1
            way.insert(short_index, k)
            pop.pop(pop.index(k))
        nodes_seq = copy.deepcopy(way)
        return nodes_seq

# 函数：解码，按约束切分TSP，得到车辆路径方案解
def splitRoutes(chrom, model):
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

# 函数：计算单条路径距离成本
def calDistance(route, model):
    distance = 0
    if len(route) == 0: return 0.0
    for i in range(len(route) - 1):
        from_node = model.node_list[route[i]]
        to_node = model.node_list[route[i + 1]]
        distance += math.sqrt((from_node.x_coord - to_node.x_coord) ** 2 + (from_node.y_coord - to_node.y_coord) ** 2)
    F_customer = model.node_list[route[0]]  # 路径中的第一个客户点
    L_customer = model.node_list[route[-1]]  # 路径中的最后一个客户点
    distance += math.sqrt(
        (F_customer.x_coord - L_customer.x_coord) ** 2 + (F_customer.y_coord - L_customer.y_coord) ** 2)
    return distance
# 函数：计算整个车辆路径方案成本
def calObj(nodes_seq, model):
    routes_dis = []
    num_vehicle, vehicle_routes = splitRoutes(nodes_seq, model)
    distance = 0
    for route in vehicle_routes:
        distance += calDistance(route, model)
        routes_dis.append(calDistance(route, model))
    return distance, vehicle_routes, routes_dis

# 函数：绘制目标函数值迭代图像
def plotObj(obj_list):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # show chinese
    plt.rcParams['axes.unicode_minus'] = False  # Show minus sign
    plt.plot(np.arange(1, len(obj_list) + 1), obj_list)
    plt.xlabel('Iterations')
    plt.ylabel('Obj Value')
    plt.grid()
    plt.xlim(1, len(obj_list) + 1)
    plt.show()
# 绘图函数：绘制车辆行驶路径图
def plot_route(model):
    plt.figure()
    for route in model.best_sol.routes:  # 对每条车辆路径进行绘制
        x_coord = []  # 生成绘图x坐标列表，先把仓库加进去，作为起点
        y_coord = []  # 生成绘图y坐标列表，先把仓库加进去，作为起点
        for i in route:  # 将路径中每个客户点坐标加进去
            x_coord.append(model.node_list[i].x_coord)
            y_coord.append(model.node_list[i].y_coord)
            plt.text(model.node_list[i].x_coord, model.node_list[i].y_coord, model.node_list[i].name,
                     fontsize=5)  # 先在图上画出每个客户点的名称
        x_coord.append(model.node_list[route[0]].x_coord)  # 最后再次加入仓库，作为终点
        y_coord.append(model.node_list[route[0]].y_coord)  # 最后再次加入仓库，作为终点
        plt.grid()  # 显示网格线，1=True=默认=显示，0=False=不显示
        plt.plot(x_coord, y_coord, 'b:', linewidth=0.5, marker='o',
                 markersize=2)  # 设置每条路径的绘图参数，线型及颜色：蓝色、点线(b:)；点型：原点，大小为5
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
    for row, route in enumerate(model.best_sol.routes):  # enumerate返回对象中各个值和对应的位置索引
        excelsheet.write(row + 1, 0, f'v{row + 1}')  # 从第2行开始，依次在第1列中写入车辆编号
        excelsheet.write(row + 1, 1, str(route))  # 从第2行开始，依次在第2列中写入路径
    for row, dis in enumerate(model.best_sol.routes_dis):
        excelsheet.write(row + 1, 2, dis)
    excel.close()

#函数：运行SA
def run(filepath,T0,Tf,detaT,v_cap,opt_type):
    """
    T0: 初始温度
    Tf: 终止温度
    deltaT: 降温率
    v_cap:车辆载重
    opt_type: 0表示优化目标为最小化行驶总里程;1表示优化目标为最小化总用车数
    """
    #实例化算例
    start_time = time.time()  # 定义算法起始时间
    model=Model()
    model.vehicle_cap=v_cap
    model.salemen=opt_type
    readExcel(filepath,model)
    #生成初始解
    history_best_obj=[]
    sol=Sol()
    sol.nodes_seq=genInitialSol(model=model)
    sol.obj,sol.routes,sol.routes_dis=calObj(sol.nodes_seq,model)
    model.best_sol=copy.deepcopy(sol)
    history_best_obj.append(sol.obj)
    #others preparation
    dist = np.zeros((model.number_of_nodes-model.salemen+1, model.number_of_nodes-model.salemen+1), dtype=float)
    for i in range(model.number_of_nodes-model.salemen+1):
        for j in range(model.number_of_nodes-model.salemen+1):
            dist[i, j] = math.sqrt((model.node_list[i].x_coord - model.node_list[j].x_coord) ** 2 +
                                   (model.node_list[i].y_coord - model.node_list[j].y_coord) ** 2)
    #设定当前温度为初始温度
    Tk=T0
    #构建禁忌列表
    model.tabu_list=[[[0]],[0]]
    #开始迭代求解
    while Tk>=Tf and time.time() - start_time < 60:
        # 构建邻域算子列表
        action_list = createActions(model.number_of_nodes, Tk)
        #初始化局部最优解为无穷大
        local_new_sol=Sol()
        local_new_sol.obj=float('inf')
        #遍历邻域算子列表：
        temp_action = []
        for i in range(len(action_list)):
            # 若当前未被禁忌
            if action_list[i] not in model.tabu_list[0]:
                #执行当前算子，得到新解
                new_sol=Sol()
                new_sol.nodes_seq=doACtion(sol=sol, action=action_list[i], dist=dist, model=model)
                new_sol.obj,new_sol.routes,new_sol.routes_dis=calObj(new_sol.nodes_seq,model)
                # 若新解优于当前局部最优解，进行更新
                if new_sol.obj < local_new_sol.obj:
                    local_new_sol = copy.deepcopy(new_sol)
                    temp_action = copy.deepcopy(action_list[i])
        if temp_action not in model.tabu_list[0]:
            model.tabu_list[0].append(temp_action)
            model.tabu_list[1].append(21)
        # 更新当前解为局部最优解
        if local_new_sol.obj < sol.obj:
            sol = local_new_sol
        #若当前解优于全局最优解，更新全局最优解
        if sol.obj<model.best_sol.obj:
            model.best_sol=copy.deepcopy(sol)
        for i in range(len(model.tabu_list[0])):
            #if it % 2 == 0:
            #将其他算子禁忌长度减一(最小归为0，表示不被禁忌)
            model.tabu_list[1][i]=max(model.tabu_list[1][i]-1,0)
        for i in range(len(model.tabu_list[0])):
            if i!=0 and model.tabu_list[1][i] == 0:
                model.tabu_list[0].pop(i)
                model.tabu_list[1].pop(i)
                break
        #更新温度.=
        if detaT<1:
            Tk=Tk*detaT
        else:
            Tk = Tk - detaT
        #更新历史最优解
        history_best_obj.append(model.best_sol.obj)
        print("当前温度：%s，局部最优解:%s 全局最优解: %s" % (round(Tk,2),round(sol.obj,2),round(model.best_sol.obj,2)))
    #绘制迭代图
    #plot_route(model=model)
    #plt.show()
    return model

if __name__ == '__main__':
    filepath = r'作业\小组作业\测试样例\A-n32-k5.vrp'
    run_time = 8
    ran = range(3,11)
    i = 0
    all_best_obj = []
    all_best_Route = []
    all_Route_dis = []
    while i < run_time:
        print(f"*====================第{i + 1}次运行====================*")
        start_time = time.time()  # 定义算法起始时间
        model = run(filepath=filepath,T0=10000,Tf=0.001,detaT=1,v_cap=200,opt_type=ran[i])
        end_time = time.time()  # 定义算法起始时间
        print(end_time-start_time)
        all_best_obj.append(model.best_sol.obj)
        all_best_Route.append(model.best_sol.routes)
        print("最短里程：", model.best_sol.obj)
        print("最短车辆路径方案：", model.best_sol.routes)
        i += 1
        output(model=model)
    x = []
    y = []
    for i in range(run_time):
        print(f"saleman数量为:{ran[i]}")
        x.append(ran[i])
        print("最短里程：", all_best_obj[i])
        y.append(all_best_obj[i])
    # 画点图
    plt.scatter(x, y)
    # 添加标题和标签
    plt.title('Scatter Plot Example')
    plt.xlabel('saleman number')
    plt.ylabel('minimum distance')
    # 显示图形
    plt.show()



