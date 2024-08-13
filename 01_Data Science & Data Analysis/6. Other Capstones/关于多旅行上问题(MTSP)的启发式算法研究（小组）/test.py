import numpy as np
import pandas as pd  # 提供DataFrame，是一种二维表格型数据
import matplotlib.pyplot as plt  # 画图包
import xlsxwriter  # 读取Excel文件包
import math
import copy
import random
import time
import vrplib


plt.figure()
route=[[17, 47, 13, 20, 39, 48, 72, 12, 0, 6, 9, 70, 51, 27, 78], [1, 36], [54, 55, 8, 53], [75, 71, 44, 21, 3, 31, 49], [52, 69, 66, 65, 35, 41, 50, 76, 2], [57, 37], [60, 56, 25, 34, 64, 68, 46, 18, 74, 19, 77, 7, 67, 42, 15], [59, 38], [73, 28, 4, 43, 11, 22, 61, 62, 10, 33, 23, 5, 29, 58, 26, 30, 16], [63, 45, 24, 40, 14, 32]]
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
plt.show()