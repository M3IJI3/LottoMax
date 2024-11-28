import random
import pandas as pd
import numpy as np

# 设置彩票的参数
num_draws = 7  # 每次抽取的主号码数量
num_simulations = 100000  # 模拟的次数
number_range = 50  # 号码的最大值

# 步骤 1：从 CSV 文件中读取历史数据
df = pd.read_csv('numbers.csv', header=None)
historical_data = df.values.tolist()  # 将数据转换为二维列表

# 步骤 2：统计每个主号码和 bonus number 出现的频率
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

# 步骤 3：基于出现频率计算概率分布
main_number_probabilities = np.array(main_number_frequency) / sum(main_number_frequency)
bonus_number_probabilities = np.array(bonus_number_frequency) / sum(bonus_number_frequency)

# 步骤 4：根据概率分布随机推荐下一组数据
recommended_main_numbers = random.choices(range(1, number_range + 1), weights=main_number_probabilities, k=num_draws)
recommended_bonus_number = random.choices(range(1, number_range + 1), weights=bonus_number_probabilities, k=1)

# 打印推荐的数字
print(f"推荐的主号码: {sorted(recommended_main_numbers)}")
print(f"推荐的 Bonus Number: {recommended_bonus_number[0]}")
