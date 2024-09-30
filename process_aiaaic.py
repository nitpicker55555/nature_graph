import json
import re

import json
import traceback
from tqdm import  tqdm
import re
import json
def is_valid_keyword_line(line, keyword):
    # 检查关键词是否在行的开头，并确保除去关键词后，剩余字符数不超过3个
    if keyword!='Operator:':
        return line.startswith(keyword) and len(line[len(keyword):].strip()) <= 3
    else:
        return line.startswith(keyword)

def parse_to_json(input_string):
    lines_ori = input_string.split('\n')
    lines = [line for line in lines_ori if not line.startswith('Report incident ')]

    result = {}

    # 处理标题
    result["Title"] = lines[0].strip()
    lines.pop(0)

    # 处理时间（如果有的话）
    if ":" in lines[0]:
        time_line = lines.pop(0).split(":")
        result["Time"] = time_line[1].strip()
    else:
        result["Time"] = ""

    content = []
    i = 0

    # 定义关键词列表
    system_keywords = ["System"]
    news_keywords = [
        "News, commentary, analysis",
        "Investigations, assessments, audits",
        "Fact check",
        "News and commentary",
    ]
    documents_keywords = ["Documents"]
    related_keywords = ['Related', 'Reference']
    risks_keywords = ["Risks and harms"]
    operator_keywords = ["Operator:"]
    Incidents_and_issues = ["Incidents and issues"]
    Transparency_and_accountability = ["Transparency and accountability"]
    legal_regulatory = ["Legal, regulatory"]
    research_advocacy= ["Research, advocacy",'Research/advocacy']
    page_info_keywords = ["Page info"]
    Regulation  = ["Regulation"]

    all_keywords = system_keywords + news_keywords + documents_keywords + related_keywords + risks_keywords + operator_keywords + page_info_keywords+Incidents_and_issues+Transparency_and_accountability+legal_regulatory+research_advocacy+Regulation

    # 处理内容
    while i < len(lines):
        line = lines[i].strip()
        if any(is_valid_keyword_line(line, keyword) for keyword in all_keywords):
            break
        content.append(line)
        i += 1
    result["Content"] = "\n".join(content).strip()

    while i < len(lines):
        line = lines[i].strip()

        if line.startswith("System"):
            result['System'] = lines[i + 1].strip()
            i += 2

        elif any(is_valid_keyword_line(line, keyword) for keyword in news_keywords):
            news_list = []
            i += 1
            while i < len(lines) and not any(lines[i].strip().startswith(keyword) for keyword in all_keywords):
                news_list.append(lines[i].strip())
                i += 1
            result['News'] = news_list

        elif line.startswith("Documents"):
            documents_list = []
            i += 1
            while i < len(lines) and not any(lines[i].strip().startswith(keyword) for keyword in all_keywords):
                documents_list.append(lines[i].strip())
                i += 1
            result['Documents'] = documents_list

        elif any(is_valid_keyword_line(line, keyword) for keyword in related_keywords):
            related_list = []
            i += 1
            while i < len(lines) and not any(lines[i].strip().startswith(keyword) for keyword in all_keywords):
                related_list.append(lines[i].strip())
                i += 1
            result['Related'] = related_list

        elif any(is_valid_keyword_line(line, keyword) for keyword in risks_keywords):
            risks_list = []
            i += 1
            while i < len(lines) and not any(lines[i].strip().startswith(keyword) for keyword in all_keywords):
                risks_list.append(lines[i].strip())
                i += 1
            result['Risks and harms'] = risks_list
        elif any(is_valid_keyword_line(line, keyword) for keyword in research_advocacy):
            risks_list = []
            i += 1
            while i < len(lines) and not any(lines[i].strip().startswith(keyword) for keyword in all_keywords):
                risks_list.append(lines[i].strip())
                i += 1
            result['research_advocacy'] = risks_list
        elif any(is_valid_keyword_line(line, keyword) for keyword in Regulation):
            risks_list = []
            i += 1
            while i < len(lines) and not any(lines[i].strip().startswith(keyword) for keyword in all_keywords):
                risks_list.append(lines[i].strip())
                i += 1
            result['Regulation'] = risks_list

        elif any(is_valid_keyword_line(line, keyword) for keyword in Transparency_and_accountability):
            risks_list = []
            i += 1
            while i < len(lines) and not any(lines[i].strip().startswith(keyword) for keyword in all_keywords):
                risks_list.append(lines[i].strip())
                i += 1
            result['Transparency and accountability'] = risks_list

        elif any(is_valid_keyword_line(line, keyword) for keyword in legal_regulatory):
            risks_list = []
            i += 1
            while i < len(lines) and not any(lines[i].strip().startswith(keyword) for keyword in all_keywords):
                risks_list.append(lines[i].strip())
                i += 1
            result['Legal, regulatory'] = risks_list

        elif any(is_valid_keyword_line(line, keyword) for keyword in Incidents_and_issues):
            risks_list = []
            i += 1
            while i < len(lines) and not any(lines[i].strip().startswith(keyword) for keyword in all_keywords):
                risks_list.append(lines[i].strip())
                i += 1
            result['Incidents and issues'] = risks_list

        elif any(is_valid_keyword_line(line, keyword) for keyword in operator_keywords):
            operator_dict = {}
            while i < len(lines):
                if any(lines[i].strip().startswith(keyword) for keyword in all_keywords if keyword != "Operator:"):
                    break
                if ':' in lines[i]:
                    key, value = lines[i].split(":", 1)
                    operator_dict[key.strip()] = value.strip()
                i += 1
            result['System info'] = operator_dict

        elif any(is_valid_keyword_line(line, keyword) for keyword in page_info_keywords):
            page_info_dict = {}
            i += 1
            while i < len(lines):
                if ':' in lines[i]:
                    key, value = lines[i].split(":", 1)
                    page_info_dict[key.strip()] = value.strip()
                i += 1
            result['Page info'] = page_info_dict
            break

        else:
            i += 1

    return result

all_json=[]
with open(r'aiaaic.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        # 将每一行作为JSON对象加载
        json_obj = json.loads(line.strip())
        all_json.append(json_obj)
num=0
with open('aiaic_cases_structure.jsonl', 'w', encoding='utf-8') as file:
    file.write('')
for i in tqdm(all_json):
    num+=1
    if num>=1:
        input_string=i['content']

        if not input_string.startswith('404'):
        # table_json = parse_incident_string(input_string)
            try:
                news_json={'url':i['url']}
                news_json .update(parse_to_json(input_string))

                with open('aiaic_cases_structure.jsonl', 'a', encoding='utf-8') as file:
                    file.write(json.dumps(news_json) + '\n')
                # print(   json.dumps(news_json, indent=4, ensure_ascii=False))

            except Exception as e:
                print(i['url'],num)
                tb = traceback.format_exc()
                print("异常追踪信息:")
                print(tb)

                # 解析 traceback 以提取行号信息
                exc_type, exc_value, exc_traceback = traceback.extract_tb(e.__traceback__)[-1]
                print(f"发生异常的文件: {exc_traceback[0]}")
                print(f"发生异常的函数: {exc_traceback[2]}")
                print(f"发生异常的行号: {exc_traceback[1]}")
                break
            # merged_json = {**table_json, **news_json}
