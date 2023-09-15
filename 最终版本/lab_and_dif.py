import requests  
import json  
  # 定义一个空字典
tag = {}  
# 定义一个字典，将难度等级映射为数值，便于后续请求中使用  
difficultyMap = {"无选择": -1, "暂无评定": 0, "入门": 1, "普及-": 2, "普及/提高-": 3, "普及+/提高": 4, "提高+/省选-": 5, "省选/NOI-": 6, "NOI/NOI+/CTSC": 7}  
# 定义请求的URL，这是洛谷的题目列表接口  
reqUrl = "https://www.luogu.com.cn/problem/list"  
# 定义两个用户代理，用于模拟浏览器行为，防止被服务器识别为爬虫  
userAgent01 = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 " \
            "Safari/537.36 Edg/116.0.1938.76 "
userAgent02 = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 SLBrowser/8.0.1.4031 SLBChan/103"  
# 定义cookie，用于模拟登录状态，获取更多数据  
cookie = "__client_id=d670d45cce0e21ad3e7f30f352487ddb8028277b; _uid=1086745"  
# 定义请求头，包括用户代理和cookie  
headers = {  
    "user-agent": userAgent02,  
    "cookie": cookie  
}  
# 定义标签URL，这是洛谷的标签列表接口  
tagUrl = "https://www.luogu.com.cn/_lfe/tags?_version=1694484943"  
# 定义一个变量，表示只获取题目内容的数量，而不获取具体内容  
_contentOnly = 1  
  
# 定义一个函数，用于获取题目ID列表和题目数量  
def getPids(difficulty, tags, keyword):  
  
    # 调用initTag函数初始化标签数据  
    initTag()  
    # 定义一个字典，用于存储请求参数  
    # 爬取json数据  
    params = {"_contentOnly": _contentOnly}  
    # 将难度等级映射为数值，并存入参数字典中  
    difficulty = difficultyMap[difficulty]  
    if difficulty != -1:  
        params["difficulty"] = difficulty  
    # 如果标签列表不为空，则遍历标签列表，将存在的标签ID存入参数字典中  
    if len(tags) != 0:  
        accessibleTags = []  
        for item in tags:  
            # 判断标签是否存在  
            if item not in tag.keys():  
                return "invalid tag", ""  
            else:  
                accessibleTags.append(tag[item])  
        if len(accessibleTags) != 0:  
            params["tag"] = accessibleTags  
    # 如果关键字不为空，则将其存入参数字典中  
    if keyword != '':  
        params["keyword"] = keyword  
    # 使用requests库发送GET请求，获取题目数据  
    resp = requests.get(reqUrl, headers=headers, params=params)  
    # 将收到的文本数据转换为JSON格式，便于后续处理  
    jsonTxt = resp.text  
    map1 = json.loads(jsonTxt)  
    # 从JSON数据中提取题目列表和总数目信息  
    map2 = map1["currentData"]["problems"]  
    totalCount = map2["count"]  
    problems = map2["result"]  
    # 返回题目总数目和题目列表信息  
    return totalCount, problems  
# 定义一个函数，名为initTag，该函数没有参数  
def initTag():  
    # 检查字典tag的长度（即它包含的键值对的数量）是否不为0  
    # 如果不为0，说明字典中已经有一些标签信息，因此直接返回，不再进行后续的操作  
    if len(tag) != 0:  
        return  
  
    # 使用requests库发送一个GET请求到tagUrl，同时传递headers作为请求头  
    # 得到的响应被存储在变量res中  
    res = requests.get(tagUrl, headers=headers)  
  
    # 检查响应的文本中是否包含"Exception"这个词  
    # 如果包含，打印出"爬取Tag列表失败..."，然后返回字符串"error"  
    if str(res.text).find("Exception") != -1:  
        print("爬取Tag列表失败...")  
        return "error"  
  
    # 使用eval函数将响应的文本转换为Python的Unicode字符串，然后转换为小写  
    # 这样做是为了防止由于编码问题导致的错误  
    jsonTxt = eval("u" + "\'" + res.text + "\'")  
  
    # 使用json库的loads函数将字符串解析为Python的字典或列表  
    map = json.loads(jsonTxt)  
  
    # 从解析得到的字典中取出键为"tags"的值，这个值应该是一个包含多个标签的列表  
    tagList = map["tags"]  
  
    # 遍历这个标签列表  
    for item in tagList:  
        # 从每个标签项中获取其名字和ID，然后将其ID存储在以名字为键的字典tag中  
        tagName = item['name']  
        tagId = item['id']  
        tag[tagName] = tagId
if __name__ == '__main__':
    totalCount, problems = getPids("入门", [], '')
    print("题目总数{}".format(totalCount))
    print(problems)
    print(len(problems))