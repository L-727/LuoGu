import json   
import re   
import urllib.parse  
import bs4   
import requests  
import os  
  # 定义题目的URL  
problemUrl = "https://www.luogu.com.cn/problem/"  
# 定义题解的URL  
solutionUrl = "https://www.luogu.com.cn/problem/solution/"  
  
# 定义User Agent，用于模拟浏览器访问网页  
userAgent02 = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 SLBrowser/8.0.1.4031 SLBChan/103"  
userAgent01 = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 " \
            "Safari/537.36 Edg/116.0.1938.76 "
  
# 定义请求头，包括User Agent和cookie  
headers = {  
    "user-agent": userAgent02,  
    "cookie": "__client_id=d670d45cce0e21ad3e7f30f352487ddb8028277b; _uid=1086745"  
}  
  
# 定义保存文件的路径  
savePath = "I:\\luogu1\\"  
  
# 定义默认难度  
defaultDifficulty = ""  
  
# 定义需要排除的字符  
exclude = ["\\", '/', ':', '*', '?', '"', '>', '<', '|']  
  
# 通过pid获取题目和题解的函数定义  
def getProblem(pid, title, d, tags, k):  
    # 拼接目录名  
    fatherDir = d  
    for i in tags:  
        fatherDir += '-'  
        fatherDir += i  
    if k != '':  
        fatherDir += "-"  
        fatherDir += k  
    if pid <str('P1000') or pid >str('P1050'):  
        return "error" 
    # 获取题目内容  
    result = getProblemDetail(pid, title, fatherDir)  
    if result == "error":  
        return "error"  
  
    # 获取题解内容  
    getSolutionDetail(pid, title, fatherDir)  
    print("{}爬取完毕！".format(pid))  
  
# 获取题目内容的函数定义  
def getProblemDetail(pid, title, fatherDir):  
    print("正在爬取{}的题目...".format(pid), end="")  
    if pid <str('P1000') or pid >str('P1050'):  
        return "error" 
    problemHtml = getHTML(problemUrl + str(pid))  # 获取题目页面的HTML内容  
    if problemHtml == "error":  # 如果获取失败，打印错误信息并返回  
        print("爬取失败，可能是不存在该题或无权查看")  
        return "error"  
    else:  # 如果获取成功，解析HTML并保存到本地  
        problemMD = getMD(problemHtml, "problem")  # 解析HTML，得到题目内容  
        print("爬取成功！正在保存...", end="")  
        dirName = pid + '-' + title  # 定义文件名和目录名  
        fileName = dirName + ".md"  # 定义文件名和文件路径  
        saveData(problemMD, dirName, fileName, fatherDir)  # 保存文件到本地  
        print("保存成功!")  
# 通过pid获取题目和题解的函数定义  
def getSolutionDetail(pid, title, fatherDir):  
    print("正在爬取{}的题解...".format(pid), end="")  # 打印正在爬取的提示信息  
    solutionHtml = getHTML(solutionUrl + str(pid))  # 获取题解页面的HTML内容  
    if solutionHtml == "error":  # 如果获取失败，打印错误信息并返回  
        print("P1050以内符合要求的所以题目已经爬取") 
        return "error" 
         
    else:  # 如果获取成功，解析HTML并保存到本地  
        solutionMD = getMD(solutionHtml, "solution")  # 解析HTML，得到题解内容  
        print("爬取成功！正在保存...", end="")  # 打印爬取成功的提示信息  
        dirName = pid + '-' + title  # 定义文件名和目录名  
        fileName = dirName + "-题解.md"  # 定义文件名和文件路径  
        saveData(solutionMD, dirName, fileName, fatherDir)  # 保存文件到本地  
        print("保存成功!")  # 打印保存成功的提示信息  
  
# 发送GET请求获取HTML内容的函数定义  
def getHTML(url):  
    res = requests.get(url, headers=headers)  # 发送GET请求，并携带自定义的请求头  
    html = res.text  # 获取响应的文本内容  
    if str(html).find("Exception") == -1:  # 如果文本内容中不包含"Exception"字符串，则返回HTML内容  
        return html  
    else:  # 如果文本内容中包含"Exception"字符串，则返回错误信息  
        return "error"  
  
# 解析html获取markdown文本的函数定义  
def getMD(html, type):  
    bs = bs4.BeautifulSoup(html, "html.parser")  # 使用BeautifulSoup库解析HTML内容  
    if type == "problem":  # 如果解析的是题目内容  
        core = bs.select("article")[0]  # 选择HTML中的"article"标签的内容  
        md = str(core)  # 将选中的内容转换为字符串  
        md = re.sub("<h1>", "# ", md)  # 使用正则表达式替换字符串中的"<h1>"为"# "，实现将H1标签转换为Markdown格式  
        md = re.sub("<h2>", "## ", md)  # 使用正则表达式替换字符串中的"<h2>"为"## "，实现将H2标签转换为Markdown格式  
        md = re.sub("<h3>", "#### ", md)  # 使用正则表达式替换字符串中的"<h3>"为"#### "，实现将H3标签转换为Markdown格式  
        md = re.sub("</?[a-zA-Z]+[^<>]*>", "", md)  # 使用正则表达式替换字符串中的HTML标签为空字符串，实现去除HTML标签  
        return md  # 返回转换后的Markdown字符串  
    if type == "solution":  # 如果解析的是题解内容  
        core = bs.select("script")[0]  # 选择HTML中的"script"标签的内容  
        script = str(core)  # 将选中的内容转换为字符串  
        index1 = script.index('"')  # 查找字符串中的第一个双引号的位置  
        index2 = script.index('"', index1 + 1)  # 查找字符串中的第二个双引号的位置  
        script = script[index1 + 1: index2]  # 截取两个双引号之间的内容  
        decodedStr = urllib.parse.unquote(script)  # 使用urllib库解码URL编码的字符串  
        map1 = json.loads(decodedStr)  # 将解码后的字符串转换为JSON对象  
        solutions = map1["currentData"]["solutions"]["result"]  # 获取JSON对象中的题解内容  
        if len(solutions) > 0:  # 如果题解内容不为空  
            bestSolution = solutions[0]  # 获取第一个题解内容  
            md = bestSolution["content"]  # 获取题解内容的文本部分  
            return md  # 返回题解的Markdown字符串  
        return "Sorry, there is no solution"  # 如果题解内容为空，返回错误信息  

# 定义保存数据的函数  
def saveData(data, dirName, fileName, fatherDir):  
    # 规范目录或文件名（去掉不合法字符）  
    dirName = cleanFileOrDirName(dirName)  
    fileName = cleanFileOrDirName(fileName)  
    fatherDir = cleanFileOrDirName(fatherDir)  
  
    dirPath = savePath + fatherDir + "\\" + dirName  # 构造目录路径  
    filePath = dirPath + "\\" + fileName  # 构造文件路径  
  
    # 判断目录是否存在，如果不存在则创建目录  
    # 判断是否存在文件夹  
    if not os.path.exists(dirPath):  
        os.makedirs(dirPath)  
  
    # 创建文件并写入数据  
    # 创建文件并写入  
    file = open(filePath, "w", encoding="utf-8")  
    for d in data:  # 遍历要保存的数据  
        file.writelines(d)  # 将数据写入文件  
    file.close()  # 关闭文件  
  
# 定义规范文件名或目录名的函数  
def cleanFileOrDirName(name):  
    result = str(name)  # 将输入转换为字符串  
    for i in exclude:  # 遍历需要排除的字符列表  
        result = result.replace(i, "")  # 将字符串中的这些字符替换为空字符串，即删除这些字符  
    return result  # 返回处理后的字符串

if __name__ == "__main__":
    getProblem("P1001", "数独", "入门", ["字符串"], "hello")