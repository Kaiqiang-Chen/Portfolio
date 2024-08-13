import pandas as pd
import numpy as np
import gurobipy as gp
from gurobipy import GRB
import matplotlib.pyplot as plt
import random
import vrplib


# 载入数据
# 算例
instance = vrplib.read_instance(r"C:\Users\10136\Desktop\大三下\课程\智能优化算法\作业\小组作业\测试样例\A-n32-k5.vrp")

# 解
# solution = vrplib.read_solution(r"作业\小组作业\测试样例\A-n32-k5.sol")

# 城市坐标
city_location = instance['node_coord']

# # 解的路径
# route = solution['routes']

print(city_location)
# print(route)

city_name = []
for i in range(len(city_location)):
    city_name.append(i+1)

print(city_name)
# print(city_location)
n = len(city_location)
m = 3
L = n - 2*m + 2
print(n)
print(m)
print(L)
print(f'---------------------------------------------')

model = gp.Model("MTSP")

Max = 1000000
# 获得坐标间的距离
dist = np.array([[float(Max)]*n]*n)
for i in range(n):
    for j in range(n):
        a = np.sqrt(pow((city_location[i][0]-city_location[j][0]),2) + pow((city_location[i][1]-city_location[j][1]),2))
        if a != 0:
            dist[i][j] = a



# 设置变量
x = model.addVars(range(m), range(n),range(n),lb=0.0,vtype=GRB.BINARY,name='x') # lb限制下限为0.0
# 设置决策变量u  ui代表点i是从出发点开始第几个被访问的点
u = model.addVars(n, vtype=GRB.CONTINUOUS, name='u')
# 设置变量判断节点i是否是depot
z = model.addVars(n,lb=0.0 , vtype=GRB.BINARY, name = 'z')

# 目标函数
objective = gp.quicksum(dist[i][j] * gp.quicksum(x[k,i,j] for k in range(m)) for i in range(n) for j in range(n) if i != j)
model.setObjective(objective, GRB.MINIMIZE)
# 约束(由于dist对角线上值为极大值，所以无需额外约束xii=0,后续约束也将其减去)
# 1
model.addConstrs(gp.quicksum(x[k,i,j] for k in range(m) for i in range(n) if i != j) == 1 for j in range(n))
# 2
model.addConstrs(gp.quicksum(x[k,i,p] for i in range(n) if i != p) - gp.quicksum(x[k,p,j] for j in range(n) if j != p) == 0 for p in range(n) for k in range(m))
# 3
model.addConstrs(gp.quicksum(x[k,i,j] for j in range(n) for i in range(n) if i != j) >= 1 for k in range(m))
# 4 回路约束(MTZ约束)
# i,j不等于0，在循环时只访问不包括起点
# 如果i在j的前面被访问，距离大于1时，x[i,j]=0(n个点n-1条路); =1时，u[i]-u[j]=-1,n*x[i,j]=n,所以相加后<=n-1
# 同样的，j在i的前面被访问时，x[i,j]=0,<n-1
model.addConstrs((u[i] - u[j] + L*gp.quicksum(x[k,i,j] for k in range(m)))<= L-1+L*z[j] for i in range(n) for j in range(n) if i != j)
# 5 决策变量约束
model.addConstrs(u[i] <= L for i in range(n))
model.addConstrs(u[i] >= 1 for i in range(n))
# 6 depot约束
model.addConstr(gp.quicksum(z[i] for i in range(n)) == m)

model.write('mtsp.lp')
model.optimize()

print(f"最优目标值为：{model.ObjVal}")

# for i in range(n):
#     if z[i].x > 0.5:
#         print(i)
# for k in range(m):
#     for i in range(n):
#         if x[k, i, 4].x > 0.5:
#             print(f"旅行商{k}在{i}")
#         elif x[k, i, 19].x > 0.5:
#             print(f"旅行商{k}在{i}")
#         elif x[k, i, 22].x > 0.5:
#             print(f"旅行商{k}在{i}")


spot=[]
all_route = []
for i in range(m):
    for q in range(n):
        if z[q].x > 0.5 and q not in spot:
            current_city = q
            spot.append(q)
            each_route = []
            visited_cities = []
            each_route.append(current_city)
            visited_cities.append(current_city)
            for k in range(n):
                if k not in spot and x[i, current_city, k].x > 0.5:
                    current_city = k
                    visited_cities.append(k)
                    each_route.append(k)
                    while x[i, current_city, q].x < 0.5:
                        for t in range(n):
                            if x[i, current_city, t].x > 0.5 and t not in visited_cities:
                                visited_cities.append(t)
                                each_route.append(t)
                                current_city = t
                    # 输出该旅行商的路径
                    each_route.append(q)
                    print(f'路径{i}为{each_route}')
                    all_route.append(each_route)
                    break
            break


# 生成随机颜色
def generate_random_color():
    r = random.random()
    g = random.random()
    b = random.random()
    return (r, g, b)

# 绘制城市坐标
for i, (x, y) in enumerate(city_location):
    plt.scatter(x, y, color='blue')
    plt.text(x, y, city_name[i], fontsize=8)

# 绘制每个旅行商的路径，并使用随机颜色
for route in all_route:
    color = generate_random_color()
    for i in range(len(route) - 1):
        city1_index = route[i]
        city2_index = route[i+1]
        city1 = city_location[city1_index]
        city2 = city_location[city2_index]
        plt.plot([city1[0], city2[0]], [city1[1], city2[1]], color=color)

plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.title('Traveling Salesman Problem Solution')
plt.show()
