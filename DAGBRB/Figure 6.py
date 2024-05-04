import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

# 原始数据
batch_size = [1, 500, 900,1000, 1500, 2000, 2500, 3000,3500,4000,4500,5000,5500]
clientstps20 = [19, 8750, 10,10, 10, 10, 10, 10,10, 10, 10, 10, 10]  # client tps 20曲线的数据
clientstps15 = [14, 6220, 9693,10, 10, 10, 10, 10,10, 10, 10, 10, 10]  # client tps 15曲线的数据
clientstps10 = [9, 4380,7245,7890, 12160, 10, 10, 10,10, 10, 10, 10, 10]  # client tps 10曲线的数据
clientstps5 = [4,2100,3645,4030,5970,7380,8750,10440,12005,13520,13950,14900,10] # client tps 5曲线的数据
# 插值平滑曲线
x_new = np.linspace(min(batch_size), max(batch_size), 100)
f1 = interp1d(batch_size, clientstps20, kind='linear')
f2 = interp1d(batch_size, clientstps15, kind='linear')
f3 = interp1d(batch_size, clientstps10, kind='linear')
f4 = interp1d(batch_size, clientstps5, kind='linear')
# 创建一个图形对象
plt.figure()

# 绘制平滑的曲线
plt.plot(x_new, f1(x_new), linestyle='-', label='Client\'s TPS 20')
plt.plot(x_new, f2(x_new), linestyle='-', label='Client\'s TPS 15')
plt.plot(x_new, f3(x_new), linestyle='-', label='Client\'s TPS 10')
plt.plot(x_new, f4(x_new), linestyle='-', label='Client\'s TPS 5')
# 绘制原始数据的标记
plt.scatter(batch_size, clientstps20, marker='o', color='blue')
plt.scatter(batch_size, clientstps15, marker='o', color='orange')
plt.scatter(batch_size, clientstps10, marker='o', color='green')
plt.scatter(batch_size, clientstps5, marker='o', color='red')

# 添加标题和标签
plt.xlabel('BatchSize')
plt.ylabel('Throughput (tx/s)')

# 显示网格
plt.grid(True)

# 添加图例
plt.legend()

plt.savefig('Figure 6.png')





