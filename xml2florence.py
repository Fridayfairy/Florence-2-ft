"""
# Author： YCX
# Date:    2024.08.26
# Description:  把xml 修改成 florence  https://blog.roboflow.com/fine-tune-florence-2-object-detection/
{"prefix": "<OD>", "suffix": "10 of clubs<loc_142><loc_101><loc_465><loc_451>9 of clubs<loc_387><loc_146><loc_665><loc_454>", "image": "rot_0_7471_png_jpg.rf.30ec1d3771a6b126e7d5f14ad0b3073b.jpg"}
{"prefix": "<OD>", "suffix": "10 of clubs<loc_142><loc_101><loc_465><loc_451>9 of clubs<loc_387><loc_146><loc_665><loc_454>", "image": "rot_0_7471_png_jpg.rf.30ec1d3771a6b126e7d5f14ad0b3073b.jpg"}

JSONL（JSON Lines）是一种文件格式，它将 JSON 对象序列化成多行文本，每行包含一个单独的 JSON 对象。这种格式特别适合日志文件、数据流处理和大数据应用，因为它易于人类阅读和解析，同时保持了 JSON 的结构化特性。
特点：
每行是一个有效的 JSON 对象。
行与行之间用换行符分隔。
文件可以包含任意数量的 JSON 对象。
读写 JSONL 文件的方法：
读取 JSONL 文件：
使用 Python 的内置 open 函数打开文件。
逐行读取文件内容。
使用 json.loads 函数将每行的字符串解析为 Python 字典。
python
import json

# 打开 JSONL 文件
with open('data.jsonl', 'r', encoding='utf-8') as file:
    # 逐行读取并解析 JSON 对象
    for line in file:
        obj = json.loads(line)
        print(obj)  # 处理解析后的字典
写入 JSONL 文件：
使用 Python 的内置 open 函数以写入模式打开文件。
对于每个要写入的对象，使用 json.dumps 函数将其转换为 JSON 格式的字符串。
将字符串写入文件，并确保每行结束后添加换行符。
python
import json

# 要写入的 Python 字典列表
data = [
    {'id': 1, 'name': 'Alice'},
    {'id': 2, 'name': 'Bob'}
]

# 打开文件以写入 JSONL
with open('output.jsonl', 'w', encoding='utf-8') as file:
    for obj in data:
        # 将字典转换为 JSON 字符串，并写入文件，每行一个 JSON 对象
        file.write(json.dumps(obj) + '\n')
注意事项：
确保在读取和写入文件时使用正确的编码，通常是 'utf-8'。
在写入时，json.dumps 默认不会添加额外的空格或换行符，它只负责将 Python 对象转换为 JSON 格式的字符串。
在读取时，如果文件非常大，考虑使用生成器逐行读取，这样可以减少内存使用。
JSONL 是一种简单但功能强大的数据交换格式，特别适合处理流式数据或大量独立的数据记录。
"""

import json
import xml.etree.ElementTree as ET
import os
from tqdm import tqdm

def xml_to_json(xml_paths):
    jsons = []
    for xml_path in tqdm(xml_paths):
        # 解析XML文件
        tree = ET.parse(xml_path)
        root = tree.getroot()
        size = root.find('size')
        width = int(size.find('width').text)
        height = int(size.find('height').text)

        # 获取图片的绝对路径
        path_tmp = os.path.abspath(xml_path).replace('/Annotations/', '/images/')
        
        for ext in ['.jpg', '.JPG', '.png']:
            image_path = os.path.abspath(path_tmp).replace('.xml', ext)
            if os.path.exists(image_path):
                break
        else:
            print(f"no {xml_path}")
            continue

        # 初始化图片的标注列表
        suffix = ""

        # 遍历所有的object元素
        for obj in root.findall('object'):
            # 获取文本内容
            class_name = obj.find('name').text
            if class_name in chinese_2_english.keys():
                class_name = chinese_2_english[class_name]
            else:
                continue
            # 获取bounding box坐标
            bndbox = obj.find('bndbox')
            x1 = float(bndbox.find('xmin').text)
            y1 = float(bndbox.find('ymin').text)
            x2 = float(bndbox.find('xmax').text)
            y2 = float(bndbox.find('ymax').text)

            # # 2. 将所有定位框坐标按照图像的高和宽归一化到(0,1000).即x=x*1000/width，y=y*1000/height  merge_box中实现
            x1 = int(x1 * 1000 / width)
            x2 = int(x2 * 1000 / width)
            y1 = int(y1 * 1000 / height)
            y2 = int(y2 * 1000 / height)

            
            # 将标注添加到列表中
            suffix += "{}<loc_{}><loc_{}><loc_{}><loc_{}>".format(class_name, x1, y1, x2, y2)

        # 将图片路径和标注列表添加到字典中
        jsons.append(
            {
                "prefix": "<OD>",
                "suffix": suffix,
                "image": image_path
            }
        )
    return jsons

chinese_2_english = {
    'fire': 'fire',
    'smoke': 'smoke',
    'niaochao': 'nest',
    'dxyw': 'foreign_object_wire',
    'dxyw_fz': 'kite_on_wire',
    'dxyw_lj': 'garbage_on_wire',
    'dxyw_qq': 'balloon_on_wire',
    'dxyw_yw': 'foreign_object_wire',
    'chanche': 'forklift',
    'tuituji': 'dozer',
    'dazhuangji': 'pile_driver',
    'fandouche': 'dump_truck',
    'youguanche': 'tanker_truck',
    'wajueji': 'excavator',
    'kache': 'truck',
    'jiaobanche': 'mixer_truck',
    'snbc': 'mixer_truck',
    'qizhongji': 'crane',
    'diaoche': 'crane',
    'tadiao': 'crane',
    'caigangwa': 'steel_tile',
    'fangchenwang': 'dust_net',
}

if __name__ == "__main__":
    xml_directory = '/data1/datasets/shudian/Annotations/'  # 替换为你的XML文件所在目录
    xml_files = []
    for xml_file in tqdm(os.listdir(xml_directory)):
        if xml_file.endswith('.xml'):
            xml_files.append(os.path.join(xml_directory, xml_file))
    print(f"find {len(xml_files)} xml")
    

    # 遍历所有的XML文件并转换
    jsons = xml_to_json(xml_files)

    print(f"find {len(jsons)} json")

    train_jsons = jsons[:int(0.9*len(jsons))]
    val_jsons = jsons[int(0.9*len(jsons)):]
    # 打开文件以写入 JSONL
    with open('od_datasets/train_set.jsonl', 'w', encoding='utf-8') as file:
        for obj in train_jsons:
            # 将字典转换为 JSON 字符串，并写入文件，每行一个 JSON 对象
            file.write(json.dumps(obj) + '\n')

    with open('od_datasets/val_set.jsonl', 'w', encoding='utf-8') as file:
        for obj in val_jsons:
            # 将字典转换为 JSON 字符串，并写入文件，每行一个 JSON 对象
            file.write(json.dumps(obj) + '\n')
    print("JSON转换完成并保存。")



