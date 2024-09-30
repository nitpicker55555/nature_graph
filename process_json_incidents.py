import json
import re


def parse_incident_string(input_string):
    input_string=input_string.replace("Responded\n",'')
    # 初始化结果字典
    result = {}

    # 按行分割输入字符串，并去除可能的空行
    lines = [line.strip() for line in input_string.strip().split("\n") if line.strip()]

    if len(lines) < 2:
        raise ValueError("输入字符串格式不正确，至少需要两行。")

    # 解析第一行:index 和 topic
    first_line = lines[0].strip()
    index, topic = first_line.split(":", 1)  # 分割第一个冒号
    result["index"] = int(index.split()[-1])  # 获取index的数字部分
    result["topic"] = topic.strip()

    # 解析第二行:description
    second_line = lines[1]
    match = re.match(r"description\s*:\s*(.+)", second_line, re.IGNORECASE)
    if not match:
        raise ValueError("第二行格式不正确，应为 'description:string'。")
    result["description"] = match.group(1).strip()

    # 寻找"Incident Stats"到"Incident Reports"之间的部分
    try:
        start_idx = lines.index("Incident Stats") + 1
    except ValueError:
        raise ValueError("未找到 'Incident Stats' 行。")

    try:
        end_idx = lines.index("Incident Reports")
    except ValueError:
        end_idx = len(lines)

    stats_lines = lines[start_idx:end_idx]

    # 初始化解析状态
    current_table = "Incident Stats"  # 默认第一个表格
    result[current_table] = {}
    result_tables = {current_table: result[current_table]}

    previous_label = None  # 用于处理值的延续
    expecting_value = True if current_table == "Incident Stats" else False

    # 用于捕捉表头
    i = 0
    while i < len(stats_lines):
        line = stats_lines[i]

        # 检查是否是"Show Fewer Classifications"，跳过
        if line == "Show Fewer Classifications":
            i += 1
            continue

        # 检查是否是"Taxonomy Details"
        if line == "Taxonomy Details":
            if i == 0:
                raise ValueError("'Taxonomy Details' 之前没有表头。")
            # 前一行是表头
            table_header = stats_lines[i - 1]
            current_table = table_header
            if current_table not in result:
                result[current_table] = {}
            result_tables[current_table] = result[current_table]
            expecting_value = False  # 切换到标签状态
            previous_label = None
            i += 1
            continue

        # 如果是表头且不是"Incident Stats"或被"Taxonomy Details"标识，可能需要处理
        # 但根据当前规则，表头由"Taxonomy Details"标识，所以这里不处理

        # 根据当前表格类型处理
        if current_table == "Incident Stats":
            # Incident Stats 中标签和值交替
            if expecting_value:
                # 当前行是值
                label = line
                previous_label = label
                expecting_value = False

            else:
                # 当前行是标签
                value = line
                result_tables[current_table][previous_label] = value
                expecting_value = True
        else:
            # 其他表格中标签和值交替，但需要处理值的延续
            if expecting_value:
                # 当前行是值，可能有延续
                value = line
                # 检查下一行是否是值的延续（包含英文标点）
                j = i + 1
                while j < len(stats_lines):
                    next_line = stats_lines[j]
                    if re.search(r"[.,!?;:]", next_line):
                        value += " " + next_line
                        j += 1
                        i = j - 1  # 更新主循环的i
                    else:
                        break
                result_tables[current_table][previous_label] = value
                expecting_value = False
            else:
                # 当前行是标签
                label = line
                previous_label = label
                expecting_value = True

        i += 1

    return result


import json

import json

def is_url(string):
    # 定义一个匹配URL的正则表达式
    if ' · ' not in string:
        return False
    string=string.split(" · ")[0]
    url_pattern = re.compile(
        r'^(https?:\/\/)?'  # 匹配http://或https://（可选）
        r'([a-zA-Z0-9.-]+)?'  # 匹配www.或其他域名前缀（可选）
        r'([a-zA-Z0-9-]+\.[a-zA-Z]{2,})'  # 匹配主域名（如example.com）
        r'(:\d+)?'  # 匹配端口号（可选）
        r'(\/[^\s]*)?$'  # 匹配路径及参数（可选）
    )
    return re.match(url_pattern, string) is not None
def parse_news_to_json(input_string):
    lines = input_string.split('\n')
    news_list = []
    i = 0
    while i < len(lines):
        # 找到第一个 Collapse 行
        if 'Collapse' in lines[i]:
            # 找到 Collapse 行前的第一个 .com 行
            j = i - 1
            while j >= 0 and not is_url(lines[j]):
                j -= 1

            if j >= 1:  # 确保有足够的行来找到标题和地址
                address = lines[j]
                title = lines[j - 1]

                # 获取 content
                content_lines = []
                k = j + 1
                while k < i:  # i 是当前 Collapse 行的位置
                    content_lines.append(lines[k])
                    k += 1

                content = "\n".join(content_lines).strip()

                # 将新闻单元加入列表
                news_list.append({
                    "title": title,
                    "address": address,
                    "content": content
                })

                # 跳过已经处理的部分，i 跳到 Collapse 行的下一行
                i += 1
                continue

        i += 1

    return {"news": news_list}

all_json=[]
with open(r'results2.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        # 将每一行作为JSON对象加载
        json_obj = json.loads(line.strip())
        all_json.append(json_obj)
num=0
for i in all_json:
    input_string=list(i.values())[0]
    if not str(input_string).startswith('Citation record for Incident') :
        num+=1
        try:
            table_json = parse_incident_string(input_string)
        except:
            print(input_string)
            break
        news_json = parse_news_to_json(input_string)
        merged_json = {**table_json, **news_json}
        with open('incidents_cases_structure.jsonl', 'a', encoding='utf-8') as file:
            file.write(json.dumps(merged_json) + '\n')
        # print(json.dumps(merged_json, ensure_ascii=False, indent=4))
print(num)