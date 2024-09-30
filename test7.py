from test8 import *
from test9 import *

full_num=0
no_duplicate=[]
not_include=[]
from collections import defaultdict

def find_common_elements(json_data):
    # 创建一个字典，用于存储元素和它们对应的键名
    element_to_keys = defaultdict(list)

    # 遍历 JSON 数据的键值对
    for key, value_list in json_data.items():
        for element in value_list:
            # 将元素与它对应的键关联
            element_to_keys[element].append(key)

    # 过滤出那些出现在多个键下的元素
    common_elements = {element: keys for element, keys in element_to_keys.items() if len(keys) > 1}

    return common_elements


def unique_elements(list1, list2):
    # 将list1中的带逗号的元素断开，并将它们加入新的列表
    new_list2 = []
    for item in list2:
        if ',' in item:
            # 将带逗号的元素按逗号分割，并去除前后空格后加入新列表
            new_list2.extend([i.strip() for i in item.split(',')])
        else:
            new_list2.append(item)
    new_list1 = []
    for item in list1:
        if ',' in item:
            # 将带逗号的元素按逗号分割，并去除前后空格后加入新列表
            new_list1.extend([i.strip() for i in item.split(',')])
        else:
            new_list1.append(item)
    print('隔断后 已有',len(new_list1))
    print('隔断后 本有',len(new_list2))

    # 将两个列表转换为集合，利用集合的差集找出不重复的元素
    # unique_in_list1 = set(new_list1) - set(new_list2)
    unique_in_list2 = set(new_list2) - set(new_list1)

    # 合并两个差集的结果
    result = unique_in_list2
    print('not ',len(result))
    result.remove('Brian Hood')
    result.remove('David Harris')
    result.remove('Jonathan Turley')
    return result
def merge_json_lists(json1, json2):
    # 创建一个新的字典用于存储合并结果
    merged_json = {}

    # 遍历第一个 JSON 的键值对
    for key, value in json1.items():
        if key in json2:
            # 如果两个 JSON 中有相同的键，合并两个列表并去重
            merged_json[key] = list(set(value + json2[key]))
        else:
            # 如果键只存在于第一个 JSON 中，直接加入结果
            merged_json[key] = value

    # 处理第二个 JSON 中只存在于它自身的键
    for key, value in json2.items():
        if key not in merged_json:
            merged_json[key] = value

    return merged_json

# issues_incidents_json_combined=victim_incidents_json
issues_incidents_json_combined=merge_json_lists(victim_incidents_json,victim_incidents_json_new)
ori_json=victim_incidents
for i in issues_incidents_json_combined:
    for ii in issues_incidents_json_combined[i]:
        if ii in ori_json and ii not in no_duplicate:
            no_duplicate.append(ii)

    # full_num+=len(issues_incidents_json[i])
print(len(ori_json))
print(len(no_duplicate))
print("not classified ",unique_elements(no_duplicate,ori_json))

print((list(issues_incidents_json_combined.keys())))
print(issues_incidents_json_combined)
print(find_common_elements(issues_incidents_json_combined))

