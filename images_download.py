import requests
import os

# 输入文件，包含ID和URL
input_file = 'images.txt'
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
    for line in file:
        # 移除换行符并分割ID和URL
        parts = line.strip().split(',')
        if len(parts) != 2:
            continue  # 跳过格式不正确的行

        id_, url = parts
        # 发送HTTP请求并获取图片内容 使用stream=True来避免一次性加载整个图片到内存
        response = requests.get(url, stream=True)
        status_message = f"Downloading {id_} from {url}"
        print(status_message)  # 打印下载状态
        if response.status_code == 200:
            # 构建保存图片的完整路径
            image_path = os.path.join(download_dir, f'{id_}.jpg')
            # 保存图片，文件名以ID命名
            with open(image_path, 'wb') as image_file:
                # image_file.write(response.content)
                # 分块写入文件 每次写入1024字节
                for chunk in response.iter_content(1024):
                    if chunk:  # 如果chunk不为空，则写入文件
                        image_file.write(chunk)
        else:
            print(f"Failed to download image with ID {id_}. Status code: {response.status_code}")
            continue  # 跳过当前图片，继续下一个

print("Download completed.")
