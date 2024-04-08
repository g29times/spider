import pandas as pd
import re

import os
import requests

task = '2023 Spring trim'

# 读取本地Excel文件
df = pd.read_excel(task + '.xlsx', engine='openpyxl')

# 创建一个字典来存储每个SPU的所有SKU型号和图片地址
spus_dict = {}
image_urls = []
sku_list = []

# 遍历DataFrame，填充字典
for index, row in df.iterrows():
    col1 = row['Col1']  # SKU型号
    spu_name = re.search(r'([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)*)', col1).group()  # SPU名称
    spu_code = re.search(r'(S\d+)|(\d+)', col1).group()
    # spu_code = col1.split()[1].split('/')[0]  # SPU编号
    sku_count = int(row['Col3'].replace(' colorways', ''))  # SKU数量

    # 根据SKU数量生成SKU型号列表
    sku_list = [f"{spu_code}/{i:02d}" for i in range(1, sku_count + 1)]

    # 构建基础图片地址
    base_image_url = "https://amaya.pollackassociates.com/media/catalog/product"
    image_urls = [
        f"{base_image_url}/{spu_code[0]}/{spu_code[1]}/{spu_code}_{i:02d}_870.jpg"
        for i in range(1, sku_count + 1)]
    # 存储SPU名称和对应的SKU信息及图片地址
    spus_dict[spu_name] = {
        'SKU列表': sku_list,
        '图片地址': image_urls
    }

# 确保保存图片的目录存在
dl_dir = 'downloaded_images/' + task
os.makedirs(dl_dir, exist_ok=True)

# 打印结果
for spu_key, spu_value in spus_dict.items():
    print(f"SPU名称: {spu_key}")
    print(f"SKU列表: {spu_value['SKU列表']}")
    print(f"图片地址: {spu_value['图片地址']}")

    # 下载并保存图片
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    for image_url, sku in zip(spu_value['图片地址'], spu_value['SKU列表']):
        try:
            # 从URL中提取图片名称
            filename = re.search(r'/([^/]+)$', image_url).group(1)
            # 检查图片是否已存在
            if not os.path.exists(os.path.join(dl_dir, filename)):
                # 发送HTTP GET请求获取图片内容
                response = requests.get(image_url, headers=headers)
                # 检查请求是否成功
                if response.status_code == 200:
                    # 保存图片到指定目录
                    with open(os.path.join(dl_dir, filename), 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:  # 过滤掉保持连接的新块
                                f.write(chunk)
                        # f.write(response.content)
                    print(f"图片 {filename} 下载成功。")
                else:
                    print(f"错误：无法从 {image_url} 获取图片，HTTP状态码：{response.status_code}。")
            else:
                print(f"图片 {filename} 已存在，跳过下载。")
        except requests.exceptions.RequestException as e:
            print(f"请求异常：{e}。")

    print("所有图片下载完成。")
    print('-' * 40)
