import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

# 原始数据
nodes = [4,7,16,22,31]
bathSize1000ToServerTPS = [4030, 3408, 10,10,10]
batchSize500ToServerTPS = [2100, 1865, 1475,10,10]
batchSize200ToServerTPS = [930, 872, 670,590,10]
# 插值平滑曲线
x_new = np.linspace(min(nodes ), max(nodes ), 100)
f1 = interp1d(nodes , bathSize1000ToServerTPS, kind='linear')
f2 = interp1d(nodes , batchSize500ToServerTPS, kind='linear')
f3 = interp1d(nodes , batchSize200ToServerTPS, kind='linear')
# 创建一个图形对象
plt.figure()

# 绘制平滑的曲线
plt.plot(x_new, f1(x_new), linestyle='-', label='Client\'s TPS:5 batchSize=1000')
plt.plot(x_new, f2(x_new), linestyle='-', label='Client\'s TPS:5 batchSize=500')
plt.plot(x_new, f3(x_new), linestyle='-', label='Client\'s TPS:5 batchSize=200')

# 绘制原始数据的标记
plt.scatter(nodes , bathSize1000ToServerTPS, marker='o', color='blue')
plt.scatter(nodes , batchSize500ToServerTPS, marker='o', color='orange')
plt.scatter(nodes , batchSize200ToServerTPS, marker='o', color='green')

# 添加标题和标签
plt.xlabel('replicas')
plt.ylabel('Throughput (tx/s)')

# 显示网格
plt.grid(True)

# 添加图例
plt.legend()

plt.savefig('Figure 7.png')





