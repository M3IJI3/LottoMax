import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
from sklearn.model_selection import train_test_split
import numpy as np

# 读取数据并指定列名
column_names = ['Number1', 'Number2', 'Number3', 'Number4', 'Number5', 'Number6', 'Number7', 'BonusNumber']
df = pd.read_csv('cleaned_numbers.csv', header=None, names=column_names)

# 提取特征和标签（这里使用所有8个数字作为输入和目标）
X = df[['Number1', 'Number2', 'Number3', 'Number4', 'Number5', 'Number6', 'Number7', 'BonusNumber']].values

# 使用 MinMaxScaler 进行数据缩放
scaler = MinMaxScaler(feature_range=(1, 50))  # 设置特征范围为1到50
X_scaled = scaler.fit_transform(X)

# 划分训练集和测试集
X_train, X_test = train_test_split(X_scaled, test_size=0.2, random_state=42)

# 定义模型
model = Sequential()
model.add(Input(shape=(8,)))  # 输入层，8个特征
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(8, activation='linear'))  # 输出层，预测8个数字

# 编译模型
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# 训练模型
model.fit(X_train, X_train, epochs=50, batch_size=32, validation_data=(X_test, X_test))

# 使用训练好的模型进行预测
predictions = model.predict(X_test)

# 将预测结果从0-1范围转换为原始的1-50范围，并四舍五入为整数
predictions_rescaled = scaler.inverse_transform(predictions)

# 强制结果在1到50之间，并四舍五入为整数
predictions_rescaled_clipped = np.clip(predictions_rescaled, 1, 50)  # 限制值在[1, 50]范围内
predictions_rescaled_rounded = np.round(predictions_rescaled_clipped).astype(int)

# 强制确保每组数据没有重复数字
def remove_duplicates(predictions):
    result = []
    for prediction in predictions:
        # 使每组预测中的数字唯一
        unique_prediction = np.unique(prediction)  # 去除重复数字
        if len(unique_prediction) == len(prediction):
            result.append(unique_prediction)
        else:
            # 如果有重复，重新生成
            result.append(np.unique(np.random.choice(range(1, 51), 8, replace=False)))
    return result

# 清除重复的数字
predictions_no_duplicates = remove_duplicates(predictions_rescaled_rounded)

# 输出预测的下一组数字
print("Predicted Next Set of Numbers (for test data sample):")
print(predictions_no_duplicates[:5])  # 输出前5个预测结果

# 假设你希望生成一组新的预测数据，可以选择一个新的输入数据（例如，随机生成的数字）
new_input = np.random.rand(1, 8)  # 随机生成一组数据作为输入（8个数字）
scaled_input = scaler.transform(new_input)  # 缩放该输入数据

# 预测新的输入
new_prediction = model.predict(scaled_input)
new_prediction_rescaled = scaler.inverse_transform(new_prediction)

# 强制结果在1到50之间，并四舍五入为整数
new_prediction_clipped = np.clip(new_prediction_rescaled, 1, 50)
new_prediction_rounded = np.round(new_prediction_clipped).astype(int)

# 确保新预测没有重复
new_prediction_no_duplicates = remove_duplicates(new_prediction_rounded)

print(f"Predicted Next Set of Numbers for new random input: {new_prediction_no_duplicates}")
