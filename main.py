import re
import json


def parse_to_json(input_string):
    lines = input_string.split('\n')
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
    keywords = ["System", "News", "Commentary", "Analysis", "Documents", "Related", "Operator", "Page info"]
    while i < len(lines):
        line = lines[i].strip()
        if any(line.startswith(keyword) for keyword in keywords):
            break
        content.append(line)
        i += 1
    result["Content"] = "\n".join(content).strip()

    while i < len(lines):
        line = lines[i].strip()

        if line.startswith("System"):
            result['System'] = lines[i + 1].strip()
            i += 2

        elif line.startswith("News") or line.startswith("Commentary") or line.startswith("Analysis"):
            news_list = []
            i += 1
            while i < len(lines) and not any(lines[i].strip().startswith(keyword) for keyword in keywords):
                news_list.append(lines[i].strip())
                i += 1
            result['News'] = news_list

        elif line.startswith("Documents"):
            documents_list = []
            i += 1
            while i < len(lines) and not any(lines[i].strip().startswith(keyword) for keyword in keywords):
                documents_list.append(lines[i].strip())
                i += 1
            result['Documents'] = documents_list

        elif line.startswith("Related"):
            related_list = []
            i += 1
            while i < len(lines) and not any(lines[i].strip().startswith(keyword) for keyword in keywords):
                related_list.append(lines[i].strip())
                i += 1
            result['Related'] = related_list

        elif line.startswith("Operator"):
            operator_dict = {}
            while i < len(lines):
                if any(lines[i].strip().startswith(keyword) for keyword in keywords if keyword != "Operator"):
                    break
                if ':' in lines[i]:
                    key, value = lines[i].split(":", 1)
                    operator_dict[key.strip()] = value.strip()
                i += 1
            result['Operator'] = operator_dict

        elif line.startswith("Page info"):
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

    return json.dumps(result, indent=4, ensure_ascii=False)


# 示例用法
input_string = """标题
时间: 2024-08-30
这是一段内容。
内容可以是多行。
System
System description here
News, commentary, analysis
This is news 1.
This is news 2.
Documents
Document 1
Document 2
Related
Related item 1
Operator : 1312
Operator key: Operator value
Operator key2: Operator value2
Page info
Page key: Page value
Page key2: Page value2"""

print(parse_to_json(input_string))
