import json
from collections import defaultdict

# 定义文件名
filename = 'aiaic_cases_structure.jsonl'

# 使用 defaultdict 初始化一个字典来记录出现的次数
harmed_parties_count = defaultdict(int)
print(harmed_parties_count)
# 打开并逐行读取文件
num=0
with open(filename, 'r', encoding='utf-8') as file:
    for line in file:
        num+=1
        try:
            # 将每一行转换为JSON对象
            json_obj = json.loads(line)

            # 检查 'ALLEGED HARMED OR NEARLY HARMED PARTIES' 键是否存在

                # 获取对应的值
            if 'System info' in json_obj:
                harmed_parties = json_obj['System info']['Issue']

            # 将该值作为键，计数 +1+
                if '; ' in harmed_parties:
                    for each_label in str(harmed_parties).split('; '):
                        harmed_parties_count[each_label] += 1
                else:
                    harmed_parties_count[harmed_parties] += 1
            else:
                print(json_obj['url'])
                num+=1

        except json.JSONDecodeError:
            print("Invalid JSON format.")
sorted_harmed_parties_count = sorted(harmed_parties_count.items(), key=lambda x: x[1], reverse=True)


for party, count in sorted_harmed_parties_count:
    print(f"{party}: {count}")
print(num)
