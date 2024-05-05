import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

# 原始数据
clientstps = [20, 40, 60,80,100,120,140,160,180,200,220,240]
serverstps = [19, 39, 58, 79, 95, 115, 134, 153, 171,180,175,10]


# 插值平滑曲线
x_new = np.linspace(min(clientstps), max(clientstps), 100)
f1 = interp1d(clientstps, serverstps, kind='linear')

# 创建一个图形对象
plt.figure()

# 绘制平滑的曲线
plt.plot(x_new, f1(x_new), linestyle='-',label='Server\'s TPS')

# 绘制原始数据的标记
plt.scatter(clientstps, serverstps, marker='o', color='blue')


# 添加标题和标签
plt.xlabel('Client\'s TPS')
plt.ylabel('Throughput (tx/s)')

# 显示网格
plt.grid(True)

# 添加图例
plt.legend()

plt.savefig('Figure 5.png')





