import json
import re

indexs=[]
indexs2=[]
all_=[]
def list_to_jsonl(data, output_file=None):
    jsonl_lines = []
    for item in data:
        # 将列表中的每个元素转换为 JSON 格式字符串
        jsonl_line = json.dumps(item, ensure_ascii=False)
        jsonl_lines.append(jsonl_line)

    # 如果指定了输出文件，将结果写入文件
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            for line in jsonl_lines:
                f.write(line + '\n')
    else:
        # 如果没有指定输出文件，返回所有行的字符串表示
        return '\n'.join(jsonl_lines)
# 读取jsonl文件
with open('incidents_cases.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        # 将每一行作为JSON对象加载
        json_obj = json.loads(line.strip())
        # if int(list(json_obj.keys())[0]) not in {512, 130, 269, 237, 365, 442, 338, 342, 247, 90, 542}:
        #     all_.append(json_obj)

        indexs.append(int(list(json_obj.keys())[0]))
print(len(indexs))
# list_to_jsonl(all_,'incidents_cases.jsonl')
def extract_numbers(string):
    # 使用正则表达式查找字符串中的所有数字
    numbers = re.findall(r'\d+', string)
    # 将找到的数字字符串转换为整数列表
    return [int(num) for num in numbers][0]
def non_intersecting_elements(list1, list2):
    # 使用集合操作找出只在list1或list2中出现的元素
    set1 = set(list1)
    set2 = set(list2)

    # 找到list1中不在list2中的元素
    unique_to_list1 = set1 - set2
    print(unique_to_list1)
    # 找到list2中不在list1中的元素
    unique_to_list2 = set2 - set1
    print(unique_to_list2)
    # 将两个集合合并并转换为列表返回
    # non_intersecting = list(unique_to_list1.union(unique_to_list2))

    # return non_intersecting
with open('incidents_table.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        # 将每一行作为JSON对象加载
        json_obj = json.loads(line.strip())
        indexs2.append(extract_numbers(json_obj["INCIDENT ID"]))

print(len(indexs2))
# print(non_intersecting_elements(indexs,indexs2))