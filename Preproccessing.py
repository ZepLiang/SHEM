import pandas as pd
from datetime import datetime

# 读取 Excel 文件
file_path = r"C:\Users\liang\Documents\GitHub\CLP\LD001_pp_01AUG2018_to_15AUG2018.xlsx"
df = pd.read_excel(file_path)

# 提取指定列的数据
data = df[['device_id', 'measurement_time(UTC)', 'power(W)']]

# 转换日期时间格式并移除时区信息
data.loc[:, 'measurement_time(UTC)'] = pd.to_datetime(data['measurement_time(UTC)']).dt.tz_localize(None)

# 按照 device_id 和 measurement_time(UTC) 进行排序
sorted_data = data.sort_values(by=['device_id', 'measurement_time(UTC)'])

# 检查并补充缺失的时间戳
device_ids = sorted_data['device_id'].unique()
result = []

for device_id in device_ids:
    device_data = sorted_data.loc[sorted_data['device_id'] == device_id]
    min_time = device_data['measurement_time(UTC)'].min()
    max_time = device_data['measurement_time(UTC)'].max()
    full_range = pd.date_range(min_time, max_time, freq='1min')
    full_data = pd.DataFrame({'device_id': device_id, 'measurement_time(UTC)': full_range})
    merged_data = pd.concat([full_data.set_index(['device_id', 'measurement_time(UTC)']),
                             device_data.set_index(['device_id', 'measurement_time(UTC)'])], axis=1).reset_index()
    merged_data['power(W)'] = merged_data['power(W)'].fillna(0)  # 填充缺失的功率值为0
    result.append(merged_data)

merged_result = pd.concat(result)

# 保存补充缺失后的数据到新的 Excel 文件
output_file_path = r"C:\Users\liang\Documents\GitHub\CLP\sorted_and_filled_data.xlsx"
merged_result.to_excel(output_file_path, index=False)

print("补充缺失后的数据已保存到新的 Excel 文件：", output_file_path)

# # 使用groupby和pivot_table将数据重塑
# df_new = df.groupby(['measurement_time(UTC)', 'device_id'])['power(W)'].sum().unstack()
#
# # 重置索引
# df_new = df_new.reset_index()
#
# # 结果
# output_file_path = r"C:\Users\liang\Documents\GitHub\CLP\Reorder_sorted_and_filled_data.xlsx"
# df_new.to_excel(output_file_path, index=False)