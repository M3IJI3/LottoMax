import random
import pandas as pd
import matplotlib.pyplot as plt

# 设置彩票的参数
num_draws = 7  # 每次抽取的主号码数量
num_simulations = 100000  # 模拟的次数
number_range = 50  # 号码的最大值

# 步骤 1：从 CSV 文件中读取历史数据
df = pd.read_csv('numbers.csv', header=None)
historical_data = df.values.tolist()  # 将数据转换为二维列表

# 步骤 2：模拟 Lotto Max 抽奖过程
main_number_frequency = [0] * number_range  # 用于记录每个主号码的出现次数
bonus_number_frequency = [0] * number_range  # 用于记录每个 bonus number 的出现次数

# 进行多次模拟
for _ in range(num_simulations):
    # 模拟一次抽奖，随机选择 7 个主号码
    simulated_draw = random.sample(range(1, number_range + 1), num_draws)
    
    # 模拟 bonus number，从剩下的号码中随机选一个
    remaining_numbers = list(set(range(1, number_range + 1)) - set(simulated_draw))
    bonus_number = random.choice(remaining_numbers)
    
    # 统计每个主号码的出现频率
    for number in simulated_draw:
        main_number_frequency[number - 1] += 1  # 累计主号码出现次数
    
    # 统计 bonus number 的出现频率
    bonus_number_frequency[bonus_number - 1] += 1

# 步骤 3：将统计结果转换为 DataFrame 便于查看和分析
df_main_frequency = pd.DataFrame({
    'Number': list(range(1, number_range + 1)),
    'Main Frequency': main_number_frequency
})

df_bonus_frequency = pd.DataFrame({
    'Number': list(range(1, number_range + 1)),
    'Bonus Frequency': bonus_number_frequency
})

# 步骤 4：按出现频率排序
df_main_frequency = df_main_frequency.sort_values(by='Main Frequency', ascending=False)
df_bonus_frequency = df_bonus_frequency.sort_values(by='Bonus Frequency', ascending=False)

# 打印最常出现的前 10 个主号码和 bonus number
print("最常出现的 10 个主号码：")
print(df_main_frequency.head(10))

print("\n最常出现的 10 个 Bonus Numbers：")
print(df_bonus_frequency.head(10))

# 步骤 5：绘制数字出现频率的柱状图
plt.figure(figsize=(10, 6))

# 绘制主号码的柱状图
plt.subplot(1, 2, 1)
plt.bar(df_main_frequency['Number'], df_main_frequency['Main Frequency'], color='skyblue')
plt.title('Main Number Frequency in Monte Carlo Simulation')
plt.xlabel('Number')
plt.ylabel('Frequency')

# 绘制 Bonus Number 的柱状图
plt.subplot(1, 2, 2)
plt.bar(df_bonus_frequency['Number'], df_bonus_frequency['Bonus Frequency'], color='orange')
plt.title('Bonus Number Frequency in Monte Carlo Simulation')
plt.xlabel('Number')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()
