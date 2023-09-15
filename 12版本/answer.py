import re
import urllib.request,urllib.error
import bs4
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PIL import Image
import pytesseract
import os
import markdown

T_base_url = "https://www.luogu.com.cn/problem/solution/P%s"
start_suffix = 1011  # 递增后缀的起始值
end_suffix = 1011  # 递增后缀的结束值 # <a data-v-0640126c data-v-258e49ac <span data-v-258e49ac data-v-0640126c>登录</span>
content_list = []

url = 'https://www.luogu.com.cn/auth/login'# 

def save_to_markdown(content_list, output_file):
    markdown_text = ''
    for content in content_list:
        if content['type'] == 'text':
            markdown_text += '<p>' + content['text'] + '</p>\n\n'
        elif content['type'] == 'code':
            markdown_text += '```' + content['code'] + '\n```\n\n'

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(markdown_text)


driver = webdriver.Edge()

# 打开登录界面
driver.get(url)

# 定义等待时间
wait = WebDriverWait(driver, 5)

# 循环等待用户登录成功
while True:
    try:
        # 在此处执行登录操作，例如输入用户名和密码，点击登录按钮
        
        # 在登录操作完成后，等待登录按钮消失
        wait.until(EC.invisibility_of_element_located((By.XPATH, "//span[contains(text(), '登录')]")))
        
        # 登录成功，退出循环
        break
    except:
        # 捕捉异常，继续等待用户登录
        continue

for suffix in range(start_suffix, end_suffix + 1):
    # 构建当前网页的URL
    T_url = T_base_url % suffix
    # <div data-v-7ce0c448 data-v-6906cdde class="marked" data-v-7f3c782d>…</div>
    # 反爬机制
    headers = {
        "Cookie":"client_id=98cfc2cc86d451827cf762d426dc1b5e5551a763; login_referer=https%3A%2F%2Fwww.luogu.com.cn%2Fproblem%2FP1000; _uid=561385",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    driver.get(T_url)
    
    # 将以下代码进行修改
    div_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.marked')))

    # 修改循环以处理单个 div_element
    children = div_element.find_elements(By.XPATH, './*')

    # 初始化文本内容和代码内容
    text_content = ''
    code_content = ''

    # <h1 data-v-2dfcfd35 class="lfe-h1">P1000 超级玛丽游戏 题解</h1>
    # 遍历子元素，将<pre>部分作为代码段，其他部分作为文本
    for child in children:
        if child.tag_name == 'p':
            text_content = child.text + '\n'
            content_list.append({'type': 'text', 'text': '<p>' + text_content.strip() + '</p>'})
        else:
            code_content = child.text + '\n'
            content_list.append({'type': 'code', 'language': 'cpp', 'code': code_content.strip()})

    
    # 查找class为"lfe-h1"的h1元素<h1 data-v-2dfcfd35 class="lfe-h1">P1000 超级玛丽游戏 题解</h1>
    h1_element = driver.find_element(By.XPATH, "//h1[@class='lfe-h1']")

    # 获取文本内容
    text_content = h1_element.text

    # 找到第一个和最后一个空格的位置
    first_space_index = text_content.index(" ")
    last_space_index = text_content.rindex(" ")

    # 替换第一个和最后一个空格为连字符
    text_content = text_content[:first_space_index] + "-" + text_content[first_space_index + 1:last_space_index] + "-" + text_content[last_space_index + 1:]
    
    filename = text_content

    #将所有"-"变成【空格】
    text_content = text_content.replace("-", " ")

    # 在第一个空格前添加连字符
    parts = text_content.split(" ", 1)  # 将文本按照第一个空格分割为两部分
    text_content = "-".join(parts)  # 将两部分用连字符连接起来    
    
    #  print(text_content)

    # 去掉最后三个字符（-题解）
    text_content = text_content[:-3]
    # 获取桌面路径
    #desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    desktop_path = os.path.join("I:\\luogu")
    folder_path = os.path.join(desktop_path, "题库", f"{text_content}")
    output_file = os.path.join(folder_path, filename + ".md")
    print("P",suffix-start_suffix,"-题解爬取成功")
    save_to_markdown(content_list, output_file)
   
# 关闭 WebDriver
driver.quit()