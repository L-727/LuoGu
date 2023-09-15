import re
import urllib.request,urllib.error
import bs4
import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import unquote 
import json 
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# URL of the Luogu login page
url = "https://www.luogu.com.cn/auth/login"
driver = webdriver.Edge('I:\edgedrive\msedgedriver.exe')
# Initialize a WebDriver (you need to have a compatible driver installed, e.g., ChromeDriver)
#driver = webdriver.Edge()

driver.get(url)
# 打开登录界面


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

#题目+题解
baseUrl = "https://www.luogu.com.cn/problem/P"
baseUrl1 = "https://www.luogu.com.cn/problem/solution/P"
savePath = "I:\\luogu\\Problem"
unquote(baseUrl1)
#请求载体的身份标识
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
}
#发起请求
response = requests.get(baseUrl, headers=headers)

minn = 1002
maxn = 1003        #最大题号

def main():   
    print("计划爬取到P{}".format(maxn))
    for i in range(minn,maxn+1):
        time.sleep(1)
        print("正在爬取P{}...".format(i),end="")
        html = getHTML(baseUrl + str(i))
        if html == "error":
            print("题目爬取失败，可能是不存在该题或无权查看")
        else:
            problemMD,title = getMD(html)
            print("题目爬取成功！正在保存...",end="")
            filename = "P" + str(i)
            saveData(problemMD,filename,title)
            print("题目保存成功!")
        html1 = getHTML(baseUrl1 + str(i))
        if html1 == "error":
            print("题解爬取失败，可能是不存在该解或无权查看")
        else:
            text,code = extract_text_and_code(html1)
            markdown = convert_to_markdown(text,code)
            print("题解爬取成功！正在保存...",end="")
            filename1 = "P" + str(i)
            saveData(markdown,filename1,"题解")
            print("题解保存成功!")
    print("爬取完毕")

# 从HTML中提取文本和代码
def extract_text_and_code(html):
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('div', class_='marked')
    if div is None:
        return None, None
    text = div.get_text().strip()
    pre_code = div.find('pre')
    if pre_code is None:
        return text, None
    code = pre_code.find('code').get_text().strip()
    return text, code

# 将文本和代码转换为Markdown格式
def convert_to_markdown(text, code):
    if text is None:
        return ""
    markdown = f"{text}\n\n```cpp\n{code}\n```" if code else text
    return markdown

def getHTML(url):
    headers = {
        "user-agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 85.0.4183.121 Safari / 537.36"
    }
    request = urllib.request.Request(url = url,headers = headers)
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf-8')
    if str(html).find("Exception") == -1:        #洛谷中没找到该题目或无权查看的提示网页中会有该字样
        return html
    else:
        return "error"

def getMD(html):
    bs = bs4.BeautifulSoup(html,"html.parser")
    core = bs.select("article")[0]
    h1_tag = bs.find("h1")  # 查找第一个出现的<h1>标签

    if h1_tag:
        title_span = h1_tag.find("span", attrs={"title": True})  # 在<h1>标签内查找具有title属性的<span>标签
        if title_span:
            title_text = title_span.text.strip()  # 提取<span>标签内的文本并去除首尾空格
        else:
            title_text = "Unknown"
    else:
        title_text = "No <h1> tag found"
    md = str(core)
    md = re.sub("<h1>","# ",md)
    md = re.sub("<h2>","## ",md)
    md = re.sub("<h3>","#### ",md)
    md = re.sub("</?[a-zA-Z]+[^<>]*>","",md)
    return md,title_text

def saveData(data, filename, title):
    cfilename = savePath + filename + "-" + title + ".md"
    file = open(cfilename, "w", encoding="utf-8")
    for d in data:
        file.writelines(d)
    file.close()

if __name__ == '__main__':
    main()


