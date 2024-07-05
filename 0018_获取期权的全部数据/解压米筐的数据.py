import pickle
import os

data_root = "E:\\data\\米筐\\米筐1分钟数据-1个品种一个文件\\"
file_list = list(os.listdir(data_root))
for file_name in file_list:
    file_path = os.path.join(data_root, file_name)
    with open(file_path, 'rb') as f:
        data = pickle.load(f)
        for key, value in data.items():
            value.to_csv(data_root + key + '.csv')
            print(f"{key}解压完成")
        # print(type(data))
        # print(len(data))
