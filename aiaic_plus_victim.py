import json
from collections import defaultdict
from chat_py import *
# 定义文件名
filename = 'aiaic_cases_structure.jsonl'
from tqdm import tqdm
# 使用 defaultdict 初始化一个字典来记录出现的次数
harmed_parties_count = defaultdict(int)
print(harmed_parties_count)
# 打开并逐行读取文件
num=0
json_list=[]
messages = []
system_prompt="""Based on the given news information, identify which entity's interests have been harmed in this 
news. Please output the type of entity or profession, not specific names or uncommon nouns, and format the response 
in JSON: {"victim"} """
with open(filename, 'r', encoding='utf-8') as file:
    for line in tqdm(file):
            num+=1
            if num>=1:

                    # 将每一行转换为JSON对象
                    json_obj = json.loads(line)
                    content=json_obj['Content']

                    messages.append(message_template('system',system_prompt))
                    messages.append(message_template('user',content))
                    result=json.loads(chat_single(messages,'json'))

                    with open('aiaic_victim.jsonl', 'a', encoding='utf-8') as f:
                        f.write(json.dumps(result) + '\n')
                    # print(result)
                    # print(result['first class'])
                    # break
