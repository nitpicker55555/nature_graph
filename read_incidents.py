import json
from collections import defaultdict

# 定义文件名
filename = 'incidents_cases_structure.jsonl'


# 打开并逐行读取文件
with open(filename, 'r', encoding='utf-8') as file:
    for line in file:
        try:
            # 将每一行转换为JSON对象
            json_obj = json.loads(line)
            print(json_obj['Content'])
        except:
            pass

