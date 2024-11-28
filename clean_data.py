# 读取并处理 CSV 文件
input_file = 'numbers.csv'
output_file = 'cleaned_numbers.csv'

# 打开输入文件和输出文件
with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        # 去除每行开头的内容，直到第一个逗号及其之前的字符
        cleaned_line = line.split(',', 1)[-1]  # 获取第一个逗号后的部分
        outfile.write(cleaned_line)  # 写入处理后的行

print(f"处理完成，清理后的文件保存为 {output_file}")
