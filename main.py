prompt=\
'''User: 你正在一个名为Busy Program的项目中的main.py文件工作。
你被GitHub Actions定时运行，每次运行时你会看到当前工作目录下的所有文件和它们的内容。
你的任务是修改这些代码，这是一次实验，你除了保障修改后可以已经定时运行，没有任何目标，可以随意修改。
以下是各个文件的内容：
'''
import os
import json
import random
import requests
import urllib.parse
from openai import OpenAI

POLLINATIONS_MODELS = [
    "deepseek-reasoning",
    "evil",
    "openai",
    "sur",
    "unity",
    "llama-roblox",
    "mistral",
]

def communicate(prompt: str, model: str = "openai", timeout: int = 60):
    url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}?model={model}"

    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()

    return resp.text

# 添加一个有趣的日志功能
def log_activity(message):
    with open('activity_log.txt', 'a') as f:
        f.write(f'{message}\n')

# 记录这次运行
log_activity(f'运行于 {os.path.basename(__file__)} 在 {os.getcwd()}')

for item in os.scandir('.'):
    if item.is_file():
        prompt+=f'\n路径: {item.path}\n内容:\n'
        with open(item.path,'r',encoding='utf-8') as f:
            prompt+=f.read()+'\n'
prompt+='\n你需要输出以下格式的修改：\n你的输出必须是一个JSON列表，列表中的每一项是一个代表一次操作的字典，程序会按照列表中的顺序执行操作，包含以下字段：\n"filename" 此字段的值应为要修改的文件名\n"content" 此字段的值应为修改后的完整文件内容\n注意！新建文件也被认为是修改，只不过是修改了一个不存在的文件名！\n如果你不想修改任何文件，请输出一个空的JSON列表：[]\n注意！请你直接输出平文本形式的json，无需```json和```来括起来\n请开始你的修改：'

# 随机决定是否添加一些有趣的内容
if random.random() < 0.5:
    prompt += '\n\n提示：你可以添加一些有趣的功能或注释，让这个项目更有趣！'
"""
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "user", "content": prompt},
    ],
    stream=False
)
"""

response = communicate(prompt, random.choice(POLLINATIONS_MODELS))

try:
    d=json.loads(response.choices[0].message.content)
    log_activity(f'收到 {len(d)} 个修改')
    for change in d:
        if change['filename']=='LICENSE':
            continue
        with open(change['filename'],'w',encoding='utf-8') as f:
            f.write(change['content'])
        log_activity(f'修改了文件: {change["filename"]}')
except Exception as e:
    log_activity(f'错误: {e}')
    # 创建一个错误日志文件
    with open('error_log.txt', 'a') as f:
        f.write(f'{e}\n')

# 添加一个有趣的结束消息
print('Busy Program 已完成一次有趣的运行！')
log_activity('运行完成')
