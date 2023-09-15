import requests
from bs4 import BeautifulSoup

# 定义洛谷题目列表页面的URL
url = 'https://www.luogu.com.cn/problem/list?page=1&_contentOnly=1'

# 发送HTTP请求获取页面内容
response = requests.get(url)

# 解析页面内容
soup = BeautifulSoup(response.content, 'html.parser')

# 获取前50道题目的信息
problems = soup.find_all('div', class_='problem')

# 创建一个Markdown格式的文本
markdown_text = "# 洛谷前50道题目\n\n"

for problem in problems[:50]:
    # 获取题目标题
    title = problem.find('span', class_='problem-title').text.strip()
    
    # 获取题目难度级别
    difficulty = problem.find('span', class_='mdui-color-theme').text.strip()
    
    # 获取题目关键词
    keywords = problem.find('span', class_='mdui-m-r-2').text.strip()
    
    # 构建Markdown格式的信息
    markdown_text += f"## {title}\n\n"
    markdown_text += f"**难度级别:** {difficulty}\n\n"
    markdown_text += f"**关键词:** {keywords}\n\n"

# 将Markdown文本保存为本地文件
with open('luogu_problems.md', 'w', encoding='utf-8') as file:
    file.write(markdown_text)

print("爬取完成并保存为Markdown文件：luogu_problems.md")