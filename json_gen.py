import json
import os

# 输入文件，包含ID和URL
input_file = 'json_descs.txt'
# 当前工作目录作为根目录
root_dir = os.getcwd()
# download目录的完整路径
download_dir = os.path.join(root_dir, 'download')

# 确保输入文件存在
if not os.path.isfile(input_file):
    print(f"Error: File '{input_file}' not found.")
    exit(1)

# 如果download目录不存在，则创建它
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# 读取文件并下载图片
with open(input_file, 'r', encoding='utf-8') as file:
    # 遍历每行文本
    for line in file:
        # 提取行号和描述
        number, description = line.split(',', 1)
        number = number.strip()  # 移除行号两端的空格
        description = description.strip()  # 移除描述两端的空格

        # 创建JSON对象
        json_data = {"prompt": description}

        # 构建保存图片的完整路径
        json_path = os.path.join(download_dir, f'{number}.json')
        # 将JSON对象写入文件，文件名基于行号
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)

        # # 将JSON对象写入文件，文件名基于行号
        # with open(f"{number}.json", 'w', encoding='utf-8') as json_file:
        #     json.dump(json_data, json_file, ensure_ascii=False, indent=4)

print("JSON files have been created successfully.")
