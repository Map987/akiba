import os
import requests
from datetime import datetime, timedelta

# 基础URL
base_url = "https://image-org-s.akiba-souken.com/assets/images/article/"
config_file = "star.config"

# 读取配置文件中的起始编号
if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        start_number = int(f.read().strip())
else:
    start_number = 1058896  # 如果配置文件不存在，则从默认起始编号开始

# 结束编号是起始编号加上100
end_number = start_number + 100

# 用于下载和保存图片的函数
def download_and_save_image(image_number):
    section = str(image_number)[1:4]
    image_url = f"{base_url}001/{section}/{image_number}.jpg"
    response = requests.get(image_url)

    if response.status_code == 200:
        # 获取当前时间并格式化
        current_time = datetime.utcnow()
        current_time += timedelta(hours=8)  # UTC+8
        formatted_date = current_time.strftime("%Y-%m-%d")
        formatted_time = current_time.strftime("%H.%M")

        # 新的文件名
        new_filename = f"{image_number}.{formatted_date}..{formatted_time}.jpg"
        with open(new_filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded and saved: {new_filename}")
        return image_number
    else:
        print(f"Image {image_number}.jpg not found, skipping.")
        return None

# 遍历图片编号并下载
last_valid_number = start_number
for number in range(start_number, end_number + 1):
    valid_number = download_and_save_image(number)
    if valid_number is not None:
        last_valid_number = valid_number

# 更新配置文件以记录最后一个有效的图片编号
with open(config_file, 'w') as f:
    f.write(str(last_valid_number))
