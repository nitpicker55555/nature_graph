import json


def get_nested_value(data, key_path):
    keys = key_path.split('.')
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return None
    return data


def find_matching_keys(jsonl_file1, jsonl_file2, key1, key2):
    matching_items = []

    # 读取第一个 JSONL 文件并存储指定键路径对应的键值
    with open(jsonl_file1, 'r', encoding='utf-8') as file1:
        data1 = [json.loads(line) for line in file1]
        values1 = set()
        for item in data1:
            value = get_nested_value(item, key1)
            if value is not None:
                # 将逗号分隔的值分成独立的部分
                values1.update([v.strip() for v in value.split(',')])

    # 读取第二个 JSONL 文件，检查是否有匹配的键值
    with open(jsonl_file2, 'r', encoding='utf-8') as file2:
        data2 = [json.loads(line) for line in file2]
        for item in data2:
            value2 = get_nested_value(item, key2)
            if value2 is not None:
                # 检查 value2 是否包含在 values1 中的任何一个值
                if any(v in value2 for v in values1):
                    matching_items.append(item)

    return matching_items


# 使用示例
key1s=["CSETv0 Taxonomy Classifications.Technology Purveyor",'CSETv0 Taxonomy Classifications.System Developer']
key2="System info.Developer"
for key1 in key1s:
    matching_results = find_matching_keys(r'C:\Users\Morning\Desktop\hiwi\nature_gra[ph\aiaic_cases_structure.jsonl', r'C:\Users\Morning\Desktop\hiwi\nature_gra[ph\incidents_cases_structure.jsonl',key2, key1 )
    for result in matching_results:
        print(result)
